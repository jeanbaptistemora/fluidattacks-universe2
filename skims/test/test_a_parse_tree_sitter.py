# Third party libraries
from typing import Tuple
from aioextensions import (
    run_decorator,
)
import pytest

# Local libraries
from model import (
    core_model,
)
from sast.parse import (
    get_graph_db,
)
from sast_symbolic_evaluation.evaluate import (
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
@pytest.mark.parametrize(
    "files_to_test,suffix_out",
    [
        (
            (
                'skims/test/data/benchmark/instance_references/src/App.java',
                'skims/test/data/benchmark/instance_references/src/User.java',
            ),
            'instance_ref',
        ),
        (
            (
                'skims/test/data/benchmark/owasp/BenchmarkTest00001.java',
                'skims/test/data/benchmark/owasp/BenchmarkTest00008.java',
                'skims/test/data/benchmark/owasp/BenchmarkTest00167.java',
            ),
            'benchmark',
        ),
        (
            (
                'skims/test/data/lib_path/f031_cwe378/Test.java',
                'skims/test/data/lib_path/f063_path_traversal/Test.java',
            ),
            'findings',
        ),
        (
            ('skims/test/data/sast/TestCFG.java', ),
            'cfg',
        ),
    ],
)
async def test_graph_generation(
    files_to_test: Tuple[str, ...],
    suffix_out: str,
) -> None:
    # Test the GraphDB
    graph_db = await get_graph_db(files_to_test)
    graph_db_as_json_str = json_dumps(graph_db, indent=2, sort_keys=True)

    if SHOULD_UPDATE_TESTS:
        with open(
                f'skims/test/data/sast/root-graph_{suffix_out}.json',
                'w',
        ) as handle:
            handle.write(graph_db_as_json_str)

    with open(f'skims/test/data/sast/root-graph_{suffix_out}.json') as handle:
        expected = handle.read()

    # Test SymEval
    syntax_steps = {
        finding.name: get_possible_syntax_steps(graph_db, finding)
        for finding in core_model.FindingEnum
    }
    syntax_steps_as_json_str = json_dumps(
        syntax_steps,
        indent=2,
        sort_keys=True,
    )

    if SHOULD_UPDATE_TESTS:
        with open(
                f'skims/test/data/sast/root-graph-syntax_{suffix_out}.json',
                'w',
        ) as handle:
            handle.write(syntax_steps_as_json_str)

    with open(f'skims/test/data/sast/root-graph-syntax_{suffix_out}.json',
              ) as handle:
        expected = handle.read()

    assert syntax_steps_as_json_str == expected
