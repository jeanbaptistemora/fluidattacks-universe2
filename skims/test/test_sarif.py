from itertools import (
    zip_longest,
)
import json
import os
import pytest
from pytest_mock import (
    MockerFixture,
)
from test.test_z_functional import (
    skims,
)
from typing import (
    Any,
)


def _format_sarif_res(
    content: Any,
) -> list[dict[str, str]]:
    result: list[dict[str, str]] = []
    for row in content:
        result.append(row)
    result.sort(key=str)
    return result


def check_that_sarif_results_match() -> None:
    with open("skims/test/outputs/report.sarif", encoding="utf-8") as produced:
        expected_path = os.path.join(
            os.environ["STATE"], "skims/test/data/sarif/report.sarif"
        )
        os.makedirs(os.path.dirname(expected_path), exist_ok=True)
        with open(expected_path, "w", encoding="utf-8") as expected:
            expected.write(produced.read())
            produced.seek(0)

        with open(
            "skims/test/data/sarif/report.sarif", encoding="utf-8"
        ) as expected:
            for producted_item, expected_item in zip_longest(
                _format_sarif_res(json.load(produced)["runs"][0]["results"]),
                _format_sarif_res(json.load(expected)["runs"][0]["results"]),
                fillvalue=None,
            ):
                assert producted_item == expected_item


def run_skims_for_sarif(mocker: MockerFixture) -> None:
    path = "skims/test/data/sarif/config.yaml"
    with mocker.patch(
        "core.result.get_repo_branch",
        return_value="trunk",
    ):
        code, stdout, stderr = skims("scan", path)
    assert code == 0, stdout
    assert "[INFO] Startup work dir is:" in stdout
    assert "[INFO] Success: True" in stdout
    assert not stderr, stderr
    check_that_sarif_results_match()


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("sarif_report")
def test_sarif_report(mocker: MockerFixture) -> None:
    run_skims_for_sarif(mocker)
