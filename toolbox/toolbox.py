"""Main module to build and check Assert Exploits."""

# Standard library
import os
import re
import sys
import glob
import json
import textwrap
import functools
import ast
import multiprocessing
import datetime

from time import time
from typing import Any, Dict, List, Tuple

# Third parties libraries
import ruamel.yaml as yaml

# Local libraries
from toolbox import api, constants, helper, logger, utils

# Compiled regular expresions
RE_DAILY_COMMIT = re.compile(r'proj\(\w+\):\s+(\w+)')
RE_EXPLOITS_COMMIT = re.compile(r'\w+\(exp\):\s+(?:#\d+(?:\.\d+)?\s*)?(\w+)')

RE_FINDING_TITLE = re.compile(r'^\s*(\w+)[^\d]*(\d+).*$', flags=re.I)

RE_SPACE_CHARS = re.compile(r'\s', flags=re.M)
RE_NOT_ALLOWED_CHARS = re.compile(r'[^a-zá-úñÁ-ÚÑA-Z0-9\s,._]', flags=re.M)

RE_EXPLOIT_NAME = re.compile(
    r'/(?:\w+)-\d+-(\d+)\.(exp|mock\.exp|cannot.exp)$')


@functools.lru_cache(maxsize=None, typed=True)
def scan_exploit_for_kind_and_id(exploit_path: str) -> tuple:
    """Scan the exploit in search of metadata."""
    # /fin-1234-567890.exp        -> 567890, 'exp'
    # /fin-1234-567890.mock.exp   -> 567890, 'mock.exp'
    # /fin-1234-567890.cannot.exp -> 567890, 'cannot.exp'
    exploit_kind, finding_id = '', ''
    re_match = RE_EXPLOIT_NAME.search(exploit_path)
    if re_match:
        finding_id, exploit_kind = re_match.groups()
    else:
        logger.warn('no kind or id found in', exploit_path)
    return exploit_kind, finding_id


def sanitize_string(string: Any) -> str:
    """Sanitize the string to allow only certain values."""
    string = RE_NOT_ALLOWED_CHARS.sub('', str(string)[0:512])
    string = RE_SPACE_CHARS.sub(' ', string)
    string = string.strip()
    return string


def create_mock__get_reason(exploit_path: str) -> str:
    """Return the reason of why an exploit was not created."""
    with open(exploit_path, 'r') as exploit:
        reasons: List[str] = []

        for line in exploit.read().splitlines():
            reason = re.sub(r'^[#s]+', '', line)
            reason = reason.replace("\\", "\\\\").replace("'", "\\'").strip()
            if reason:
                reasons.append(f"' {reason}'")

        reason = '[' + ','.join(reasons) + ']'
    if not reasons:
        reason = """['We are working on it, you will see it soon!']"""
    return reason


def create_mock_static_exploit(
        exploit_path: str, finding_state: bool, finding_repos: tuple,
        finding_title: str, finding_description: str, finding_threat: str,
        finding_attack_vector: str, finding_recommendation: str) -> None:
    """Mock a exploit according to it's status."""
    reason: str = create_mock__get_reason(exploit_path)

    finding_repos_escaped = [
        repo.replace("\\", "\\\\").replace("'", "\\'")
        for repo in finding_repos]
    finding_repos_str = ','.join(f"'{repo}'" for repo in finding_repos_escaped)

    with open(exploit_path, 'w') as exploit:
        exploit.write(re.sub(r'^[ ]{12}', '', f'''
            import utilities
            from fluidasserts.utils import generic

            if utilities.is_current_dir_in_repositories({finding_repos_str}):
                generic.add_finding('{finding_title}')
                generic.check_function(
                    lambda: {finding_state},
                    metadata = {{
                        'title': '{finding_title}',
                        'description': '{finding_description}',
                        'threat': '{finding_threat}',
                        'attack_vector': '{finding_attack_vector}',
                        'recommendation': '{finding_recommendation}',
                        'message': {reason},
                        'source': 'Integrates'}})
            else:
                generic.add_finding((
                    '[Skipped] {finding_title} '
                    '(it does not apply to this repo)'))
            '''[1:], flags=re.MULTILINE))


def create_mock_dynamic_exploit(
        exploit_path: str, finding_state: bool,
        finding_title: str, finding_description: str, finding_threat: str,
        finding_attack_vector: str, finding_recommendation: str) -> None:
    """Mock a exploit according to it's status."""
    reason: str = create_mock__get_reason(exploit_path)

    with open(exploit_path, 'w') as exploit:
        exploit.write(re.sub(r'^[ ]{12}', '', f'''
            from fluidasserts.utils import generic

            generic.add_finding('{finding_title}')
            generic.check_function(
                lambda: {finding_state},
                metadata = {{
                    'title': '{finding_title}',
                    'description': '{finding_description}',
                    'threat': '{finding_threat}',
                    'attack_vector': '{finding_attack_vector}',
                    'recommendation': '{finding_recommendation}',
                    'message': {reason},
                    'source': 'Integrates'}})
            '''[1:], flags=re.MULTILINE))


