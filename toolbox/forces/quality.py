# Standard library
import datetime
import glob
import json
import os
import textwrap
from typing import (
    Any,
    List,
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


def are_exploits_synced__show(outputs_to_show: List[str]):
    """Print the results of a list of outputs."""
    logger.info('')
    logger.info('Please check the outputs in the following files:')
    while outputs_to_show:
        logger.info('- ', outputs_to_show.pop())


def are_exploits_synced__static(subs: str, exp_name: str) -> Tuple[bool, Any]:
    """Check if exploits results are the same as on Integrates."""
    success: bool = True
    results: list = []
    outputs_to_show: list = []

    logger.info(textwrap.dedent("""
        ###################################################################

        We will run your static exploits and see if they are synced.

        The applied logic is:
            Given an exploit 'E' for the finding 'F' and a repository 'R':
                - See the status on Integrates for the finding 'F' and the
                    repository 'R', (OPEN, CLOSED)
                - Run the exploit 'E' over repository 'R' and see the
                    status (OPEN, CLOSED, UNKNOWN, ERRORS, ETC)
                - Break the pipeline if the status Integrates vs Asserts
                    differs

            There are three possible outcomes:
                - The exploit is wrong
                - Integrates is wrong
                - Both are wrong

            Please update whatever needs to be corrected.

        ###################################################################
        """))

    fernet_key: str = utils.get_sops_secret(
        f'break_build_aws_secret_access_key',
        f'subscriptions/{subs}/config/secrets.yaml',
        f'continuous-{subs}')

    bb_resources = os.path.abspath(
        f'subscriptions/{subs}/break-build/static/resources')

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
            analyst_status: Any = integrates_status.get(repo, False)
            asserts_status: Any = None
            repository_path: str = f'subscriptions/{subs}/fusion/{repo}'
            if os.path.isdir(repository_path):
                asserts_status, asserts_stdout, _ = utils.run_command(
                    cmd=(f"echo '---'                          "
                         f"  >> '{exploit_output_path}';       "
                         f"echo 'repository: {repo}'           "
                         f"  >> '{exploit_output_path}';       "
                         f"asserts -eec -n -ms '{exploit_path}'"
                         f"  >  '{exploit_output_path}_';      "
                         f"exit_code=$?;                       "
                         f"cat  '{exploit_output_path}_';      "
                         f"cat  '{exploit_output_path}_'       "
                         f"  >> '{exploit_output_path}';       "
                         f"rm   '{exploit_output_path}_'       "
                         f"  >  /dev/null;                     "
                         f"exit ${{exit_code}};                "),
                    cwd=repository_path,
                    env={'FA_NOTRACK': 'true',
                         'FA_STRICT': 'true',
                         'BB_FERNET_KEY': fernet_key,
                         'BB_RESOURCES': bb_resources,
                         'CURRENT_EXPLOIT_KIND': 'static'})
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
                success = False
                outputs_to_show.append(exploit_output_path)
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

    if not success:
        logger.info('')
        logger.error('This subscription is new or has been synced in the past'
                     '  please maintain it synced')
        are_exploits_synced__show(outputs_to_show)

    return success, results


def are_exploits_synced__dynamic(subs: str, exp_name: str) -> Tuple[bool, Any]:
    """Check if exploits results are the same as on Integrates."""
    success: bool = True
    results: list = []
    outputs_to_show: list = []

    logger.info(textwrap.dedent("""
        ###################################################################

        We will run your dynamic exploits and see if they are synced.

        We are aware that some environments are reachable only via VPN.

        For this reason, we'll only break the pipeline
        if Asserts says 'EXPLOIT-ERROR'

        The applied logic is:
            Given an exploit 'E' for the finding 'F':
                - See the status on Integrates for
                    the finding 'F', (OPEN, CLOSED)
                - Run the exploit 'E' and see the status
                    (OPEN, CLOSED, UNKNOWN, ERRORS, ETC)
                - Report here if the status Integrates vs Asserts differ
                - Break the pipeline if Asserts says 'EXPLOIT-ERROR'

            There are three possible outcomes:
                - if the environment needs VPN:
                    - It's understandable, usually it's not your fault,
                        if you like you can still check just to make sure
                - else:
                    - The exploit is wrong
                    - Integrates is wrong
                    - Both are wrong

            Please update whatever needs to be corrected.

        ###################################################################
        """))

    fernet_key: str = utils.get_sops_secret(
        f'break_build_aws_secret_access_key',
        f'subscriptions/{subs}/config/secrets.yaml',
        f'continuous-{subs}')

    aws_role_arns_path = (f'subscriptions/{subs}/break-build/dynamic/'
                          'resources/BB_AWS_ROLE_ARNS.list')

    bb_resources = os.path.abspath(
        f'subscriptions/{subs}/break-build/dynamic/resources')

    aws_arn_roles = None
    if os.path.exists(aws_role_arns_path):
        with open(aws_role_arns_path) as file:
            aws_arn_roles = tuple(
                role_arn.strip() for role_arn in file.readlines() if role_arn)
    else:
        aws_arn_roles = ()

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
        finding_title = helper.integrates.get_finding_title(finding_id)
        find_wheres = helper.integrates.get_finding_wheres(finding_id)
        find_wheres = tuple(filter(
            lambda w: w[2] and w[0] in constants.DAST, find_wheres))

        if os.path.isfile(exploit_output_path):
            os.remove(exploit_output_path)

        analyst_status = helper.integrates.is_finding_open(
            finding_id, constants.DAST)

        asserts_status, asserts_stdout, _ = utils.run_command(
            cmd=(f"asserts -eec -n -ms '{exploit_path}'"
                 f"  >  '{exploit_output_path}_';      "
                 f"exit_code=$?;                       "
                 f"cat  '{exploit_output_path}_';      "
                 f"cat  '{exploit_output_path}_'       "
                 f"  >> '{exploit_output_path}';       "
                 f"rm   '{exploit_output_path}_'       "
                 f"  >  /dev/null;                     "
                 f"exit ${{exit_code}};                "),
            cwd=f'subscriptions/{subs}',
            env={'FA_NOTRACK': 'true',
                 'FA_STRICT': 'true',
                 'BB_FERNET_KEY': fernet_key,
                 'CURRENT_EXPLOIT_KIND': 'dynamic',
                 'BB_RESOURCES': bb_resources,
                 'BB_AWS_ROLE_ARNS': ','.join(aws_arn_roles)})

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
            if 'ERROR' in amsg:
                success = False
                outputs_to_show.append(exploit_output_path)
        results.append({
            'datetime': datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
            'exploit_path': os.path.relpath(exploit_path),
            'exploit_type': 'dynamic',
            'num_open_asserts': asserts_summary.get('vulnerabilities', 0),
            'num_open_integrates': len(find_wheres),
            'pipeline_id': os.environ.get('CI_PIPELINE_ID', None),
            'result_asserts': amsg,
            'result_integrates': imsg,
            'subscription': subs,
            'synced': 'yes' if imsg == amsg else 'no',
        })

    if not success:
        logger.info('')
        msg = 'Some exploit ended with EXPLOIT-ERROR status. Please check.'
        logger.error(msg)
        are_exploits_synced__show(outputs_to_show)

    return success, results


def are_exploits_synced(subs: str, exp_name: str) -> bool:
    """Check if exploits results are the same as on Integrates."""
    utils.aws_login(f'continuous-{subs}')

    config = helper.forces.get_forces_configuration(subs)
    config = config['schedules']['synchronization']

    # Always run locally, and conditionally on the CI
    should_run_static = \
        not utils.is_env_ci() or config['static']['run']
    should_run_dynamic = \
        not utils.is_env_ci() or config['dynamic']['run']

    # If we didn't run, assume it's synced
    success_static: bool = True
    results_static: list = []
    if should_run_static:
        success_static, results_static = \
            are_exploits_synced__static(subs, exp_name)

    # If we didn't run, assume it's synced
    success_dynamic: bool = True
    results_dynamic: list = []
    if should_run_dynamic:
        success_dynamic, results_dynamic = \
            are_exploits_synced__dynamic(subs, exp_name)

    logger.info('')
    if utils.is_env_ci():
        logger.info('You can run this check locally:')
        logger.info(f'  continuous $ pip3 install '
                    f'break-build/packages/toolbox[with_asserts]')
        logger.info(f'  continuous $ fluid forces --check-sync {subs}')
    else:
        logger.info('You can check the exploits output at:')
        msg = f'  subscriptions/{subs}/break-build/*/exploits/*.exp.out.yml'
        logger.info(msg)

    with open(f'check-sync-results.{subs}.json.stream', 'w') as results_handle:
        for json_obj in results_static + results_dynamic:
            results_handle.write(json.dumps({
                'stream': 'results',
                'record': json_obj,
            }, sort_keys=True))
            results_handle.write('\n')

    return success_static and success_dynamic
