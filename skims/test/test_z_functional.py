from cli import (
    cli,
)
from contextlib import (
    redirect_stderr,
    redirect_stdout,
)
import csv
import io
from itertools import (
    zip_longest,
)
from model import (
    cvss3_model,
)
import os
import pytest
from typing import (
    Callable,
    Dict,
    Iterable,
    List,
    Text,
    Tuple,
)
from utils.logs import (
    configure,
)


def _default_snippet_filter(snippet: str) -> str:
    return snippet


def skims(*args: str) -> Tuple[int, str, str]:
    out_buffer, err_buffer = io.StringIO(), io.StringIO()

    code: int = 0
    with redirect_stdout(out_buffer), redirect_stderr(err_buffer):
        try:
            configure()
            cli.main(args=list(args), prog_name="skims")
        except SystemExit as exc:  # NOSONAR
            if isinstance(exc.code, int):
                code = exc.code
    try:
        return code, out_buffer.getvalue(), err_buffer.getvalue()
    finally:
        del out_buffer
        del err_buffer


def get_suite_config(suite: str) -> str:
    return f"skims/test/data/config/{suite}.yaml"


def get_suite_expected_results(suite: str) -> str:
    return f"skims/test/data/results/{suite}.csv"


def get_suite_produced_results(suite: str) -> str:
    return f"skims/test/outputs/{suite}.csv"


def _format_csv(
    content: Iterable[Text],
    *,
    snippet_filter: Callable[[str], str],
) -> List[Dict[str, str]]:
    result: List[Dict[str, str]] = []
    for row in csv.DictReader(content):
        row["snippet"] = snippet_filter(row["snippet"])
        result.append(row)
    result.sort(key=str)
    return result


def check_that_csv_results_match(
    suite: str,
    *,
    snippet_filter: Callable[[str], str] = _default_snippet_filter,
) -> None:
    with open(get_suite_produced_results(suite), encoding="utf-8") as produced:
        expected_path = os.path.join(
            os.environ["STATE"], get_suite_expected_results(suite)
        )
        os.makedirs(os.path.dirname(expected_path), exist_ok=True)
        with open(expected_path, "w", encoding="utf-8") as expected:
            expected.write(produced.read())
            produced.seek(0)

        with open(
            get_suite_expected_results(suite), encoding="utf-8"
        ) as expected:
            for producted_item, expected_item in zip_longest(
                _format_csv(produced, snippet_filter=snippet_filter),
                _format_csv(expected, snippet_filter=snippet_filter),
                fillvalue=None,
            ):
                assert producted_item == expected_item


@pytest.mark.skims_test_group("unittesting")
def test_find_score_data() -> None:
    assert cvss3_model.find_score_data("001") == cvss3_model.Score(
        attack_complexity=cvss3_model.AttackComplexity.L,
        attack_vector=cvss3_model.AttackVector.N,
        availability_impact=cvss3_model.AvailabilityImpact.N,
        confidentiality_impact=cvss3_model.ConfidentialityImpact.N,
        exploitability=cvss3_model.Exploitability.P,
        integrity_impact=cvss3_model.IntegrityImpact.L,
        privileges_required=cvss3_model.PrivilegesRequired.N,
        remediation_level=cvss3_model.RemediationLevel.O,
        report_confidence=cvss3_model.ReportConfidence.R,
        severity_scope=cvss3_model.SeverityScope.U,
        user_interaction=cvss3_model.UserInteraction.N,
    )

    assert cvss3_model.find_score_data("172") == cvss3_model.Score(
        attack_complexity=cvss3_model.AttackComplexity.H,
        attack_vector=cvss3_model.AttackVector.L,
        availability_impact=cvss3_model.AvailabilityImpact.N,
        confidentiality_impact=cvss3_model.ConfidentialityImpact.L,
        exploitability=cvss3_model.Exploitability.X,
        integrity_impact=cvss3_model.IntegrityImpact.N,
        privileges_required=cvss3_model.PrivilegesRequired.N,
        remediation_level=cvss3_model.RemediationLevel.O,
        report_confidence=cvss3_model.ReportConfidence.X,
        severity_scope=cvss3_model.SeverityScope.U,
        user_interaction=cvss3_model.UserInteraction.N,
    )

    assert cvss3_model.find_score_data("402") == cvss3_model.Score(
        attack_complexity=cvss3_model.AttackComplexity.H,
        attack_vector=cvss3_model.AttackVector.N,
        availability_impact=cvss3_model.AvailabilityImpact.N,
        confidentiality_impact=cvss3_model.ConfidentialityImpact.N,
        exploitability=cvss3_model.Exploitability.P,
        integrity_impact=cvss3_model.IntegrityImpact.L,
        privileges_required=cvss3_model.PrivilegesRequired.L,
        remediation_level=cvss3_model.RemediationLevel.O,
        report_confidence=cvss3_model.ReportConfidence.R,
        severity_scope=cvss3_model.SeverityScope.U,
        user_interaction=cvss3_model.UserInteraction.N,
    )


