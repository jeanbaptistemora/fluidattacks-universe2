from aioextensions import (
    run_decorator,
)
from model import (
    core_model,
)
import os
import pytest
from sast.parse import (
    get_graph_db,
)
from sast_symbolic_evaluation.evaluate import (
    get_all_possible_syntax_steps,
)
from typing import (
    Tuple,
)
from utils.encodings import (
    json_dumps,
)


@pytest.mark.skims_test_group("unittesting")
@run_decorator
@pytest.mark.parametrize(
    "files_to_test,suffix_out",
    [
        (
            (
                "skims/test/data/benchmark/instance_references/src/App.java",
                "skims/test/data/benchmark/instance_references/src/User.java",
            ),
            "instance_ref",
        ),
        (
            (
                "skims/test/data/benchmark/owasp/BenchmarkTest00001.java",
                "skims/test/data/benchmark/owasp/BenchmarkTest00008.java",
                "skims/test/data/benchmark/owasp/BenchmarkTest00167.java",
            ),
            "benchmark",
        ),
        (
            (
                "skims/test/data/lib_path/f160/Test.java",
                "skims/test/data/lib_path/f063_path_traversal/Test.java",
            ),
            "findings",
        ),
        (
            (
                "skims/test/data/sast/TestCFG.java",
                "skims/test/data/sast/test_cfg.js",
                "skims/test/data/sast/test_cfg.go",
                "skims/test/data/sast/test_cfg.kt",
            ),
            "cfg",
        ),
        (
            (
                (
                    "skims/test/data/benchmark/nist/"
                    "CWE89_SQL_Injection__Web_Params_Get_Web_CommandText_01.cs"
                ),
                "skims/test/data/benchmark/nist/StudentController.cs",
                "skims/test/data/benchmark/nist/HouseController.cs",
                "skims/test/data/benchmark/nist/block_chaining_insecure.cs",
            ),
            "nist",
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

    expected_path = os.path.join(
        os.environ["STATE"],
        f"skims/test/data/sast/root-graph_{suffix_out}.json",
    )
    os.makedirs(os.path.dirname(expected_path), exist_ok=True)
    with open(expected_path, "w") as handle:
        handle.write(graph_db_as_json_str)

    with open(f"skims/test/data/sast/root-graph_{suffix_out}.json") as handle:
        expected = handle.read()

    assert graph_db_as_json_str == expected

    # Test SymEval
    syntax_steps = {
        finding.name: get_all_possible_syntax_steps(graph_db, finding)
        for finding in core_model.FindingEnum
    }
    syntax_steps_as_json_str = json_dumps(
        syntax_steps,
        indent=2,
        sort_keys=True,
    )

    expected_path = os.path.join(
        os.environ["STATE"],
        f"skims/test/data/sast/root-graph-syntax_{suffix_out}.json",
    )
    os.makedirs(os.path.dirname(expected_path), exist_ok=True)
    with open(expected_path, "w") as handle:
        handle.write(syntax_steps_as_json_str)

    with open(
        f"skims/test/data/sast/root-graph-syntax_{suffix_out}.json",
    ) as handle:
        expected = handle.read()

    assert syntax_steps_as_json_str == expected
