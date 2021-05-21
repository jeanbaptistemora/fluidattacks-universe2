# Standard library
from itertools import (
    count,
)
import json
import os
from typing import (
    Any,
    AsyncIterable,
    Dict,
    Iterator,
    Optional,
    Tuple,
)
from aioextensions import (
    CPU_CORES,
    in_process,
    resolve,
)

# Third party libraries
from tree_sitter import (
    Language,
    Node,
    Parser,
    Tree,
)

# Local libraries
from model.graph_model import (
    Graph,
    GraphDB,
    GraphDBContext,
    GraphShard,
    GraphShardCacheable,
    GraphShardMetadataLanguage,
)
from sast import (
    inspectors,
)
from sast.context import (
    java_resources,
)
from sast_syntax_readers import (
    generate as generate_syntax_readers,
)
from sast_transformations import (
    control_flow,
    danger_nodes,
    program_dependencie,
    styles,
)
from utils.ctx import (
    CTX,
    STATE_FOLDER,
    TREE_SITTER_CSHARP,
    TREE_SITTER_JAVA,
    TREE_SITTER_TSX,
)
from utils.encodings import (
    json_dump,
)
from utils.graph import (
    copy_ast,
    copy_cfg,
    copy_pdg,
    to_svg,
)
from utils.logs import (
    log,
    log_blocking,
)
from utils.string import (
    get_debug_path,
)

# Constants
LANGUAGES_SO = os.path.join(STATE_FOLDER, "languages.so")

# Side effects
Language.build_library(
    LANGUAGES_SO,
    [
        TREE_SITTER_CSHARP,
        TREE_SITTER_JAVA,
        TREE_SITTER_TSX,
    ],
)


def get_fields(source: str) -> Dict[str, Tuple[str, ...]]:
    with open(f"{source}/src/node-types.json") as handle:
        java_fields: Dict[str, Tuple[str, ...]] = {
            node["type"]: fields
            for node in json.load(handle)
            for fields in [tuple(node.get("fields", {}))]
            if fields
        }

    return java_fields


class ParsingError(Exception):
    pass


FIELDS_BY_LANGAUGE: Dict[
    GraphShardMetadataLanguage, Dict[str, Tuple[str, ...]]
] = {
    GraphShardMetadataLanguage.CSHARP: get_fields(TREE_SITTER_CSHARP),
    GraphShardMetadataLanguage.JAVA: get_fields(TREE_SITTER_JAVA),
    GraphShardMetadataLanguage.TSX: get_fields(TREE_SITTER_TSX),
}


def hash_node(node: Node) -> int:
    return hash(
        (
            node.end_point,
            node.start_point,
            node.type,
        )
    )


def _is_final_node(obj: Any, language: GraphShardMetadataLanguage) -> bool:
    return any(
        (
            (
                language == GraphShardMetadataLanguage.JAVA
                and obj.type
                in {
                    "array_type",
                    "character_literal",
                    "field_access",
                    "floating_point_type",
                    "generic_type",
                    "integral_type",
                    "scoped_identifier",
                    "scoped_type_identifier",
                    "this",
                    "type_identifier",
                }
            ),
            (
                language == GraphShardMetadataLanguage.CSHARP
                and obj.type
                in {
                    "string_literal",
                    "boolean_literal",
                    "character_literal",
                    "integer_literal",
                    "null_literal",
                    "real_literal",
                    "verbatim_string_literal",
                    "this_expression",
                    "assignment_operator",
                }
            ),
        )
    )


def _build_ast_graph(
    content: bytes,
    language: GraphShardMetadataLanguage,
    obj: Any,
    *,
    _counter: Optional[Iterator[str]] = None,
    _edge_index: Optional[str] = None,
    _graph: Optional[Graph] = None,
    _parent: Optional[str] = None,
    _parent_fields: Optional[Dict[int, str]] = None,
) -> Graph:
    # Handle first level of recurssion, where _graph is None
    _counter = map(str, count(1)) if _counter is None else _counter
    _graph = Graph() if _graph is None else _graph

    if isinstance(obj, Tree):
        return _build_ast_graph(content, language, obj.root_node)

    if not isinstance(obj, Node):
        raise NotImplementedError()

    if obj.has_error:
        raise ParsingError()

    n_id = next(_counter)

    _graph.add_node(
        n_id,
        label_c=obj.start_point[1] + 1,
        label_l=obj.start_point[0] + 1,
        label_type=obj.type,
    )

    if _parent is not None:
        _graph.add_edge(
            _parent,
            n_id,
            label_ast="AST",
            label_index=_edge_index,
        )

        if field := (_parent_fields or {}).get(hash_node(obj)):
            _graph.nodes[_parent][f"label_field_{field}"] = n_id

    if not obj.children or _is_final_node(obj, language):
        # Consider it a final node, extract the text from it
        _graph.nodes[n_id]["label_text"] = content[
            obj.start_byte : obj.end_byte
        ].decode("latin-1")
    elif language != GraphShardMetadataLanguage.NOT_SUPPORTED:
        parent_fields: Dict[int, str] = {}
        parent_fields = {
            hash_node(child): field
            for field in FIELDS_BY_LANGAUGE[language].get(obj.type, ())
            for child in [obj.child_by_field_name(field)]
            if child
        }

        # It's not a final node, recurse
        for edge_index, child in enumerate(obj.children):
            _build_ast_graph(
                content,
                language,
                child,
                _counter=_counter,
                _edge_index=str(edge_index),
                _graph=_graph,
                _parent=n_id,
                _parent_fields=parent_fields,
            )

    return _graph


