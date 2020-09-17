# Standard library
import asyncio
from contextlib import (
    redirect_stderr,
    redirect_stdout,
)
import io
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
    read,
)
from zone import (
    set_locale,
    t,
)


# Side effects
set_locale(LocalesEnum.EN)


def skims(*args: str) -> Tuple[int, str, str]:
    out_buffer, err_buffer = io.StringIO(), io.StringIO()

    with redirect_stdout(out_buffer), redirect_stderr(err_buffer):
        try:
            dispatch.main(args=list(args), prog_name='skims')
        except SystemExit as exc:
            code: int = exc.code

    return code, out_buffer.getvalue(), err_buffer.getvalue()


async def get_group_data(group: str) -> Set[
    Tuple[str, str, Tuple[Tuple[str, str], ...]],
]:
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

    findings_vulns_summary: List[List[Tuple[str, str]]] = []
    for vulnerabilities in findings_vulns:
        findings_vulns_summary.append([])
        async for vulnerability in vulnerabilities.iterate():
            if vulnerability.state is VulnerabilityStateEnum.OPEN:
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


def test_help() -> None:
    code, stdout, stderr = skims('--help')
    assert code == 0
    assert 'Usage:' in stdout
    assert not stderr


def test_non_existent_config() -> None:
    code, stdout, stderr = skims('#')
    assert code == 2
    assert not stdout, stdout
    assert "File '#' does not exist." in stderr, stderr


def test_config_with_extra_parameters() -> None:
    code, stdout, stderr = skims('test/data/config/bad_extra_things.yaml')
    assert code == 1
    assert not stdout, stdout
    assert not stderr, stderr


def test_bad_integrates_api_token(test_group: str) -> None:
    code, stdout, stderr = skims(
        '--token', '123',
        '--group', test_group,
        'test/data/config/correct_nothing_to_do.yaml',
    )
    assert code == 1
    assert not stdout, stdout
    assert not stderr, stderr


@run_decorator
async def test_reset_environment_run(
    test_group: str,
    test_integrates_session: None,
) -> None:
    findings = await get_group_findings(group=test_group)
    findings_deleted = await collect([
        do_delete_finding(finding_id=finding.identifier)
        for finding in findings
    ])

    assert all(findings_deleted)


@run_decorator
async def test_reset_environment_assert(
    test_group: str,
    test_integrates_session: None,
) -> None:
    # No findings should exist because we just reset the environment
    await get_group_data(test_group) == set()


def test_debug_correct_nothing_to_do_run(test_group: str) -> None:
    code, stdout, stderr = skims(
        '--debug',
        '--group', test_group,
        'test/data/config/correct_nothing_to_do.yaml',
    )
    assert code == 0
    assert not stdout, stdout
    assert not stderr, stderr


@run_decorator
async def test_debug_correct_nothing_to_do_assert(
    test_group: str,
    test_integrates_session: None,
) -> None:
    # No findings should be created, there is nothing to do !
    await get_group_data(test_group) == set()


def test_correct_run(test_group: str) -> None:
    code, stdout, stderr = skims(
        '--group', test_group,
        'test/data/config/correct.yaml',
    )
    assert code == 0
    assert not stdout, stdout
    assert not stderr, stderr


