# Standard library
import datetime
import glob
import json
import operator
import os
import textwrap
from typing import (
    Dict,
    List,
    Set,
    Tuple,
)
# Third party libraries

# Local libraries
from toolbox import (
    helper,
    api,
    logger,
    utils,
)

# The applied logic in static exploits is:
#   Given an exploit 'E' for the finding 'F' and a repository 'R':
#     - See the status on Integrates for the finding 'F' and the
#       repository 'R', (OPEN, CLOSED)
#     - Run the exploit 'E' over repository 'R' and see the
#       status (OPEN, CLOSED, UNKNOWN, ERROR, ETC)
#     - Report here if the status Integrates vs Asserts differ
#
# The applied logic in dynamic exploits is:
#   Given an exploit 'E' for the finding 'F':
#     - See the status on Integrates for
#       the finding 'F', (OPEN, CLOSED)
#     - Run the exploit 'E' and see the status
#       (OPEN, CLOSED, UNKNOWN, ERROR, ETC)
#     - Report here if the status Integrates vs Asserts differ


def _get_bb_fernet_key(subscription: str) -> str:
    return utils.generic.get_sops_secret(
        f'break_build_aws_secret_access_key',
        f'subscriptions/{subscription}/config/secrets.yaml',
        f'continuous-{subscription}')


def _get_bb_aws_role_arns(subs: str) -> Tuple[str, ...]:
    config_path = (
        f'subscriptions/{subs}'
        f'/break-build/dynamic/resources/BB_AWS_ROLE_ARNS.list'
    )

    if os.path.exists(config_path):
        with open(config_path) as config_handle:
            return tuple(
                filter(operator.truth,
                       map(operator.methodcaller('strip'),
                           config_handle.readlines())))

    return tuple()


def _get_bb_resources(subs: str, kind: str) -> str:
    return \
        os.path.abspath(f'subscriptions/{subs}/break-build/{kind}/resources')


def _print_results_summary(results: List[dict]):
    if all(result['synced'] == 'yes' for result in results):
        logger.info(f'Summary: {len(results)} tests, all ok!')
    else:
        logger.info(f'Summary: {len(results)} tests, some of them failed')


def _run_static_exploit(
    *,
    exploit_path: str,
    exploit_output_path: str,
    repository_path: str,
    bb_fernet_key: str,
    bb_resources: str,
) -> Tuple[int, str, str]:
    """Run a static exploit and return it's exit_code, stdout and stderr."""
    repo: str = os.path.basename(repository_path)

    cmd: str = f"""
        echo '---' >> '{exploit_output_path}'
        echo 'repository: {repo}' >> '{exploit_output_path}'
        asserts -eec -n -ms '{exploit_path}' > '{exploit_output_path}_'
        exit_code=$?
        cat '{exploit_output_path}_'
        cat '{exploit_output_path}_' >> '{exploit_output_path}'
        rm -f '{exploit_output_path}_' >  /dev/null
        exit ${{exit_code}}
        """

    cmd = ';'.join(textwrap.dedent(cmd)[1:-1].splitlines())

    env: Dict[str, str] = {
        'FA_NOTRACK': 'true',
        'FA_STRICT': 'true',
        'BB_FERNET_KEY': bb_fernet_key,
        'BB_RESOURCES': bb_resources,
        'CURRENT_EXPLOIT_KIND': 'static'
    }

    return utils.generic.run_command_old(cmd=cmd, cwd=repository_path, env=env)


def _run_dynamic_exploit(
    *,
    exploit_path: str,
    exploit_output_path: str,
    subs_path: str,
    bb_aws_role_arns: Tuple[str, ...],
    bb_fernet_key: str,
    bb_resources: str,
) -> Tuple[int, str, str]:
    """Run a dynamic exploit and return it's exit_code, stdout and stderr."""
    cmd: str = f"""
        asserts -eec -n -ms '{exploit_path}' > '{exploit_output_path}_'
        exit_code=$?
        cat '{exploit_output_path}_'
        cat '{exploit_output_path}_' >> '{exploit_output_path}'
        rm -f '{exploit_output_path}_' >  /dev/null
        exit ${{exit_code}}
        """

    cmd = ';'.join(textwrap.dedent(cmd)[1:-1].splitlines())

    env: Dict[str, str] = {
        'BB_AWS_ROLE_ARNS': ','.join(bb_aws_role_arns),
        'BB_FERNET_KEY': bb_fernet_key,
        'BB_RESOURCES': bb_resources,
        'CURRENT_EXPLOIT_KIND': 'dynamic',
        'FA_NOTRACK': 'true',
        'FA_STRICT': 'true',
    }

    return utils.generic.run_command_old(cmd=cmd, cwd=subs_path, env=env)


