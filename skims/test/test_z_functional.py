# Standard library
from contextlib import (
    redirect_stderr,
    redirect_stdout,
)
import io
from typing import (
    Dict,
    List,
    Set,
    Tuple,
)

# Third party libraries
from aioextensions import (
    collect,
    run_decorator,
)
import pytest

# Local libraries
from cli import (
    dispatch,
)
from integrates.dal import (
    do_delete_finding,
    get_finding_current_release_status,
    get_finding_vulnerabilities,
    get_group_findings,
)
from state.ephemeral import (
    EphemeralStore,
)
from utils.ctx import (
    SHOULD_UPDATE_TESTS,
)
from utils.logs import (
    configure,
)
from model import (
    core_model,
)
from zone import (
    t,
)


def skims(*args: str) -> Tuple[int, str, str]:
    out_buffer, err_buffer = io.StringIO(), io.StringIO()

    with redirect_stdout(out_buffer), redirect_stderr(err_buffer):
        try:
            configure()
            dispatch.main(args=list(args), prog_name='skims')
        except SystemExit as exc:
            code: int = exc.code

    try:
        return code, out_buffer.getvalue(), err_buffer.getvalue()
    finally:
        del out_buffer
        del err_buffer


def get_suite_config(suite: str) -> str:
    return f'skims/test/data/config/{suite}.yaml'


def get_suite_expected_results(suite: str) -> str:
    return f'skims/test/data/results/{suite}.csv'


def get_suite_produced_results(suite: str) -> str:
    return f'skims/test/outputs/{suite}.csv'


def sorted_csv(lines: List[str]) -> List[str]:
    if len(lines) >= 2:
        return [lines[0]] + sorted(lines[1:])

    return lines


def check_that_csv_results_match(suite: str) -> None:
    with open(get_suite_produced_results(suite)) as produced:
        if SHOULD_UPDATE_TESTS:
            with open(get_suite_expected_results(suite), 'w') as expected:
                expected.writelines(sorted_csv(produced.readlines()))
                produced.seek(0)

        with open(get_suite_expected_results(suite)) as expected:
            assert sorted_csv(produced.readlines()) == expected.readlines()


async def get_group_data(group: str) -> Set[
    Tuple[str, str, Tuple[Tuple[str, str], ...]],
]:
    """Return a set of (finding, release_status, num_open, num_closed)."""
    titles_to_finding: Dict[str, core_model.FindingEnum] = {
        t(finding.value.title): finding for finding in core_model.FindingEnum
    }

    findings = await get_group_findings(group=group)
    findings_statuses: Tuple[core_model.FindingReleaseStatusEnum, ...] = \
        await collect([
            get_finding_current_release_status(
                finding_id=finding.identifier,
            )
            for finding in findings
        ])
    findings_vulns: Tuple[EphemeralStore, ...] = await collect([
        get_finding_vulnerabilities(
            finding=titles_to_finding[finding.title],
            finding_id=finding.identifier,
        )
        for finding in findings
    ])

    findings_vulns_summary: List[List[Tuple[str, str]]] = []
    for vulnerabilities in findings_vulns:
        findings_vulns_summary.append([])
        async for vulnerability in vulnerabilities.iterate():
            if vulnerability.state is core_model.VulnerabilityStateEnum.OPEN:
                findings_vulns_summary[-1].append((
                    vulnerability.what,
                    vulnerability.where,
                ))

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


@pytest.mark.skims_test_group('unittesting')
def test_help() -> None:
    code, stdout, stderr = skims('--help')
    assert code == 0
    assert 'Usage:' in stdout
    assert not stderr


@pytest.mark.skims_test_group('unittesting')
def test_non_existent_config() -> None:
    code, stdout, stderr = skims('#')
    assert code == 2
    assert not stdout, stdout
    assert 'File \'#\' does not exist.' in stderr, stderr


@pytest.mark.skims_test_group('unittesting')
def test_config_with_extra_parameters() -> None:
    suite: str = 'bad_extra_things'
    code, stdout, stderr = skims(get_suite_config(suite))
    assert code == 1
    assert 'Some keys were not recognized: unrecognized_key' in stdout, stdout
    assert not stderr, stderr


