"""Main module to update resources"""

# Standard library
import base64
from contextlib import contextmanager
import os
import stat
import sys
import json
from shlex import quote as shq
import shutil
import subprocess
import urllib.parse
from multiprocessing import cpu_count
from multiprocessing.pool import ThreadPool
from subprocess import DEVNULL, Popen, PIPE, check_output
import tempfile
from typing import (
    Any,
    Dict,
    Iterator,
    List,
    Optional,
)

# Third parties imports
from alive_progress import alive_bar, config_handler


# Local libraries
from toolbox import logger
from toolbox import utils
from toolbox.constants import API_TOKEN
from toolbox.api import integrates

config_handler.set_global(length=25)


def cmd_execute(cmnd, folder='.'):
    """ Execute a cmd command in the folder """
    env_vars: Dict[str, str] = {
        'GIT_SSL_NO_VERIFY': '1',
    }
    process = Popen(
        cmnd,
        stdin=DEVNULL,
        stdout=PIPE,
        stderr=PIPE,
        cwd=folder,
        env={**os.environ.copy(), **env_vars})
    result = process.communicate()
    result = list(map(lambda x: x.decode('utf-8', 'ignore'), result))
    return result


def print_problems(problems, branches):
    """ print problems in the repos"""
    logger.info('Problems with the following repositories:' +
                f'[{len(problems)}/{len(branches)}]\n\n')
    for problem in problems:
        logger.info(problem['repo'] + '\n')
        logger.info(problem['problem'])


def has_vpn(code, subs):
    """ check if the group has a vpn """
    does_have_vpn = code.get('vpn')
    if does_have_vpn:
        logger.info(f"{subs} needs VPN. ")
        logger.info("Make sure to run your VPN software before cloning.\n")


@contextmanager
def setup_ssh_key(baseurl: str) -> Iterator[str]:
    try:
        credentials = utils.generic.get_sops_secret(
            'repo_key', '../config/secrets-prod.yaml', 'continuous-admin')
        key = base64.b64decode(credentials).decode('utf-8')

        with tempfile.NamedTemporaryFile(delete=False) as keyfile:
            os.chmod(keyfile.name, stat.S_IREAD | stat.S_IWRITE)
            keyfile.write(key.encode())

        os.chmod(keyfile.name, stat.S_IREAD)

        # Avoid ssh warning prompt:
        host = baseurl.split('@')[1].split(':')[0]
        subprocess.getstatusoutput(
            f"ssh-keyscan -H {host} >> ~/.ssh/known_hosts")
        yield keyfile.name
    finally:
        cmd_execute([
            'ssh-agent', 'sh', '-c', ';'.join(
                ('ssh-add -D', f'rm -f {shq(keyfile.name)}'))
        ])


def repo_url(baseurl: str):
    """ return the repo url """
    for user, passw in ['repo_user', 'repo_pass'], \
                       ['repo_user_2', 'repo_pass_2']:
        repo_user = ''
        repo_pass = ''
        with open('../config/secrets-prod.yaml') as secrets:
            if f'{user}:' in secrets.read():
                repo_user = utils.generic.get_sops_secret(
                    user,
                    '../config/secrets-prod.yaml',
                    'continuous-admin'
                )
                repo_pass = utils.generic.get_sops_secret(
                    passw,
                    '../config/secrets-prod.yaml',
                    'continuous-admin'
                )
                repo_user = urllib.parse.quote_plus(repo_user)
                repo_pass = urllib.parse.quote_plus(repo_pass)
        uri = baseurl.replace('<user>', repo_user)
        uri = uri.replace('<pass>', repo_pass)
        # check if the user has permissions in the repo
        cmd = cmd_execute(['git', 'ls-remote', uri])
        if 'fatal' not in cmd[1]:
            return uri
    return cmd[1]


