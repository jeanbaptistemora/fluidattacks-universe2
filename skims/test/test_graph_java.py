# Third party libraries
from aioextensions import (
    run_decorator,
)
import pytest

# Local libraries
from graph_java.get import (
    get as java_get_graph,
)
from graph_java.transformations.cfg import (
    ALWAYS,
    FALSE,
    MAYBE,
    TRUE,
)
from model import (
    core_model,
)
from utils import (
    graph as g,
)
from utils.ctx import (
    SHOULD_UPDATE_TESTS,
)
from utils.encodings import (
    json_dumps,
)
from utils.fs import (
    get_file_raw_content,
)
from utils.graph import (
    export_graph_as_json,
    has_labels,
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
@pytest.mark.skims_test_group('unittesting')
async def test_graph_generation(path: str, name: str) -> None:
    content = await get_file_raw_content(path)

    # New way, comprised
    graph = await java_get_graph(
        core_model.Grammar.JAVA9, content=content, path=path,
    )
    graph_as_json = export_graph_as_json(graph)
    graph_as_json_str = json_dumps(graph_as_json, indent=2, sort_keys=True)

    if SHOULD_UPDATE_TESTS:
        with open(f'test/data/parse_java/{name}.graph.json', 'w') as handle:
            handle.write(graph_as_json_str)

    with open(f'test/data/parse_java/{name}.graph.json') as handle:
        expected = handle.read()

    assert graph_as_json_str == expected


@run_decorator
@pytest.mark.skims_test_group('unittesting')
async def test_control_flow_1() -> None:
    path = 'test/data/parse_java/TestCFG.java'
    graph = await java_get_graph(
        core_model.Grammar.JAVA9,
        content=await get_file_raw_content(path),
        path=path,
    )

    for s_id, t_id, edge_attrs in (
        # MethodDeclaration
        (61, 91, ALWAYS),
        # Block
        (91, 93, ALWAYS),
        # BlockStatements
        (93, 95, ALWAYS),
        (95, 129, ALWAYS),
        (129, 168, ALWAYS),
        # TryStatement
        (168, 170, ALWAYS),  # try
        (170, 172, ALWAYS),  # {}
        (170, 329, MAYBE),  # catch
        # IfThenStatement
        (454, 479, TRUE),  # then
        (454, 663, FALSE),  # pass through
        # IfThenElseStatement
        (663, 688, TRUE),  # then
        (663, 735, FALSE),  # else
        # SwitchStatement
        (2153, 2433, ALWAYS),
        # WhileStatement
        (2844, 2881, TRUE),
        (2844, 2947, FALSE),
        # DoStatement
        (2985, 3648, ALWAYS),
        # BasicForStatement
        (3648, 3730, TRUE),
        (3648, 3784, FALSE),
        # EnhancedForStatement
        (3876, 3911, TRUE),
        (3876, 4269, FALSE),
    ):
        assert has_labels(graph[str(s_id)][str(t_id)], **edge_attrs)


@run_decorator
@pytest.mark.skims_test_group('unittesting')
async def test_control_flow_2() -> None:
    path = 'test/data/lib_path/f063_path_traversal/Test.java'
    graph = await java_get_graph(
        core_model.Grammar.JAVA9,
        content=await get_file_raw_content(path),
        path=path,
    )

    assert g.flows(
        graph,
        input_type='function',
        sink_type='F063_PATH_TRAVERSAL',
    ) == (
        (0, ('30', '85', '87', '91', '125', '185', '286', '351')),
        (1, ('30', '85', '87', '91', '125', '185', '286', '351')),
    )
