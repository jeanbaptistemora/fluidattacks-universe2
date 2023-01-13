from ctx import (
    CTX,
    TREE_SITTER_PARSERS,
)
from itertools import (
    count,
)
import json
from model.graph_model import (
    Graph,
    GraphDB,
    GraphDBContext,
    GraphShard,
    GraphShardCacheable,
    GraphShardMetadata,
    GraphShardMetadataLanguage,
)
import os
from sast.context import (
    java_resources,
)
from sast_syntax_readers import (
    generate as generate_syntax_readers,
)
from sast_transformations import (
    control_flow,
    styles,
)
from syntax_cfg.generate import (
    add_syntax_cfg,
)
from syntax_graph.generate import (
    build_syntax_graph,
)
from tree_sitter import (
    Language,
    Node,
    Parser,
    Tree,
)
from typing import (
    Dict,
    Iterable,
    Iterator,
    Optional,
    Tuple,
)
from utils.encodings import (
    json_dump,
)
from utils.fs import (
    decide_language,
    safe_sync_get_file_raw_content,
)
from utils.graph import (
    copy_ast,
    copy_cfg,
    to_svg,
)
from utils.logs import (
    log_blocking,
)
from utils.string import (
    get_debug_path,
)


class ParsingError(Exception):
    pass


FIELDS_BY_LANGUAGE: Dict[
    GraphShardMetadataLanguage, Dict[str, Tuple[str, ...]]
] = {}


def _get_fields_by_language() -> None:
    for lang in GraphShardMetadataLanguage:
        if lang == GraphShardMetadataLanguage.NOT_SUPPORTED:
            continue

        path: str = os.path.join(
            TREE_SITTER_PARSERS, f"{lang.value}-fields.json"
        )

        with open(path, encoding="utf-8") as file:
            FIELDS_BY_LANGUAGE[lang] = json.load(file)


_get_fields_by_language()


def hash_node(node: Node) -> int:
    return hash((node.end_point, node.start_point, node.type))


def _is_final_node(node: Node, language: GraphShardMetadataLanguage) -> bool:
    return (
        (
            language == GraphShardMetadataLanguage.CSHARP
            and node.type
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
        )
        or (
            language == GraphShardMetadataLanguage.DART
            and node.type
            in {
                "decimal_floating_point_literal",
                "decimal_integer_literal",
                "false",
                "hex_integer_literal",
                "list_literal",
                "null_literal",
                "set_or_map_literal",
                "string_literal",
                "symbol_literal",
                "true",
            }
        )
        or (
            language == GraphShardMetadataLanguage.GO
            and node.type
            in {
                "interface_type",
                "interpreted_string_literal",
            }
        )
        or (
            language == GraphShardMetadataLanguage.JAVA
            and node.type
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
        )
        or (
            language == GraphShardMetadataLanguage.JAVASCRIPT
            and node.type
            in {
                "this",
                "super",
                "number",
                "string",
                "template_string",
                "regex",
                "true",
                "false",
                "null",
                "undefined",
            }
        )
        or (
            language == GraphShardMetadataLanguage.PHP
            and node.type
            in {
                "named_type",
            }
        )
        or (
            language == GraphShardMetadataLanguage.RUBY
            and node.type in {"scope_resolution"}
        )
        or (
            language == GraphShardMetadataLanguage.TYPESCRIPT
            and node.type
            in {
                "this",
                "super",
                "number",
                "string",
                "template_string",
                "regex",
                "true",
                "false",
                "null",
                "undefined",
            }
        )
        or (
            language == GraphShardMetadataLanguage.KOTLIN
            and node.type in {"boolean_literal", "line_string_literal"}
        )
    )


def _build_ast_graph(
    content: bytes,
    language: GraphShardMetadataLanguage,
    node: Node,
    counter: Iterator[str],
    graph: Graph,
    *,
    _edge_index: Optional[str] = None,
    _parent: Optional[str] = None,
    _parent_fields: Optional[Dict[int, str]] = None,
) -> Graph:
    if not isinstance(node, Node):
        raise NotImplementedError()

    if node.has_error:
        raise ParsingError()

    n_id = next(counter)
    raw_l, raw_c = node.start_point

    graph.add_node(
        n_id, label_l=raw_l + 1, label_c=raw_c + 1, label_type=node.type
    )

    if _parent is not None:
        graph.add_edge(_parent, n_id, label_ast="AST", label_index=_edge_index)

        # if the node is a parent field acording node_type file, associate id
        # example node-types files at https://github.com/
        # tree-sitter/tree-sitter-c-sharp/blob/master/src/node-types.json
        # tree-sitter/tree-sitter-java/blob/master/src/node-types.json
        if field := (_parent_fields or {}).get(hash_node(node)):
            graph.nodes[_parent][f"label_field_{field}"] = n_id

    if not node.children or _is_final_node(node, language):
        # Consider it a final node, extract the text from it
        node_content = content[node.start_byte : node.end_byte]
        graph.nodes[n_id]["label_text"] = node_content.decode("latin-1")

    elif language != GraphShardMetadataLanguage.NOT_SUPPORTED:
        # It's not a final node, recurse
        for edge_index, child in enumerate(node.children):
            _build_ast_graph(
                content,
                language,
                child,
                counter,
                graph,
                _edge_index=str(edge_index),
                _parent=n_id,
                _parent_fields={
                    hash_node(child): fld
                    for fld in FIELDS_BY_LANGUAGE[language].get(node.type, ())
                    for child in [node.child_by_field_name(fld)]
                    if child
                },
            )

    return graph