def decide_language(path: str) -> GraphShardMetadataLanguage:
    language = GraphShardMetadataLanguage.NOT_SUPPORTED

    if path.endswith(".java"):
        language = GraphShardMetadataLanguage.JAVA

    if path.endswith(".cs"):
        language = GraphShardMetadataLanguage.CSHARP

    if (
        path.endswith(".js")
        or path.endswith(".jsx")
        or path.endswith(".ts")
        or path.endswith(".tsx")
    ):
        language = GraphShardMetadataLanguage.TSX

    return language


def _parse_one_cached(
    *,
    content: bytes,
    language: GraphShardMetadataLanguage,
    _: int,
) -> GraphShardCacheable:
    parser: Parser = Parser()
    parser.set_language(Language(LANGUAGES_SO, language.value))

    raw_tree: Tree = parser.parse(content)

    graph: Graph = _build_ast_graph(content, language, raw_tree)
    control_flow.add(graph, language)
    program_dependencie.add(graph, language)
    syntax = generate_syntax_readers.read_from_graph(graph, language)
    danger_nodes.mark(graph, language, syntax)
    styles.add(graph)

    metadata = inspectors.get_metadata(graph, language)

    return GraphShardCacheable(
        graph=graph,
        metadata=metadata,
        syntax=syntax,
    )


def parse_one(
    *,
    language: GraphShardMetadataLanguage,
    path: str,
    version: int = 20,
) -> Optional[GraphShard]:
    with open(os.path.join(CTX.config.working_dir, path), "rb") as handle:
        content = handle.read()

    try:
        graph = _parse_one_cached(
            content=content,
            language=language,
            _=version,
        )
    except ParsingError:
        log_blocking("warning", "Grammar error: %s, ignoring", path)
        return None
    except (
        ArithmeticError,
        AttributeError,
        BufferError,
        EOFError,
        LookupError,
        MemoryError,
        NameError,
        OSError,
        ReferenceError,
        RuntimeError,
        SystemError,
        TypeError,
        ValueError,
    ):
        log_blocking("warning", "Error while parsing: %s, ignoring", path)
        return None

    if CTX.debug:
        output = get_debug_path("tree-sitter-" + path)
        to_svg(graph.graph, output)
        to_svg(copy_ast(graph.graph), f"{output}.ast")
        to_svg(copy_cfg(graph.graph), f"{output}.cfg")
        to_svg(copy_pdg(graph.graph), f"{output}.pdg")

    return GraphShard(
        graph=graph.graph,
        metadata=graph.metadata,
        path=path,
        syntax=graph.syntax,
    )


async def parse_many(paths: Tuple[str, ...]) -> AsyncIterable[GraphShard]:
    for graph_lazy in resolve(
        (
            in_process(
                parse_one,
                language=language,
                path=path,
            )
            for path in paths
            for language in [decide_language(path)]
            if language != GraphShardMetadataLanguage.NOT_SUPPORTED
        ),
        workers=CPU_CORES,
    ):
        if graph_shard := await graph_lazy:
            yield graph_shard


async def get_graph_db(paths: Tuple[str, ...]) -> GraphDB:
    # Reproducibility
    paths = tuple(sorted(paths))

    graph_db = GraphDB(
        context=GraphDBContext(
            java_resources=java_resources.load(paths),
        ),
        shards=[],
        shards_by_java_class={},
        shards_by_path={},
    )

    index = 0
    async for shard in parse_many(paths):
        index += 1
        await log("info", "Generated shard %s: %s", index, shard.path)

        graph_db.shards.append(shard)
        graph_db.shards_by_path[shard.path] = index - 1

    for shard in graph_db.shards:
        graph_db.shards_by_java_class.update(
            {
                f"{shard.metadata.java.package}{_class}": shard.path
                for _class in shard.metadata.java.classes
            }
        )

    if CTX.debug:
        output = get_debug_path("tree-sitter")
        with open(f"{output}.json", "w") as handle:
            json_dump(graph_db, handle, indent=2, sort_keys=True)

    return graph_db