@functools.lru_cache(maxsize=None, typed=True)
def is_valid_commit() -> bool:
    """Return True if the last commit in git history has the subs name."""
    commit_msg: str = os.popen('git log --max-count 1 --format=%s').read()[:-1]
    return bool(RE_DAILY_COMMIT.search(commit_msg)) or \
        bool(RE_EXPLOITS_COMMIT.search(commit_msg))


def is_gitlab_ci_and_master() -> bool:
    """Return True if we are in the GitLab CI and in the master branch."""
    return os.environ.get('CI_COMMIT_REF_NAME') == 'master'


def get_finding_static_repos_states(finding_id: str) -> dict:
    """Return a dict mappin repos to its expected state (OPEN, CLOSED)."""
    regex = re.compile(r'^([^/\\]+).*$')
    where_states = \
        helper.integrates.get_finding_static_where_states(finding_id)
    repos_states: dict = {}
    for repo, state in map(
            lambda x: (regex.sub(r'\1', x['path']), x['state']), where_states):
        try:
            repos_states[repo] = repos_states[repo] or state
        except KeyError:
            repos_states[repo] = state
    return repos_states


@functools.lru_cache(maxsize=None, typed=True)
def get_subscription_from_commit_msg() -> str:
    """Return the subscription name from the commmit msg."""
    commit_msg: str = os.popen('git log --max-count 1 --format=%s').read()[:-1]
    re_search: Any = RE_DAILY_COMMIT.search(commit_msg)
    if not re_search:
        re_search = RE_EXPLOITS_COMMIT.search(commit_msg)
    if not re_search:
        subscription: str = ''
    else:
        subscription, = re_search.groups()
    return subscription


def fill_with_mocks(subs_glob: str, create_files: bool = True) -> tuple:
    """Fill every exploit in continuous repository with a mock."""
    subs_glob = subs_glob.lower()

    created_static_mocks: dict = {}
    created_dynamic_mocks: dict = {}

    for roots in sorted(glob.glob(
            f'subscriptions/{subs_glob}/break-build/static')):
        re_match: Any = re.search(
            r'subscriptions/(\w+)/break-build/static', roots)
        subscription = re_match.groups(0)[0]
        created_static_mocks[subscription] = []
        created_dynamic_mocks[subscription] = []

        for finding_id, finding_title in \
                helper.integrates.get_project_findings(subscription):
            re_match = RE_FINDING_TITLE.search(finding_title)
            if not re_match:
                logger.error(f'bad title format for {finding_title}')
                continue
            let, num = re_match.groups(0)

            exploit_name = f'{let.lower()}-{num}-{finding_id}.exp'
            cannot_exploit_name = \
                f'{let.lower()}-{num}-{finding_id}.cannot.exp'

            sast, dast = helper.integrates.get_finding_type(finding_id)

            sast_folder = \
                f'subscriptions/{subscription}/break-build/static/exploits'
            dast_folder = \
                f'subscriptions/{subscription}/break-build/dynamic/exploits'
            sast_path = f'{sast_folder}/{exploit_name}'
            dast_path = f'{dast_folder}/{exploit_name}'
            cannot_sast_path = f'{sast_folder}/{cannot_exploit_name}'
            cannot_dast_path = f'{dast_folder}/{cannot_exploit_name}'

            finding_title = helper.integrates.get_finding_title(finding_id)

            if sast and not any(map(os.path.exists,
                                    (sast_path, cannot_sast_path))):
                if not os.path.exists(sast_folder):
                    os.makedirs(sast_folder)
                sast_path_mock = sast_path.replace('.exp', '.mock.exp')
                created_static_mocks[subscription].append(sast_path_mock)
                if create_files:
                    with open(sast_path_mock, 'w+'):
                        logger.info(f'mock supplied for {finding_title}')
                        logger.info(f'mock supplied for {sast_path}')
            if dast and not any(map(os.path.exists,
                                    (dast_path, cannot_dast_path))):
                if not os.path.exists(dast_folder):
                    os.makedirs(dast_folder)
                dast_path_mock = dast_path.replace('.exp', '.mock.exp')
                created_dynamic_mocks[subscription].append(dast_path_mock)
                if create_files:
                    with open(dast_path_mock, 'w+'):
                        logger.info(f'mock supplied for {finding_title}')
                        logger.info(f'mock supplied for {sast_path}')

    return created_static_mocks, created_dynamic_mocks


