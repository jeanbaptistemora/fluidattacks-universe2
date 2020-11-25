# Standard library
from contextlib import (
    redirect_stderr,
    redirect_stdout,
)
import io
from typing import (
    Any,
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
from utils.logs import (
    configure,
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


def do_csv_results_match(caller: Callable[..., Any]) -> bool:
    with open(f'test/outputs/results.csv') as results:
        with open(f'test/data/{caller.__name__}.csv') as expected:
            assert sorted(results.readlines()) == sorted(expected.readlines())
            return sorted(results.readlines()) == sorted(expected.readlines())


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
    assert 'Some keys were not recognized: unrecognized_key' in stdout, stdout
    assert not stderr, stderr


def test_bad_integrates_api_token(test_group: str) -> None:
    code, stdout, stderr = skims(
        '--token', '123',
        '--group', test_group,
        'test/data/config/correct_nothing_to_do.yaml',
    )
    assert code == 1
    assert 'StopRetrying: Invalid API token' in stdout, stdout
    assert not stderr, stderr


@pytest.mark.flaky(reruns=0)
def test_correct_run_no_group(test_group: str) -> None:
    code, stdout, stderr = skims('test/data/config/correct.yaml')

    assert code == 0
    assert '[INFO] Startup working dir is:' in stdout
    assert '[INFO] An output file has been written:' in stdout
    assert '[INFO] Files to be tested:' in stdout
    assert '[INFO] Success: True' in stdout
    assert not stderr, stderr
    assert do_csv_results_match(test_correct_run_no_group)


@pytest.mark.flaky(reruns=0)
def test_correct_run_no_group_again(test_group: str) -> None:
    # Execute it again to verify that cache retrievals work as expected
    # and are reproducible
    test_correct_run_no_group(test_group)


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
    assert await get_group_data(test_group) == set()


def test_debug_correct_nothing_to_do_run(test_group: str) -> None:
    code, stdout, stderr = skims(
        '--debug',
        '--group', test_group,
        'test/data/config/correct_nothing_to_do.yaml',
    )
    assert code == 0
    assert '[INFO] Startup working dir is:' in stdout
    assert '[INFO] Files to be tested: 0' in stdout
    assert f'[INFO] Results will be synced to group: {test_group}' in stdout
    assert f'[INFO] Your role in group {test_group} is: admin' in stdout
    assert '[INFO] Success: True' in stdout
    assert not stderr, stderr


@run_decorator
async def test_debug_correct_nothing_to_do_assert(
    test_group: str,
    test_integrates_session: None,
) -> None:
    # No findings should be created, there is nothing to do !
    assert await get_group_data(test_group) == set()


def test_correct_run(test_group: str) -> None:
    code, stdout, stderr = skims(
        '--group', test_group,
        'test/data/config/correct.yaml',
    )
    assert code == 0
    assert '[INFO] Startup working dir is:' in stdout
    assert '[INFO] Files to be tested:' in stdout
    assert f'[INFO] Results will be synced to group: {test_group}' in stdout
    assert f'[INFO] Your role in group {test_group} is: admin' in stdout
    assert '[INFO] Success: True' in stdout
    assert not stderr, stderr


@run_decorator
async def test_correct_assert(
    test_group: str,
    test_integrates_session: None,
) -> None:
    # The following findings must be met
    assert await get_group_data(test_group) == {
        # Finding, status, open vulnerabilities
        ('F001_JPA', 'APPROVED', (
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
            ('test/data/lib_path/f009/java.properties', '1'),
            ('test/data/lib_path/f009/java.properties', '2'),
            ('test/data/lib_path/f009/java.properties', '4'),
            ('test/data/lib_path/f009/java.properties', '8'),
            ('test/data/lib_path/f009/javascript.js', '3'),
            ('test/data/lib_path/f009/javascript.js', '4'),
            ('test/data/lib_path/f009/javascript.js', '5'),
            ('test/data/lib_path/f009/javascript.js', '6'),
            ('test/data/lib_path/f009/javascript.js', '7'),
            ('test/data/lib_path/f009/javascript.js', '8'),
            ('test/data/lib_path/f009/secrets.yaml', '1'),
            ('test/data/lib_path/f009/secrets.yaml.json', '1'),
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
        ('F022', 'SUBMITTED', (
            ('test/data/lib_path/f022/java.properties', '1'),
            ('test/data/lib_path/f022/java.properties', '4'),
        )),
        ('F031_AWS', 'APPROVED', (
            ('test/data/lib_path/f031_aws/cfn_admin_policy_attached.yaml', '10'),
            ('test/data/lib_path/f031_aws/cfn_admin_policy_attached.yaml', '6'),
            ('test/data/lib_path/f031_aws/cfn_admin_policy_attached.yaml', '8'),
            ('test/data/lib_path/f031_aws/cfn_admin_policy_attached.yaml.json', '11'),
            ('test/data/lib_path/f031_aws/cfn_admin_policy_attached.yaml.json', '7'),
            ('test/data/lib_path/f031_aws/cfn_admin_policy_attached.yaml.json', '9'),
            ('test/data/lib_path/f031_aws/cfn_negative_statement.yaml', '15'),
            ('test/data/lib_path/f031_aws/cfn_negative_statement.yaml', '18'),
            ('test/data/lib_path/f031_aws/cfn_negative_statement.yaml', '22'),
            ('test/data/lib_path/f031_aws/cfn_negative_statement.yaml', '23'),
            ('test/data/lib_path/f031_aws/cfn_negative_statement.yaml', '37'),
            ('test/data/lib_path/f031_aws/cfn_negative_statement.yaml', '38'),
            ('test/data/lib_path/f031_aws/cfn_negative_statement.yaml.json', '16'),
            ('test/data/lib_path/f031_aws/cfn_negative_statement.yaml.json', '20'),
            ('test/data/lib_path/f031_aws/cfn_negative_statement.yaml.json', '25'),
            ('test/data/lib_path/f031_aws/cfn_negative_statement.yaml.json', '26'),
            ('test/data/lib_path/f031_aws/cfn_negative_statement.yaml.json', '50'),
            ('test/data/lib_path/f031_aws/cfn_negative_statement.yaml.json', '51'),
            ('test/data/lib_path/f031_aws/cfn_open_passrole.yaml', '17'),
            ('test/data/lib_path/f031_aws/cfn_open_passrole.yaml', '18'),
            ('test/data/lib_path/f031_aws/cfn_open_passrole.yaml', '8'),
            ('test/data/lib_path/f031_aws/cfn_open_passrole.yaml', '9'),
            ('test/data/lib_path/f031_aws/cfn_open_passrole.yaml.json', '10'),
            ('test/data/lib_path/f031_aws/cfn_open_passrole.yaml.json', '11'),
            ('test/data/lib_path/f031_aws/cfn_open_passrole.yaml.json', '25'),
            ('test/data/lib_path/f031_aws/cfn_open_passrole.yaml.json', '26'),
            ('test/data/lib_path/f031_aws/cfn_permissive_policy.yaml', '10'),
            ('test/data/lib_path/f031_aws/cfn_permissive_policy.yaml', '11'),
            ('test/data/lib_path/f031_aws/cfn_permissive_policy.yaml', '12'),
            ('test/data/lib_path/f031_aws/cfn_permissive_policy.yaml', '13'),
            ('test/data/lib_path/f031_aws/cfn_permissive_policy.yaml', '35'),
            ('test/data/lib_path/f031_aws/cfn_permissive_policy.yaml', '36'),
            ('test/data/lib_path/f031_aws/cfn_permissive_policy.yaml', '37'),
            ('test/data/lib_path/f031_aws/cfn_permissive_policy.yaml', '38'),
            ('test/data/lib_path/f031_aws/cfn_permissive_policy.yaml.json', '13'),
            ('test/data/lib_path/f031_aws/cfn_permissive_policy.yaml.json', '14'),
            ('test/data/lib_path/f031_aws/cfn_permissive_policy.yaml.json', '15'),
            ('test/data/lib_path/f031_aws/cfn_permissive_policy.yaml.json', '17'),
            ('test/data/lib_path/f031_aws/cfn_permissive_policy.yaml.json', '57'),
            ('test/data/lib_path/f031_aws/cfn_permissive_policy.yaml.json', '58'),
            ('test/data/lib_path/f031_aws/cfn_permissive_policy.yaml.json', '59'),
            ('test/data/lib_path/f031_aws/cfn_permissive_policy.yaml.json', '61'),
            ('test/data/lib_path/f031_aws/hcl2_admin_policy_attached.tf', '23'),
            ('test/data/lib_path/f031_aws/hcl2_admin_policy_attached.tf', '33'),
            ('test/data/lib_path/f031_aws/hcl2_admin_policy_attached.tf', '38'),
            ('test/data/lib_path/f031_aws/hcl2_negative_statement.tf','33'),
            ('test/data/lib_path/f031_aws/hcl2_negative_statement.tf','5'),
            ('test/data/lib_path/f031_aws/hcl2_open_passrole.tf', '5'),
            ('test/data/lib_path/f031_aws/hcl2_permissive_policy.tf', '37'),
            ('test/data/lib_path/f031_aws/hcl2_permissive_policy.tf', '5'),
            ('test/data/lib_path/f031_aws/hcl2_permissive_policy.tf', '73'),
        )),
        ('F031_CWE378', 'APPROVED', (
            ('test/data/lib_path/f031_cwe378/Test.java', '6'),
        )),
        ('F037', 'SUBMITTED', (
            ('test/data/lib_path/f037/javascript.js', '20'),
            ('test/data/lib_path/f037/javascript.js', '28'),
            ('test/data/lib_path/f037/javascript.js', '36'),
            ('test/data/lib_path/f037/javascript.js', '45'),
            ('test/data/lib_path/f037/javascript.js', '6'),
        )),
        ('F047_AWS', 'SUBMITTED', (
            ('test/data/lib_path/f047_aws/cfn_allows_anyone_to_admin_ports.yaml', '24'),
            ('test/data/lib_path/f047_aws/cfn_allows_anyone_to_admin_ports.yaml', '25'),
            ('test/data/lib_path/f047_aws/cfn_allows_anyone_to_admin_ports.yaml', '27'),
            ('test/data/lib_path/f047_aws/cfn_allows_anyone_to_admin_ports.yaml', '31'),
            ('test/data/lib_path/f047_aws/cfn_allows_anyone_to_admin_ports.yaml', '32'),
            ('test/data/lib_path/f047_aws/cfn_allows_anyone_to_admin_ports.yaml', '38'),
            ('test/data/lib_path/f047_aws/cfn_allows_anyone_to_admin_ports.yaml', '6'),
            ('test/data/lib_path/f047_aws/cfn_allows_anyone_to_admin_ports.yaml', '7'),
            ('test/data/lib_path/f047_aws/cfn_allows_anyone_to_admin_ports.yaml', '9'),
            ('test/data/lib_path/f047_aws/cfn_allows_anyone_to_admin_ports.yaml.json', '11'),
            ('test/data/lib_path/f047_aws/cfn_allows_anyone_to_admin_ports.yaml.json', '36'),
            ('test/data/lib_path/f047_aws/cfn_allows_anyone_to_admin_ports.yaml.json', '37'),
            ('test/data/lib_path/f047_aws/cfn_allows_anyone_to_admin_ports.yaml.json', '39'),
            ('test/data/lib_path/f047_aws/cfn_allows_anyone_to_admin_ports.yaml.json', '47'),
            ('test/data/lib_path/f047_aws/cfn_allows_anyone_to_admin_ports.yaml.json', '48'),
            ('test/data/lib_path/f047_aws/cfn_allows_anyone_to_admin_ports.yaml.json', '56'),
            ('test/data/lib_path/f047_aws/cfn_allows_anyone_to_admin_ports.yaml.json', '8'),
            ('test/data/lib_path/f047_aws/cfn_allows_anyone_to_admin_ports.yaml.json', '9'),
            ('test/data/lib_path/f047_aws/cfn_unrestricted_protocols.yaml', '26'),
            ('test/data/lib_path/f047_aws/cfn_unrestricted_protocols.yaml', '31'),
            ('test/data/lib_path/f047_aws/cfn_unrestricted_protocols.yaml', '40'),
            ('test/data/lib_path/f047_aws/cfn_unrestricted_protocols.yaml', '49'),
            ('test/data/lib_path/f047_aws/cfn_unrestricted_protocols.yaml', '69'),
            ('test/data/lib_path/f047_aws/cfn_unrestricted_protocols.yaml', '78'),
            ('test/data/lib_path/f047_aws/cfn_unrestricted_protocols.yaml', '8'),
            ('test/data/lib_path/f047_aws/cfn_unrestricted_protocols.yaml.json', '10'),
            ('test/data/lib_path/f047_aws/cfn_unrestricted_protocols.yaml.json', '111'),
            ('test/data/lib_path/f047_aws/cfn_unrestricted_protocols.yaml.json', '38'),
            ('test/data/lib_path/f047_aws/cfn_unrestricted_protocols.yaml.json', '46'),
            ('test/data/lib_path/f047_aws/cfn_unrestricted_protocols.yaml.json', '60'),
            ('test/data/lib_path/f047_aws/cfn_unrestricted_protocols.yaml.json', '72'),
            ('test/data/lib_path/f047_aws/cfn_unrestricted_protocols.yaml.json', '99'),
            ('test/data/lib_path/f047_aws/cnf_unrestricted_cidrs.yaml', '24'),
            ('test/data/lib_path/f047_aws/cnf_unrestricted_cidrs.yaml', '25'),
            ('test/data/lib_path/f047_aws/cnf_unrestricted_cidrs.yaml', '27'),
            ('test/data/lib_path/f047_aws/cnf_unrestricted_cidrs.yaml', '29'),
            ('test/data/lib_path/f047_aws/cnf_unrestricted_cidrs.yaml', '36'),
            ('test/data/lib_path/f047_aws/cnf_unrestricted_cidrs.yaml', '45'),
            ('test/data/lib_path/f047_aws/cnf_unrestricted_cidrs.yaml', '54'),
            ('test/data/lib_path/f047_aws/cnf_unrestricted_cidrs.yaml', '55'),
            ('test/data/lib_path/f047_aws/cnf_unrestricted_cidrs.yaml', '6'),
            ('test/data/lib_path/f047_aws/cnf_unrestricted_cidrs.yaml', '61'),
            ('test/data/lib_path/f047_aws/cnf_unrestricted_cidrs.yaml.json', '36'),
            ('test/data/lib_path/f047_aws/cnf_unrestricted_cidrs.yaml.json', '37'),
            ('test/data/lib_path/f047_aws/cnf_unrestricted_cidrs.yaml.json', '39'),
            ('test/data/lib_path/f047_aws/cnf_unrestricted_cidrs.yaml.json', '44'),
            ('test/data/lib_path/f047_aws/cnf_unrestricted_cidrs.yaml.json', '55'),
            ('test/data/lib_path/f047_aws/cnf_unrestricted_cidrs.yaml.json', '67'),
            ('test/data/lib_path/f047_aws/cnf_unrestricted_cidrs.yaml.json', '79'),
            ('test/data/lib_path/f047_aws/cnf_unrestricted_cidrs.yaml.json', '8'),
            ('test/data/lib_path/f047_aws/cnf_unrestricted_cidrs.yaml.json', '80'),
            ('test/data/lib_path/f047_aws/cnf_unrestricted_cidrs.yaml.json', '88'),
            ('test/data/lib_path/f047_aws/cnf_unrestricted_ports.yaml', '37'),
            ('test/data/lib_path/f047_aws/cnf_unrestricted_ports.yaml', '41'),
            ('test/data/lib_path/f047_aws/cnf_unrestricted_ports.yaml', '55'),
            ('test/data/lib_path/f047_aws/cnf_unrestricted_ports.yaml', '61'),
            ('test/data/lib_path/f047_aws/cnf_unrestricted_ports.yaml', '7'),
            ('test/data/lib_path/f047_aws/cnf_unrestricted_ports.yaml', '76'),
            ('test/data/lib_path/f047_aws/cnf_unrestricted_ports.yaml', '79'),
            ('test/data/lib_path/f047_aws/cnf_unrestricted_ports.yaml', '9'),
            ('test/data/lib_path/f047_aws/cnf_unrestricted_ports.yaml.json', '109'),
            ('test/data/lib_path/f047_aws/cnf_unrestricted_ports.yaml.json', '11'),
            ('test/data/lib_path/f047_aws/cnf_unrestricted_ports.yaml.json', '112'),
            ('test/data/lib_path/f047_aws/cnf_unrestricted_ports.yaml.json', '56'),
            ('test/data/lib_path/f047_aws/cnf_unrestricted_ports.yaml.json', '61'),
            ('test/data/lib_path/f047_aws/cnf_unrestricted_ports.yaml.json', '80'),
            ('test/data/lib_path/f047_aws/cnf_unrestricted_ports.yaml.json', '88'),
            ('test/data/lib_path/f047_aws/cnf_unrestricted_ports.yaml.json', '9')
        )),
        ('F052', 'APPROVED', (
            ('test/data/lib_path/f052/csharp.cs', '2'),
            ('test/data/lib_path/f052/csharp.cs', '3'),
            ('test/data/lib_path/f052/csharp.cs', '5'),
            ('test/data/lib_path/f052/java.java', '1'),
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
            ('test/data/lib_path/f052/java.java', '36'),
            ('test/data/lib_path/f052/java.java', '4'),
            ('test/data/lib_path/f052/java.java', '5'),
            ('test/data/lib_path/f052/java.java', '6'),
            ('test/data/lib_path/f052/java.java', '8'),
            ('test/data/lib_path/f052/java.java', '9'),
            ('test/data/lib_path/f052/java.properties', '2'),
            ('test/data/lib_path/f052/java.properties', '3'),
            ('test/data/lib_path/f052/java.properties', '4'),
            ('test/data/lib_path/f052/java.properties', '6'),
        )),
        ('F055_AWS', 'SUBMITTED', (
            ('test/data/lib_path/f055_aws/cfn_instances_without_profile.yaml', '5'),
            ('test/data/lib_path/f055_aws/cfn_instances_without_profile.yaml.json', '5'),
            ('test/data/lib_path/f055_aws/cfn_public_buckets.yaml', '16'),
            ('test/data/lib_path/f055_aws/cfn_public_buckets.yaml', '6'),
            ('test/data/lib_path/f055_aws/cfn_public_buckets.yaml.json', '24'),
            ('test/data/lib_path/f055_aws/cfn_public_buckets.yaml.json', '7'),
            ('test/data/lib_path/f055_aws/cfn_unencrypted_buckets.yaml', '6'),
            ('test/data/lib_path/f055_aws/cfn_unencrypted_buckets.yaml.json', '6'),
            ('test/data/lib_path/f055_aws/cfn_unencrypted_volumes.yaml', '12'),
            ('test/data/lib_path/f055_aws/cfn_unencrypted_volumes.yaml', '18'),
            ('test/data/lib_path/f055_aws/cfn_unencrypted_volumes.yaml', '6'),
            ('test/data/lib_path/f055_aws/cfn_unencrypted_volumes.yaml.json', '14'),
            ('test/data/lib_path/f055_aws/cfn_unencrypted_volumes.yaml.json', '22'),
            ('test/data/lib_path/f055_aws/cfn_unencrypted_volumes.yaml.json', '7'),
            ('test/data/lib_path/f055_aws/hcl2_public_buckets.tf', '24'),
            ('test/data/lib_path/f055_aws/hcl2_unencrypted_buckets.tf', '1'),
        )),
        ('F060', 'APPROVED', (
            ('test/data/lib_path/f031_cwe378/Test.java', '7'),
            ('test/data/lib_path/f060/Test.java', '11'),
            ('test/data/lib_path/f060/Test.java', '12'),
            ('test/data/lib_path/f060/Test.java', '4'),
            ('test/data/lib_path/f060/Test.java', '5'),
            ('test/data/lib_path/f060/Test.java', '7'),
            ('test/data/lib_path/f060/Test.java', '8'),
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
        ('F073', 'APPROVED', (
            ('test/data/lib_path/f073/Test.cs', '20'),
            ('test/data/lib_path/f073/Test.cs', '3'),
            ('test/data/lib_path/f073/Test.cs', '41'),
            ('test/data/lib_path/f073/Test.cs', '44'),
            ('test/data/lib_path/f073/Test.java', '44'),
            ('test/data/lib_path/f073/Test.java', '92'),
            ('test/data/lib_path/f073/javascript.js', '3'),
            ('test/data/lib_path/f073/javascript.tsx', '4'),
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
    assert '[INFO] Startup working dir is:' in stdout
    assert '[INFO] Files to be tested: 0' in stdout
    assert f'[INFO] Results will be synced to group: {test_group}' in stdout
    assert f'[INFO] Your role in group {test_group} is: admin' in stdout
    assert '[INFO] Success: True' in stdout
    assert not stderr, stderr


@run_decorator
async def test_correct_nothing_to_do_assert(
    test_group: str,
    test_integrates_session: None,
) -> None:
    # Skims should persist the null state, closing everything on Integrates
    assert await get_group_data(test_group) == {
        # Finding, status, open vulnerabilities
        ('F001_JPA', 'APPROVED', ()),
        ('F009', 'APPROVED', ()),
        ('F011', 'APPROVED', ()),
        ('F022', 'SUBMITTED', ()),
        ('F031_AWS', 'APPROVED', ()),
        ('F031_CWE378', 'APPROVED', ()),
        ('F037', 'SUBMITTED', ()),
        ('F047_AWS', 'SUBMITTED', ()),
        ('F052', 'APPROVED', ()),
        ('F055_AWS', 'SUBMITTED', ()),
        ('F060', 'APPROVED', ()),
        ('F061', 'APPROVED', ()),
        ('F073', 'APPROVED', ()),
        ('F085', 'APPROVED', ()),
        ('F117', 'APPROVED', ()),
    }
