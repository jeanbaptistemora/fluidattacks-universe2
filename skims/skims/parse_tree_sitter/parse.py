# Standard library
from itertools import (
    count,
)
import os
from typing import (
    Any,
    AsyncIterable,
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
from parse_tree_sitter import (
    inspectors,
)
from parse_tree_sitter.transformations import (
    control_flow,
    styles,
)
from state import (
    STATE_FOLDER,
)
from state.cache import (
    CACHE_ETERNALLY,
)
from utils.ctx import (
    CTX,
    TREE_SITTER_JAVA,
)
from utils.graph import (
    copy_ast,
    copy_cfg,
    to_svg,
)
from utils.logs import (
    log,
)
from utils.model import (
    Graph,
    GraphDB,
    GraphShard,
    GraphShardCacheable,
)
from utils.string import (
    get_debug_path,
)

# Constants
LANGUAGES_SO = os.path.join(STATE_FOLDER, 'languages.so')

# Side effects
Language.build_library(LANGUAGES_SO, [
    TREE_SITTER_JAVA,
])

# Constants
PARSER_JAVA: Parser = Parser()
PARSER_JAVA.set_language(Language(LANGUAGES_SO, 'java'))


class ParsingError(Exception):
    pass


def _build_ast_graph(
    content: bytes,
    obj: Any,
    *,
    _counter: Optional[Iterator[str]] = None,
    _edge_index: Optional[str] = None,
    _graph: Optional[Graph] = None,
    _parent: Optional[str] = None,
) -> Graph:
    # Handle first level of recurssion, where _graph is None
    _counter = map(str, count(1)) if _counter is None else _counter
    _graph = Graph() if _graph is None else _graph

    if isinstance(obj, Tree):
        _graph = _build_ast_graph(content, obj.root_node)

    elif isinstance(obj, Node):
        if obj.has_error:
            raise ParsingError()

        n_id = next(_counter)

        _graph.add_node(
            n_id,
            label_c=obj.start_point[1] + 1,
            label_l=obj.start_point[0] + 1,
            label_type=obj.type,
        )

        if not obj.children or obj.type in {
            'scoped_identifier',
            'scoped_type_identifier',
        }:
            _graph.nodes[n_id]['label_text'] = content[
                obj.start_byte:
                obj.end_byte
            ].decode('latin-1')

        if _parent is not None:
            _graph.add_edge(
                _parent,
                n_id,
                label_ast='AST',
                label_index=_edge_index,
            )

        for edge_index, child in enumerate(obj.children):
            _build_ast_graph(
                content,
                child,
                _counter=_counter,
                _edge_index=str(edge_index),
                _graph=_graph,
                _parent=n_id,
            )

    else:
        raise NotImplementedError()

    return _graph


def decide_language(path: str) -> str:
    language = ''

    if path.endswith('.java'):
        language = 'java'

    return language


@CACHE_ETERNALLY
def _parse_one_cached(
    *,
    content: bytes,
    language: str,
    _: int,
) -> GraphShardCacheable:
    parser: Parser = Parser()
    parser.set_language(Language(LANGUAGES_SO, language))

    raw_tree: Tree = parser.parse(content)

    graph: Graph = _build_ast_graph(content, raw_tree)
    control_flow.add(graph)
    styles.add(graph)

    return GraphShardCacheable(
        graph=graph,
        language=language,
        metadata=inspectors.get_metadata(graph, language),
    )


def parse_one(
    *,
    language: str,
    path: str,
    version: int = 15,
) -> GraphShard:
    if not language:
        raise ParsingError()

    with open(os.path.join(CTX.config.working_dir, path), 'rb') as handle:
        content = handle.read()

    graph = _parse_one_cached(
        content=content,
        language=language,
        _=version,
    )

    if CTX.debug:
        output = get_debug_path('tree-sitter-' + path)
        to_svg(graph.graph, output)
        to_svg(copy_ast(graph.graph), f'{output}.ast')
        to_svg(copy_cfg(graph.graph), f'{output}.cfg')

    return GraphShard(
        graph=graph.graph,
        language=graph.language,
        metadata=graph.metadata,
        path=path,
    )


async def parse_many(paths: Tuple[str, ...]) -> AsyncIterable[
    Optional[GraphShard],
]:
    graphs_lazy = resolve((
        in_process(
            parse_one,
            language=decide_language(path),
            path=path,
        )
        for path in paths
    ), workers=CPU_CORES)

    for graph_lazy, path in zip(
        graphs_lazy, paths,
    ):
        try:
            yield await graph_lazy
        except ParsingError:
            await log('warning', 'Unable to parse: %s, ignoring', path)
            yield None


async def get_graph_db(paths: Tuple[str, ...]) -> GraphDB:
    # Reproducibility
    paths = tuple(sorted(paths))

    graph_db = GraphDB(
        shards=[],
        shards_by_path={},
    )

    index = 0
    index_max: int = len(paths)
    async for shard in parse_many(paths):
        index += 1
        if shard:
            await log(
                'info', 'Generated graph shard %s of %s: %s',
                index, index_max, shard.path,
            )

            graph_db.shards.append(shard)
            graph_db.shards_by_path[shard.path] = index

    return graph_db
