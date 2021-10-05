from aioextensions import (
    collect,
    run_decorator,
)
from cli import (
    cli,
)
from contextlib import (
    redirect_stderr,
    redirect_stdout,
)
import csv
from integrates.dal import (
    do_add_git_root,
    do_delete_finding,
    get_finding_current_release_status,
    get_finding_vulnerabilities,
    get_group_findings,
    get_group_roots,
)
import io
from itertools import (
    zip_longest,
)
from model import (
    core_model,
)
import os
import pytest
from state.ephemeral import (
    EphemeralStore,
)
from typing import (
    Callable,
    Dict,
    Iterable,
    List,
    Set,
    Text,
    Tuple,
)
from utils.logs import (
    configure,
)
from uuid import (
    uuid4 as uuid,
)
from zone import (
    t,
)


def _default_snippet_filter(snippet: str) -> str:
    return snippet


def skims(*args: str) -> Tuple[int, str, str]:
    out_buffer, err_buffer = io.StringIO(), io.StringIO()

    with redirect_stdout(out_buffer), redirect_stderr(err_buffer):
        try:
            configure()
            cli.main(args=list(args), prog_name="skims")
        except SystemExit as exc:  # NOSONAR
            code: int = exc.code

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


async def get_group_data(
    group: str,
) -> Set[Tuple[str, str, Tuple[Tuple[str, str], ...]]]:
    """Return a set of (finding, release_status, num_open, num_closed)."""
    titles_to_finding: Dict[str, core_model.FindingEnum] = {
        t(finding.value.title): finding for finding in core_model.FindingEnum
    }

    findings = await get_group_findings(group=group)
    findings_statuses: Tuple[
        core_model.FindingReleaseStatusEnum, ...
    ] = await collect(
        [
            get_finding_current_release_status(
                finding_id=finding.identifier,
            )
            for finding in findings
        ]
    )
    findings_vulns: Tuple[EphemeralStore, ...] = await collect(
        [
            get_finding_vulnerabilities(
                finding=titles_to_finding[finding.title],
                finding_id=finding.identifier,
            )
            for finding in findings
        ]
    )

    findings_vulns_summary: List[List[Tuple[str, str]]] = []
    for vulnerabilities in findings_vulns:
        findings_vulns_summary.append([])
        async for vulnerability in vulnerabilities.iterate():
            if vulnerability.state is core_model.VulnerabilityStateEnum.OPEN:
                findings_vulns_summary[-1].append(
                    (
                        vulnerability.what_on_integrates,
                        vulnerability.where,
                    )
                )

    result: Set[Tuple[str, str, Tuple[Tuple[str, str], ...]]] = set(
        (
            titles_to_finding[finding.title].name,
            status.name,
            tuple(sorted(finding_vulns_summary)),
        )
        for finding, status, finding_vulns_summary in zip(
            findings,
            findings_statuses,
            findings_vulns_summary,
        )
    )

    return result


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


@pytest.mark.skims_test_group("unittesting")
def test_bad_integrates_api_token(test_group: str) -> None:
    suite: str = "nothing_to_do"
    code, stdout, stderr = skims(
        "scan",
        "--token",
        "123",
        "--group",
        test_group,
        get_suite_config(suite),
    )
    assert code == 1
    assert "StopRetrying: Invalid API token" in stdout, stdout
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
            line for line in snippet.splitlines() if "< Date: " not in line
        )

    _run_no_group("lib_http", snippet_filter=snippet_filter)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group("lib_path")
def test_lib_path() -> None:
    _run_no_group("lib_path")


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
@pytest.mark.skims_test_group("nist_c_sharp")
def test_nist_c_sharp() -> None:
    _run_no_group("nist_c_sharp")


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
    assert "[INFO] Startup working dir is:" in stdout
    assert "[INFO] An output file has been written:" in stdout
    assert "[INFO] Success: True" in stdout
    assert not stderr, stderr
    check_that_csv_results_match(suite, snippet_filter=snippet_filter)

    # Execute it again to verify that cache retrievals work as expected
    # and are reproducible
    code, stdout, stderr = skims("scan", get_suite_config(suite))
    check_that_csv_results_match(suite, snippet_filter=snippet_filter)