def _ssh_repo_cloning(git_root: Dict[str, str]) -> Optional[Dict[str, str]]:
    """ cloning or updated a repository ssh """
    baseurl = git_root['url']
    if 'source.developers.google' not in baseurl:
        baseurl = baseurl.replace('ssh://', '')
    branch = urllib.parse.unquote(git_root['branch'])

    problem: Optional[Dict[str, Any]] = None

    # handle urls special chars in branch names
    repo_name = baseurl.split('/')[-1]
    folder = repo_name
    with setup_ssh_key(baseurl) as keyfile:
        if os.path.isdir(folder):
            # Update already existing repo
            command = [
                'ssh-agent',
                'sh',
                '-c',
                ';'.join((
                    f"ssh-add {shq(keyfile)}",
                    f"git pull origin {shq(branch)}",
                )),
            ]

            cmd = cmd_execute(command, folder)
            if len(cmd[0]) == 0 and 'fatal' in cmd[1]:
                logger.error(f'{repo_name}/{branch} failed')
                logger.error(cmd[1])
                problem = {'repo': repo_name, 'problem': cmd[1]}
        else:
            # Clone repo:
            command = [
                'ssh-agent',
                'sh',
                '-c',
                ';'.join(
                    (f"ssh-add {shq(keyfile)}", f"git clone -b {shq(branch)} "
                     f"--single-branch {shq(baseurl)}")),
            ]

            cmd = cmd_execute(command)
            if len(cmd[0]) == 0 and 'fatal' in cmd[1]:
                logger.error(f'{repo_name}/{branch} failed')
                logger.error(cmd[1])
                problem = {'repo': repo_name, 'problem': cmd[1]}

    if problem:
        utils.integrates.update_root_cloning_status(
            git_root['id'],
            'FAILED',
            problem['problem'],
        )
    else:
        utils.integrates.update_root_cloning_status(
            git_root['id'],
            'OK',
            'Cloned successfully',
        )
    return problem


def _http_repo_cloning(git_root: Dict[str, str]) -> Optional[Dict[str, str]]:
    """ cloning or updated a repository https """
    # script does not support vpns atm
    baseurl = git_root['url']
    repo_name = baseurl.split('/')[-1]
    branch = git_root['branch']

    problem: Optional[Dict[str, Any]] = None

    # check if user has access to current repository
    baseurl = repo_url(git_root['url'])
    if 'fatal:' in baseurl:
        logger.error(f'{repo_name}/{branch} failed')
        logger.error(baseurl)
        problem = {'repo': repo_name, 'problem': baseurl}

    branch = git_root['branch']
    folder = repo_name
    if os.path.isdir(folder):
        # Update already existing repo
        cmd = cmd_execute(['git', 'pull', 'origin', branch], folder)
        if len(cmd[0]) == 0 and 'fatal' in cmd[1]:
            logger.error(f'{repo_name}/{branch} failed')
            logger.error(cmd[1:])
            problem = {'repo': repo_name, 'problem': cmd[1]}
    # validate if there is no problem with the baseurl
    elif not problem:
        cmd = cmd_execute([
            'git',
            'clone',
            '-b',
            branch,
            '--single-branch',
            baseurl,
        ])
        if len(cmd[0]) == 0 and 'fatal' in cmd[1]:
            logger.error(f'{repo_name}/{branch} failed')
            problem = {'repo': repo_name, 'problem': cmd[1]}

    if problem:
        utils.integrates.update_root_cloning_status(
            git_root['id'],
            'FAILED',
            problem['problem'],
        )
    else:
        utils.integrates.update_root_cloning_status(
            git_root['id'],
            'OK',
            'Cloned successfully',
        )
    return problem


def repo_cloning(subs: str) -> bool:
    """ cloning or updated a repository"""

    success = True
    problems: list = []
    original_dir: str = os.getcwd()
    destination_folder = f'groups/{subs}/fusion'

    os.makedirs(destination_folder, exist_ok=True)
    os.chdir(destination_folder)

    repo_request = integrates.Queries.git_roots(
        API_TOKEN,
        subs,
    )
    if not repo_request.ok:
        logger.error(repo_request.errors)
        return False

    repositories: List[Dict[str, str]] = repo_request.data['project']['roots']

    repos_fusion = os.listdir('.')

    repo_names: list = [repo['url'].split('/')[-1] for repo in repositories]

    repo_difference = set(repos_fusion).difference(set(repo_names))

    # delete repositories of fusion that are not in the config
    for repo_dif in repo_difference:
        logger.info(f'Deleting {repo_dif}')
        shutil.rmtree(repo_dif)

    utils.generic.aws_login('continuous-admin')

    with alive_bar(len(repositories), enrich_print=False) as progress_bar:

        def action(git_root: Dict[str, str]) -> None:
            repo_type = 'ssh' if git_root['url'].startswith('ssh') else 'https'
            problem: Optional[Dict[str, str]] = None

            # check if current repo is active
            if git_root['state'] != 'ACTIVE':
                return

            if repo_type == 'ssh':
                problem = _ssh_repo_cloning(git_root)
            elif repo_type == 'https':
                problem = _http_repo_cloning(git_root)
            else:
                logger.info("Invalid git-type on group %s", subs)
                problem = {
                    'repo': git_root['url'],
                    'problem': f'Invalid git-type on group {subs}'
                }
            if problem:
                problems.append(problem)
            else:
                progress_bar()

        with ThreadPool(processes=cpu_count()) as worker:
            worker.map(action, repositories)

    if problems:
        logger.error("Some problems occured: \n")

        for problem in problems:
            print(f'Repository: {problem["repo"]}')
            print(f'Description: {problem["problem"]}')
        success = False
    os.chdir(original_dir)

    return success