def parse_content(
    content: bytes,
    language: GraphShardMetadataLanguage,
) -> Tree:
    path: str = os.path.join(TREE_SITTER_PARSERS, f"{language.value}.so")
    parser: Parser = Parser()
    parser.set_language(Language(path, language.value))
    return parser.parse(content)


def _parse_one_cached(
    *,
    content: bytes,
    path: str,
    language: GraphShardMetadataLanguage,
) -> Optional[GraphShardCacheable]:
    raw_tree: Tree = parse_content(content, language)
    node: Node = raw_tree.root_node

    counter = map(str, count(1))
    try:
        graph: Graph = _build_ast_graph(
            content, language, node, counter, Graph()
        )
    except ParsingError:
        return None

    syntax_support = {
        GraphShardMetadataLanguage.CSHARP,
        GraphShardMetadataLanguage.DART,
        GraphShardMetadataLanguage.GO,
        GraphShardMetadataLanguage.JAVA,
        GraphShardMetadataLanguage.JAVASCRIPT,
        GraphShardMetadataLanguage.KOTLIN,
        GraphShardMetadataLanguage.TYPESCRIPT,
    }

    if language in syntax_support:
        if syntax_graph := build_syntax_graph(path, language, graph):
            syntax_graph = add_syntax_cfg(syntax_graph)
    else:
        syntax_graph = None

    control_flow.add(graph, language)
    syntax = generate_syntax_readers.read_from_graph(graph, language)
    metadata = GraphShardMetadata(
        language=language,
    )

    styles.add(graph)

    return GraphShardCacheable(
        graph=graph,
        metadata=metadata,
        syntax=syntax,
        syntax_graph=syntax_graph,
    )


def parse_one(
    path: str,
    language: GraphShardMetadataLanguage,
    content: Optional[bytes] = None,
) -> Optional[GraphShard]:
    if not content:
        return None
    try:
        graph = _parse_one_cached(
            content=content,
            path=path,
            language=language,
        )
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
        ParsingError,
    ):
        log_blocking("warning", "Error while parsing: %s, ignoring", path)
        return None

    if not graph:
        return None

    if CTX.debug:
        output = get_debug_path("tree-sitter-" + path)
        to_svg(graph.graph, output)
        to_svg(copy_ast(graph.graph), f"{output}.ast")
        to_svg(copy_cfg(graph.graph), f"{output}.cfg")

    return GraphShard(
        graph=graph.graph,
        metadata=graph.metadata,
        path=path,
        syntax=graph.syntax,
        syntax_graph=graph.syntax_graph,
    )


def _get_content(path: str) -> Tuple[str, Optional[bytes]]:
    full_path = os.path.join(CTX.config.working_dir, path)
    return (path, safe_sync_get_file_raw_content(full_path))


def parse_many(paths: Tuple[str, ...]) -> Iterable[GraphShard]:
    paths_and_languages = [
        (path, language)
        for path in paths
        for language in [decide_language(path)]
        if language != GraphShardMetadataLanguage.NOT_SUPPORTED
    ]

    files_content = dict([_get_content(x[0]) for x in paths_and_languages])

    for path, language, content in zip(
        [x[0] for x in paths_and_languages],
        [x[1] for x in paths_and_languages],
        [files_content[x[0]] for x in paths_and_languages],
    ):
        if parsed := parse_one(path, language, content):
            yield parsed


def get_graph_db(paths: Tuple[str, ...]) -> GraphDB:
    # Reproducibility
    paths = tuple(sorted(paths))
    available_languages = {"java", "c_sharp"}

    graph_db = GraphDB(
        context=GraphDBContext(
            java_resources=java_resources.load(paths),
        ),
        shards=[],
        shards_by_language_class={
            language: {} for language in available_languages
        },
        shards_by_path={},
    )

    for index, shard in enumerate(parse_many(paths), start=1):
        graph_db.shards.append(shard)
        graph_db.shards_by_path[shard.path] = index - 1

    for shard in graph_db.shards:
        for language in ("java", "c_sharp"):
            if shard.metadata.language.value == language:
                graph_db.shards_by_language_class[language].update(
                    {
                        _class: shard.path
                        for _class in getattr(shard.metadata, language).classes
                    }
                )

    if CTX.debug:
        output = get_debug_path("tree-sitter")
        with open(f"{output}.json", "w", encoding="utf-8") as handle:
            json_dump(graph_db, handle, indent=2, sort_keys=True)

    return graph_db
