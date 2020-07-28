"""Main module to update resources"""

# Standard library
import base64
import os
import sys
import json
import platform
import shlex
import shutil
import subprocess
import urllib.parse
from multiprocessing import cpu_count
from multiprocessing.pool import ThreadPool
from subprocess import Popen, PIPE, check_output
from typing import Dict, List, Tuple

# Third parties imports
from progress.bar import ChargingBar
import ruamel.yaml as yaml

# Local libraries
from toolbox import logger
from toolbox import utils


def cmd_execute(cmnd, folder='.'):
    """ Execute a cmd command in the folder """
    env_vars: Dict[str, str] = {
        'GIT_SSL_NO_VERIFY': '1',
    }
    process = Popen(
        shlex.split(cmnd),
        stdout=PIPE,
        stderr=PIPE,
        cwd=folder,
        env={**os.environ.copy(), **env_vars})
    result = process.communicate()
    result = list(map(lambda x: x.decode('utf-8', 'ignore'), result))
    return result


def print_problems(problems, branches):
    """ print problems in the repos"""
    logger.info(f'Problems with the following repositories:' +
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


def repo_url(baseurl, repo):
    """ return the repo url """
    for user, passw in ['repo_user', 'repo_pass'], \
                       ['repo_user_2', 'repo_pass_2']:
        repo_user = ''
        repo_pass = ''
        with open('../config/secrets-prod.yaml') as secrets:
            if f'{user}:' in secrets.read():
                repo_user = utils.generic.get_sops_secret(
                    user,
                    f'../config/secrets-prod.yaml',
                    f'continuous-admin'
                )
                repo_pass = utils.generic.get_sops_secret(
                    passw,
                    f'../config/secrets-prod.yaml',
                    f'continuous-admin'
                )
                repo_user = urllib.parse.quote_plus(repo_user)
                repo_pass = urllib.parse.quote_plus(repo_pass)
        uri = baseurl + "/" + repo
        uri = uri.replace('<user>', repo_user)
        uri = uri.replace('<pass>', repo_pass)
        # check if the user has permissions in the repo
        command = f"git ls-remote {uri}"
        cmd = cmd_execute(command)
        if 'fatal' not in cmd[1]:
            return uri
    return cmd[1]


def ssh_repo_cloning(subs, code) -> bool:
    """ cloning or updated a repository ssh """
    problems: list = []
    credentials = utils.generic.get_sops_secret(
        'repo_key',
        f'../config/secrets-prod.yaml',
        f'continuous-admin'
    )
    key = base64.b64decode(credentials).decode('utf-8')
    # Improve compatibility with windows
    if 'Windows' in platform.system():
        keyfile = 'key'
    else:
        keyfile = os.popen('mktemp').read()[:-1]
        os.system(f"chmod 600 '{keyfile}'")
    file = open(keyfile, 'w+')
    file.write(key)
    file.close()
    os.system("chmod 0400 " + keyfile)
    baseurl = code.get('url')[0]
    if 'source.developers.google' not in baseurl:
        baseurl = baseurl.replace('ssh://', '')
    branches = code.get('branches')
    # Avoid ssh warning prompt:
    host = baseurl.split('@')[1].split(':')[0]
    subprocess.getstatusoutput(
        "ssh-keyscan -H " + host + " >> ~/.ssh/known_hosts")
    progress = ChargingBar(
        'Progress:',
        max=len(branches),
        suffix='%(percent)d%% [%(index)d/%(max)d]')

    def action(repo_br):
        has_vpn(code, subs)
        repo = '/'.join(repo_br.split('/')[0:-1])
        branch = repo_br.split('/')[-1]
        # handle urls special chars in branch names
        branch = (urllib.parse.unquote(branch)) if "%2" in branch else branch
        uri = baseurl + repo
        folder = repo.split('/')[-1]
        if os.path.isdir(folder):
            # Update already existing repo
            command = f""" ssh-agent sh -c "ssh-add '{keyfile}'; \
                     git pull origin '{branch}'"; """

            cmd = cmd_execute(command, folder)
            if len(cmd[0]) == 0 and 'fatal' in cmd[1]:
                problems.append({'repo': repo_br, 'problem': cmd[1]})
            else:
                progress.next()
                logger.info(
                    f"""\n#UPDATING {repo_br} ....\n{cmd[1]}\n{cmd[0]}""")
        else:
            # Clone repo:
            command = f""" ssh-agent sh -c "ssh-add '{keyfile}'; \
                    git clone -b '{branch}' --single-branch '{uri}'"; """

            cmd = cmd_execute(command)
            if len(cmd[0]) == 0 and 'fatal' in cmd[1]:
                problems.append({'repo': repo_br, 'problem': cmd[1]})
            else:
                progress.next()
                logger.info(
                    f"""\n#CLONNING {repo_br} ....\n{cmd[1]}\n{cmd[0]}""")

    with ThreadPool(processes=cpu_count()) as worker:
        worker.map(action, branches)
        progress.finish()

    if len(problems) > 0:
        print_problems(problems, branches)
        return False
    # Remove identities and keys
    clear = 'ssh-agent sh -c "ssh-add -D; rm -f ' + keyfile + '"'
    os.system(clear)
    return True


def http_repo_cloning(subs, code) -> bool:
    """ cloning or updated a repository https """
    problems: list = []
    # script does not support vpns atm
    baseurl = code.get('url')[0]
    branches = code.get('branches')
    progress = ChargingBar(
        'Progress:',
        max=len(branches),
        suffix='%(percent)d%% [%(index)d/%(max)d]')

    def action(repo_br):
        has_vpn(code, subs)
        repo = '/'.join(repo_br.split('/')[0:-1])
        uri = repo_url(baseurl, repo)
        branch = repo_br.split('/')[-1]
        folder = repo.split('/')[-1]
        if os.path.isdir(folder):
            # Update already existing repo
            if platform.system() == 'Linux':
                command = f"git pull origin '{branch}'"
            else:
                command = f"git pull origin {branch}"
            cmd = cmd_execute(command, folder)
            if len(cmd[0]) == 0 and 'fatal' in cmd[1]:
                problems.append({'repo': repo_br, 'problem': cmd[1]})
            else:
                progress.next()
                logger.info(
                    f"""\n#UPDATING {repo_br} ....\n{cmd[0]}\n{cmd[1]}""")
        else:
            if platform.system() == 'Linux':
                command = \
                    f"git clone -b '{branch}' --single-branch '{uri}'"
            else:
                command = f"git clone -b {branch} --single-branch {uri}"

            cmd = cmd_execute(command)
            if len(cmd[0]) == 0 and 'fatal' in cmd[1]:
                problems.append({'repo': repo_br, 'problem': cmd[1]})
            else:
                progress.next()
                logger.info(
                    f"""\n#CLONNING {repo_br} ....\n{cmd[0]}\n{cmd[1]}""")

    with ThreadPool(processes=cpu_count()) as worker:
        worker.map(action, branches)
        progress.finish()

    if problems:
        print_problems(problems, branches)
        return False
    return True


def repo_cloning(subs: str) -> bool:
    """ cloning or updated a repository"""

    success = True
    original_dir: str = os.getcwd()
    config_file = f'groups/{subs}/config/config.yml'
    destination_folder = f'groups/{subs}/fusion'

    if not os.path.isfile(config_file):
        logger.error("No config file in the current directory")
        success = False
    else:
        with open(config_file) as config_handle:
            config = yaml.safe_load(config_handle.read())

        if platform.system() == 'Windows' \
                and os.path.isdir(destination_folder):
            shutil.rmtree(destination_folder)

        os.makedirs(destination_folder, exist_ok=True)
        os.chdir(destination_folder)

        repos_config = config.get('code', [])
        repos_fusion = os.listdir('.')

        repo_names: list = []
        for repo in repos_config:
            repo_names.extend(
                ''.join(i.split('/')[:-1]) for i in repo['branches'])

        repo_difference = set(repos_fusion).difference(set(repo_names))

        # delete repositories of fusion that are not in the config
        for repo_dif in repo_difference:
            logger.info(f'Deleting {repo_dif}')
            shutil.rmtree(repo_dif)

        utils.generic.aws_login('continuous-admin')

        for repo in repos_config:
            repo_type = repo.get('git-type')
            if repo_type == 'ssh':
                success = ssh_repo_cloning(subs, repo)
            elif repo_type == 'https':
                success = http_repo_cloning(subs, repo)
            else:
                logger.info(f"Invalid git-type on group {subs}")
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


def get_active_missing_repos(subs):
    """ Get inactive and missing repositories in the config file """
    path: str = f"groups/{subs}"
    repos: Tuple = (None, None)
    config_file: str = f'groups/{subs}/config/config.yml'
    if not os.path.exists(path):
        logger.error(f"There is no project with the name: {subs}")
        return repos

    with open(config_file) as config_handle:
        config = yaml.safe_load(config_handle.read())
        if 'code' not in config:
            return repos

    repositories: List[Dict] = utils.integrates.get_project_repos(subs)
    integrates_active: List[str] = []
    # Filter active repositories
    for repo in repositories:
        repo_full_url = repo.get('urlRepo', None)
        repo_branch = repo.get('branch', None)
        if not repo_full_url or not repo_branch:
            continue
        if 'historic_state' not in repo \
                or repo['historic_state'][-1:][0]['state'] == 'ACTIVE':
            integrates_active.append(f'{repo_full_url}/{repo_branch}')

    if not os.path.isfile(config_file):
        logger.error("No config file in the current directory")
        return repos

    with open(config_file) as config_handle:
        config = yaml.safe_load(config_handle.read())
        repos_config: List[Dict] = config.get('code', [])
        repo_names: List[str] = []
        for repo in repos_config:
            repo_names.extend(
                ''.join(
                    i.split('/')[-2])
                for i in repo.get('branches') or [])
        inactive_repos: List[str] = []
        missing_repos: List[str] = []
        for repo in repo_names:
            is_inactive = next((
                False
                for active in integrates_active
                if repo in active), True)
            if is_inactive:
                inactive_repos.append(repo)
        for active in integrates_active:
            is_missing = next((
                False
                for repo in repo_names
                if repo in active), True)
            if is_missing:
                missing_repos.append(active)
        if missing_repos or inactive_repos:
            repos = (inactive_repos, missing_repos)
    return repos


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


def check_repositories(subs) -> bool:
    projects = os.listdir('groups')
    if subs != 'all':
        projects = [subs]
    for project in projects:
        inactive_repos, missing_repos = get_active_missing_repos(project)
        if inactive_repos or missing_repos:
            print_inactive_missing_repos(project, inactive_repos,
                                         missing_repos)
        elif subs != 'all':
            return False
    return True


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
