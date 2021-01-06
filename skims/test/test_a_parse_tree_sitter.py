# Third party libraries
import pytest

# Local libraries
from parse_tree_sitter.parse import (
    parse,
    PARSER_JAVA,
)
from utils.graph import (
    export_graph_as_json,
)
from utils.encodings import (
    json_dumps,
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
@pytest.mark.skims_test_group('unittesting')
def test_graph_generation(path: str, name: str) -> None:
    with open(path, 'r') as handle:
        graph = parse(
            content=handle.read().encode(),
            parser=PARSER_JAVA,
            path=path,
        )

    graph_as_json = export_graph_as_json(graph)
    graph_as_json_str = json_dumps(graph_as_json, indent=2, sort_keys=True)

    with open(f'test/data/parse_tree_sitter/{name}.graph.json') as handle:
        expected = handle.read()

    assert graph_as_json_str == expected
