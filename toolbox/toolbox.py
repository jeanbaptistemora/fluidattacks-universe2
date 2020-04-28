"""Main module to build and check Assert Exploits."""

# Standard library
import datetime
import os
import re
import glob
import json
import multiprocessing
import textwrap
from time import time
from typing import (
    Any,
    Dict,
    List,
    Tuple,
)

# Third parties libraries
import ruamel.yaml as yaml

# Local libraries
from toolbox import api, constants, logger, utils

# Compiled regular expresions
RE_SPACE_CHARS = re.compile(r'\s', flags=re.M)
RE_NOT_ALLOWED_CHARS = re.compile(r'[^a-zá-úñÁ-ÚÑA-Z0-9\s,._]', flags=re.M)


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


def append_finding_title_to_exploit(
    exploit_path: str,
    finding_title: str,
):
    """Append the finding title to an exploit at the beginning."""
    with open(exploit_path) as exploit:
        exploit_content = exploit.read()

    with open(exploit_path, 'w') as exploit:
        exploit.write(textwrap.dedent(
            f"""
            # {datetime.datetime.utcnow()}
            from fluidasserts.utils import generic

            generic.add_finding('{finding_title}')
            del generic

            """)[1:])
        exploit.write(exploit_content)


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
        exploit.write(textwrap.dedent(
            f"""
            import utilities
            from fluidasserts.utils import generic

            if utilities.is_current_dir_in_repositories({finding_repos_str}):
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
            """))


def create_mock_dynamic_exploit(
        exploit_path: str, finding_state: bool,
        finding_title: str, finding_description: str, finding_threat: str,
        finding_attack_vector: str, finding_recommendation: str) -> None:
    """Mock a exploit according to it's status."""
    reason: str = create_mock__get_reason(exploit_path)

    with open(exploit_path, 'w') as exploit:
        exploit.write(textwrap.dedent(
            f"""
            from fluidasserts.utils import generic

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
            """))


def fill_with_mocks(subs_glob: str, create_files: bool = True) -> tuple:
    """Fill every exploit in continuous repository with a mock."""
    subs_glob = subs_glob.lower()

    created_static_mocks: dict = {}
    created_dynamic_mocks: dict = {}

    for roots in sorted(glob.glob(
            f'subscriptions/{subs_glob}/forces/static')):
        re_match: Any = re.search(
            r'subscriptions/(\w+)/forces/static', roots)
        subscription = re_match.groups(0)[0]
        created_static_mocks[subscription] = []
        created_dynamic_mocks[subscription] = []

        for finding_id, finding_title in \
                utils.integrates.get_project_findings(subscription):
            exploit_name = f'{finding_id}.exp'
            cannot_exploit_name = f'{finding_id}.cannot.exp'

            sast, dast = utils.integrates.get_finding_type(finding_id)

            sast_folder = \
                f'subscriptions/{subscription}/forces/static/exploits'
            dast_folder = \
                f'subscriptions/{subscription}/forces/dynamic/exploits'
            sast_path = f'{sast_folder}/{exploit_name}'
            dast_path = f'{dast_folder}/{exploit_name}'
            cannot_sast_path = f'{sast_folder}/{cannot_exploit_name}'
            cannot_dast_path = f'{dast_folder}/{cannot_exploit_name}'

            finding_title = utils.integrates.get_finding_title(finding_id)

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
    for path in sorted(glob.glob(f'subscriptions/{subs_glob}/forces/*')):
        os.makedirs(f'{path}/resources', exist_ok=True)
        os.makedirs(f'{path}/mocked-exploits', exist_ok=True)
        os.makedirs(f'{path}/accepted-exploits', exist_ok=True)
        os.makedirs(f'{path}/extra-packages', exist_ok=True)

    for exploit_path in sorted(glob.glob(
            f'subscriptions/{subs_glob}/forces/*/exploits/*.exp')):
        logger.info(f'processing {exploit_path}')

        subscription = \
            subscription_regex.search(exploit_path).group(1)  # type: ignore

        exploit_kind, finding_id = \
            utils.forces.scan_exploit_for_kind_and_id(exploit_path)

        if not exploit_kind or not finding_id:
            logger.warn(f'{exploit_path} has no (exploit-kind or finding-id)!')
            os.remove(exploit_path)
            continue

        if not utils.integrates.does_finding_exist(finding_id):
            logger.warn(f'{exploit_path} does not exist on Integrates!')
            os.remove(exploit_path)
            continue

        if not utils.integrates.is_finding_released(finding_id):
            logger.warn(f'{exploit_path} has not been released on Integrates!')
            os.remove(exploit_path)
            continue

        if not utils.integrates.is_finding_in_subscription(
                finding_id, subscription):
            logger.warn(f'{exploit_path} is not member of {subscription}!')
            os.remove(exploit_path)
            continue

        finding_title = sanitize_string(
            utils.integrates.get_finding_title(finding_id))

        # If it's a mock, then create it on the mocks folder
        is_a_mock: bool = exploit_kind in ('mock.exp', 'cannot.exp')
        if is_a_mock:
            finding_description = sanitize_string(
                utils.integrates.get_finding_description(finding_id))
            finding_threat = sanitize_string(
                utils.integrates.get_finding_threat(finding_id))
            finding_attack_vector = sanitize_string(
                utils.integrates.get_finding_attack_vector(finding_id))
            finding_recommendation = sanitize_string(
                utils.integrates.get_finding_recommendation(finding_id))

            if '/forces/static/exploits/' in exploit_path:
                finding_state = utils.integrates.is_finding_open(
                    finding_id, constants.SAST)
                finding_repos = utils.integrates.get_finding_repos(
                    finding_id)
                create_mock_static_exploit(
                    exploit_path, finding_state, finding_repos,
                    finding_title, finding_description, finding_threat,
                    finding_attack_vector, finding_recommendation)
            elif '/forces/dynamic/exploits/' in exploit_path:
                finding_state = utils.integrates.is_finding_open(
                    finding_id, constants.DAST)
                create_mock_dynamic_exploit(
                    exploit_path, finding_state,
                    finding_title, finding_description, finding_threat,
                    finding_attack_vector, finding_recommendation)
            else:
                logger.warn(f'{exploit_path} is not static nor dynamic')

        # Append the finding id to the exploit
        append_finding_title_to_exploit(exploit_path, finding_title)

        # If it's accepted, move it to the accepted-exploits folder
        if utils.integrates.is_finding_accepted(finding_id):
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