def generate_exploits(subs_glob: str) -> bool:
    """Generate needed arsenal and move troops to the battlefield."""
    subs_glob = subs_glob.lower()
    subscription_regex = re.compile(r'subscriptions/(\w+)')

    # Create the needed directories
    for path in sorted(glob.glob(f'subscriptions/{subs_glob}/break-build/*')):
        os.makedirs(f'{path}/resources', exist_ok=True)
        os.makedirs(f'{path}/mocked-exploits', exist_ok=True)
        os.makedirs(f'{path}/accepted-exploits', exist_ok=True)
        os.makedirs(f'{path}/extra-packages', exist_ok=True)

    for exploit_path in sorted(glob.glob(
            f'subscriptions/{subs_glob}/break-build/*/exploits/*.exp')):
        logger.info(f'processing {exploit_path}')

        subscription = \
            subscription_regex.search(exploit_path).group(1)  # type: ignore

        exploit_kind, finding_id = \
            scan_exploit_for_kind_and_id(exploit_path)

        if not exploit_kind or not finding_id:
            logger.warn(f'{exploit_path} has no (exploit-kind or finding-id)!')
            os.remove(exploit_path)
            continue

        if not helper.integrates.does_finding_exist(finding_id):
            logger.warn(f'{exploit_path} does not exist on Integrates!')
            os.remove(exploit_path)
            continue

        if not helper.integrates.is_finding_released(finding_id):
            logger.warn(f'{exploit_path} has not been released on Integrates!')
            os.remove(exploit_path)
            continue

        if not helper.integrates.is_finding_in_subscription(
                finding_id, subscription):
            logger.warn(f'{exploit_path} is not member of {subscription}!')
            os.remove(exploit_path)
            continue

        # If it's a mock, then create it on the mocks folder
        is_a_mock: bool = exploit_kind in ('mock.exp', 'cannot.exp')
        if is_a_mock:
            finding_title = sanitize_string(
                helper.integrates.get_finding_title(finding_id))
            finding_description = sanitize_string(
                helper.integrates.get_finding_description(finding_id))
            finding_threat = sanitize_string(
                helper.integrates.get_finding_threat(finding_id))
            finding_attack_vector = sanitize_string(
                helper.integrates.get_finding_attack_vector(finding_id))
            finding_recommendation = sanitize_string(
                helper.integrates.get_finding_recommendation(finding_id))

            if '/break-build/static/exploits/' in exploit_path:
                finding_state = helper.integrates.is_finding_open(
                    finding_id, constants.SAST)
                finding_repos = helper.integrates.get_finding_repos(
                    finding_id)
                create_mock_static_exploit(
                    exploit_path, finding_state, finding_repos,
                    finding_title, finding_description, finding_threat,
                    finding_attack_vector, finding_recommendation)
            elif '/break-build/dynamic/exploits/' in exploit_path:
                finding_state = helper.integrates.is_finding_open(
                    finding_id, constants.DAST)
                create_mock_dynamic_exploit(
                    exploit_path, finding_state,
                    finding_title, finding_description, finding_threat,
                    finding_attack_vector, finding_recommendation)
            else:
                logger.warn(f'{exploit_path} is not static nor dynamic')

        # If it's accepted, move it to the accepted-exploits folder
        if helper.integrates.is_finding_accepted(finding_id):
            logger.info(f'MOVE: {exploit_path} is accepted...')
            os.rename(
                exploit_path,
                exploit_path.replace('exploits', 'accepted-exploits'))
        elif is_a_mock:
            logger.info(f'MOVE: {exploit_path} is mocked and not accepted...')
            os.rename(
                exploit_path,
                exploit_path.replace('exploits', 'mocked-exploits'))

    return True


def are_exploits_synced__show(outputs_to_show: List[str]):
    """Print the results of a list of outputs."""
    if not is_gitlab_ci_and_master():
        logger.info('')
        logger.info('Please check the outputs in the following files:')
        while outputs_to_show:
            logger.info('- ', outputs_to_show.pop())