@run_decorator
@pytest.mark.skims_test_group("functional")
@pytest.mark.usefixtures("test_integrates_session")
@pytest.mark.usefixtures("test_mocks_ssl_unsafe")
async def test_integrates_group_is_pristine_run(
    test_group: str,
) -> None:
    findings = await get_group_findings(group=test_group)
    findings_deleted = await collect(
        [
            do_delete_finding(finding_id=finding.identifier)
            for finding in findings
        ]
    )

    assert all(findings_deleted)


@run_decorator
@pytest.mark.skims_test_group("functional")
@pytest.mark.usefixtures("test_integrates_session")
async def test_integrates_group_is_pristine_check(
    test_group: str,
) -> None:
    # No findings should exist because we just reset the environment
    assert await get_group_data(test_group) == set()


@run_decorator
@pytest.mark.skims_test_group("functional")
@pytest.mark.usefixtures("test_integrates_session")
async def test_integrates_group_has_required_roots(
    test_group: str,
) -> None:
    roots: Set[str] = {
        result.nickname for result in await get_group_roots(group=test_group)
    }

    for namespace in ("namespace", "namespace2"):
        if namespace in roots:
            assert True
        else:
            assert await do_add_git_root(
                group_name=test_group,
                nickname=namespace,
                url=(
                    f"git@gitlab.com:fluidattacks/{namespace}-{uuid().hex}.git"
                ),
            )


@pytest.mark.skims_test_group("functional")
def test_should_report_nothing_to_integrates_run(test_group: str) -> None:
    suite: str = "nothing_to_do"
    code, stdout, stderr = skims(
        "--debug",
        "scan",
        "--group",
        test_group,
        get_suite_config(suite),
    )
    assert code == 0
    assert "[INFO] Startup working dir is:" in stdout
    assert f"[INFO] Results will be synced to group: {test_group}" in stdout
    assert f"[INFO] Your role in group {test_group} is: admin" in stdout
    assert "[INFO] Success: True" in stdout
    assert not stderr, stderr


@run_decorator
@pytest.mark.skims_test_group("functional")
@pytest.mark.usefixtures("test_integrates_session")
async def test_should_report_nothing_to_integrates_verify(
    test_group: str,
) -> None:
    # No findings should be created, there is nothing to do !
    assert await get_group_data(test_group) == set()


@pytest.mark.skims_test_group("functional")
def test_should_report_vulns_to_namespace_run(test_group: str) -> None:
    suite: str = "integrates"
    code, stdout, stderr = skims(
        "scan",
        "--group",
        test_group,
        get_suite_config(suite),
    )
    assert code == 0
    assert "[INFO] Startup working dir is:" in stdout
    assert "[INFO] Files to be tested:" in stdout
    assert f"[INFO] Results will be synced to group: {test_group}" in stdout
    assert f"[INFO] Your role in group {test_group} is: admin" in stdout
    assert "[INFO] Success: True" in stdout
    assert not stderr, stderr
    check_that_csv_results_match(suite)


@run_decorator
@pytest.mark.skims_test_group("functional")
@pytest.mark.usefixtures("test_integrates_session")
async def test_should_report_vulns_to_namespace_verify(
    test_group: str,
) -> None:
    # The following findings must be met
    assert await get_group_data(test_group) == {
        # Finding, status, open vulnerabilities
        (
            "F133",
            "SUBMITTED",
            (
                (
                    "localhost:4446 (namespace)",
                    "server refuses connections with PFS support",
                ),
            ),
        ),
        (
            "F117",
            "APPROVED",
            (
                ("namespace/skims/test/data/lib_path/f117/.project", "1"),
                ("namespace/skims/test/data/lib_path/f117/MyJar.class", "1"),
                ("namespace/skims/test/data/lib_path/f117/MyJar.jar", "1"),
            ),
        ),
    }


