# Standard library
import json

# Third party libraries
from aioextensions import (
    run_decorator,
)
import pytest

# Local libraries
from graph_java.get import (
    get as java_get_graph,
)
from eval_java.evaluate import (
    evaluate,
)
from graph_java.transformations.sinks import (
    SINKS,
)
from graph_java.transformations.control_flow import (
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
            'f031_cwe378',
        ),
        (
            'test/data/lib_path/f063_path_traversal/Test.java',
            'f063_path_traversal',
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
    graph = await java_get_graph(Grammar.JAVA9, content=content, path=path)
    graph_as_json = export_graph_as_json(graph)
    graph_as_json_str = json.dumps(graph_as_json, indent=2, sort_keys=True)

    assert await to_svg(graph, f'test/outputs/{name}.graph')

    with open(f'test/data/parse_java/{name}.graph.json') as handle:
        expected = handle.read()

    assert graph_as_json_str == expected

    for sink in SINKS:
        for index, path in enumerate(  # type: ignore
            sorted(g.flows(graph, sink_type=sink)),
        ):
            statements = evaluate(
                graph,
                path,  # type: ignore
                allow_incomplete=True,
            )
            statements_as_json = json.dumps(statements, indent=2, sort_keys=True)

            with open(f'test/data/parse_java/{name}.{sink}.{index}.statements.json') as handle:
                expected = handle.read()

            assert statements_as_json == expected


@run_decorator
async def test_control_flow_1() -> None:
    path = 'test/data/parse_java/TestCFG.java'
    graph = await java_get_graph(
        Grammar.JAVA9,
        content=await get_file_raw_content(path),
        path=path,
    )

    # Check IfThenStatement
    assert has_labels(graph['346']['392'], **TRUE)

    # Check IfThenElseStatement
    assert has_labels(graph['1075']['1122'], **TRUE)
    assert has_labels(graph['1075']['1135'], **FALSE)

    # Check BlockStatement
    assert has_labels(graph['3138']['3140'], **ALWAYS)
    assert has_labels(graph['3140']['3144'], **ALWAYS)
    assert has_labels(graph['3144']['3193'], **ALWAYS)
    assert has_labels(graph['3279']['3316'], **ALWAYS)
    assert has_labels(graph['3316']['3561'], **FALSE)
    assert has_labels(graph['3561']['3193'], **ALWAYS)
    assert has_labels(graph['3193']['3056'], **ALWAYS)

    # Check WhileStatement
    assert has_labels(graph['816']['853'], **TRUE)
    assert has_labels(graph['1266']['816'], **ALWAYS)

    # Check DoWhileStatement
    assert has_labels(graph['2985']['3648'], **ALWAYS)
    assert has_labels(graph['3056']['2985'], **TRUE)
    assert has_labels(graph['3056']['3648'], **FALSE)

    # Check BreakStatement
    assert has_labels(graph['1128']['1216'], **BREAK)
    assert has_labels(graph['1663']['2100'], **BREAK)  # break in switch
    assert has_labels(graph['4440']['4495'], **BREAK)  # break in for
    assert has_labels(graph['4658']['4725'], **BREAK)  # break in while

    # Check ContinueStatement
    assert has_labels(graph['3553']['3316'], **CONTINUE)  # continue in nested loop for-for-while
    assert has_labels(graph['1141']['920'], **CONTINUE)  # continue in nested loop while-for
    assert has_labels(graph['5138']['4971'], **CONTINUE)

    # Check ForStatement
    assert has_labels(graph['920']['1002'], **TRUE)
    assert has_labels(graph['920']['1216'], **FALSE)
    assert has_labels(graph['1148']['920'], **ALWAYS)

    # Check SwitchStatement
    assert has_labels(graph['1568']['1591'], **ALWAYS)
    assert has_labels(graph['1593']['1619'], **TRUE)
    assert has_labels(graph['1591']['1973'], **ALWAYS)  # Break
    assert has_labels(graph['1591']['1666'], **ALWAYS)  # no Break

    # TryStatement
    assert has_labels(graph['168']['170'], **ALWAYS)  # try -> block
    assert has_labels(graph['170']['329'], **MAYBE)  # block -> catch

    assert has_labels(graph['5950']['5952'], **ALWAYS)  # try -> block
    assert has_labels(graph['5952']['5993'], **MAYBE)  # block -> catch
    assert has_labels(graph['5952']['6041'], **MAYBE)  # block -> catch

    assert has_labels(graph['6097']['6099'], **ALWAYS)  # try -> block
    assert has_labels(graph['6099']['6103'], **ALWAYS)  # block -> finally


@run_decorator
async def test_control_flow_2() -> None:
    path = 'test/data/lib_path/f063_path_traversal/Test.java'
    graph = await java_get_graph(
        Grammar.JAVA9,
        content=await get_file_raw_content(path),
        path=path,
    )

    assert sorted(g.flows(graph, sink_type='F063_PATH_TRAVERSAL')) == [
        ('30', '85', '87', '91', '125', '185', '286', '351', '352', '368', '392', '422'),
    ]
