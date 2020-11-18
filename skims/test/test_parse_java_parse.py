# Standard library
import json

# Third party libraries
from aioextensions import (
    run_decorator,
)
import pytest

# Local libraries
from parse_antlr.parse import (
    parse,
)
from parse_antlr.model import (
    from_parse_tree as model_from_parse_tree,
)
from parse_java.parse import (
    from_antlr_model,
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


@pytest.mark.parametrize(  # type: ignore
    'path,name',
    [
        (
            'test/data/lib_path/f031_cwe378/Test.java',
            'small_java_program',
        ),
        (
            'test/data/benchmark/owasp/BenchmarkTest00008.java',
            'owasp_benchmark_00008',
        ),
        (
            'test/data/benchmark/owasp/BenchmarkTest00167.java',
            'owasp_benchmark_00167'
        )
    ],
)
@run_decorator
async def test_graph_generation(path: str, name: str) -> None:
    parse_tree = await parse(
        Grammar.JAVA9,
        content=await get_file_raw_content(path),
        path=path,
    )
    model = model_from_parse_tree(parse_tree)
    model_as_json = json.dumps(model, indent=2)
    graph = from_antlr_model(model)
    graph_as_json = export_graph_as_json(graph)
    graph_as_json_str = json.dumps(graph_as_json, indent=2, sort_keys=True)

    assert export_graph(graph, f'test/outputs/{name}.graph')
    assert await graphviz_to_svg(f'test/outputs/{name}.graph')

    with open(f'test/outputs/{name}.model.json', 'w') as handle:
        handle.write(model_as_json)

    with open(f'test/data/parse_java/{name}.graph.json', 'w') as handle:
        handle.write(graph_as_json_str)

    with open(f'test/data/parse_java/{name}.graph.json') as handle:
        expected = handle.read()

    assert graph_as_json_str == expected
