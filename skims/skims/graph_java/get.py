# Standard library
import json
import os

# Third party libraries
import networkx as nx

# Local libraries
from parse_antlr import (
    graph as antlr_graph,
    parse as antlr_parse,
    model as antlr_model,
)
from graph_java.transformations import (
    control_flow,
    inputs,
    reducers,
    sinks,
    styles,
)
from state.cache import (
    CACHE_1SEC,
)
from utils.graph import (
    to_svg,
)
from utils.model import (
    Grammar,
)


def _get_debug_path(path: str) -> str:
    return os.path.join(
        'test/outputs',
        os.path.relpath(path).replace('/', '__'),
    )


@CACHE_1SEC
async def get(
    grammar: Grammar,
    *,
    content: bytes,
    debug: bool = False,
    path: str,
) -> nx.DiGraph:
    parse_tree = await antlr_parse.parse(grammar, content=content, path=path)
    model = antlr_model.from_parse_tree(parse_tree)

    if debug:
        output = _get_debug_path(path)
        with open(f'{output}.model.json', 'w') as handle:
            json.dump(model, handle, indent=2, sort_keys=True)

    graph = antlr_graph.from_model(model)
    reducers.reduce(graph)
    inputs.mark(graph)
    sinks.mark(graph)
    control_flow.analyze(graph)
    styles.stylize(graph)

    if debug:
        output = _get_debug_path(path)
        await to_svg(graph, output)

    return graph