def are_exploits_synced__static(subs: str, exp_name: str) -> Tuple[bool, Any]:
    """Check if exploits results are the same as on Integrates."""
    success: bool = True
    results: list = []
    outputs_to_show: list = []
    if not is_gitlab_ci_and_master():
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

        finding_id = scan_exploit_for_kind_and_id(exploit_path)[1]
        finding_title = helper.integrates.get_finding_title(finding_id)

        if os.path.isfile(exploit_output_path):
            os.remove(exploit_output_path)

        integrates_status = get_finding_static_repos_states(finding_id)

        local_repos: set = set(filter(
            lambda repo: os.path.isdir(f'subscriptions/{subs}/fusion/{repo}'),
            os.listdir(f'subscriptions/{subs}/fusion')))

        integrates_repos: set = set(integrates_status.keys())

        for repo in integrates_repos.union(local_repos):
            analyst_status: Any = integrates_status.get(repo, False)
            asserts_status: Any = None
            repository_path: str = f'subscriptions/{subs}/fusion/{repo}'
            if os.path.isdir(repository_path):
                asserts_status, _, _ = utils.run_command(
                    cmd=(f"echo '---'                          "
                         f"  >> '{exploit_output_path}';       "
                         f"echo 'repository: {repo}'           "
                         f"  >> '{exploit_output_path}';       "
                         f"asserts -eec -n -ms '{exploit_path}'"
                         f"  >> '{exploit_output_path}'        "),
                    cwd=repository_path,
                    env={'FA_NOTRACK': 'true',
                         'FA_STRICT': 'true',
                         'BB_FERNET_KEY': fernet_key,
                         'BB_RESOURCES': bb_resources,
                         'CURRENT_EXPLOIT_KIND': 'static'})
            else:
                continue

            imsg = 'OPEN' if analyst_status else 'CLOSED'
            amsg = constants.RICH_EXIT_CODES_INV.get(
                asserts_status, 'OTHER').upper()

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
                'num_open_asserts': 0,
                'num_open_integrates': 0,
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

    if not is_gitlab_ci_and_master():
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

        finding_id = scan_exploit_for_kind_and_id(exploit_path)[1]
        finding_title = helper.integrates.get_finding_title(finding_id)

        if os.path.isfile(exploit_output_path):
            os.remove(exploit_output_path)

        analyst_status = helper.integrates.is_finding_open(
            finding_id, constants.DAST)

        asserts_status, _, _ = utils.run_command(
            cmd=(f"asserts -eec -n -ms '{exploit_path}'"
                 f"  >> '{exploit_output_path}'        "),
            cwd=f'subscriptions/{subs}',
            env={'FA_NOTRACK': 'true',
                 'FA_STRICT': 'true',
                 'BB_FERNET_KEY': fernet_key,
                 'CURRENT_EXPLOIT_KIND': 'dynamic',
                 'BB_RESOURCES': bb_resources,
                 'BB_AWS_ROLE_ARNS': ','.join(aws_arn_roles)})

        imsg = 'OPEN' if analyst_status else 'CLOSED'
        amsg = constants.RICH_EXIT_CODES_INV.get(
            asserts_status, 'OTHER').upper()

        if imsg != amsg:
            if once:
                logger.info(f'    *{finding_id:<10} {finding_title}*')
                once = False
            logger.info('        {i} {a}'.format(
                i=f'Integrates: {imsg!s:<6}', a=f'Asserts: {amsg!s:<17}'))
            if amsg == 'EXPLOIT-ERROR':
                success = False
                outputs_to_show.append(exploit_output_path)
        results.append({
            'datetime': datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
            'exploit_path': os.path.relpath(exploit_path),
            'exploit_type': 'dynamic',
            'num_open_asserts': 0,
            'num_open_integrates': 0,
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

    success_static, results_static = \
        are_exploits_synced__static(subs, exp_name)
    success_dynamic, results_dynamic = \
        are_exploits_synced__dynamic(subs, exp_name)

    logger.info('')
    if utils.is_env_ci():
        logger.info('You can run this check locally:')
        logger.info(f'  continuous $ pip3 install '
                    f'break-build/packages/toolbox[with_fluidasserts]')
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


def were_exploits_uploaded(subs: str) -> bool:
    """Break build if there are less exploits in continuous than possible."""
    success = True
    something_found = False

    static_mocks, dynamic_mocks = fill_with_mocks(
        subs_glob=subs, create_files=False)

    logger.info(f'Hi!')
    logger.info('')
    logger.info('```')

    for kind, finding_types in (('static', constants.SAST),
                                ('dynamic', constants.DAST)):
        mock_exploits = static_mocks if kind == 'static' else dynamic_mocks
        mock_exploits = mock_exploits.get(subs, [])
        cont_exploits = sorted(glob.glob(
            f'subscriptions/{subs}/break-build/{kind}/exploits/*.exp'))

        num_exploits = len(cont_exploits)
        num_possible = num_exploits + len(mock_exploits)

        if mock_exploits:
            something_found = True
            logger.info(f'Some {kind} exploits are not in continuous yet')
            logger.info(f'  All possible exploits: {num_possible}')
            logger.info(f'  Continuous exploits:   {num_exploits}')
            logger.info('')
            for exploit_path in mock_exploits:
                _, finding_id = scan_exploit_for_kind_and_id(exploit_path)
                finding_title = \
                    helper.integrates.get_finding_title(finding_id)
                exploit_name = os.path.basename(exploit_path).replace(
                    '.mock.exp', '.exp')
                finding_state = helper.integrates.is_finding_open(
                    finding_id, finding_types)
                finding_status = "OPEN" if finding_state else "CLOSED"
                logger.info(f'    {finding_status:<6}'
                            f' {exploit_name:<25} {finding_title}')
            logger.info()
            if kind == 'static':
                success = False
    if something_found:
        logger.error(f'Please upload more exploits to your subscription')
    else:
        logger.info(f'Thanks for constantly uploading your exploits!')
    logger.info(f'```')

    return success


def _run_static_exploit(
        exploit_path: str, repository_path: str, fernet_key: str):
    """Helper to run 1 exploit."""
    exploit_name = os.path.basename(exploit_path)
    repo: str = os.path.basename(repository_path)

    bb_resources = os.path.join(os.path.dirname(os.path.dirname(
        os.path.abspath(exploit_path))), 'resources')

    start_time: float = time()
    status, stdout, _ = utils.run_command(
        cmd=f"""
            echo '---'
            && echo "repository: '{repo}'"
            && asserts -n -eec '{exploit_path}'
            """.replace('\n', ' '),
        cwd=repository_path,
        env={'FA_NOTRACK': 'true',
             'FA_STRICT': 'true',
             'BB_FERNET_KEY': fernet_key,
             'BB_RESOURCES': bb_resources,
             'CURRENT_EXPLOIT_KIND': 'static'})
    elapsed: float = time() - start_time
    status = constants.RICH_EXIT_CODES_INV.get(status, 'OTHER').upper()
    logger.info(
        f'{exploit_name:<25} : {elapsed:>8.2f} s : {status:<17} : {repo}')
    return exploit_name, repo, stdout, elapsed


def run_static_exploits(
        subs: str, exp_name: str, verbose: bool = True) -> bool:
    """Run exploits."""

    utils.aws_login(f'continuous-{subs}')

    fernet_key: str = utils.get_sops_secret(
        f'break_build_aws_secret_access_key',
        f'subscriptions/{subs}/config/secrets.yaml',
        f'continuous-{subs}')

    repositories_to_run: tuple = tuple(map(
        lambda repository_path: os.path.join(os.getcwd(), repository_path),
        sorted(glob.glob(f'subscriptions/{subs}/fusion/*'))))

    exploits_to_run: tuple = tuple(map(
        lambda exploit_path: os.path.join(os.getcwd(), exploit_path),
        filter(
            lambda e: (exp_name or '') in e,
            glob.glob(
                f'subscriptions/{subs}/break-build/static/exploits/*.exp'))))

    for exploit_path in exploits_to_run:
        if os.path.isfile(f'{exploit_path}.out.yml'):
            os.remove(f'{exploit_path}.out.yml')

    times: Dict[str, Any] = {}
    stdouts: Dict[str, Any] = {}
    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as worker:
        for exploit_name, repo, stdout, elapsed in worker.starmap(
                func=_run_static_exploit,
                iterable=(
                    (exploit_path, repository_path, fernet_key)
                    for exploit_path in exploits_to_run
                    for repository_path in repositories_to_run
                ),
                chunksize=1):
            try:
                times[repo][exploit_name] = elapsed
            except KeyError:
                times[repo] = {exploit_name: elapsed}
            try:
                stdouts[exploit_name].append(stdout)
            except KeyError:
                stdouts[exploit_name] = [stdout]

    for exploit_path in exploits_to_run:
        exploit_name = os.path.basename(exploit_path)
        with open(f'{exploit_path}.out.yml', 'w') as output_handle:
            output_handle.writelines(stdouts[exploit_name])

    if not verbose:
        return True

    total = 0.0
    max_sub_total = 0.0
    for repo in sorted(times):
        logger.info(repo)
        sub_total = 0.0
        for exp in times[repo]:
            sub_total += times[repo][exp]
            logger.info(f'  {exp:<25}: {times[repo][exp]:>8.2f} s.')
        total += sub_total
        logger.info(f'  {"total":<25}: {sub_total:>8.2f} s.')
        max_sub_total = \
            max_sub_total if max_sub_total > sub_total else sub_total
    logger.info()
    logger.info(f'{"total":<27}: {total:>8.2f} s.')
    logger.info(f'{"slowest repo":<27}: {max_sub_total:>8.2f} s.')
    return True


def run_dynamic_exploits(subs: str, exp_name: str) -> bool:
    """Run exploits."""

    utils.aws_login(f'continuous-{subs}')

    start = time()
    times: Dict[str, Any] = {}
    fernet_key: str = utils.get_sops_secret(
        f'break_build_aws_secret_access_key',
        f'subscriptions/{subs}/config/secrets.yaml',
        f'continuous-{subs}')

    bb_resources = os.path.abspath(
        f'subscriptions/{subs}/break-build/dynamic/resources')

    for exploit_path in sorted(glob.glob(
            f'subscriptions/{subs}/break-build/dynamic/exploits/*.exp')):

        exploit_path = os.path.join(os.getcwd(), exploit_path)
        exploit_name = os.path.basename(exploit_path)
        exploit_output_path = f'{exploit_path}.out.yml'

        if (exp_name or '') in exploit_name:
            logger.info(f'running: {exploit_name}')
        else:
            logger.debug(f'skipped: {exploit_name}')
            continue

        if os.path.isfile(exploit_output_path):
            os.remove(exploit_output_path)

        times[exploit_name] = time()
        utils.run_command(
            cmd=(f"asserts -n -ms '{exploit_path}'"
                 f"  >> '{exploit_output_path}'   "),
            cwd=f'subscriptions/{subs}',
            env={'FA_NOTRACK': 'true',
                 'FA_STRICT': 'true',
                 'BB_FERNET_KEY': fernet_key,
                 'BB_RESOURCES': bb_resources,
                 'CURRENT_EXPLOIT_KIND': 'dynamic'})
        times[exploit_name] = time() - times[exploit_name]
        utils.run_command(
            cmd=(f"echo '# elapsed: {times[exploit_name]}'"
                 f"  >> '{exploit_output_path}'"),
            cwd=f'subscriptions/{subs}',
            env={})

    logger.info('')
    for exp in times:
        logger.info(f'{exp:<25}: {times[exp]:>8.2f} s.')
    logger.info('')
    logger.info(f'{"total":<25}: {time()-start:>8.2f} s.')
    return True


def delete_pending_vulnerabilities(subs: str,
                                   exp: str = '',
                                   run_kind: str = 'all'):
    """Delete pending vulnerabilities for a subscription."""
    for _, vulns_path in utils.iter_vulns_path(subs, exp, run_kind):
        _, finding_id = scan_exploit_for_kind_and_id(vulns_path)

        result = False
        exp_kind = vulns_path.split('/')[3]
        if not exp_kind == run_kind and run_kind != 'all':
            continue

        logger.info(
            f'deleting: {vulns_path}')

        result = helper.integrates.delete_pending_vulns(
            finding_id=finding_id)

        if result:
            logger.info('   ', 'Success')
        else:
            logger.info('   ', 'Failed')


def report_vulnerabilities(subs: str, vulns_name: str,
                           run_kind: str = 'all') -> bool:
    """Automatically report exploit vulnerabilities to integrates."""
    success: bool = True
    for vulns_path, exploit_path in utils.iter_vulns_path(
            subs, vulns_name, run_kind):
        _, finding_id = scan_exploit_for_kind_and_id(exploit_path)

        kind = vulns_path.split('/')[3]
        if not run_kind == kind and run_kind != 'all':
            continue

        logger.info(f'reporting: {vulns_path}')
        response = api.integrates.Mutations.upload_file(
            api_token=constants.API_TOKEN,
            identifier=finding_id,
            file_path=vulns_path)

        success = success and response.ok
        if response.ok:
            logger.info('  ', 'Success')
        else:
            logger.error('  ', 'Failed')

    return success


def _normalize(who: str, where: str) -> Tuple[str, str]:
    """Some checks like has_not_text don't have line number."""
    try:
        int(where)
    except ValueError:
        who = f'{who} [{where}]'
        where = '0'
    return who, where


def get_vulnerabilities_yaml(subs: str, run_kind: str = 'all') -> bool:
    """Get you the vulnerabilities.yml for every exploit."""
    vulns: int = 0
    for exploit_path in sorted(filter(
            lambda x: os.path.exists(f'{x}.out.yml'),
            glob.glob(f'subscriptions/{subs}/break-build/*/exploits/*.exp'))):

        kind = exploit_path.split('/')[3]
        if not run_kind == kind and run_kind != 'all':
            continue

        exploit_vulns_path = f'{exploit_path}.vulns.yml'
        exploit_output_path = f'{exploit_path}.out.yml'

        logger.info(exploit_path, end=' ')

        if os.path.isfile(exploit_vulns_path):
            os.remove(exploit_vulns_path)

        lines: List[Tuple[str, str]] = []
        inputs: List[Tuple[str, str]] = []

        for kind, who, where in api.asserts.iterate_results_from_file(
                exploit_output_path):
            vulns += 1
            if kind == 'SAST':
                lines.append(_normalize(who, where))
            elif kind == 'SCA':
                lines.append(_normalize(who, where))
            elif kind == 'DAST':
                inputs.append((who, where))

        stream: dict = {}
        with open(exploit_vulns_path, 'a+') as handle:
            if lines:
                stream['lines'] = [
                    {
                        'path': str(who),
                        'line': str(where),
                        'state': 'open',
                    }
                    for who, where in lines
                ]
            if inputs:
                stream['inputs'] = [
                    {
                        'url': str(who),
                        'field': str(where),
                        'state': 'open',
                    }
                    for who, where in inputs
                ]
            stream_as_yaml: str = yaml.safe_dump(  # type: ignore
                stream, allow_unicode=True, default_flow_style=False)
            handle.write(stream_as_yaml)

        logger.info(f'Done with {vulns} vulns')
    return True


def get_exps_fragments(subs: str, exp_name: str) -> bool:
    """Run exploits."""
    specific_context: int = 10
    path_to_fusion: str = f'subscriptions/{subs}/fusion'
    for exploit_output_path in sorted(glob.glob(
            f'subscriptions/{subs}'
            f'/break-build/static/exploits/*.exp.out.yml')):
        logger.info(os.path.basename(exploit_output_path), end=' ')

        if (exp_name or '') in exploit_output_path:
            logger.info(f'creating: {exploit_output_path}')
        else:
            logger.debug(f'skipped: {exploit_output_path}')
            continue

        fragments_path: str = exploit_output_path.replace(
            '.out.yml', '.fragments.lst')

        if os.path.isfile(fragments_path):
            os.remove(fragments_path)

        with open(fragments_path, 'a+') as fragments_file:
            for kind, who, where in api.asserts.iterate_results_from_file(
                    exploit_output_path):
                if kind != 'SAST':
                    continue
                whom, where = _normalize(who, where)
                line_no = int(where) - 1
                with open(file=os.path.join(path_to_fusion, who),
                          errors='backslashreplace') as target_handle:
                    lines = target_handle.read().splitlines()
                    context = specific_context if line_no == 0 else 10 ** 6
                    fragments_file.writelines([
                        f'{whom} @ {i:>6}:{lines[i]}\n'
                        for i in range(
                            max(0, line_no - context),
                            min(line_no + context, len(lines))
                        )
                    ])
                    fragments_file.write('=' * 256 + '\n')
        logger.info(f'Done')
    return True


def get_static_dictionary(subs: str, exp: str = 'all') -> bool:
    """Print a dictionary with the subscription findings."""
    exploit_paths = sorted(
        glob.glob(f'subscriptions/{subs}/break-build/*/exploits/*.exp'))
    integrates_findings_ = helper.integrates.get_project_findings(subs)
    if exp == 'local':
        integrates_findings = [
            record for record in integrates_findings_
            if any([
                record[0] in scan_exploit_for_kind_and_id(path)[1]
                for path in exploit_paths
            ])
        ]
    elif exp != 'all':
        integrates_findings = [
            record for record in integrates_findings_
            if exp in record[1] or exp in record[0]
        ]
    else:
        integrates_findings = list(integrates_findings_)

    for finding_id, finding_title in integrates_findings:
        logger.info(finding_id, finding_title)

        dictionary: Dict[str, Any] = {}
        for element in helper.integrates.get_finding_static_where_states(
                finding_id):

            try:
                repo, rel_path = element['path'].split('/', 1)
            except ValueError:
                logger.warn('Ignored due to bad format:', element['path'])
                continue

            try:
                dictionary[repo].add(rel_path)
            except KeyError:
                dictionary[repo] = {rel_path}

        dictionary = {k: list(sorted(v)) for k, v in dictionary.items()}

        logger.info(json.dumps(dictionary, indent=4, sort_keys=True))

    return True


def check_finding_title_match_integrates(path: str) -> bool:
    calls = set()
    with open(path, "r") as exploit_file:
        tree = ast.parse(exploit_file.read())
        for node in ast.walk(tree):
            # Filtering only function calls
            if isinstance(node, ast.Call)\
                    and isinstance(node.func, ast.Name):
                calls.add(node.func.id)
            elif isinstance(node, ast.Call)\
                    and isinstance(node.func, ast.Attribute):
                calls.add(node.func.attr)
    return "add_finding" in calls or "generic_static_exploit" in calls


def lint_exploits(subs: str, exp_name: str) -> bool:
    """Lint exploits for a subscription."""
    success: bool = True
    profile_path: str = "break-build/config/prospector/exploits.yml"
    for exploit_path in sorted(glob.glob(
            f'subscriptions/{subs}/break-build/*/exploits/*.exp')):

        if (exp_name or '') in exploit_path:
            logger.info(f'linting: {exploit_path}')
        else:
            logger.debug(f'skipped: {exploit_path}')
            continue

        logger.info(f'LINT: {exploit_path}')
        status_prosp, stdout_prosp, stderr_prosp = utils.run_command(
            cmd=(f'prospector'
                 f'    --output-format=vscode'
                 f'    --messages-only '
                 f"    --profile '{profile_path}'"
                 f"  '{exploit_path}'"),
            cwd='.',
            env={})
        status_mypy, stdout_mypy, stderr_mypy = utils.run_command(
            cmd=(f'mypy'
                 f'    --ignore-missing-imports'
                 f"  '{exploit_path}'"),
            cwd='.',
            env={})
        if status_prosp or status_mypy:
            if status_prosp:
                logger.info(stdout_prosp)
                logger.info(stderr_prosp)
            if status_mypy:
                logger.info(stdout_mypy)
                logger.info(stderr_mypy)
            success = False
        else:
            logger.info('  OK')
            logger.info()
        logger.info(f"Checking title match {exploit_path}")
        if ".cannot" not in exploit_path:
            if not check_finding_title_match_integrates(exploit_path):
                logger.error("There is not add_finding "
                             f"or generic_static_exploit in {exploit_path}")
                logger.info()
                success = False
        else:
            logger.info(f"skipped {exploit_path}")
    return success


def has_break_build(subs: str) -> bool:
    """Return True if the subscription has an asserts folder."""
    return os.path.isdir(f'subscriptions/{subs}/break-build')


def does_subs_exist(subs: str) -> bool:
    """Return True if the subscription exists."""
    if f'subscriptions/{subs}' in glob.glob('subscriptions/*'):
        return True
    logger.error(f'"{subs}" is not an existing subscription')
    logger.info(f'  please adjust your commit message, sire.')
    return False


def encrypt_secrets(subs: str) -> bool:
    """Encrypt a secrets.yml file for a subscription."""
    # pylint: disable=import-outside-toplevel
    from fluidasserts.helper import crypto

    utils.aws_login(f'continuous-{subs}')

    for resources_path in glob.glob(
            f'subscriptions/{subs}/break-build/*/resources'):
        plaintext_path: str = f'{resources_path}/plaintext.yml'
        encrypted_path: str = f'{resources_path}/secrets.yml'

        logger.info(
            f'Moving secrets from {plaintext_path} to {encrypted_path}')

        with open(plaintext_path) as plaintext_handle, \
                open(encrypted_path, 'w') as encrypted_handle:
            crypto.create_encrypted_yaml(
                key_b64=utils.get_sops_secret(
                    f'break_build_aws_secret_access_key',
                    f'subscriptions/{subs}/config/secrets.yaml',
                    f'continuous-{subs}'),
                secrets={
                    str(key): str(value)
                    for key, value in yaml.safe_load(
                        plaintext_handle.read())['secrets'].items()
                },
                file=encrypted_handle)

        logger.info('  Done!')
    return True


def decrypt_secrets(subs: str) -> bool:
    """Decrypt a secrets.yml file for a subscription."""
    # pylint: disable=import-outside-toplevel
    from fluidasserts.helper import crypto

    utils.aws_login(f'continuous-{subs}')

    for resources_path in glob.glob(
            f'subscriptions/{subs}/break-build/*/resources'):
        plaintext_path: str = f'{resources_path}/plaintext.yml'
        encrypted_path: str = f'{resources_path}/secrets.yml'

        logger.info(
            f'Moving secrets from {encrypted_path} to {plaintext_path}')

        if not os.path.exists(encrypted_path):
            logger.error(
                f'  No secrets.yml file found for {subs}')
            logger.error(
                f'    1. run $ fluid forces --init-secrets {subs}')
            logger.error(
                f'    2. put your secrets in {plaintext_path}')
            logger.error(
                f'    3. run $ fluid forces --encrypt {subs} ')
            sys.exit(78)
        else:
            crypto.create_decrypted_yaml(
                key_b64=utils.get_sops_secret(
                    f'break_build_aws_secret_access_key',
                    f'subscriptions/{subs}/config/secrets.yaml',
                    f'continuous-{subs}'),
                input_file=encrypted_path,
                output_file=plaintext_path)

            logger.info('  Done!')
    return True


def init_secrets(subs: str) -> bool:
    """Encrypt a secrets.yml file for a subscription."""
    for resources_path in (
            f'subscriptions/{subs}/break-build/static/resources',
            f'subscriptions/{subs}/break-build/dynamic/resources'):
        os.makedirs(resources_path, exist_ok=True)
        plaintext_path: str = f'{resources_path}/plaintext.yml'

        logger.info(f'Initializing {plaintext_path}')
        if not os.path.exists(plaintext_path):
            with open(plaintext_path, 'w') as plaintext_handle:
                plaintext_handle.write(yaml.safe_dump({  # type: ignore
                    'secrets': {
                        'test_user': 'Einstein',
                        'test_password': 'E=m*C^2',
                    },
                }))
        logger.info('  Done!')

    encrypt_secrets(subs)
    return True