def _validate_one_static_exploit(
    *,
    bb_fernet_key: str,
    bb_resources: str,
    exploit_output_path: str,
    exploit_path: str,
    finding_id: str,
    subs: str,
) -> List[dict]:
    """Validate Synchronization in one static exploit and return results."""
    results: List[dict] = []

    if os.path.isfile(exploit_output_path):
        os.remove(exploit_output_path)

    integrates_repositories_status = \
        helper.integrates.get_finding_static_repos_states(finding_id)
    integrates_repositories_vulns = \
        helper.integrates.get_finding_static_repos_vulns(finding_id)

    repositories_local: Set[str] = {
        repository
        for repository in os.listdir(f'subscriptions/{subs}/fusion')
        if os.path.isdir(f'subscriptions/{subs}/fusion/{repository}')
    }

    repositories_integrates: Set[str] = \
        set(integrates_repositories_status.keys())

    for repo in repositories_integrates.union(repositories_local):
        repository_path: str = f'subscriptions/{subs}/fusion/{repo}'

        if not os.path.isdir(repository_path):
            # This repo exist on Integrates and not locally, we cannot test
            continue

        _, asserts_stdout, _ = _run_static_exploit(
            exploit_path=exploit_path,
            exploit_output_path=exploit_output_path,
            repository_path=repository_path,
            bb_fernet_key=bb_fernet_key,
            bb_resources=bb_resources)

        integrates_vulns_open = \
            integrates_repositories_vulns.get(repo, {}).get('open', 0)
        integrates_vulns_closed = \
            integrates_repositories_vulns.get(repo, {}).get('closed', 0)

        asserts_vulns = tuple(
            api.asserts.iterate_vulnerabilities_from_content(
                asserts_stdout, repo))
        asserts_vulns_open = \
            sum(vul.status.startswith('OPEN') for vul in asserts_vulns)
        asserts_vulns_unknown = \
            sum(vul.status.startswith('UNKNOWN') for vul in asserts_vulns)
        asserts_vulns_error = \
            sum(vul.status.startswith('ERROR') for vul in asserts_vulns)

        # Open if at least one vuln is open
        imsg = 'OPEN' if integrates_vulns_open > 0 else 'CLOSED'

        # Error if at least one error
        # Open if at least one open and no errors
        # Unknown if at least one unknown, no errors and no opens
        # Closed if no errors or opens or unknowns
        amsg = {
            asserts_vulns_unknown > 0: 'UNKNOWN',
            asserts_vulns_open > 0: 'OPEN',
            asserts_vulns_error > 0: 'ERROR',
        }.get(True, 'CLOSED')

        # The synced equation
        is_synced = \
            asserts_vulns_error == 0 \
            and asserts_vulns_open == integrates_vulns_open

        if not is_synced:
            logger.info(
                f'  {finding_id:<10}: {repo:<60} '
                f'{imsg!s:<6} I ('
                f'{integrates_vulns_open!s:<3} o, '
                f'{integrates_vulns_closed!s:<3} c), '
                f'{amsg!s:<7} E ('
                f'{asserts_vulns_error!s:<3} e, '
                f'{asserts_vulns_open!s:<3} o, '
                f'{asserts_vulns_unknown!s:<3} u)'
            )

        asserts_summary = \
            api.asserts.get_exp_result_summary(asserts_stdout)

        results.append(dict(
            datetime=datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
            exploit_path=os.path.relpath(exploit_path),
            exploit_type='static',
            num_open_asserts=asserts_summary.get('vulnerabilities', 0),
            num_open_integrates=integrates_vulns_open,
            pipeline_id=os.environ.get('CI_PIPELINE_ID'),
            repository=repo,
            result_asserts=amsg,
            result_integrates=imsg,
            subscription=subs,
            synced='yes' if is_synced else 'no',
        ))

    return results


