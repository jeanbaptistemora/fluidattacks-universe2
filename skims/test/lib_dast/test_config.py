import csv
from itertools import (
    zip_longest,
)
import os
import pytest
from pytest_mock import (
    MockerFixture,
)
from test.lib_dast.mocks import (
    f024,
)
from test.test_z_functional import (
    skims,
)
from typing import (
    Any,
    Callable,
    Iterable,
    Text,
)

MOCKERS: dict[str, Callable] = {
    "f024": f024.mock_data,
}


def _default_snippet_filter(snippet: str) -> str:
    return snippet


def get_finding_expected_results(finding: str) -> str:
    return f"skims/test/lib_dast/results/{finding}.csv"


def get_finding_produced_results(finding: str) -> str:
    return f"skims/test/lib_dast/outputs/{finding}.csv"


def _format_csv(
    content: Iterable[Text],
    *,
    snippet_filter: Callable[[str], str],
) -> list[dict[str, str]]:
    result: list[dict[str, str]] = []
    for row in csv.DictReader(content):
        row["snippet"] = snippet_filter(row["snippet"])
        result.append(row)
    result.sort(key=str)
    return result


def get_mock_info(finding: str) -> dict[str, Any]:
    data = MOCKERS.get(finding)
    if data:
        return data()
    return {}


def check_that_csv_results_match(finding: str) -> None:
    snippet_filter: Callable[[str], str] = _default_snippet_filter
    with open(
        get_finding_produced_results(finding), encoding="utf-8"
    ) as produced:
        expected_path = os.path.join(
            os.environ["STATE"], get_finding_expected_results(finding)
        )
        os.makedirs(os.path.dirname(expected_path), exist_ok=True)
        with open(expected_path, "w", encoding="utf-8") as expected:
            expected.write(produced.read())
            produced.seek(0)

        with open(
            get_finding_expected_results(finding), encoding="utf-8"
        ) as expected:
            for producted_item, expected_item in zip_longest(
                _format_csv(produced, snippet_filter=snippet_filter),
                _format_csv(expected, snippet_filter=snippet_filter),
                fillvalue=None,
            ):
                assert producted_item == expected_item


def run_finding(finding: str, mocker: MockerFixture) -> None:
    path = "skims/test/lib_dast/template.yaml"
    mock_data = get_mock_info(finding)
    with mocker.patch(
        f"dast.aws.{finding}.run_boto3_fun",
        return_value=mock_data,
    ):
        code, stdout, stderr = skims("scan", path)
    assert code == 0, stdout
    assert "[INFO] Startup work dir is:" in stdout
    assert "[INFO] An output file has been written:" in stdout
    assert "[INFO] Success: True" in stdout
    assert not stderr, stderr
    check_that_csv_results_match(finding)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("lib_dast")
def test_aws(mocker: MockerFixture) -> None:
    run_finding("f024", mocker)