@pytest.mark.skims_test_group("functional")
def test_should_report_vulns_to_namespace2_run(test_group: str) -> None:
    suite: str = "integrates2"
    code, stdout, stderr = skims(
        "scan",
        "--group",
        test_group,
        get_suite_config(suite),
    )
    assert code == 0
    assert "[INFO] Startup working dir is:" in stdout
    assert "[INFO] Files to be tested:" in stdout
    assert f"[INFO] Results will be synced to group: {test_group}" in stdout
    assert f"[INFO] Your role in group {test_group} is: admin" in stdout
    assert "[INFO] Success: True" in stdout
    assert not stderr, stderr
    check_that_csv_results_match(suite)


@run_decorator
@pytest.mark.skims_test_group("functional")
@pytest.mark.usefixtures("test_integrates_session")
async def test_should_report_vulns_to_namespace2_verify(
    test_group: str,
) -> None:
    # The following findings must be met
    assert await get_group_data(test_group) == {
        # Finding, status, open vulnerabilities
        (
            "F133",
            "SUBMITTED",
            (
                (
                    "localhost:4446 (namespace2)",
                    "server refuses connections with PFS support",
                ),
            ),
        ),
        (
            "F117",
            "APPROVED",
            (
                ("namespace/skims/test/data/lib_path/f117/.project", "1"),
                ("namespace/skims/test/data/lib_path/f117/MyJar.class", "1"),
                ("namespace/skims/test/data/lib_path/f117/MyJar.jar", "1"),
                ("namespace2/skims/test/data/lib_path/f117/.project", "1"),
                ("namespace2/skims/test/data/lib_path/f117/MyJar.class", "1"),
                ("namespace2/skims/test/data/lib_path/f117/MyJar.jar", "1"),
            ),
        ),
    }


@pytest.mark.skims_test_group("functional")
def test_should_close_vulns_to_namespace_run(test_group: str) -> None:
    suite: str = "integrates3"
    code, stdout, stderr = skims(
        "scan",
        "--group",
        test_group,
        get_suite_config(suite),
    )
    assert code == 0
    assert "[INFO] Startup working dir is:" in stdout
    assert f"[INFO] Results will be synced to group: {test_group}" in stdout
    assert f"[INFO] Your role in group {test_group} is: admin" in stdout
    assert "[INFO] Success: True" in stdout
    assert not stderr, stderr
    check_that_csv_results_match(suite)


@run_decorator
@pytest.mark.skims_test_group("functional")
@pytest.mark.usefixtures("test_integrates_session")
async def test_should_close_vulns_to_namespace_verify(
    test_group: str,
) -> None:
    # The following findings must be met
    assert await get_group_data(test_group) == {
        # Finding, status, open vulnerabilities
        (
            "F133",
            "SUBMITTED",
            (
                (
                    "localhost:4446 (namespace2)",
                    "server refuses connections with PFS support",
                ),
            ),
        ),
        (
            "F117",
            "APPROVED",
            (
                ("namespace2/skims/test/data/lib_path/f117/.project", "1"),
                ("namespace2/skims/test/data/lib_path/f117/MyJar.class", "1"),
                ("namespace2/skims/test/data/lib_path/f117/MyJar.jar", "1"),
            ),
        ),
    }


@pytest.mark.skims_test_group("functional")
def test_should_close_vulns_on_namespace2_run(test_group: str) -> None:
    suite: str = "integrates4"
    code, stdout, stderr = skims(
        "scan",
        "--group",
        test_group,
        get_suite_config(suite),
    )
    assert code == 0
    assert "[INFO] Startup working dir is:" in stdout
    assert f"[INFO] Results will be synced to group: {test_group}" in stdout
    assert f"[INFO] Your role in group {test_group} is: admin" in stdout
    assert "[INFO] Success: True" in stdout
    assert not stderr, stderr
    check_that_csv_results_match(suite)


@run_decorator
@pytest.mark.skims_test_group("functional")
@pytest.mark.usefixtures("test_integrates_session")
async def test_should_close_vulns_on_namespace2_verify(
    test_group: str,
) -> None:
    # Skims should persist the null state, closing everything on Integrates
    assert await get_group_data(test_group) == {
        # Finding, status, open vulnerabilities
        ("F133", "SUBMITTED", ()),
        ("F117", "APPROVED", ()),
    }
