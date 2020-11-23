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
    ALWAYS,
    BREAK,
    CONTINUE,
    FALSE,
    TRUE,
)
from utils.fs import (
    get_file_raw_content,
)
from utils.graph import (
    export_graph_as_json,
    to_svg,
    has_labels,
)
from utils.model import (
    Grammar,
)


@pytest.mark.parametrize(
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
            'owasp_benchmark_00167',
        ),
        (
            'test/data/parse_java/TestCFG.java',
            'apply_control_flow',
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

    assert await to_svg(graph, f'test/outputs/{name}.graph')

    with open(f'test/outputs/{name}.model.json', 'w') as handle:
        handle.write(model_as_json)

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
    assert has_labels(graph['352']['398'], **TRUE)

    # Check IfThenElseStatement
    assert has_labels(graph['531']['556'], **TRUE)
    assert has_labels(graph['531']['603'], **FALSE)

    # Check BlockStatement
    assert has_labels(graph['176']['178'], **ALWAYS)

    # Check WhileStatement
    assert has_labels(graph['1965']['2009'], **TRUE)
    assert has_labels(graph['1965']['2069'], **FALSE)
    assert has_labels(graph['2058']['1965'], **ALWAYS)

    # Check DoWhileStatement
    assert has_labels(graph['2107']['2118'], **TRUE)
    assert has_labels(graph['2167']['2215'], **FALSE)
    assert has_labels(graph['2167']['2107'], **ALWAYS)

    # Check breakStatement
    assert has_labels(graph['2928']['2995'], **BREAK)

    # Check for statement
    assert has_labels(graph['2215']['2303'], **TRUE)
    assert has_labels(graph['2303']['2215'], **ALWAYS)
    assert has_labels(graph['2535']['2623'], **TRUE)
    assert has_labels(graph['2715']['2535'], **ALWAYS)
    assert has_labels(graph['2708']['2763'], **BREAK)

    # Check SwitchStatement
    assert has_labels(graph['910']['967'], **ALWAYS)
    assert has_labels(graph['910']['1041'], **ALWAYS)
    assert has_labels(graph['1081']['1213'], **ALWAYS)
    assert has_labels(graph['910']['1115'], **ALWAYS)
