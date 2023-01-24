import csv
from itertools import (
    zip_longest,
)
import os
import pytest
from pytest_mock import (
    MockerFixture,
)
import tempfile
from test.lib_dast.mocks import (
    f016,
    f024,
    f031,
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
    "F016": f016.mock_data,
    "F024": f024.mock_data,
    "F031": f031.mock_data,
}


def create_config(
    finding: str,
) -> str:
    template = "skims/test/lib_dast/template.yaml"
    with open(template, "r", encoding="utf-8") as file:
        content = file.read()
        content = content.replace("{FINDING}", str(finding))
        return content


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
    with tempfile.TemporaryDirectory() as tmp_dir:
        path = os.path.join(tmp_dir, f"{finding}.yaml")
        with open(path, "w", encoding="utf-8") as tmpfile:
            tmpfile.write(create_config(finding))
        mock_data = get_mock_info(finding)
        with mocker.patch(
            f"dast.aws.{finding.lower()}.run_boto3_fun",
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
@pytest.mark.skims_test_group("dast_f016")
def test_dast_f016(mocker: MockerFixture) -> None:
    run_finding("F016", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("dast_f024")
def test_dast_f024(mocker: MockerFixture) -> None:
    run_finding("F024", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("dast_f031")
def test_dast_f031(mocker: MockerFixture) -> None:
    run_finding("F031", mocker)
