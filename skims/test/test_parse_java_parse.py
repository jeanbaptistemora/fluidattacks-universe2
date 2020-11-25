# Standard library
import json

# Third party libraries
from aioextensions import (
    run_decorator,
)
import pytest

# Local libraries
from parse_java.parse import (
    parse_from_content,
)
from parse_java.graph.control_flow import (
    ALWAYS,
    BREAK,
    CONTINUE,
    FALSE,
    MAYBE,
    TRUE,
)
from utils import (
    graph as g,
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
            'test/data/benchmark/owasp/BenchmarkTest00001.java',
            'owasp_benchmark_00001',
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

    # New way, comprised
    graph = await parse_from_content(Grammar.JAVA9, content=content, path=path)
    graph_as_json = export_graph_as_json(graph)
    graph_as_json_str = json.dumps(graph_as_json, indent=2, sort_keys=True)

    assert await to_svg(graph, f'test/outputs/{name}.graph')

    with open(f'test/data/parse_java/{name}.graph.json') as handle:
        expected = handle.read()

    assert graph_as_json_str == expected


@run_decorator
async def test_control_flow_1() -> None:
    path = 'test/data/parse_java/TestCFG.java'
    graph = await parse_from_content(
        Grammar.JAVA9,
        content=await get_file_raw_content(path),
        path=path,
    )

    # Check IfThenStatement
    assert has_labels(graph['346']['392'], **TRUE)

    # Check IfThenElseStatement
    assert has_labels(graph['525']['550'], **TRUE)
    assert has_labels(graph['525']['597'], **FALSE)

    # Check BlockStatement
    assert has_labels(graph['61']['91'], **ALWAYS)
    assert has_labels(graph['91']['93'], **ALWAYS)
    assert has_labels(graph['93']['95'], **ALWAYS)
    assert has_labels(graph['95']['129'], **ALWAYS)
    assert has_labels(graph['129']['168'], **ALWAYS)
    assert has_labels(graph['168']['454'], **ALWAYS)
    assert has_labels(graph['454']['525'], **ALWAYS)

    # Check WhileStatement

    # Check DoWhileStatement

    # Check breakStatement

    # Check for statement

    # Check SwitchStatement

    # TryStatement
    assert has_labels(graph['168']['170'], **ALWAYS)  # try -> block
    assert has_labels(graph['170']['329'], **MAYBE)  # block -> catch

    assert has_labels(graph['4194']['4196'], **ALWAYS)  # try -> block
    assert has_labels(graph['4196']['4237'], **MAYBE)  # block -> catch
    assert has_labels(graph['4196']['4285'], **MAYBE)  # block -> catch

    assert has_labels(graph['4440']['4442'], **ALWAYS)  # try -> block
    assert has_labels(graph['4442']['4482'], **ALWAYS)  # block -> finally


@run_decorator
async def test_control_flow_2() -> None:
    path = 'test/data/lib_path/f063_path_traversal/Test.java'
    graph = await parse_from_content(
        Grammar.JAVA9,
        content=await get_file_raw_content(path),
        path=path,
    )

    assert sorted(g.flows(graph, sink_type='F063_PATH_TRAVERSAL')) == [
        ('30', '85', '87', '91', '125', '185', '286', '351', '352', '368', '392', '422'),
        ('30', '85', '87', '91', '93', '123', '125', '185', '286', '351', '352', '368', '392', '422'),
    ]
