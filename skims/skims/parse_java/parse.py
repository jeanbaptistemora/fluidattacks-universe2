# Standard library
import json
from typing import (
    Any,
    Optional,
)

# Third party libraries
from aioextensions import (
    in_process,
)
import networkx as nx

# Local libraries
from parse_antlr import (
    graph as antlr_graph,
    parse as antlr_parse,
    model as antlr_model,
)
from parse_java.graph.control_flow import (
    analyze as analyze_control_flow,
)
from parse_java.graph.inputs import (
    mark as mark_inputs,
)
from parse_java.graph.reducers import (
    reduce as reduce_graph,
)
from parse_java.graph.styles import (
    stylize,
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


def from_antlr_model(model: Any) -> nx.OrderedDiGraph:
    graph = antlr_graph.from_model(model)

    reduce_graph(graph)
    mark_inputs(graph)
    analyze_control_flow(graph)
    stylize(graph)

    return graph


@CACHE_1SEC
async def parse_from_content(
    grammar: Grammar,
    *,
    content: bytes,
    output: Optional[str] = None,
    path: str,
) -> nx.OrderedDiGraph:
    parse_tree = await antlr_parse.parse(grammar, content=content, path=path)
    model = await in_process(antlr_model.from_parse_tree, parse_tree)

    if output:
        with open(f'{output}.model.json', 'w') as handle:
            json.dump(model, handle, indent=2, sort_keys=True)

    graph = await in_process(from_antlr_model, model)

    if output:
        await to_svg(graph, output)

    return graph