def _validate_one_dynamic_exploit(
    *,
    bb_aws_role_arns: Tuple[str, ...],
    bb_fernet_key: str,
    bb_resources: str,
    exploit_output_path: str,
    exploit_path: str,
    finding_id: str,
    subs: str,
) -> List[dict]:
    """Validate Synchronization in one static exploit and return results."""
    results: List[dict] = []

    if os.path.isfile(exploit_output_path):
        os.remove(exploit_output_path)

    integrates_vulns = \
        helper.integrates.get_finding_dynamic_states(finding_id)
    integrates_vulns_open = \
        sum(1 for _, _, is_open in integrates_vulns if is_open)
    integrates_vulns_closed = \
        sum(1 for _, _, is_open in integrates_vulns if not is_open)

    _, asserts_stdout, _ = _run_dynamic_exploit(
        exploit_path=exploit_path,
        exploit_output_path=exploit_output_path,
        subs_path=f'subscriptions/{subs}',
        bb_aws_role_arns=bb_aws_role_arns,
        bb_fernet_key=bb_fernet_key,
        bb_resources=bb_resources)

    asserts_vulns = tuple(
        api.asserts.iterate_vulnerabilities_from_content(asserts_stdout))
    asserts_vulns_open = \
        sum(vul.status.startswith('OPEN') for vul in asserts_vulns)
    asserts_vulns_unknown = \
        sum(vul.status.startswith('UNKNOWN') for vul in asserts_vulns)
    asserts_vulns_error = \
        sum(vul.status.startswith('ERROR') for vul in asserts_vulns)

    # Open if at least one vuln is open
    imsg = 'OPEN' if integrates_vulns_open > 0 else 'CLOSED'

    # Error if at least one error
    # Open if at least one open and no errors
    # Unknown if at least one unknown, no errors and no opens
    # Closed if no errors or opens or unknowns
    amsg = {
        asserts_vulns_unknown > 0: 'UNKNOWN',
        asserts_vulns_open > 0: 'OPEN',
        asserts_vulns_error > 0: 'ERROR',
    }.get(True, 'CLOSED')

    # The synced equation
    is_synced = \
        asserts_vulns_error == 0 \
        and asserts_vulns_open == integrates_vulns_open

    if not is_synced:
        logger.info(
            f'  {finding_id:<10}: {str():<60} '
            f'{imsg!s:<6} I ('
            f'{integrates_vulns_open!s:<3} o, '
            f'{integrates_vulns_closed!s:<3} c), '
            f'{amsg!s:<7} E ('
            f'{asserts_vulns_error!s:<3} e, '
            f'{asserts_vulns_open!s:<3} o, '
            f'{asserts_vulns_unknown!s:<3} u)'
        )

    results.append(dict(
        datetime=datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
        exploit_path=os.path.relpath(exploit_path),
        exploit_type='dynamic',
        num_open_asserts=asserts_vulns_open,
        num_open_integrates=integrates_vulns_open,
        pipeline_id=os.environ.get('CI_PIPELINE_ID'),
        repository='',
        result_asserts=amsg,
        result_integrates=imsg,
        subscription=subs,
        synced='yes' if is_synced else 'no',
    ))

    return results


def are_exploits_synced__static(subs: str, exp_name: str) -> List[dict]:
    """Check if exploits results are the same as on Integrates."""
    logger.info()
    logger.info('Static exploits:')

    results: List[dict] = []

    bb_fernet_key: str = _get_bb_fernet_key(subs)
    bb_resources = _get_bb_resources(subs, 'static')

    for exploit_path in sorted(glob.glob(
            f'subscriptions/{subs}/break-build/static/exploits/*.exp')):
        if '.cannot.exp' in exploit_path:
            continue

        exploit_path = os.path.join(os.getcwd(), exploit_path)
        exploit_output_path = f'{exploit_path}.out.yml'

        if (exp_name or '') not in exploit_path:
            logger.debug(f'skipped: {exploit_path}')
            continue

        finding_id = \
            helper.forces.scan_exploit_for_kind_and_id(exploit_path)[1]

        if not helper.integrates.does_finding_exist(finding_id):
            logger.error(f'This finding does not exist at integrates!')
            logger.error(f'  finding_id: {finding_id}')
            logger.error(f'  exploit_path: {exploit_path}')
            continue

        results.extend(_validate_one_static_exploit(
            bb_fernet_key=bb_fernet_key,
            bb_resources=bb_resources,
            exploit_output_path=exploit_output_path,
            exploit_path=exploit_path,
            finding_id=finding_id,
            subs=subs,
        ))

    return results


