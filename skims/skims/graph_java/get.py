# Standard library
import json

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
    copy_ast,
    copy_cfg,
    to_svg,
)
from utils.model import (
    Grammar,
    Graph,
)
from utils.ctx import (
    CTX,
)
from utils.string import (
    get_debug_path,
)

# Constants
VERSION: int = 0


async def get(
    grammar: Grammar,
    *,
    content: bytes,
    path: str,
) -> Graph:
    return await _get(
        grammar,
        content=content,
        path=path,
        _=VERSION,
    )


@CACHE_ETERNALLY
async def _get(
    grammar: Grammar,
    *,
    content: bytes,
    path: str,
    _: int,
) -> Graph:
    parse_tree = await antlr_parse.parse(
        grammar,
        content=content,
        path=path,
    )
    model = antlr_model.from_parse_tree(parse_tree)

    if CTX.debug:
        output = get_debug_path('antlr-' + path)
        with open(f'{output}.model.json', 'w') as handle:
            json.dump(model, handle, indent=2, sort_keys=True)

    graph = antlr_graph.from_model(model)
    reducers.reduce(graph)
    inputs.mark(graph)
    sinks.mark(graph)
    cfg.analyze(graph)
    styles.stylize(graph)

    if CTX.debug:
        output = get_debug_path('antlr-' + path)
        to_svg(graph, output)
        to_svg(copy_ast(graph), f'{output}.ast')
        to_svg(copy_cfg(graph), f'{output}.cfg')

    return graph
