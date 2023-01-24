import os
import pytest
from pytest_mock import (
    MockerFixture,
)
import tempfile
from test.data.lib_dast import (
    f016,
    f024,
    f031,
)
from test.test_z_functional import (
    check_that_csv_results_match,
    skims,
)
from typing import (
    Any,
    Callable,
    Optional,
)

MOCKERS: dict[str, Callable] = {
    "F016": f016.mock_data,
    "F024": f024.mock_data,
    "F031": f031.mock_data,
}


def create_config(
    finding: str,
) -> str:
    template = "skims/test/data/config/template.yaml"
    with open(template, "r", encoding="utf-8") as file:
        content = file.read()
        content = content.replace("{FINDING}", str(finding))
        content = content.replace("{FINDING_LOWER}", str(finding.lower()))
        return content


def get_mock_info(finding: str) -> Optional[dict[str, Any]]:
    data = MOCKERS.get(finding)
    if data:
        return data()
    return None


def run_finding(finding: str, mocker: MockerFixture) -> None:
    with tempfile.TemporaryDirectory() as tmp_dir:
        path = os.path.join(tmp_dir, f"{finding}.yaml")
        with open(path, "w", encoding="utf-8") as tmpfile:
            tmpfile.write(create_config(finding))

        if mock_data := get_mock_info(finding):
            with mocker.patch(
                f"dast.aws.{finding.lower()}.run_boto3_fun",
                return_value=mock_data,
            ):
                code, stdout, stderr = skims("scan", path)
        else:
            code, stdout, stderr = skims("scan", path)

        assert code == 0, stdout
        assert "[INFO] Startup work dir is:" in stdout
        assert "[INFO] An output file has been written:" in stdout
        assert "[INFO] Success: True" in stdout
        assert not stderr, stderr
        check_that_csv_results_match(finding)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f001")
def test_f001(mocker: MockerFixture) -> None:
    run_finding("F001", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f004")
def test_f004(mocker: MockerFixture) -> None:
    run_finding("F004", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f007")
def test_f007(mocker: MockerFixture) -> None:
    run_finding("F007", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f008")
def test_f008(mocker: MockerFixture) -> None:
    run_finding("F008", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f009")
def test_f009(mocker: MockerFixture) -> None:
    run_finding("F009", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f011")
def test_f011(mocker: MockerFixture) -> None:
    run_finding("F011", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f016")
def test_f016(mocker: MockerFixture) -> None:
    run_finding("F016", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f024")
def test_f024(mocker: MockerFixture) -> None:
    run_finding("F024", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f031")
def test_f031(mocker: MockerFixture) -> None:
    run_finding("F031", mocker)