def are_exploits_synced__dynamic(subs: str, exp_name: str) -> List[dict]:
    """Check if exploits results are the same as on Integrates."""
    logger.info()
    logger.info('Dynamic exploits:')
    results: List[dict] = []

    bb_aws_role_arns: Tuple[str, ...] = _get_bb_aws_role_arns(subs)
    bb_fernet_key: str = _get_bb_fernet_key(subs)
    bb_resources = _get_bb_resources(subs, 'dynamic')

    for exploit_path in sorted(glob.glob(
            f'subscriptions/{subs}/break-build/dynamic/exploits/*.exp')):
        if '.cannot.exp' in exploit_path:
            continue

        exploit_path = os.path.join(os.getcwd(), exploit_path)
        exploit_output_path = f'{exploit_path}.out.yml'

        if (exp_name or '') not in exploit_path:
            logger.debug(f'skipped: {exploit_path}')
            continue

        finding_id = \
            helper.forces.scan_exploit_for_kind_and_id(exploit_path)[1]

        if not helper.integrates.does_finding_exist(finding_id):
            logger.error(f'This finding does not exist at integrates!')
            logger.error(f'  finding_id: {finding_id}')
            logger.error(f'  exploit_path: {exploit_path}')
            continue

        results.extend(_validate_one_dynamic_exploit(
            bb_aws_role_arns=bb_aws_role_arns,
            bb_fernet_key=bb_fernet_key,
            bb_resources=bb_resources,
            exploit_output_path=exploit_output_path,
            exploit_path=exploit_path,
            finding_id=finding_id,
            subs=subs,
        ))

    return results


def print_nomenclature():
    """Impure function to show the used nomenclature."""
    logger.info('Nomenclature:')
    logger.info()
    logger.info('  E: Exploit')
    logger.info('  I: Integrates')
    logger.info()
    logger.info('  c: closed')
    logger.info('  e: error')
    logger.info('  o: open')
    logger.info('  u: unknown')
    logger.info()
    logger.info('Something is synced if:')
    logger.info('  (E) has no (e), and #(o) on (I) equals #(o) on (E)')


def are_exploits_synced(subs: str, exp_name: str) -> bool:
    """Check if exploits results are the same as on Integrates."""
    utils.generic.aws_login(f'continuous-{subs}')

    config = helper.forces.get_forces_configuration(subs)
    config = config['schedules']['synchronization']

    # Always run locally, and conditionally on the CI
    should_run_static = \
        not utils.generic.is_env_ci() or config['static']['run']
    should_run_dynamic = \
        not utils.generic.is_env_ci() or config['dynamic']['run']

    # Let users know what are we talking about
    print_nomenclature()

    # If we didn't run, assume it's synced
    results_static: List[dict] = []
    if should_run_static:
        results_static = are_exploits_synced__static(subs, exp_name)
        _print_results_summary(results_static)
    else:
        logger.warn()
        logger.warn('Ignoring Static check due to subscription config')

    # If we didn't run, assume it's synced
    results_dynamic: List[dict] = []
    if should_run_dynamic:
        results_dynamic = are_exploits_synced__dynamic(subs, exp_name)
        _print_results_summary(results_dynamic)
    else:
        logger.warn()
        logger.warn('Ignoring Dynamic check due to subscription config')

    with open(f'check-sync-results.{subs}.json.stream', 'w') as results_handle:
        for json_obj in results_static + results_dynamic:
            results_handle.write(json.dumps({
                'stream': 'results',
                'record': json_obj,
            }, sort_keys=True))
            results_handle.write('\n')

    return True
