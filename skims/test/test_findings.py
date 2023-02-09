import os
import pytest
from pytest_mock import (
    MockerFixture,
)
import tempfile
from test.data.lib_dast import (
    f005,
    f016,
    f024,
    f031,
    f070,
    f073,
    f081,
    f099,
    f101,
    f109,
    f165,
    f177,
    f200,
    f203,
    f246,
    f250,
    f256,
    f257,
    f258,
    f259,
    f277,
    f281,
    f325,
    f333,
    f335,
    f363,
    f372,
    f394,
    f396,
    f400,
    f406,
    f407,
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
    "F005": f005.mock_data,
    "F016": f016.mock_data,
    "F024": f024.mock_data,
    "F031": f031.mock_data,
    "F070": f070.mock_data,
    "F073": f073.mock_data,
    "F081": f081.mock_data,
    "F099": f099.mock_data,
    "F101": f101.mock_data,
    "F109": f109.mock_data,
    "F165": f165.mock_data,
    "F177": f177.mock_data,
    "F200": f200.mock_data,
    "F203": f203.mock_data,
    "F246": f246.mock_data,
    "F250": f250.mock_data,
    "F256": f256.mock_data,
    "F257": f257.mock_data,
    "F258": f258.mock_data,
    "F259": f259.mock_data,
    "F277": f277.mock_data,
    "F281": f281.mock_data,
    "F325": f325.mock_data,
    "F333": f333.mock_data,
    "F335": f335.mock_data,
    "F363": f363.mock_data,
    "F372": f372.mock_data,
    "F394": f394.mock_data,
    "F396": f396.mock_data,
    "F400": f400.mock_data,
    "F406": f406.mock_data,
    "F407": f407.mock_data,
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
@pytest.mark.skims_test_group("f005")
def test_f005(mocker: MockerFixture) -> None:
    run_finding("F005", mocker)


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
@pytest.mark.skims_test_group("f012")
def test_f012(mocker: MockerFixture) -> None:
    run_finding("F012", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f015")
def test_f015(mocker: MockerFixture) -> None:
    run_finding("F015", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f016")
def test_f016(mocker: MockerFixture) -> None:
    run_finding("F016", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f017")
def test_f017(mocker: MockerFixture) -> None:
    run_finding("F017", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f021")
def test_f021(mocker: MockerFixture) -> None:
    run_finding("F021", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f022")
def test_f022(mocker: MockerFixture) -> None:
    run_finding("F022", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f024")
def test_f024(mocker: MockerFixture) -> None:
    run_finding("F024", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f031")
def test_f031(mocker: MockerFixture) -> None:
    run_finding("F031", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f034")
def test_f034(mocker: MockerFixture) -> None:
    run_finding("F034", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f035")
def test_f035(mocker: MockerFixture) -> None:
    run_finding("F035", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f037")
def test_f037(mocker: MockerFixture) -> None:
    run_finding("F037", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f042")
def test_f042(mocker: MockerFixture) -> None:
    run_finding("F042", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f044")
def test_f044(mocker: MockerFixture) -> None:
    run_finding("F044", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f052")
def test_f052(mocker: MockerFixture) -> None:
    run_finding("F052", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f055")
def test_f055(mocker: MockerFixture) -> None:
    run_finding("F055", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f056")
def test_f056(mocker: MockerFixture) -> None:
    run_finding("F056", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f058")
def test_f058(mocker: MockerFixture) -> None:
    run_finding("F058", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f059")
def test_f059(mocker: MockerFixture) -> None:
    run_finding("F059", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f060")
def test_f060(mocker: MockerFixture) -> None:
    run_finding("F060", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f063")
def test_f063(mocker: MockerFixture) -> None:
    run_finding("F063", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f065")
def test_f065(mocker: MockerFixture) -> None:
    run_finding("F065", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f066")
def test_f066(mocker: MockerFixture) -> None:
    run_finding("F066", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f070")
def test_f070(mocker: MockerFixture) -> None:
    run_finding("F070", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f073")
def test_f073(mocker: MockerFixture) -> None:
    run_finding("F073", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f075")
def test_f075(mocker: MockerFixture) -> None:
    run_finding("F075", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f079")
def test_f079(mocker: MockerFixture) -> None:
    run_finding("F079", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f081")
def test_f081(mocker: MockerFixture) -> None:
    run_finding("F081", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f083")
def test_f083(mocker: MockerFixture) -> None:
    run_finding("F083", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f085")
def test_f085(mocker: MockerFixture) -> None:
    run_finding("F085", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f086")
def test_f086(mocker: MockerFixture) -> None:
    run_finding("F086", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f089")
def test_f089(mocker: MockerFixture) -> None:
    run_finding("F089", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f091")
def test_f091(mocker: MockerFixture) -> None:
    run_finding("F091", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f096")
def test_f096(mocker: MockerFixture) -> None:
    run_finding("F096", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f097")
def test_f097(mocker: MockerFixture) -> None:
    run_finding("F097", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f098")
def test_f098(mocker: MockerFixture) -> None:
    run_finding("F098", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f099")
def test_f099(mocker: MockerFixture) -> None:
    run_finding("F099", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f100")
def test_f100(mocker: MockerFixture) -> None:
    run_finding("F100", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f101")
def test_f101(mocker: MockerFixture) -> None:
    run_finding("F101", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f107")
def test_f107(mocker: MockerFixture) -> None:
    run_finding("F107", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f109")
def test_f109(mocker: MockerFixture) -> None:
    run_finding("F109", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f112")
def test_f112(mocker: MockerFixture) -> None:
    run_finding("F112", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f117")
def test_f117(mocker: MockerFixture) -> None:
    run_finding("F117", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f120")
def test_f120(mocker: MockerFixture) -> None:
    run_finding("F120", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f127")
def test_f127(mocker: MockerFixture) -> None:
    run_finding("F127", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f128")
def test_f128(mocker: MockerFixture) -> None:
    run_finding("F128", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f134")
def test_f134(mocker: MockerFixture) -> None:
    run_finding("F134", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f135")
def test_f135(mocker: MockerFixture) -> None:
    run_finding("F135", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f143")
def test_f143(mocker: MockerFixture) -> None:
    run_finding("F143", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f148")
def test_f148(mocker: MockerFixture) -> None:
    run_finding("F148", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f149")
def test_f149(mocker: MockerFixture) -> None:
    run_finding("F149", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f152")
def test_f152(mocker: MockerFixture) -> None:
    run_finding("F152", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f153")
def test_f153(mocker: MockerFixture) -> None:
    run_finding("F153", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f157")
def test_f157(mocker: MockerFixture) -> None:
    run_finding("F157", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f160")
def test_f160(mocker: MockerFixture) -> None:
    run_finding("F160", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f164")
def test_f164(mocker: MockerFixture) -> None:
    run_finding("F164", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f165")
def test_f165(mocker: MockerFixture) -> None:
    run_finding("F165", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f176")
def test_f176(mocker: MockerFixture) -> None:
    run_finding("F176", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f177")
def test_f177(mocker: MockerFixture) -> None:
    run_finding("F177", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f183")
def test_f183(mocker: MockerFixture) -> None:
    run_finding("F183", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f188")
def test_f188(mocker: MockerFixture) -> None:
    run_finding("F188", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f200")
def test_f200(mocker: MockerFixture) -> None:
    run_finding("F200", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f203")
def test_f203(mocker: MockerFixture) -> None:
    run_finding("F203", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f211")
def test_f211(mocker: MockerFixture) -> None:
    run_finding("F211", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f234")
def test_f234(mocker: MockerFixture) -> None:
    run_finding("F234", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f236")
def test_f236(mocker: MockerFixture) -> None:
    run_finding("F236", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f237")
def test_f237(mocker: MockerFixture) -> None:
    run_finding("F237", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f239")
def test_f239(mocker: MockerFixture) -> None:
    run_finding("F239", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f246")
def test_f246(mocker: MockerFixture) -> None:
    run_finding("F246", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f250")
def test_f250(mocker: MockerFixture) -> None:
    run_finding("F250", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f256")
def test_f256(mocker: MockerFixture) -> None:
    run_finding("F256", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f257")
def test_f257(mocker: MockerFixture) -> None:
    run_finding("F257", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f258")
def test_f258(mocker: MockerFixture) -> None:
    run_finding("F258", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f259")
def test_f259(mocker: MockerFixture) -> None:
    run_finding("F259", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f266")
def test_f266(mocker: MockerFixture) -> None:
    run_finding("F266", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f267")
def test_f267(mocker: MockerFixture) -> None:
    run_finding("F267", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f277")
def test_f277(mocker: MockerFixture) -> None:
    run_finding("F277", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f280")
def test_f280(mocker: MockerFixture) -> None:
    run_finding("F280", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f281")
def test_f281(mocker: MockerFixture) -> None:
    run_finding("F281", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f297")
def test_f297(mocker: MockerFixture) -> None:
    run_finding("F297", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f300")
def test_f300(mocker: MockerFixture) -> None:
    run_finding("F300", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f309")
def test_f309(mocker: MockerFixture) -> None:
    run_finding("F309", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f320")
def test_f320(mocker: MockerFixture) -> None:
    run_finding("F320", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f325")
def test_f325(mocker: MockerFixture) -> None:
    run_finding("F325", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f332")
def test_f332(mocker: MockerFixture) -> None:
    run_finding("F332", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f338")
def test_f338(mocker: MockerFixture) -> None:
    run_finding("F338", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f333")
def test_f333(mocker: MockerFixture) -> None:
    run_finding("F333", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f335")
def test_f335(mocker: MockerFixture) -> None:
    run_finding("F335", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f343")
def test_f343(mocker: MockerFixture) -> None:
    run_finding("F343", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f344")
def test_f344(mocker: MockerFixture) -> None:
    run_finding("F344", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f346")
def test_f346(mocker: MockerFixture) -> None:
    run_finding("F346", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f350")
def test_f350(mocker: MockerFixture) -> None:
    run_finding("F350", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f353")
def test_f353(mocker: MockerFixture) -> None:
    run_finding("F353", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f354")
def test_f354(mocker: MockerFixture) -> None:
    run_finding("F354", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f363")
def test_f363(mocker: MockerFixture) -> None:
    run_finding("F363", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f366")
def test_f366(mocker: MockerFixture) -> None:
    run_finding("F366", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f368")
def test_f368(mocker: MockerFixture) -> None:
    run_finding("F368", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f371")
def test_f371(mocker: MockerFixture) -> None:
    run_finding("F371", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f372")
def test_f372(mocker: MockerFixture) -> None:
    run_finding("F372", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f379")
def test_f379(mocker: MockerFixture) -> None:
    run_finding("F379", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f380")
def test_f380(mocker: MockerFixture) -> None:
    run_finding("F380", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f381")
def test_f381(mocker: MockerFixture) -> None:
    run_finding("F381", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f393")
def test_f393(mocker: MockerFixture) -> None:
    run_finding("F393", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f394")
def test_f394(mocker: MockerFixture) -> None:
    run_finding("F394", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f396")
def test_f396(mocker: MockerFixture) -> None:
    run_finding("F396", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f400")
def test_f400(mocker: MockerFixture) -> None:
    run_finding("F400", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f401")
def test_f401(mocker: MockerFixture) -> None:
    run_finding("F401", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f402")
def test_f402(mocker: MockerFixture) -> None:
    run_finding("F402", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f403")
def test_f403(mocker: MockerFixture) -> None:
    run_finding("F403", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f405")
def test_f405(mocker: MockerFixture) -> None:
    run_finding("F405", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f406")
def test_f406(mocker: MockerFixture) -> None:
    run_finding("F406", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f407")
def test_f407(mocker: MockerFixture) -> None:
    run_finding("F407", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f408")
def test_f408(mocker: MockerFixture) -> None:
    run_finding("F408", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f412")
def test_f412(mocker: MockerFixture) -> None:
    run_finding("F412", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f413")
def test_f413(mocker: MockerFixture) -> None:
    run_finding("F413", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f414")
def test_f414(mocker: MockerFixture) -> None:
    run_finding("F414", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f416")
def test_f416(mocker: MockerFixture) -> None:
    run_finding("F416", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f418")
def test_f418(mocker: MockerFixture) -> None:
    run_finding("F418", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f423")
def test_f423(mocker: MockerFixture) -> None:
    run_finding("F423", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f426")
def test_f426(mocker: MockerFixture) -> None:
    run_finding("F426", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f427")
def test_f427(mocker: MockerFixture) -> None:
    run_finding("F427", mocker)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("f428")
def test_f428(mocker: MockerFixture) -> None:
    run_finding("F428", mocker)
