# Standard library
import json

# Third party libraries
import networkx as nx

# Local libraries
from parse_antlr import (
    graph as antlr_graph,
    parse as antlr_parse,
    model as antlr_model,
)
from graph_java.transformations import (
    cfg,
    inputs,
    reducers,
    sinks,
    styles,
)
from state.cache import (
    CACHE_ETERNALLY,
)
from utils.graph import (
    to_svg,
)
from utils.model import (
    Grammar,
)
from utils.ctx import (
    CTX,
)
from utils.string import (
    get_debug_path,
)


def get(
    grammar: Grammar,
    *,
    content: bytes,
    path: str,
    # Update this number to indicate a new graph version
    # This also invalidates the cache
    graph_version: int = 4,
) -> nx.DiGraph:
    return _get(
        grammar,
        content=content,
        graph_version=graph_version,
        path=path,
    )


@CACHE_ETERNALLY
async def _get(
    grammar: Grammar,
    *,
    content: bytes,
    graph_version: int,
    path: str,
) -> nx.DiGraph:
    parse_tree = await antlr_parse.parse(
        grammar,
        content=content,
        path=path,
        _=graph_version,
    )
    model = antlr_model.from_parse_tree(parse_tree)

    if CTX.debug:
        output = get_debug_path(path)
        with open(f'{output}.model.json', 'w') as handle:
            json.dump(model, handle, indent=2, sort_keys=True)

    graph = antlr_graph.from_model(model)
    reducers.reduce(graph)
    inputs.mark(graph)
    sinks.mark(graph)
    cfg.analyze(graph)
    styles.stylize(graph)

    if CTX.debug:
        output = get_debug_path(path)
        await to_svg(graph, output)

    return graph
