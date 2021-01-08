# Standard library
from itertools import (
    count,
)
import os
from typing import (
    Any,
    AsyncIterable,
    Iterator,
    NamedTuple,
    Optional,
    Tuple,
)
from aioextensions import (
    CPU_CORES,
    in_process,
    in_thread,
    resolve,
)
from more_itertools import (
    mark_ends,
)

# Third party libraries
import networkx as nx
from tree_sitter import (
    Language,
    Node,
    Parser,
    Tree,
)

# Local libraries
from parse_tree_sitter.transformations.control_flow import (
    add as add_control_flow,
)
from parse_tree_sitter.transformations.styles import (
    add as add_styles,
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
    copy_depth,
    to_svg,
)
from utils.logs import (
    log,
)
from utils.model import (
    GraphWithMeta,
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
    _graph: Optional[nx.DiGraph] = None,
    _parent: Optional[str] = None,
) -> nx.DiGraph:
    # Handle first level of recurssion, where _graph is None
    _counter = map(str, count(1)) if _counter is None else _counter
    _graph = nx.DiGraph() if _graph is None else _graph

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
            label_parent_ast=_parent,
            label_type=obj.type,
        )

        if not obj.children or obj.type in {
            'scoped_identifier',
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
) -> GraphWithMeta:
    parser: Parser = Parser()
    parser.set_language(Language(LANGUAGES_SO, language))

    raw_tree: Tree = parser.parse(content)

    graph: nx.DiGraph = _build_ast_graph(content, raw_tree)
    add_control_flow(graph)

    return GraphWithMeta(
        graph=graph,
    )


def parse_one(
    *,
    language: str,
    path: str,
    version: int = 8,
) -> GraphWithMeta:
    if not language:
        raise ParsingError()

    with open(path, 'rb') as handle:
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

    return graph


class ParseManyOutput(NamedTuple):
    graph: nx.DiGraph
    language: str
    path: str
    shard: int


async def parse_many(paths: Tuple[str, ...]) -> AsyncIterable[ParseManyOutput]:
    languages = tuple(map(decide_language, paths))
    shards = tuple(range(0, len(paths)))
    graphs_lazy = resolve((
        in_process(
            parse_one,
            language=language,
            path=path,
        )
        for language, path in zip(languages, paths)
    ), workers=CPU_CORES)

    for graph_lazy, language, path, shard in zip(
        graphs_lazy, languages, paths, shards,
    ):
        try:
            graph = await graph_lazy
        except ParsingError:
            await log('warning', 'Unable to parse: %s, ignoring', path)
        else:
            yield ParseManyOutput(
                graph=graph.graph,
                language=language,
                path=path,
                shard=shard,
            )


async def get_root(paths: Tuple[str, ...]) -> nx.DiGraph:
    # Reproducibility
    paths = tuple(sorted(paths))

    root = nx.DiGraph()
    root.add_node('root')

    paths_count: int = len(paths)
    async for result in parse_many(paths):
        await log(
            'info', 'Generating graph shard %s of %s: %s',
            result.shard,
            paths_count,
            result.path,
        )

        # Copy nodes from shard
        for first, _, (n_id, n_attrs) in mark_ends(result.graph.nodes.items()):
            n_id = f'shard-{result.shard}-{n_id}'

            if first:
                # Create the shard in the root graph
                shard_id = f'shard-{result.shard}'
                root.add_node(
                    shard_id,
                    label_language=result.language,
                    label_path=result.path,
                )

                # Link root to the shard
                root.add_edge('root', shard_id)
                root.add_edge(shard_id, n_id)

            root.add_node(n_id, **n_attrs)
            root.nodes[n_id]['label_parent_ast'] = (
                None
                if n_attrs['label_parent_ast'] is None
                else f'shard-{result.shard}-{n_attrs["label_parent_ast"]}'
            )

        # Copy edges from shard
        for u_id, v_id in result.graph.edges:
            root.add_edge(
                f'shard-{result.shard}-{u_id}',
                f'shard-{result.shard}-{v_id}',
                **result.graph[u_id][v_id],
            )

    add_styles(root)

    if CTX.debug:
        await in_thread(
            to_svg,
            copy_depth(root, 'root', 1),
            get_debug_path('tree-sitter-root'),
        )

    return root
