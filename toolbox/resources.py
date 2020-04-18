"""Main module to update resources"""

# Standard library
import base64
import os
import re
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
from typing import Dict, Iterator

# Third parties imports
from progress.bar import ChargingBar
import ruamel.yaml as yaml

# Local libraries
from toolbox import logger
from toolbox import utils, helper


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
    """ check if the subscription has a vpn """
    does_have_vpn = code.get('vpn')
    if does_have_vpn:
        logger.info(f"{subs} needs VPN. ")
        logger.info("Make sure to run your VPN software before cloning.\n")


def repo_url(subs, baseurl, repo):
    """ return the repo url """
    for user, passw in ['repo_user', 'repo_pass'], \
                       ['repo_user_2', 'repo_pass_2']:
        repo_user = ''
        repo_pass = ''
        with open('../config/secrets.yaml') as secrets:
            if f'{user}:' in secrets.read():
                repo_user = utils.get_sops_secret(
                    user,
                    f'../config/secrets.yaml',
                    f'continuous-{subs}'
                )
                repo_pass = utils.get_sops_secret(
                    passw,
                    f'../config/secrets.yaml',
                    f'continuous-{subs}'
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
    credentials = utils.get_sops_secret(
        'repo_key',
        f'../config/secrets.yaml',
        f'continuous-{subs}'
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
        uri = repo_url(subs, baseurl, repo)
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
    config_file = f'subscriptions/{subs}/config/config.yml'
    destination_folder = f'subscriptions/{subs}/fusion'

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

        utils.aws_login(f'continuous-{subs}')

        for repo in repos_config:
            repo_type = repo.get('git-type')
            if repo_type == 'ssh':
                success = ssh_repo_cloning(subs, repo)
            elif repo_type == 'https':
                success = http_repo_cloning(subs, repo)
            else:
                logger.info(f"Invalid git-type on subscription {subs}")
                success = False

    os.chdir(original_dir)

    return success


def edit_secrets(subs: str) -> bool:
    """
    Open config/secrets.yaml file of a project
    """
    status: bool = True
    profile = f'continuous-{subs}'
    secrets_file = f'subscriptions/{subs}/config/secrets.yaml'
    if not os.path.exists(secrets_file):
        logger.error(f'secrets.yaml does not exist in {subs}')
        status = False
    else:
        utils.aws_login(f'continuous-{subs}')
        subprocess.call(
            f'sops --aws-profile {profile} {secrets_file}',
            shell=True
        )
    return status


def vpn(subs: str) -> bool:
    """ using subscription vpn """

    success: bool = True
    config_file = f'toolbox/vpns/{subs}'
    vpn_list = [f for f in os.listdir('toolbox/vpns/')
                if os.path.isfile(os.path.join('toolbox/vpns/', f))]

    if (os.path.exists(f'{config_file}-bogota.sh') and
            os.path.exists(f'{config_file}-medellin.sh')):
        city = input(('Do you want to use bogota\'s or medellin\'s'
                      ' VPN? [1: Bogota - 2: Medellin]: '))
        if city == '1':
            utils.aws_login(f'continuous-{subs}')
            subprocess.call(
                f'./{config_file}-bogota.sh',
                shell=True
            )
        else:
            utils.aws_login(f'continuous-{subs}')
            subprocess.call(
                f'./{config_file}-medellin.sh',
                shell=True
            )
    else:
        if not os.path.isfile(f'{config_file}.sh'):
            logger.error("No VPN file found")
            logger.info(f'Available VPNs:\n{vpn_list}')
            success = False
        else:
            utils.aws_login(f'continuous-{subs}')
            subprocess.call(
                f'./{config_file}.sh',
                shell=True
            )
    return success


def read_secrets(subs: str) -> bool:
    """
    Print config/secrets.yaml file of a project to stdout
    """
    status: bool = True
    profile = f'continuous-{subs}'
    secrets_file = f'subscriptions/{subs}/config/secrets.yaml'
    if not os.path.exists(secrets_file):
        logger.error(f'secrets.yaml does not exist in {subs}')
        status = False
    else:
        utils.aws_login(f'continuous-{subs}')
        logger.info(f'Printing {subs} secrets: \n')
        subprocess.call(
            f'sops --aws-profile {profile} -d {secrets_file}',
            shell=True
        )
    return status


def check_mailmap(subs: str) -> bool:
    """ verify if mailmap is sorted and .
    """
    flag = True
    filename = '.mailmap'
    path = 'subscriptions/' + subs
    logger.info(f'Checking {subs} mailmap')
    if not os.path.exists(path) or not subs:
        failuremsg = f"Please run inside a project or use --subs\n"
        failuremsg += 'continuous/subscription/..\n'
        logger.error(failuremsg)
        flag = False
    elif not os.path.exists(f'{path}/{filename}'):
        failuremsg = f"No mailmap in {subs} \n"
        logger.error(failuremsg)
        flag = False
    else:
        with open(f'{path}/{filename}', 'r+') as mailmap:
            linelist = mailmap.readlines()
            sort = sorted(linelist)
            if linelist == []:
                flag = False
                logger.error("Mailmap is empty \n")
            elif linelist != sort:
                logger.error("Mailmap is not properly sorted \n")
                mailmap.seek(0)
                mailmap.truncate(0)
                for sorted_lines in sort:
                    mailmap.write(str(sorted_lines) + '\n')
                logger.info("^ Mailmap was sorted, I did it for you ;) \n")
                flag = False
            else:
                logger.info("Mailmap sorted")

            mailmap.seek(0)
            regex = re.compile(r'^[A-Z][a-z]*\s[A-z][a-z]*\s<')
            for line in mailmap:
                # Check if all authors start with Single name
                # and Last name on Title case:
                if not regex.match(line):
                    failuremsg = f" Author {line} is not properly formatted \n"
                    logger.error(failuremsg)
                    flag = False
        logger.info("Done!")
    return flag


def get_fingerprint(subs: str) -> bool:
    """ Get the hash and date of every folder in fusion
    """
    results = []
    max_hash = None
    max_date = ''
    path = f"subscriptions/{subs}"
    if not os.path.exists(path):
        logger.error(f"There is no project with the name: {subs}")
        logger.info("Please run fingerprint inside a project or use subs")
        return False
    path += "/fusion"
    if not os.path.exists(path):
        logger.error("There is no a fusion folder in the subscription")
        return False
    listpath = os.listdir(f"subscriptions/{subs}/fusion")

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
    path = f"subscriptions/{subs}"
    repos: tuple = (None, None)
    config_file = f'subscriptions/{subs}/config/config.yml'
    if not os.path.exists(path):
        logger.error(f"There is no project with the name: {subs}")
        return (None, None)
    with open(config_file) as config_handle:
        config = yaml.safe_load(config_handle.read())
        if not config.get('code'):
            return (None, None)
    repositories = helper.integrates.get_project_repos(subs)
    integrates_active: list = []
    # Filter active repositories
    for repo in repositories:
        repo_full_url = repo['urlRepo']
        repo_branch = repo['branch']
        if 'historic_state' not in repo \
                or repo['historic_state'][-1:][0]['state'] == 'ACTIVE':
            integrates_active.append(f'{repo_full_url}/{repo_branch}')
    if not os.path.isfile(config_file):
        logger.error("No config file in the current directory")
    else:
        with open(config_file) as config_handle:
            config = yaml.safe_load(config_handle.read())
            repos_config = config.get('code')
            repo_names: list = []
            for repo in repos_config:
                if repo['branches']:
                    repo_names.extend(
                        ''.join(i.split('/')[-2]) for i in repo['branches'])
            inactive_repos: list = []
            missing_repos: list = []
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


def print_inactive_missing_repos(subscription, inactive_repos,
                                 missing_repos) -> None:
    print(json.dumps({
        'stream': 'repositories',
        'record': {
            'subscription': subscription,
            'inactive': inactive_repos,
            'missing': missing_repos,
        }
    }))


def check_repositories(subs)-> bool:
    projects = os.listdir('subscriptions')
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
    toolboxpath = os.path.dirname(__file__)
    rules_file = f'{toolboxpath}/rules.def'
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
        os.remove('ignored.txt')
    return filepaths


def does_project_exist(subs: str) -> bool:
    path = f"subscriptions/{subs}"
    if not os.path.exists(path):
        logger.info(f"There is no project with the name: {subs}")
        return False
    return True


def does_project_have_fusion_folder(subs: str) -> bool:
    path = f"subscriptions/{subs}/fusion"
    if not os.path.exists(path):
        logger.info(f"There is no fusion folder in the subscription")
        return False
    return True


def yield_subscription_repositories(subs: str) -> Iterator[str]:
    repositories = os.listdir(f"subscriptions/{subs}/fusion")
    yield from repositories


def yield_remote_repositories(subs: str) -> Iterator[str]:
    remote_path = f"'s3://continuous-repositories/{subs}/active/'"
    list_command_s3 = f"aws s3 ls {remote_path}"
    ls_s3 = utils.run_command(list_command_s3, ".", {})
    repos_set = list(ls_s3[1].replace(" ", "")
                             .replace("PRE", "")
                             .replace("/", "")
                             .splitlines())
    yield from repos_set


def sync_inactive_repo_to_s3(subs: str, repo: str):
    active_s3_bucket = f"s3://continuous-repositories/{subs}/active/{repo}/"
    inactive_s3_bucket = (f"s3://continuous-repositories/"
                          f"{subs}/inactive/{repo}/")
    if not is_in_local(subs, repo):
        logger.info(f"Moving {repo} to inactive folder in s3")
        sync_command = ["aws", "s3", "mv", active_s3_bucket,
                        inactive_s3_bucket,
                        "--recursive",
                        "--sse", "AES256"]
        subprocess.run(sync_command, check=True)
        logger.info(f"Repo {repo} moved to inactive folder!")


def sync_active_repo_to_s3(subs: str, repo: str):
    active_s3_bucket = f"s3://continuous-repositories/{subs}/active/{repo}/"
    logger.info(f"Uploading {repo} to s3")
    subs_path = f"subscriptions/{subs}/fusion/{repo}"
    sync_command = ["aws", "s3", "sync", subs_path, active_s3_bucket,
                    "--sse", "AES256"]
    subprocess.run(sync_command, check=True)
    logger.info(f"Repo {repo} sync completed!")


def is_in_s3(subs: str, repo: str) -> bool:
    repos_set = set(yield_remote_repositories(subs))
    return repo in repos_set


def is_in_local(subs: str, repo: str) -> bool:
    local_path = f"subscriptions/{subs}/fusion/"
    repos_set = set(os.listdir(local_path))
    return repo in repos_set


def sync_repositories_to_s3(subs: str) -> bool:
    if not does_project_exist(subs) or\
       not does_project_have_fusion_folder(subs):
        return False
    remote_repositories = yield_remote_repositories(subs)
    local_repositories = yield_subscription_repositories(subs)
    utils.aws_login(f"continuous-{subs}")
    logger.info("Checking inactive repositories")
    for repo in remote_repositories:
        sync_inactive_repo_to_s3(subs, repo)
    logger.info("Checking active repositories")
    for repo in local_repositories:
        sync_active_repo_to_s3(subs, repo)
    return True


def sync_active_repo_to_fusion(subs: str):
    local_path = f"subscriptions/{subs}/fusion/"
    bucket_path = f"s3://continuous-repositories/{subs}/active/"
    if not os.path.exists(local_path):
        os.makedirs(local_path, exist_ok=True)
    sync_command = ["aws", "s3", "sync", bucket_path, local_path,
                    "--sse", "AES256", "--quiet"]
    subprocess.run(sync_command, check=True)


def sync_s3_to_fusion(subs: str) -> bool:
    if not does_project_exist(subs):
        return False
    logger.info(f"Dowloading {subs} repositories")
    sync_active_repo_to_fusion(subs)
    return True
