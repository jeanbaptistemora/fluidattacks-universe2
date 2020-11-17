# Standard library
import json

# Third party libraries
from aioextensions import (
    run_decorator,
)

# Local libraries
from parse_antlr.parse import (
    parse,
)
from parse_antlr.model import (
    from_parse_tree as model_from_parse_tree,
)
from parse_antlr.graph import (
    from_model as graph_from_model,
)
from utils.fs import (
    get_file_raw_content,
)
from utils.graph import (
    export_graph,
    export_graph_as_json,
    graphviz_to_svg,
)
from utils.model import (
    Grammar,
)


@run_decorator
async def test_graph_generation_easy() -> None:
    path = 'test/data/lib_path/f031_cwe378/Test.java'
    parse_tree = await parse(
        Grammar.JAVA9,
        content=await get_file_raw_content(path),
        path=path,
    )
    model = model_from_parse_tree(parse_tree)
    graph = graph_from_model(model)
    graph_as_json = export_graph_as_json(graph)
    graph_as_json_str = json.dumps(graph_as_json, indent=2, sort_keys=True)

    assert export_graph(graph, 'test/outputs/test_graph_generation_easy.graph')
    assert await graphviz_to_svg('test/outputs/test_graph_generation_easy.graph')

    with open('test/data/parse_antlr/graph_generation_easy.json') as handle:
        expected = handle.read()

    assert graph_as_json_str == expected


@run_decorator
async def test_graph_generation_hard() -> None:
    path = 'test/data/benchmark/owasp/BenchmarkTest00008.java'
    parse_tree = await parse(
        Grammar.JAVA9,
        content=await get_file_raw_content(path),
        path=path,
    )
    model = model_from_parse_tree(parse_tree)
    graph = graph_from_model(model)
    graph_as_json = export_graph_as_json(graph)
    graph_as_json_str = json.dumps(graph_as_json, indent=2)

    assert export_graph(graph, 'test/outputs/test_graph_generation_hard.graph')
    assert await graphviz_to_svg('test/outputs/test_graph_generation_hard.graph')

    with open('test/data/parse_antlr/graph_generation_hard.json') as handle:
        expected = handle.read()

    assert graph_as_json_str == expected
