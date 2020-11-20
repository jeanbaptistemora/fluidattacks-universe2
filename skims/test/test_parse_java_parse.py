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
    parse_from_content,
)
from parse_java.graph.control_flow import (
    analyze as analyze_control_flow,
)
from utils.fs import (
    get_file_raw_content,
)
from utils.graph import (
    export_graph_as_json,
    export_graph_as_svg,
    has_labels,
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
        ),
        (
            'test/data/parse_java/TestCFG.java',
            'apply_control_flow'
        )
    ],
)
@run_decorator
async def test_graph_generation(path: str, name: str) -> None:
    content = await get_file_raw_content(path)

    # Old way
    parse_tree = await parse(Grammar.JAVA9, content=content, path=path)
    model = model_from_parse_tree(parse_tree)
    model_as_json = json.dumps(model, indent=2)
    graph = from_antlr_model(model)

    # New way, comprised
    graph = await parse_from_content(Grammar.JAVA9, content=content, path=path)
    graph_as_json = export_graph_as_json(graph)
    graph_as_json_str = json.dumps(graph_as_json, indent=2, sort_keys=True)

    assert await export_graph_as_svg(graph, f'test/outputs/{name}.graph')

    with open(f'test/outputs/{name}.model.json', 'w') as handle:
        handle.write(model_as_json)

    with open(f'test/data/parse_java/{name}.graph.json', 'w') as handle:
        handle.write(graph_as_json_str)

    with open(f'test/data/parse_java/{name}.graph.json') as handle:
        expected = handle.read()

    assert graph_as_json_str == expected


@run_decorator
async def test_apply_control_flow() -> None:
    path = 'test/data/parse_java/TestCFG.java'
    parse_tree = await parse(
        Grammar.JAVA9,
        content=await get_file_raw_content(path),
        path=path,
    )
    model = model_from_parse_tree(parse_tree)
    graph = from_antlr_model(model)

    # Check IfThenStatement
    assert has_labels(graph['352']['398'], label_cfg='CFG', label_true='true')

    # Check IfThenElseStatement
    assert has_labels(graph['531']['556'], label_cfg='CFG', label_true='true')
    assert has_labels(graph['531']['603'], label_cfg='CFG', label_false='false')

    # Check BlockStatement
    assert has_labels(graph['967']['1007'], label_cfg='CFG', label_e='e')

    # Check WhileStatement
    assert has_labels(graph['1965']['2009'], label_cfg='CFG', label_true='true')
    assert has_labels(graph['1965']['2069'], label_cfg='CFG', label_false='false')
    assert has_labels(graph['2058']['1965'], label_cfg='CFG', label_e='e')

    # Check DoWhileStatement
    assert has_labels(graph['2107']['2118'], label_cfg='CFG', label_true='true')
    assert has_labels(graph['2167']['2215'], label_cfg='CFG', label_false='false')
    assert has_labels(graph['2167']['2107'], label_cfg='CFG', label_e='e')

    # Check breakStatement
    assert has_labels(graph['2928']['2995'], label_cfg='CFG', label_break='break')