@run_decorator
async def test_correct_assert(
    test_group: str,
    test_integrates_session: None,
) -> None:
    # The following findings must be met
    await get_group_data(test_group) == {
        # Finding, status, open vulnerabilities
        ('F001_JPA', 'SUBMITTED', (
            ('test/data/lib_path/f001_jpa/java.java', '23'),
            ('test/data/lib_path/f001_jpa/java.java', '26'),
            ('test/data/lib_path/f001_jpa/java.java', '36'),
            ('test/data/lib_path/f001_jpa/java.java', '39'),
            ('test/data/lib_path/f001_jpa/java.java', '42'),
            ('test/data/lib_path/f001_jpa/java.java', '45'),
        )),
        ('F009', 'APPROVED', (
            ('test/data/lib_path/f009/Dockerfile', '1'),
            ('test/data/lib_path/f009/Dockerfile', '2'),
            ('test/data/lib_path/f009/javascript.js', '3'),
            ('test/data/lib_path/f009/javascript.js', '4'),
            ('test/data/lib_path/f009/javascript.js', '5'),
            ('test/data/lib_path/f009/javascript.js', '6'),
            ('test/data/lib_path/f009/javascript.js', '7'),
            ('test/data/lib_path/f009/javascript.js', '8'),
            ('test/data/lib_path/f009/secrets.yaml', '1'),
        )),
        ('F011', 'APPROVED', (
            ('test/data/lib_path/f011/package-lock.json (hoek v5.0.0) [CVE-2018-3728]', '6'),
            ('test/data/lib_path/f011/package.json (hoek v^5.0.0) [CVE-2018-3728]', '5'),
            ('test/data/lib_path/f011/package.json (jquery v0.*) [CVE-2011-4969]', '7'),
            ('test/data/lib_path/f011/package.json (jquery v0.*) [CVE-2015-9251]', '7'),
            ('test/data/lib_path/f011/package.json (jquery v0.*) [CVE-2017-16012]', '7'),
            ('test/data/lib_path/f011/package.json (jquery v0.*) [CVE-2019-11358]', '7'),
            ('test/data/lib_path/f011/package.json (jquery v0.*) [CVE-2020-7656]', '7'),
            ('test/data/lib_path/f011/package.json (lodash v0.*) [CVE-2018-16487]', '6'),
            ('test/data/lib_path/f011/package.json (lodash v0.*) [CVE-2018-3721]', '6'),
            ('test/data/lib_path/f011/package.json (lodash v0.*) [CVE-2019-1010266]', '6'),
            ('test/data/lib_path/f011/package.json (lodash v0.*) [CVE-2019-10744]', '6'),
            ('test/data/lib_path/f011/package.json (lodash v0.*) [CVE-2020-8203]', '6'),
            ('test/data/lib_path/f011/package.json (lodash v0.*) [github.com/lodash/lodash/issues/4874]', '6'),
        )),
        ('F031_AWS', 'SUBMITTED', (
            ('test/data/lib_path/f031_aws/cfn_negative_statement.yaml', '13'),
            ('test/data/lib_path/f031_aws/cfn_negative_statement.yaml', '17'),
            ('test/data/lib_path/f031_aws/cfn_negative_statement.yaml', '21'),
            ('test/data/lib_path/f031_aws/cfn_negative_statement.yaml', '36'),
            ('test/data/lib_path/f031_aws/cfn_negative_statement.yaml.json', '14'),
            ('test/data/lib_path/f031_aws/cfn_negative_statement.yaml.json', '19'),
            ('test/data/lib_path/f031_aws/cfn_negative_statement.yaml.json', '24'),
            ('test/data/lib_path/f031_aws/cfn_negative_statement.yaml.json', '49'),
            ('test/data/lib_path/f031_aws/cfn_permissive_policy.yaml', '9'),
            ('test/data/lib_path/f031_aws/cfn_permissive_policy.yaml.json', '12'),
        )),
        ('F031_CWE378', 'APPROVED', (
            ('test/data/lib_path/f031_cwe378/Test.java', '6'),
        )),
        ('F052', 'APPROVED', (
            ('test/data/lib_path/f052/csharp.cs', '2'),
            ('test/data/lib_path/f052/csharp.cs', '3'),
            ('test/data/lib_path/f052/csharp.cs', '5'),
            ('test/data/lib_path/f052/java.java', '1'),
            ('test/data/lib_path/f052/java.java', '11'),
            ('test/data/lib_path/f052/java.java', '12'),
            ('test/data/lib_path/f052/java.java', '13'),
            ('test/data/lib_path/f052/java.java', '14'),
            ('test/data/lib_path/f052/java.java', '15'),
            ('test/data/lib_path/f052/java.java', '17'),
            ('test/data/lib_path/f052/java.java', '18'),
            ('test/data/lib_path/f052/java.java', '19'),
            ('test/data/lib_path/f052/java.java', '20'),
            ('test/data/lib_path/f052/java.java', '21'),
            ('test/data/lib_path/f052/java.java', '22'),
            ('test/data/lib_path/f052/java.java', '23'),
            ('test/data/lib_path/f052/java.java', '24'),
            ('test/data/lib_path/f052/java.java', '25'),
            ('test/data/lib_path/f052/java.java', '26'),
            ('test/data/lib_path/f052/java.java', '27'),
            ('test/data/lib_path/f052/java.java', '30'),
            ('test/data/lib_path/f052/java.java', '33'),
            ('test/data/lib_path/f052/java.java', '35'),
            ('test/data/lib_path/f052/java.java', '4'),
            ('test/data/lib_path/f052/java.java', '5'),
            ('test/data/lib_path/f052/java.java', '6'),
            ('test/data/lib_path/f052/java.java', '8'),
            ('test/data/lib_path/f052/java.java', '9'),
        )),
        ('F060', 'APPROVED', (
            ('test/data/lib_path/f031_cwe378/Test.java', '7'),
            ('test/data/lib_path/f060/csharp.cs', '2'),
            ('test/data/lib_path/f060/csharp.cs', '3'),
            ('test/data/lib_path/f060/csharp.cs', '4'),
            ('test/data/lib_path/f060/csharp.cs', '5'),
            ('test/data/lib_path/f060/java.java', '2'),
            ('test/data/lib_path/f060/java.java', '3'),
            ('test/data/lib_path/f060/java.java', '4'),
            ('test/data/lib_path/f060/java.java', '5'),
            ('test/data/lib_path/f060/python.py', '2'),
            ('test/data/lib_path/f060/python.py', '4'),
            ('test/data/lib_path/f060/python.py', '5'),
            ('test/data/lib_path/f060/swift.swift', '5'),
            ('test/data/lib_path/f060/swift.swift', '6'),
            ('test/data/lib_path/f060/swift.swift', '7'),
            ('test/data/lib_path/f061/swift.swift', '5'),
            ('test/data/lib_path/f061/swift.swift', '6'),
            ('test/data/lib_path/f061/swift.swift', '7'),
        )),
        ('F061', 'APPROVED', (
            ('test/data/lib_path/f031_cwe378/Test.java', '7'),
            ('test/data/lib_path/f061/csharp.cs', '2'),
            ('test/data/lib_path/f061/java.java', '2'),
            ('test/data/lib_path/f061/javascript.js', '3'),
            ('test/data/lib_path/f061/javascript.js', '4'),
            ('test/data/lib_path/f061/javascript.js', '5'),
            ('test/data/lib_path/f061/python.py', '21'),
            ('test/data/lib_path/f061/swift.swift', '5'),
            ('test/data/lib_path/f061/swift.swift', '6'),
            ('test/data/lib_path/f061/swift.swift', '7'),
        )),
        ('F085', 'APPROVED', (
            ('test/data/lib_path/f085/react.jsx', '1'),
            ('test/data/lib_path/f085/react.jsx', '4'),
            ('test/data/lib_path/f085/react.jsx', '5'),
            ('test/data/lib_path/f085/react.jsx', '6'),
        )),
        ('F117', 'APPROVED', (
            ('test/data/lib_path/f117/MyJar.class', '1'),
            ('test/data/lib_path/f117/MyJar.jar', '1'),
        )),
    }


def test_correct_nothing_to_do_run(test_group: str) -> None:
    code, stdout, stderr = skims(
        '--group', test_group,
        'test/data/config/correct_nothing_to_do.yaml',
    )
    assert code == 0
    assert not stdout, stdout
    assert not stderr, stderr


@run_decorator
async def test_correct_nothing_to_do_assert(
    test_group: str,
    test_integrates_session: None,
) -> None:
    # Skims should persist the null state, closing everything on Integrates
    await get_group_data(test_group) == {
        # Finding, status, open vulnerabilities
        ('F001_JPA', 'SUBMITTED', ()),
        ('F009', 'APPROVED', ()),
        ('F011', 'APPROVED', ()),
        ('F031_AWS', 'SUBMITTED', ()),
        ('F031_CWE378', 'APPROVED', ()),
        ('F052', 'APPROVED', ()),
        ('F060', 'APPROVED', ()),
        ('F061', 'APPROVED', ()),
        ('F085', 'APPROVED', ()),
        ('F117', 'APPROVED', ()),
    }
