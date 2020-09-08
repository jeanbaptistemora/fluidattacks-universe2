# Standard library
import asyncio
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
    run_decorator,
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
from utils.system import (
    call,
)
from zone import (
    set_locale,
    t,
)


# Side effects
set_locale(LocalesEnum.EN)


async def skims(*args: str) -> Tuple[int, bytes, bytes]:
    process: asyncio.subprocess.Process = await call('skims', *args)

    stdout, stderr = await process.communicate()
    code = -1 if process.returncode is None else process.returncode

    return code, stdout, stderr


async def get_group_data(group: str) -> Set[Tuple[str, str, int, int]]:
    """Return a set of (finding, release_status, num_open, num_closed)."""
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


async def match_expected(
    group: str,
    expected: Set[Tuple[str, str, int, int]],
) -> None:
    for _ in range(10):
        if (data := await get_group_data(group)) == expected:
            break

    assert data == expected


@run_decorator
async def test_help() -> None:
    code, stdout, stderr = await skims('--help')
    assert code == 0
    assert b'Usage:' in stdout, stdout
    assert not stderr, stderr


@run_decorator
async def test_config_not_found(test_config: Callable[[str], str]) -> None:
    code, stdout, stderr = await skims('#')
    assert code == 2
    assert not stdout, stdout
    assert b"File '#' does not exist." in stderr, stderr


@run_decorator
async def test_bad_extra_things(test_config: Callable[[str], str]) -> None:
    code, stdout, stderr = await skims(test_config('bad_extra_things'))
    assert code == 1
    assert not stdout, stdout
    assert b'Some keys were not recognized: unrecognized_key' in stderr, stderr


@run_decorator
async def test_token(
    test_config: Callable[[str], str],
    test_group: str,
) -> None:
    code, stdout, stderr = await skims(
        '--token', '123',
        '--group', test_group,
        test_config('correct_nothing_to_do'),
    )
    assert code == 1
    assert not stdout, stdout
    assert b'Invalid API token' in stderr, stderr


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
    # No findings should exist because we just reset the environment
    await match_expected(test_group, set())


@run_decorator
async def test_debug_correct_nothing_to_do(
    test_config: Callable[[str], str],
    test_group: str,
    test_integrates_session: None,
) -> None:
    code, stdout, stderr = await skims(
        '--debug',
        '--group', test_group,
        test_config('correct_nothing_to_do'),
    )
    assert code == 0
    assert not stdout, stdout
    assert b'[INFO] Success: True' in stderr, stderr

    # No findings should be created, there is nothing to do !
    await match_expected(test_group, set())


@run_decorator
async def test_correct(
    test_config: Callable[[str], str],
    test_group: str,
    test_integrates_session: None,
) -> None:
    code, stdout, stderr = await skims(
        '--group', test_group,
        test_config('correct'),
    )
    assert code == 0
    assert not stdout, stdout
    assert b'[INFO] Success: True' in stderr, stderr

    # The following findings must be met
    await match_expected(test_group, {
        # Finding, status, # closed, # open
        ('F009', 'APPROVED', 0, 9),
        ('F011', 'APPROVED', 0, 13),
        ('F031_CWE378', 'SUBMITTED', 0, 1),
        ('F052', 'SUBMITTED', 0, 28),
        ('F060', 'APPROVED', 0, 18),
        ('F061', 'APPROVED', 0, 10),
        ('F085', 'APPROVED', 0, 4),
        ('F117', 'APPROVED', 0, 2),
    })


@run_decorator
async def test_correct_nothing_to_do(
    test_config: Callable[[str], str],
    test_group: str,
    test_integrates_session: None,
) -> None:
    code, stdout, stderr = await skims(
        '--group', test_group,
        test_config('correct_nothing_to_do'),
    )
    assert code == 0
    assert not stdout, stdout
    assert b'[INFO] Success: True' in stderr, stderr

    # Skims should persist the null state, closing everything on Integrates
    await match_expected(test_group, {
        # Finding, status, # closed, # open
        ('F009', 'APPROVED', 9, 0),
        ('F011', 'APPROVED', 13, 0),
        ('F031_CWE378', 'SUBMITTED', 1, 0),
        ('F052', 'SUBMITTED', 28, 0),
        ('F060', 'APPROVED', 18, 0),
        ('F061', 'APPROVED', 10, 0),
        ('F085', 'APPROVED', 4, 0),
        ('F117', 'APPROVED', 2, 0),
    })
