# Third party libraries
from aioextensions import (
    run_decorator,
)
import pytest

# Local libraries
from sast.parse import (
    get_graph_db,
)
from sast.symeval import (
    get_possible_syntax_steps,
)
from utils.ctx import (
    SHOULD_UPDATE_TESTS,
)
from utils.encodings import (
    json_dumps,
)


@pytest.mark.skims_test_group('unittesting')
@run_decorator
async def test_graph_generation() -> None:
    # Test the GraphDB
    graph_db = await get_graph_db((
        'test/data/lib_path/f031_cwe378/Test.java',
        'test/data/lib_path/f063_path_traversal/Test.java',
        'test/data/benchmark/owasp/BenchmarkTest00001.java',
        'test/data/benchmark/owasp/BenchmarkTest00008.java',
        'test/data/benchmark/owasp/BenchmarkTest00167.java',
        'test/data/parse_java/TestCFG.java',
    ))
    graph_db_as_json_str = json_dumps(graph_db, indent=2, sort_keys=True)

    if SHOULD_UPDATE_TESTS:
        with open('test/data/sast/root-graph.json', 'w') as handle:
            handle.write(graph_db_as_json_str)

    with open('test/data/sast/root-graph.json') as handle:
        expected = handle.read()

    # Test SymEval
    syntax_steps = get_possible_syntax_steps(graph_db)
    syntax_steps_as_json_str = json_dumps(
        syntax_steps, indent=2, sort_keys=True,
    )

    if SHOULD_UPDATE_TESTS:
        with open('test/data/sast/root-graph-syntax.json', 'w') as handle:
            handle.write(syntax_steps_as_json_str)

    with open('test/data/sast/root-graph-syntax.json') as handle:
        expected = handle.read()

    assert syntax_steps_as_json_str == expected