@pytest.mark.skims_test_group('unittesting')
def test_bad_integrates_api_token(test_group: str) -> None:
    suite: str = 'nothing_to_do'
    code, stdout, stderr = skims(
        '--token', '123',
        '--group', test_group,
        get_suite_config(suite),
    )
    assert code == 1
    assert 'StopRetrying: Invalid API token' in stdout, stdout
    assert not stderr, stderr


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group('unittesting')
@pytest.mark.parametrize('suite', [
    'lib_path',
])
def test_run_no_group(suite: str) -> None:
    _run_no_group(suite)


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group('benchmark_cmdi')
def test_benchmark_cmdi() -> None:
    _run_no_group('benchmark_owasp_cmdi')


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group('benchmark_ldapi')
def test_benchmark_ldapi() -> None:
    _run_no_group('benchmark_owasp_ldapi')


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group('benchmark_pathtraver')
def test_benchmark_pathtraver() -> None:
    _run_no_group('benchmark_owasp_pathtraver')


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group('benchmark_securecookie')
def test_benchmark_securecookie() -> None:
    _run_no_group('benchmark_owasp_securecookie')


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group('benchmark_sqli')
def test_benchmark_sqli() -> None:
    _run_no_group('benchmark_owasp_sqli')


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group('benchmark_trustbound')
def test_benchmark_trustbound() -> None:
    _run_no_group('benchmark_owasp_trustbound')


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group('benchmark_weakrand')
def test_benchmark_weakrand() -> None:
    _run_no_group('benchmark_owasp_weakrand')


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group('benchmark_xpathi')
def test_benchmark_xpathi() -> None:
    _run_no_group('benchmark_owasp_xpathi')


@pytest.mark.flaky(reruns=0)
@pytest.mark.skims_test_group('benchmark_xss')
def test_benchmark_xss() -> None:
    _run_no_group('benchmark_owasp_xss')


def _run_no_group(suite: str) -> None:
    code, stdout, stderr = skims(get_suite_config(suite))
    assert code == 0, stdout
    assert '[INFO] Startup working dir is:' in stdout
    assert '[INFO] An output file has been written:' in stdout
    assert '[INFO] Files to be tested:' in stdout
    assert '[INFO] Success: True' in stdout
    assert not stderr, stderr
    check_that_csv_results_match(suite)

    # Execute it again to verify that cache retrievals work as expected
    # and are reproducible
    code, stdout, stderr = skims(get_suite_config(suite))
    check_that_csv_results_match(suite)


@run_decorator
@pytest.mark.skims_test_group('functional')
async def test_integrates_group_is_pristine_run(
    test_group: str,
    test_integrates_session: None,  # pylint: disable=unused-argument
) -> None:
    findings = await get_group_findings(group=test_group)
    findings_deleted = await collect([
        do_delete_finding(finding_id=finding.identifier)
        for finding in findings
    ])

    assert all(findings_deleted)


@run_decorator
@pytest.mark.skims_test_group('functional')
async def test_integrates_group_is_pristine_check(
    test_group: str,
    test_integrates_session: None,  # pylint: disable=unused-argument
) -> None:
    # No findings should exist because we just reset the environment
    assert await get_group_data(test_group) == set()


@pytest.mark.skims_test_group('functional')
def test_should_report_nothing_to_integrates_run(test_group: str) -> None:
    suite: str = 'nothing_to_do'
    code, stdout, stderr = skims(
        '--debug',
        '--group', test_group,
        get_suite_config(suite),
    )
    assert code == 0
    assert '[INFO] Startup working dir is:' in stdout
    assert '[INFO] Files to be tested: 0' in stdout
    assert f'[INFO] Results will be synced to group: {test_group}' in stdout
    assert f'[INFO] Your role in group {test_group} is: admin' in stdout
    assert '[INFO] Success: True' in stdout
    assert not stderr, stderr


@run_decorator
@pytest.mark.skims_test_group('functional')
async def test_should_report_nothing_to_integrates_verify(
    test_group: str,
    test_integrates_session: None,  # pylint: disable=unused-argument
) -> None:
    # No findings should be created, there is nothing to do !
    assert await get_group_data(test_group) == set()


@pytest.mark.skims_test_group('functional')
def test_should_report_vulns_to_namespace_run(test_group: str) -> None:
    suite: str = 'integrates'
    code, stdout, stderr = skims(
        '--group', test_group,
        get_suite_config(suite),
    )
    assert code == 0
    assert '[INFO] Startup working dir is:' in stdout
    assert '[INFO] Files to be tested:' in stdout
    assert f'[INFO] Results will be synced to group: {test_group}' in stdout
    assert f'[INFO] Your role in group {test_group} is: admin' in stdout
    assert '[INFO] Success: True' in stdout
    assert not stderr, stderr
    check_that_csv_results_match(suite)


