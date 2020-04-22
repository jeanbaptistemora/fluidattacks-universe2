# Standard library
import datetime
import glob
import json
import operator
import os
import textwrap
from typing import (
    Dict,
    Tuple,
)
# Third party libraries

# Local libraries
from toolbox import (
    constants,
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


def _get_fernet_key(subscription: str) -> str:
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


def are_exploits_synced__static(subs: str, exp_name: str):
    """Check if exploits results are the same as on Integrates."""
    results: list = []

    bb_fernet_key: str = _get_fernet_key(subs)

    bb_resources = \
        os.path.abspath(f'subscriptions/{subs}/break-build/static/resources')

    for exploit_path in sorted(glob.glob(
            f'subscriptions/{subs}/break-build/static/exploits/*.exp')):
        if '.cannot.exp' in exploit_path:
            continue

        once: bool = True

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

        finding_title = helper.integrates.get_finding_title(finding_id)

        if os.path.isfile(exploit_output_path):
            os.remove(exploit_output_path)

        integrates_status = \
            helper.integrates.get_finding_static_repos_states(finding_id)

        local_repos: set = set(filter(
            lambda repo: os.path.isdir(f'subscriptions/{subs}/fusion/{repo}'),
            os.listdir(f'subscriptions/{subs}/fusion')))

        integrates_repos: set = set(integrates_status.keys())
        find_wheres = helper.integrates.get_finding_wheres(finding_id)

        for repo in integrates_repos.union(local_repos):
            analyst_status = integrates_status.get(repo, False)
            asserts_status = None
            repository_path: str = f'subscriptions/{subs}/fusion/{repo}'
            if os.path.isdir(repository_path):
                asserts_status, asserts_stdout, _ = _run_static_exploit(
                    exploit_path=exploit_path,
                    exploit_output_path=exploit_output_path,
                    repository_path=repository_path,
                    bb_fernet_key=bb_fernet_key,
                    bb_resources=bb_resources)
            else:
                continue

            imsg = 'OPEN' if analyst_status else 'CLOSED'
            amsg = api.asserts.get_exp_error_message(asserts_stdout) \
                or constants.RICH_EXIT_CODES_INV.get(
                    asserts_status, 'OTHER').upper()

            asserts_summary = \
                api.asserts.get_exp_result_summary(asserts_stdout)

            repo_vulns_api = tuple(filter(
                lambda line, rep=repo: line[2]  # type: ignore
                and line[0] in constants.SAST
                and line[1].startswith(rep), find_wheres))

            if imsg != amsg:
                if once:
                    logger.info(f'    *{finding_id:<10} {finding_title}*')
                    once = False
                logger.info('        {i} {a}    {r}'.format(
                    i=f'Integrates: {imsg!s:<6}',
                    a=f'Asserts: {amsg!s:<17}',
                    r=repo))
            results.append({
                'datetime': datetime.datetime.now().strftime(
                    "%Y-%m-%dT%H:%M:%SZ"),
                'exploit_path': os.path.relpath(exploit_path),
                'exploit_type': 'static',
                'num_open_asserts': asserts_summary.get('vulnerabilities', 0),
                'num_open_integrates': len(repo_vulns_api),
                'pipeline_id': os.environ.get('CI_PIPELINE_ID', None),
                'repository': repo,
                'result_asserts': amsg,
                'result_integrates': imsg,
                'subscription': subs,
                'synced': 'yes' if imsg == amsg else 'no',
            })

    return results


def are_exploits_synced__dynamic(subs: str, exp_name: str):
    """Check if exploits results are the same as on Integrates."""
    results: list = []

    bb_aws_role_arns: Tuple[str, ...] = _get_bb_aws_role_arns(subs)
    bb_fernet_key: str = _get_fernet_key(subs)
    bb_resources = \
        os.path.abspath(f'subscriptions/{subs}/break-build/dynamic/resources')

    for exploit_path in sorted(glob.glob(
            f'subscriptions/{subs}/break-build/dynamic/exploits/*.exp')):
        if '.cannot.exp' in exploit_path:
            continue

        once: bool = True

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

        finding_title = helper.integrates.get_finding_title(finding_id)
        find_wheres = helper.integrates.get_finding_wheres(finding_id)
        find_wheres = tuple(filter(
            lambda w: w[2] and w[0] in constants.DAST, find_wheres))

        if os.path.isfile(exploit_output_path):
            os.remove(exploit_output_path)

        analyst_status = helper.integrates.is_finding_open(
            finding_id, constants.DAST)

        asserts_status, asserts_stdout, _ = _run_dynamic_exploit(
            exploit_path=exploit_path,
            exploit_output_path=exploit_output_path,
            subs_path=f'subscriptions/{subs}',
            bb_aws_role_arns=bb_aws_role_arns,
            bb_fernet_key=bb_fernet_key,
            bb_resources=bb_resources)

        imsg = 'OPEN' if analyst_status else 'CLOSED'
        amsg = api.asserts.get_exp_error_message(asserts_stdout) \
            or constants.RICH_EXIT_CODES_INV.get(
                asserts_status, 'OTHER').upper()

        asserts_summary = \
            api.asserts.get_exp_result_summary(asserts_stdout)

        if imsg != amsg:
            if once:
                logger.info(f'    *{finding_id:<10} {finding_title}*')
                once = False
            logger.info('        {i} {a}'.format(
                i=f'Integrates: {imsg!s:<6}', a=f'Asserts: {amsg!s:<17}'))

        results.append({
            'datetime': datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
            'exploit_path': os.path.relpath(exploit_path),
            'exploit_type': 'dynamic',
            'num_open_asserts': asserts_summary.get('vulnerabilities', 0),
            'num_open_integrates': len(find_wheres),
            'pipeline_id': os.environ.get('CI_PIPELINE_ID', ''),
            'result_asserts': amsg,
            'result_integrates': imsg,
            'subscription': subs,
            'synced': 'yes' if imsg == amsg else 'no',
        })

    return results


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

    # If we didn't run, assume it's synced
    results_static: list = []
    if should_run_static:
        results_static = are_exploits_synced__static(subs, exp_name)

    # If we didn't run, assume it's synced
    results_dynamic: list = []
    if should_run_dynamic:
        results_dynamic = are_exploits_synced__dynamic(subs, exp_name)

    with open(f'check-sync-results.{subs}.json.stream', 'w') as results_handle:
        for json_obj in results_static + results_dynamic:
            results_handle.write(json.dumps({
                'stream': 'results',
                'record': json_obj,
            }, sort_keys=True))
            results_handle.write('\n')

    return True