def edit_secrets(group: str, suffix: str, profile: str) -> bool:
    status: bool = True
    secrets_file: str = f'groups/{group}/config/secrets-{suffix}.yaml'
    if not os.path.exists(secrets_file):
        logger.error(f'secrets-{suffix}.yaml does not exist in {group}')
        status = False
    else:
        utils.generic.aws_login(profile)
        subprocess.call(
            f'sops --aws-profile {profile} {secrets_file}',
            shell=True
        )
    return status


def read_secrets(group: str, suffix: str, profile: str) -> bool:
    status: bool = True
    secrets_file: str = f'groups/{group}/config/secrets-{suffix}.yaml'
    if not os.path.exists(secrets_file):
        logger.error(f'secrets-{suffix}.yaml does not exist in {group}')
        status = False
    else:
        utils.generic.aws_login(profile)
        subprocess.call(
            f'sops --aws-profile {profile} --decrypt {secrets_file}',
            shell=True
        )
    return status


def get_fingerprint(subs: str) -> bool:
    """ Get the hash and date of every folder in fusion
    """
    results = []
    max_hash = ''
    max_date = ''
    path = f"groups/{subs}"
    if not os.path.exists(path):
        logger.error(f"There is no project with the name: {subs}")
        logger.info("Please run fingerprint inside a project or use subs")
        return False
    path += "/fusion"
    if not os.path.exists(path):
        logger.error("There is no a fusion folder in the group")
        return False
    listpath = os.listdir(f"groups/{subs}/fusion")

    for repo in (r for r in listpath if os.path.isdir(f'{path}/{r}')):
        # com -> commom command
        com = f'git -C "{path}/{repo}" log --max-count 1'
        hashr = os.popen(f'{com} --format=%h').read().replace('\n', '')
        date = os.popen(f'{com} --format=%aI').read().replace('\n', '')[0:16]
        if date > max_date:
            max_date = date
            max_hash = hashr
        results.append((repo, hashr, date))
    if results == []:
        logger.error(f"There is not any folder in fusion - Subs: {subs}")
        return False
    output_bar = '-' * 84
    output_fmt = '{:^59} {:^7} {:^16}'
    logger.info(output_bar)
    logger.info(output_fmt.format('Repository', 'Hash', 'Date'))
    logger.info(output_bar)
    for params in sorted(results):
        logger.info(output_fmt.format(*params))
    logger.info(output_bar)
    logger.info(output_fmt.format(len(results), max_hash, max_date))
    return True


def print_inactive_missing_repos(group, inactive_repos,
                                 missing_repos) -> None:
    print(json.dumps({
        'stream': 'repositories',
        'record': {
            'subscription': group,
            'inactive': inactive_repos,
            'missing': missing_repos,
        }
    }))


def fluidcounts(path):
    """Count lines of code using cloc."""
    filepaths = ''
    doc_langs = ["Markdown"]
    style_langs = ["CSS", "SASS", "LESS", "Stylus"]
    format_langs = ["XML", "XAML"]
    rules_file = '../../tools/rules.def'
    force_lang_def = '--force-lang-def=' + rules_file
    exclude_list = ",".join(doc_langs + style_langs + format_langs)
    exclude_lang = '--exclude-lang=' + exclude_list
    call_cloc = ['cloc', force_lang_def, exclude_lang]
    call_cloc += [path, '--ignored', 'ignored.txt', '--timeout', '900']
    try:
        myenv = os.environ.copy()
        myenv['LC_ALL'] = 'C'
        check_output(call_cloc, env=myenv)
        with open('ignored.txt', 'r') as outfile:
            filepaths = outfile.read()
    except OSError:
        print("You need to have Cloc installed and in your system path " +
              "for this task to work")
        sys.exit(1)
    finally:
        if os.path.exists('ignored.txt'):
            os.remove('ignored.txt')
    return filepaths