@run_decorator
@pytest.mark.skims_test_group('functional')
async def test_should_report_vulns_to_namespace_verify(
    test_group: str,
    test_integrates_session: None,  # pylint: disable=unused-argument
) -> None:
    # The following findings must be met
    assert await get_group_data(test_group) == {
        # Finding, status, open vulnerabilities
        ('F117', 'APPROVED', (
            ('namespace/skims/test/data/lib_path/f117/MyJar.class', '1'),
            ('namespace/skims/test/data/lib_path/f117/MyJar.jar', '1'),
        )),
    }


@pytest.mark.skims_test_group('functional')
def test_should_report_vulns_to_namespace2_run(test_group: str) -> None:
    suite: str = 'integrates2'
    code, stdout, stderr = skims(
        '--group', test_group,
        get_suite_config(suite),
    )
    assert code == 0
    assert '[INFO] Startup working dir is:' in stdout
    assert '[INFO] Files to be tested:' in stdout
    assert f'[INFO] Results will be synced to group: {test_group}' in stdout
    assert f'[INFO] Your role in group {test_group} is: admin' in stdout
    assert '[INFO] Success: True' in stdout
    assert not stderr, stderr
    check_that_csv_results_match(suite)


@run_decorator
@pytest.mark.skims_test_group('functional')
async def test_should_report_vulns_to_namespace2_verify(
    test_group: str,
    test_integrates_session: None,  # pylint: disable=unused-argument
) -> None:
    # The following findings must be met
    assert await get_group_data(test_group) == {
        # Finding, status, open vulnerabilities
        ('F117', 'APPROVED', (
            ('namespace/skims/test/data/lib_path/f117/MyJar.class', '1'),
            ('namespace/skims/test/data/lib_path/f117/MyJar.jar', '1'),
            ('namespace2/skims/test/data/lib_path/f117/MyJar.class', '1'),
            ('namespace2/skims/test/data/lib_path/f117/MyJar.jar', '1'),
        )),
    }


@pytest.mark.skims_test_group('functional')
def test_should_close_vulns_to_namespace_run(test_group: str) -> None:
    suite: str = 'integrates3'
    code, stdout, stderr = skims(
        '--group', test_group,
        get_suite_config(suite),
    )
    assert code == 0
    assert '[INFO] Startup working dir is:' in stdout
    assert '[INFO] Files to be tested:' in stdout
    assert f'[INFO] Results will be synced to group: {test_group}' in stdout
    assert f'[INFO] Your role in group {test_group} is: admin' in stdout
    assert '[INFO] Success: True' in stdout
    assert not stderr, stderr
    check_that_csv_results_match(suite)


@run_decorator
@pytest.mark.skims_test_group('functional')
async def test_should_close_vulns_to_namespace_verify(
    test_group: str,
    test_integrates_session: None,  # pylint: disable=unused-argument
) -> None:
    # The following findings must be met
    assert await get_group_data(test_group) == {
        # Finding, status, open vulnerabilities
        ('F117', 'APPROVED', (
            ('namespace2/skims/test/data/lib_path/f117/MyJar.class', '1'),
            ('namespace2/skims/test/data/lib_path/f117/MyJar.jar', '1'),
        )),
    }


@pytest.mark.skims_test_group('functional')
def test_should_close_vulns_on_namespace2_run(test_group: str) -> None:
    suite: str = 'integrates4'
    code, stdout, stderr = skims(
        '--group', test_group,
        get_suite_config(suite),
    )
    assert code == 0
    assert '[INFO] Startup working dir is:' in stdout
    assert '[INFO] Files to be tested: 0' in stdout
    assert f'[INFO] Results will be synced to group: {test_group}' in stdout
    assert f'[INFO] Your role in group {test_group} is: admin' in stdout
    assert '[INFO] Success: True' in stdout
    assert not stderr, stderr
    check_that_csv_results_match(suite)


@run_decorator
@pytest.mark.skims_test_group('functional')
async def test_should_close_vulns_on_namespace2_verify(
    test_group: str,
    test_integrates_session: None,  # pylint: disable=unused-argument
) -> None:
    # Skims should persist the null state, closing everything on Integrates
    assert await get_group_data(test_group) == {
        # Finding, status, open vulnerabilities
        ('F117', 'APPROVED', ()),
    }