@pytest.mark.skims_test_group("unittesting")
def test_help() -> None:
    code, stdout, stderr = skims("--help")
    assert code == 0
    assert "Usage:" in stdout
    assert not stderr


@pytest.mark.skims_test_group("unittesting")
def test_non_existent_config() -> None:
    code, stdout, stderr = skims("scan", "#")
    assert code == 2
    assert not stdout, stdout
    assert "File '#' does not exist." in stderr, stderr


@pytest.mark.skims_test_group("unittesting")
def test_config_with_extra_parameters() -> None:
    suite: str = "bad_extra_things"
    code, stdout, stderr = skims("scan", get_suite_config(suite))
    assert code == 1
    assert "Some keys were not recognized: unrecognized_key" in stdout, stdout
    assert not stderr, stderr


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("lib_apk")
def test_lib_apk() -> None:
    _run_no_group("lib_apk")


@pytest.mark.flaky(reruns=3)  # The outcome depends on third party servers
@pytest.mark.skims_test_group("lib_http")
@pytest.mark.usefixtures("test_mocks_http")
def test_lib_http() -> None:
    def snippet_filter(snippet: str) -> str:
        return "\n".join(
            line for line in snippet.splitlines() if "< Date:" not in line
        )

    _run_no_group("lib_http", snippet_filter=snippet_filter)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("lib_http_2")
def test_lib_http_2() -> None:
    _run_no_group("lib_http_2")


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("lib_ssl")
@pytest.mark.usefixtures("test_mocks_ssl_safe", "test_mocks_ssl_unsafe")
def test_lib_ssl() -> None:
    _run_no_group("lib_ssl")


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("benchmark_cmdi")
def test_benchmark_cmdi() -> None:
    _run_no_group("benchmark_owasp_cmdi")


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("benchmark_crypto")
def test_benchmark_crypto() -> None:
    _run_no_group("benchmark_owasp_crypto")


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("benchmark_hash")
def test_benchmark_hash() -> None:
    _run_no_group("benchmark_owasp_hash")


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("benchmark_ldapi")
def test_benchmark_ldapi() -> None:
    _run_no_group("benchmark_owasp_ldapi")


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("benchmark_pathtraver")
def test_benchmark_pathtraver() -> None:
    _run_no_group("benchmark_owasp_pathtraver")


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("benchmark_securecookie")
def test_benchmark_securecookie() -> None:
    _run_no_group("benchmark_owasp_securecookie")


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("benchmark_sqli")
def test_benchmark_sqli() -> None:
    _run_no_group("benchmark_owasp_sqli")


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("benchmark_trustbound")
def test_benchmark_trustbound() -> None:
    _run_no_group("benchmark_owasp_trustbound")


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("benchmark_weakrand")
def test_benchmark_weakrand() -> None:
    _run_no_group("benchmark_owasp_weakrand")


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("benchmark_xpathi")
def test_benchmark_xpathi() -> None:
    _run_no_group("benchmark_owasp_xpathi")


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("benchmark_xss")
def test_benchmark_xss() -> None:
    _run_no_group("benchmark_owasp_xss")


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("instance_references")
def test_instance_reference() -> None:
    _run_no_group("instance_references")


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("vulnerableapp")
def test_vulnerableapp() -> None:
    _run_no_group("vulnerableapp")


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("vulnerable_js_app")
def test_vulnerable_js_app() -> None:
    _run_no_group("vulnerable_js_app")


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("nist_c_sharp_f001")
def test_nist_c_sharp_f001() -> None:
    _run_no_group("nist_c_sharp_f001")


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("nist_c_sharp_f004")
def test_nist_c_sharp_f004() -> None:
    _run_no_group("nist_c_sharp_f004")


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("nist_c_sharp_f008")
def test_nist_c_sharp_f008() -> None:
    _run_no_group("nist_c_sharp_f008")


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("nist_c_sharp_f021")
def test_nist_c_sharp_f021() -> None:
    _run_no_group("nist_c_sharp_f021")


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("nist_c_sharp_f052")
def test_nist_c_sharp_f052() -> None:
    _run_no_group("nist_c_sharp_f052")


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("nist_c_sharp_f063")
def test_nist_c_sharp_f063() -> None:
    _run_no_group("nist_c_sharp_f063")


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("nist_c_sharp_f107")
def test_nist_c_sharp_f107() -> None:
    _run_no_group("nist_c_sharp_f107")


def _run_no_group(
    suite: str,
    *,
    snippet_filter: Callable[[str], str] = _default_snippet_filter,
) -> None:
    code, stdout, stderr = skims("scan", get_suite_config(suite))
    assert code == 0, stdout
    assert "[INFO] Startup work dir is:" in stdout
    assert "[INFO] An output file has been written:" in stdout
    assert "[INFO] Success: True" in stdout
    assert not stderr, stderr
    check_that_csv_results_match(suite, snippet_filter=snippet_filter)
