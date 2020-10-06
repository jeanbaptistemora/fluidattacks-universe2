# Standard library
from contextlib import (
    redirect_stderr,
    redirect_stdout,
)
import io
from textwrap import (
    dedent,
)
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


def test_correct_run_no_group(test_group: str) -> None:
    code, stdout, stderr = skims('test/data/config/correct.yaml')

    assert code == 0
    assert '[INFO] Startup working dir is:' in stdout
    assert '[INFO] Files to be tested:' in stdout
    assert '[INFO] Success: True' in stdout
    assert '\n'.join(tuple(sorted(
        line
        for line in stdout.splitlines()
        if line.startswith('[INFO] FIN')
    ))) == dedent("""
        [INFO] FIN.H.060. Insecure exceptions: test/data/lib_path/f031_cwe378/Test.java, line 7
        [INFO] FIN.H.060. Insecure exceptions: test/data/lib_path/f060/csharp.cs, line 2
        [INFO] FIN.H.060. Insecure exceptions: test/data/lib_path/f060/csharp.cs, line 3
        [INFO] FIN.H.060. Insecure exceptions: test/data/lib_path/f060/csharp.cs, line 4
        [INFO] FIN.H.060. Insecure exceptions: test/data/lib_path/f060/csharp.cs, line 5
        [INFO] FIN.H.060. Insecure exceptions: test/data/lib_path/f060/java.java, line 2
        [INFO] FIN.H.060. Insecure exceptions: test/data/lib_path/f060/java.java, line 3
        [INFO] FIN.H.060. Insecure exceptions: test/data/lib_path/f060/java.java, line 4
        [INFO] FIN.H.060. Insecure exceptions: test/data/lib_path/f060/java.java, line 5
        [INFO] FIN.H.060. Insecure exceptions: test/data/lib_path/f060/python.py, line 2
        [INFO] FIN.H.060. Insecure exceptions: test/data/lib_path/f060/python.py, line 4
        [INFO] FIN.H.060. Insecure exceptions: test/data/lib_path/f060/python.py, line 5
        [INFO] FIN.H.060. Insecure exceptions: test/data/lib_path/f060/swift.swift, line 5
        [INFO] FIN.H.060. Insecure exceptions: test/data/lib_path/f060/swift.swift, line 6
        [INFO] FIN.H.060. Insecure exceptions: test/data/lib_path/f060/swift.swift, line 7
        [INFO] FIN.H.060. Insecure exceptions: test/data/lib_path/f061/swift.swift, line 5
        [INFO] FIN.H.060. Insecure exceptions: test/data/lib_path/f061/swift.swift, line 6
        [INFO] FIN.H.060. Insecure exceptions: test/data/lib_path/f061/swift.swift, line 7
        [INFO] FIN.H.061. Errors without traceability: test/data/lib_path/f031_cwe378/Test.java, line 7
        [INFO] FIN.H.061. Errors without traceability: test/data/lib_path/f061/csharp.cs, line 2
        [INFO] FIN.H.061. Errors without traceability: test/data/lib_path/f061/java.java, line 2
        [INFO] FIN.H.061. Errors without traceability: test/data/lib_path/f061/javascript.js, line 3
        [INFO] FIN.H.061. Errors without traceability: test/data/lib_path/f061/javascript.js, line 4
        [INFO] FIN.H.061. Errors without traceability: test/data/lib_path/f061/javascript.js, line 5
        [INFO] FIN.H.061. Errors without traceability: test/data/lib_path/f061/python.py, line 21
        [INFO] FIN.H.061. Errors without traceability: test/data/lib_path/f061/swift.swift, line 5
        [INFO] FIN.H.061. Errors without traceability: test/data/lib_path/f061/swift.swift, line 6
        [INFO] FIN.H.061. Errors without traceability: test/data/lib_path/f061/swift.swift, line 7
        [INFO] FIN.H.073. Conditional statement without a default option: test/data/lib_path/f073/Test.cs, line 20
        [INFO] FIN.H.073. Conditional statement without a default option: test/data/lib_path/f073/Test.cs, line 3
        [INFO] FIN.H.073. Conditional statement without a default option: test/data/lib_path/f073/Test.cs, line 41
        [INFO] FIN.H.073. Conditional statement without a default option: test/data/lib_path/f073/Test.cs, line 44
        [INFO] FIN.H.073. Conditional statement without a default option: test/data/lib_path/f073/Test.java, line 44
        [INFO] FIN.H.073. Conditional statement without a default option: test/data/lib_path/f073/Test.java, line 92
        [INFO] FIN.H.073. Conditional statement without a default option: test/data/lib_path/f073/javascript.js, line 3
        [INFO] FIN.H.073. Conditional statement without a default option: test/data/lib_path/f073/javascript.tsx, line 4
        [INFO] FIN.S.001. SQL injection - Java Persistence API: test/data/lib_path/f001_jpa/java.java, line 23
        [INFO] FIN.S.001. SQL injection - Java Persistence API: test/data/lib_path/f001_jpa/java.java, line 26
        [INFO] FIN.S.001. SQL injection - Java Persistence API: test/data/lib_path/f001_jpa/java.java, line 36
        [INFO] FIN.S.001. SQL injection - Java Persistence API: test/data/lib_path/f001_jpa/java.java, line 39
        [INFO] FIN.S.001. SQL injection - Java Persistence API: test/data/lib_path/f001_jpa/java.java, line 42
        [INFO] FIN.S.001. SQL injection - Java Persistence API: test/data/lib_path/f001_jpa/java.java, line 45
        [INFO] FIN.S.009. Sensitive information in source code: test/data/lib_path/f009/Dockerfile, line 1
        [INFO] FIN.S.009. Sensitive information in source code: test/data/lib_path/f009/Dockerfile, line 2
        [INFO] FIN.S.009. Sensitive information in source code: test/data/lib_path/f009/java.properties, line 1
        [INFO] FIN.S.009. Sensitive information in source code: test/data/lib_path/f009/java.properties, line 2
        [INFO] FIN.S.009. Sensitive information in source code: test/data/lib_path/f009/java.properties, line 2
        [INFO] FIN.S.009. Sensitive information in source code: test/data/lib_path/f009/java.properties, line 4
        [INFO] FIN.S.009. Sensitive information in source code: test/data/lib_path/f009/java.properties, line 4
        [INFO] FIN.S.009. Sensitive information in source code: test/data/lib_path/f009/java.properties, line 8
        [INFO] FIN.S.009. Sensitive information in source code: test/data/lib_path/f009/javascript.js, line 3
        [INFO] FIN.S.009. Sensitive information in source code: test/data/lib_path/f009/javascript.js, line 4
        [INFO] FIN.S.009. Sensitive information in source code: test/data/lib_path/f009/javascript.js, line 5
        [INFO] FIN.S.009. Sensitive information in source code: test/data/lib_path/f009/javascript.js, line 6
        [INFO] FIN.S.009. Sensitive information in source code: test/data/lib_path/f009/javascript.js, line 7
        [INFO] FIN.S.009. Sensitive information in source code: test/data/lib_path/f009/javascript.js, line 8
        [INFO] FIN.S.009. Sensitive information in source code: test/data/lib_path/f009/secrets.yaml, line 1
        [INFO] FIN.S.009. Sensitive information in source code: test/data/lib_path/f009/secrets.yaml.json, line 1
        [INFO] FIN.S.011. Use of software with known vulnerabilities: test/data/lib_path/f011/package-lock.json (hoek v5.0.0) [CVE-2018-3728], line 6
        [INFO] FIN.S.011. Use of software with known vulnerabilities: test/data/lib_path/f011/package.json (hoek v^5.0.0) [CVE-2018-3728], line 5
        [INFO] FIN.S.011. Use of software with known vulnerabilities: test/data/lib_path/f011/package.json (jquery v0.*) [CVE-2011-4969], line 7
        [INFO] FIN.S.011. Use of software with known vulnerabilities: test/data/lib_path/f011/package.json (jquery v0.*) [CVE-2015-9251], line 7
        [INFO] FIN.S.011. Use of software with known vulnerabilities: test/data/lib_path/f011/package.json (jquery v0.*) [CVE-2017-16012], line 7
        [INFO] FIN.S.011. Use of software with known vulnerabilities: test/data/lib_path/f011/package.json (jquery v0.*) [CVE-2019-11358], line 7
        [INFO] FIN.S.011. Use of software with known vulnerabilities: test/data/lib_path/f011/package.json (jquery v0.*) [CVE-2020-7656], line 7
        [INFO] FIN.S.011. Use of software with known vulnerabilities: test/data/lib_path/f011/package.json (lodash v0.*) [CVE-2018-16487], line 6
        [INFO] FIN.S.011. Use of software with known vulnerabilities: test/data/lib_path/f011/package.json (lodash v0.*) [CVE-2018-3721], line 6
        [INFO] FIN.S.011. Use of software with known vulnerabilities: test/data/lib_path/f011/package.json (lodash v0.*) [CVE-2019-1010266], line 6
        [INFO] FIN.S.011. Use of software with known vulnerabilities: test/data/lib_path/f011/package.json (lodash v0.*) [CVE-2019-10744], line 6
        [INFO] FIN.S.011. Use of software with known vulnerabilities: test/data/lib_path/f011/package.json (lodash v0.*) [CVE-2020-8203], line 6
        [INFO] FIN.S.011. Use of software with known vulnerabilities: test/data/lib_path/f011/package.json (lodash v0.*) [github.com/lodash/lodash/issues/4874], line 6
        [INFO] FIN.S.022. Use of an insecure channel: test/data/lib_path/f022/java.properties, line 1
        [INFO] FIN.S.022. Use of an insecure channel: test/data/lib_path/f022/java.properties, line 4
        [INFO] FIN.S.031. Excessive privileges - AWS: test/data/lib_path/f031_aws/cfn_admin_policy_attached.yaml, line 10
        [INFO] FIN.S.031. Excessive privileges - AWS: test/data/lib_path/f031_aws/cfn_admin_policy_attached.yaml, line 6
        [INFO] FIN.S.031. Excessive privileges - AWS: test/data/lib_path/f031_aws/cfn_admin_policy_attached.yaml, line 8
        [INFO] FIN.S.031. Excessive privileges - AWS: test/data/lib_path/f031_aws/cfn_admin_policy_attached.yaml.json, line 11
        [INFO] FIN.S.031. Excessive privileges - AWS: test/data/lib_path/f031_aws/cfn_admin_policy_attached.yaml.json, line 7
        [INFO] FIN.S.031. Excessive privileges - AWS: test/data/lib_path/f031_aws/cfn_admin_policy_attached.yaml.json, line 9
        [INFO] FIN.S.031. Excessive privileges - AWS: test/data/lib_path/f031_aws/cfn_negative_statement.yaml, line 13
        [INFO] FIN.S.031. Excessive privileges - AWS: test/data/lib_path/f031_aws/cfn_negative_statement.yaml, line 17
        [INFO] FIN.S.031. Excessive privileges - AWS: test/data/lib_path/f031_aws/cfn_negative_statement.yaml, line 21
        [INFO] FIN.S.031. Excessive privileges - AWS: test/data/lib_path/f031_aws/cfn_negative_statement.yaml, line 36
        [INFO] FIN.S.031. Excessive privileges - AWS: test/data/lib_path/f031_aws/cfn_negative_statement.yaml.json, line 13
        [INFO] FIN.S.031. Excessive privileges - AWS: test/data/lib_path/f031_aws/cfn_negative_statement.yaml.json, line 18
        [INFO] FIN.S.031. Excessive privileges - AWS: test/data/lib_path/f031_aws/cfn_negative_statement.yaml.json, line 23
        [INFO] FIN.S.031. Excessive privileges - AWS: test/data/lib_path/f031_aws/cfn_negative_statement.yaml.json, line 48
        [INFO] FIN.S.031. Excessive privileges - AWS: test/data/lib_path/f031_aws/cfn_open_passrole.yaml, line 16
        [INFO] FIN.S.031. Excessive privileges - AWS: test/data/lib_path/f031_aws/cfn_open_passrole.yaml, line 7
        [INFO] FIN.S.031. Excessive privileges - AWS: test/data/lib_path/f031_aws/cfn_open_passrole.yaml.json, line 23
        [INFO] FIN.S.031. Excessive privileges - AWS: test/data/lib_path/f031_aws/cfn_open_passrole.yaml.json, line 8
        [INFO] FIN.S.031. Excessive privileges - AWS: test/data/lib_path/f031_aws/cfn_permissive_policy.yaml, line 33
        [INFO] FIN.S.031. Excessive privileges - AWS: test/data/lib_path/f031_aws/cfn_permissive_policy.yaml, line 9
        [INFO] FIN.S.031. Excessive privileges - AWS: test/data/lib_path/f031_aws/cfn_permissive_policy.yaml.json, line 11
        [INFO] FIN.S.031. Excessive privileges - AWS: test/data/lib_path/f031_aws/cfn_permissive_policy.yaml.json, line 54
        [INFO] FIN.S.031. Excessive privileges - AWS: test/data/lib_path/f031_aws/hcl2_negative_statement.tf, line 33
        [INFO] FIN.S.031. Excessive privileges - AWS: test/data/lib_path/f031_aws/hcl2_negative_statement.tf, line 5
        [INFO] FIN.S.031. Excessive privileges - AWS: test/data/lib_path/f031_aws/hcl2_open_passrole.tf, line 5
        [INFO] FIN.S.031. Excessive privileges - AWS: test/data/lib_path/f031_aws/hcl2_permissive_policy.tf, line 37
        [INFO] FIN.S.031. Excessive privileges - AWS: test/data/lib_path/f031_aws/hcl2_permissive_policy.tf, line 5
        [INFO] FIN.S.031. Excessive privileges - AWS: test/data/lib_path/f031_aws/hcl2_permissive_policy.tf, line 73
        [INFO] FIN.S.031. Excessive privileges - Temporary files: test/data/lib_path/f031_cwe378/Test.java, line 6
        [INFO] FIN.S.052. Insecure encryption algorithm: test/data/lib_path/f052/csharp.cs, line 2
        [INFO] FIN.S.052. Insecure encryption algorithm: test/data/lib_path/f052/csharp.cs, line 3
        [INFO] FIN.S.052. Insecure encryption algorithm: test/data/lib_path/f052/csharp.cs, line 5
        [INFO] FIN.S.052. Insecure encryption algorithm: test/data/lib_path/f052/java.java, line 1
        [INFO] FIN.S.052. Insecure encryption algorithm: test/data/lib_path/f052/java.java, line 11
        [INFO] FIN.S.052. Insecure encryption algorithm: test/data/lib_path/f052/java.java, line 12
        [INFO] FIN.S.052. Insecure encryption algorithm: test/data/lib_path/f052/java.java, line 13
        [INFO] FIN.S.052. Insecure encryption algorithm: test/data/lib_path/f052/java.java, line 14
        [INFO] FIN.S.052. Insecure encryption algorithm: test/data/lib_path/f052/java.java, line 15
        [INFO] FIN.S.052. Insecure encryption algorithm: test/data/lib_path/f052/java.java, line 17
        [INFO] FIN.S.052. Insecure encryption algorithm: test/data/lib_path/f052/java.java, line 18
        [INFO] FIN.S.052. Insecure encryption algorithm: test/data/lib_path/f052/java.java, line 19
        [INFO] FIN.S.052. Insecure encryption algorithm: test/data/lib_path/f052/java.java, line 20
        [INFO] FIN.S.052. Insecure encryption algorithm: test/data/lib_path/f052/java.java, line 21
        [INFO] FIN.S.052. Insecure encryption algorithm: test/data/lib_path/f052/java.java, line 22
        [INFO] FIN.S.052. Insecure encryption algorithm: test/data/lib_path/f052/java.java, line 23
        [INFO] FIN.S.052. Insecure encryption algorithm: test/data/lib_path/f052/java.java, line 24
        [INFO] FIN.S.052. Insecure encryption algorithm: test/data/lib_path/f052/java.java, line 25
        [INFO] FIN.S.052. Insecure encryption algorithm: test/data/lib_path/f052/java.java, line 26
        [INFO] FIN.S.052. Insecure encryption algorithm: test/data/lib_path/f052/java.java, line 27
        [INFO] FIN.S.052. Insecure encryption algorithm: test/data/lib_path/f052/java.java, line 30
        [INFO] FIN.S.052. Insecure encryption algorithm: test/data/lib_path/f052/java.java, line 33
        [INFO] FIN.S.052. Insecure encryption algorithm: test/data/lib_path/f052/java.java, line 35
        [INFO] FIN.S.052. Insecure encryption algorithm: test/data/lib_path/f052/java.java, line 4
        [INFO] FIN.S.052. Insecure encryption algorithm: test/data/lib_path/f052/java.java, line 5
        [INFO] FIN.S.052. Insecure encryption algorithm: test/data/lib_path/f052/java.java, line 6
        [INFO] FIN.S.052. Insecure encryption algorithm: test/data/lib_path/f052/java.java, line 8
        [INFO] FIN.S.052. Insecure encryption algorithm: test/data/lib_path/f052/java.java, line 9
        [INFO] FIN.S.052. Insecure encryption algorithm: test/data/lib_path/f052/java.properties, line 2
        [INFO] FIN.S.052. Insecure encryption algorithm: test/data/lib_path/f052/java.properties, line 3
        [INFO] FIN.S.052. Insecure encryption algorithm: test/data/lib_path/f052/java.properties, line 4
        [INFO] FIN.S.052. Insecure encryption algorithm: test/data/lib_path/f052/java.properties, line 6
        [INFO] FIN.S.085. Sensitive data stored in the client-side storage: test/data/lib_path/f085/react.jsx, line 1
        [INFO] FIN.S.085. Sensitive data stored in the client-side storage: test/data/lib_path/f085/react.jsx, line 4
        [INFO] FIN.S.085. Sensitive data stored in the client-side storage: test/data/lib_path/f085/react.jsx, line 5
        [INFO] FIN.S.085. Sensitive data stored in the client-side storage: test/data/lib_path/f085/react.jsx, line 6
        [INFO] FIN.S.117. Unverifiable files: test/data/lib_path/f117/MyJar.class, line 1
        [INFO] FIN.S.117. Unverifiable files: test/data/lib_path/f117/MyJar.jar, line 1
    """)[1:-1]
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
            ('test/data/lib_path/f031_aws/cfn_negative_statement.yaml', '13'),
            ('test/data/lib_path/f031_aws/cfn_negative_statement.yaml', '17'),
            ('test/data/lib_path/f031_aws/cfn_negative_statement.yaml', '21'),
            ('test/data/lib_path/f031_aws/cfn_negative_statement.yaml', '36'),
            ('test/data/lib_path/f031_aws/cfn_negative_statement.yaml.json', '13'),
            ('test/data/lib_path/f031_aws/cfn_negative_statement.yaml.json', '18'),
            ('test/data/lib_path/f031_aws/cfn_negative_statement.yaml.json', '23'),
            ('test/data/lib_path/f031_aws/cfn_negative_statement.yaml.json', '48'),
            ('test/data/lib_path/f031_aws/cfn_open_passrole.yaml', '16'),
            ('test/data/lib_path/f031_aws/cfn_open_passrole.yaml', '7'),
            ('test/data/lib_path/f031_aws/cfn_open_passrole.yaml.json', '23'),
            ('test/data/lib_path/f031_aws/cfn_open_passrole.yaml.json', '8'),
            ('test/data/lib_path/f031_aws/cfn_permissive_policy.yaml', '33'),
            ('test/data/lib_path/f031_aws/cfn_permissive_policy.yaml', '9'),
            ('test/data/lib_path/f031_aws/cfn_permissive_policy.yaml.json', '11'),
            ('test/data/lib_path/f031_aws/cfn_permissive_policy.yaml.json', '54'),
            ('test/data/lib_path/f031_aws/hcl2_negative_statement.tf', '33'),
            ('test/data/lib_path/f031_aws/hcl2_negative_statement.tf', '5'),
            ('test/data/lib_path/f031_aws/hcl2_open_passrole.tf', '5'),
            ('test/data/lib_path/f031_aws/hcl2_permissive_policy.tf', '37'),
            ('test/data/lib_path/f031_aws/hcl2_permissive_policy.tf', '5'),
            ('test/data/lib_path/f031_aws/hcl2_permissive_policy.tf', '73'),
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
            ('test/data/lib_path/f052/java.properties', '2'),
            ('test/data/lib_path/f052/java.properties', '3'),
            ('test/data/lib_path/f052/java.properties', '4'),
            ('test/data/lib_path/f052/java.properties', '6'),
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
        ('F052', 'APPROVED', ()),
        ('F060', 'APPROVED', ()),
        ('F061', 'APPROVED', ()),
        ('F073', 'APPROVED', ()),
        ('F085', 'APPROVED', ()),
        ('F117', 'APPROVED', ()),
    }