def _run_static_exploit(
        exploit_path: str, repository_path: str, fernet_key: str):
    """Helper to run 1 exploit."""
    exploit_name = os.path.basename(exploit_path)
    repo: str = os.path.basename(repository_path)

    bb_resources = os.path.join(os.path.dirname(os.path.dirname(
        os.path.abspath(exploit_path))), 'resources')

    start_time: float = time()
    status, stdout, _ = utils.generic.run_command_old(
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
    status_str: str = \
        constants.RICH_EXIT_CODES_INV.get(status, 'OTHER').upper()
    logger.info(
        f'{exploit_name:<25} : {elapsed:>8.2f} s : {status_str:<17} : {repo}')
    return exploit_name, repo, stdout, elapsed


def run_static_exploits(
        subs: str, exp_name: str, verbose: bool = True) -> bool:
    """Run exploits."""

    utils.generic.aws_login(f'continuous-{subs}')

    fernet_key: str = utils.generic.get_sops_secret(
        f'forces_aws_secret_access_key',
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
                f'subscriptions/{subs}/forces/static/exploits/*.exp'))))

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

    utils.generic.aws_login(f'continuous-{subs}')

    start = time()
    times: Dict[str, Any] = {}
    fernet_key: str = utils.generic.get_sops_secret(
        f'forces_aws_secret_access_key',
        f'subscriptions/{subs}/config/secrets.yaml',
        f'continuous-{subs}')

    bb_resources = os.path.abspath(
        f'subscriptions/{subs}/forces/dynamic/resources')

    for exploit_path in sorted(glob.glob(
            f'subscriptions/{subs}/forces/dynamic/exploits/*.exp')):

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
        utils.generic.run_command_old(
            cmd=(f"asserts -n -ms '{exploit_path}'"
                 f"  >> '{exploit_output_path}'   "),
            cwd=f'subscriptions/{subs}',
            env={'FA_NOTRACK': 'true',
                 'FA_STRICT': 'true',
                 'BB_FERNET_KEY': fernet_key,
                 'BB_RESOURCES': bb_resources,
                 'CURRENT_EXPLOIT_KIND': 'dynamic'})
        times[exploit_name] = time() - times[exploit_name]
        utils.generic.run_command_old(
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
    for _, vulns_path in utils.generic.iter_vulns_path(subs, exp, run_kind):
        _, finding_id = utils.forces.scan_exploit_for_kind_and_id(vulns_path)

        result = False
        exp_kind = vulns_path.split('/')[3]
        if not exp_kind == run_kind and run_kind != 'all':
            continue

        logger.info(
            f'deleting: {vulns_path}')

        result = utils.integrates.delete_pending_vulns(
            finding_id=finding_id)

        if result:
            logger.info('   ', 'Success')
        else:
            logger.info('   ', 'Failed')


def report_vulnerabilities(subs: str, vulns_name: str,
                           run_kind: str = 'all') -> bool:
    """Automatically report exploit vulnerabilities to integrates."""
    success: bool = True
    for vulns_path, exploit_path in utils.generic.iter_vulns_path(
            subs, vulns_name, run_kind):
        _, finding_id = \
            utils.forces.scan_exploit_for_kind_and_id(exploit_path)

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
            glob.glob(f'subscriptions/{subs}/forces/*/exploits/*.exp'))):

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

        for kind, who, where in api.asserts.iterate_open_results_from_file(
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
            f'/forces/static/exploits/*.exp.out.yml')):
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
            for kind, who, where in api.asserts.iterate_open_results_from_file(
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


def _get_static_dictionary(finding_id) -> dict:
    dictionary: dict = {}

    for repo, rel_path, _, _ in \
            utils.integrates.get_finding_static_states(finding_id):

        try:
            dictionary[repo].add(rel_path)
        except KeyError:
            dictionary[repo] = {rel_path}

    return {
        repo: sorted(dictionary[repo])
        for repo in sorted(dictionary)
    }


def get_static_dictionary(subs: str, exp: str = 'all') -> bool:
    """Print a dictionary with the subscription findings."""
    exploit_paths = sorted(
        glob.glob(f'subscriptions/{subs}/forces/*/exploits/*.exp'))
    integrates_findings_ = utils.integrates.get_project_findings(subs)
    if exp == 'local':
        integrates_findings = [
            record for record in integrates_findings_
            if any([
                record[0]
                in utils.forces.scan_exploit_for_kind_and_id(path)[1]
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
        dictionary = _get_static_dictionary(finding_id)
        logger.info(json.dumps(dictionary, indent=4, sort_keys=True))

    return True


def has_forces(subs: str) -> bool:
    """Return True if the subscription has an asserts folder."""
    return os.path.isdir(f'subscriptions/{subs}/forces')
