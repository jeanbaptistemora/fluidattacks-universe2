# Third party libraries
from aioextensions import (
    run_decorator,
)
import pytest

# Local libraries
from parse_tree_sitter.parse import (
    get_root,
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
    graph = await get_root((
        'test/data/lib_path/f031_cwe378/Test.java',
        'test/data/lib_path/f063_path_traversal/Test.java',
        'test/data/benchmark/owasp/BenchmarkTest00001.java',
        'test/data/benchmark/owasp/BenchmarkTest00008.java',
        'test/data/benchmark/owasp/BenchmarkTest00167.java',
        'test/data/parse_java/TestCFG.java',
    ))
    graph_as_json = export_graph_as_json(graph)
    graph_as_json_str = json_dumps(graph_as_json, indent=2, sort_keys=True)

    with open(f'test/data/parse_tree_sitter/root-graph.json') as handle:
        expected = handle.read()

    assert graph_as_json_str == expected
