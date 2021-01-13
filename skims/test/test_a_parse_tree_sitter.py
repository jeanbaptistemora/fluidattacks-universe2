# Third party libraries
from aioextensions import (
    run_decorator,
)
import pytest

# Local libraries
from sast.parse import (
    get_graph_db,
)
from utils.graph import (
    export_graph_as_json,
)
from utils.encodings import (
    json_dumps,
)


@pytest.mark.skims_test_group('unittesting')
@run_decorator
async def test_graph_generation() -> None:
    graph_db = await get_graph_db((
        'test/data/lib_path/f031_cwe378/Test.java',
        'test/data/lib_path/f063_path_traversal/Test.java',
        'test/data/benchmark/owasp/BenchmarkTest00001.java',
        'test/data/benchmark/owasp/BenchmarkTest00008.java',
        'test/data/benchmark/owasp/BenchmarkTest00167.java',
        'test/data/parse_java/TestCFG.java',
    ))
    graph_db_as_json_str = json_dumps(graph_db, indent=2, sort_keys=True)

    with open(f'test/data/sast/root-graph.json') as handle:
        expected = handle.read()

    assert graph_db_as_json_str == expected
