# Standard library
from asyncio import (
    sleep,
)
from typing import (
    Callable,
    Dict,
    List,
    Set,
    Tuple,
)

# Third party libraries
from aioextensions import (
    collect,
    run,
    run_decorator,
)
from click.testing import (
    CliRunner,
    Result,
)

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
from utils.model import (
    FindingEnum,
    FindingReleaseStatusEnum,
    LocalesEnum,
    VulnerabilityStateEnum,
)
from zone import (
    set_locale,
    t,
)


# Side effects
set_locale(LocalesEnum.EN)


def _cli(*args: str) -> Result:
    runner = CliRunner(mix_stderr=False)

    return runner.invoke(dispatch, args)


async def get_group_data(*, group: str) -> Set[Tuple[str, str, int, int]]:
    """Return a set of (finding, release_status, num_open, num_closed)."""
    # Wait some seconds until Integrates stabilizes
    await sleep(10.0)

    titles_to_finding: Dict[str, FindingEnum] = {
        t(finding.value.title): finding for finding in FindingEnum
    }

    findings = await get_group_findings(group=group)
    findings_statuses: Tuple[FindingReleaseStatusEnum, ...] = await collect([
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

    findings_closed_vulns: List[int] = []
    findings_open_vulns: List[int] = []
    for vulnerabilities in findings_vulns:
        findings_closed_vulns.append(0)
        findings_open_vulns.append(0)
        async for vulnerability in vulnerabilities.iterate():
            if vulnerability.state is VulnerabilityStateEnum.CLOSED:
                findings_closed_vulns[-1] += 1
            elif vulnerability.state is VulnerabilityStateEnum.OPEN:
                findings_open_vulns[-1] += 1
            else:
                raise NotImplementedError()

    result: Set[Tuple[str, str, int, int]] = set(
        (
            titles_to_finding[finding.title].name,
            status.name,
            finding_closed_vulns,
            finding_open_vulns,
        )
        for finding, status, finding_closed_vulns, finding_open_vulns in zip(
            findings,
            findings_statuses,
            findings_closed_vulns,
            findings_open_vulns,
        )
    )

    return result


def blocking_get_group_data(*, group: str) -> Set[Tuple[str, str, int, int]]:
    return run(get_group_data(group=group))


def test_help() -> None:
    result = _cli('--help')
    assert result.exit_code == 0
    assert 'Usage:' in result.output


def test_dispatch_config_not_found(test_config: Callable[[str], str]) -> None:
    result = _cli('#')
    assert result.exit_code != 0
    assert "File '#' does not exist." in result.stderr, \
        (result.stderr, result.stdout, result.output)


def test_dispatch_bad_extra_things(test_config: Callable[[str], str]) -> None:
    result = _cli(test_config('bad_extra_things'))
    assert result.exit_code == 1


def test_dispatch_token(
    test_config: Callable[[str], str],
    test_group: str,
) -> None:
    config: str = test_config('correct_nothing_to_do')
    result = _cli('--token', '123', '--group', test_group, config)
    assert result.exit_code == 1


@run_decorator
async def test_reset_environment(
    test_group: str,
    test_integrates_session: None,
) -> None:
    findings = await get_group_findings(group=test_group)
    findings_deleted = await collect([
        do_delete_finding(finding_id=finding.identifier)
        for finding in findings
    ])

    assert all(findings_deleted)
    assert not await get_group_data(group=test_group)


def test_dispatch_debug_correct_nothing_to_do(
    test_config: Callable[[str], str],
    test_group: str,
    test_integrates_session: None,
) -> None:
    config: str = test_config('correct_nothing_to_do')
    result = _cli('--debug', '--group', test_group, config)
    assert result.exit_code == 0

    # No findings should be created, there is nothing to do !
    assert not blocking_get_group_data(group=test_group)


def test_dispatch_correct(
    test_config: Callable[[str], str],
    test_group: str,
    test_integrates_session: None,
) -> None:
    result = _cli('--group', test_group, test_config('correct'))
    assert result.exit_code == 0

    # The following findings must be met
    assert blocking_get_group_data(group=test_group) == {
        # Finding, status, # closed, # open
        ('F009', 'APPROVED', 0, 9),
        ('F011', 'APPROVED', 0, 13),
        ('F031_CWE378', 'SUBMITTED', 0, 1),
        ('F052', 'SUBMITTED', 0, 21),
        ('F060', 'APPROVED', 0, 18),
        ('F061', 'APPROVED', 0, 10),
        ('F085', 'APPROVED', 0, 4),
        ('F117', 'APPROVED', 0, 2),
    }


def test_dispatch_correct_nothing_to_do(
    test_config: Callable[[str], str],
    test_group: str,
    test_integrates_session: None,
) -> None:
    result = _cli('--group', test_group, test_config('correct_nothing_to_do'))
    assert result.exit_code == 0

    # Skims should persist the null state, closing everything on Integrates
    assert blocking_get_group_data(group=test_group) == {
        # Finding, status, # closed, # open
        ('F009', 'APPROVED', 9, 0),
        ('F011', 'APPROVED', 13, 0),
        ('F031_CWE378', 'SUBMITTED', 1, 0),
        ('F052', 'SUBMITTED', 21, 0),
        ('F060', 'APPROVED', 18, 0),
        ('F061', 'APPROVED', 10, 0),
        ('F085', 'APPROVED', 4, 0),
        ('F117', 'APPROVED', 2, 0),
    }
