#!/usr/bin/env python3
"""Clone or update repos in continuous.

Automatically reads every config.yml.
"""

import os
import re
import json
import time
import base64
import subprocess
import urllib.parse

from typing import Iterable, List, Tuple, Any

import yaml

# Type aliases that improve clarity
JSON = Any

SOURCE = "/git/fluidsignal/continuous"
TARGET = "/git"

# exit on clonning errors
PORCELAIN = False

# repos that use OAUTH2
USEAUTH2 = (
    "Repo_Alis_Front",
)

# subscriptions with sub-subscriptions
NESTED = (
    "banistmo",
)

# repos to ignore when found inside subscriptions
IGNORE_WHEN_INSIDE = (
    "asserts",
    "integrates"
)


class BadConfigYml(Exception):
    """Raised when a bad config.yml is parsed."""


def iterate_subscriptions() -> Iterable[str]:
    """Yield paths of the subscriptions in the continuous repo."""
    for subscription in os.listdir(f"{SOURCE}/subscriptions"):
        subscription_path: str = f"{SOURCE}/subscriptions/{subscription}"
        if subscription in NESTED:
            for sub in os.listdir(subscription_path):
                if sub not in IGNORE_WHEN_INSIDE:
                    yield f"{subscription_path}/{sub}"
        else:
            if subscription not in IGNORE_WHEN_INSIDE:
                yield subscription_path


def add_ssh_key(project: str) -> None:
    """Add the ssh key of a project to the current enviroment."""
    data = base64.b64decode(
        os.popen(
            f"vault read -field=repo_key secret/continuous/{project}").read())
    os.system(f"rm -f ~/.ssh/{project}")
    with open(os.path.expanduser(f'~/.ssh/{project}'), "wb") as file:
        file.write(data)
        file.write(bytes("\n", "utf-8"))
    os.system(f"chmod 0400 ~/.ssh/{project}")
    os.system(f"ssh-add ~/.ssh/{project}")


def filter_url(url: str) -> Tuple[str, str, str, str, str, str]:
    """Filter the parts of a url."""
    match = re.match(r"(.*?)://(.*?)@(.*?)/(.*)", url)
    if match:
        groups = match.groups()
    prot, user = groups[0], groups[1]
    if groups[3]:
        rest = groups[3][0:-1] if groups[3][-1] == "/" else groups[3]
    else:
        rest = ""
    groups = groups[2].split(":")
    host, port = groups[0], groups[1] if len(groups) == 2 else ""
    host_port = f"{host}:{port}" if port else host
    return prot, user, host, port, host_port, rest


def get_project_name(subscription: str) -> str:
    """Parse the subscription path and returns the project name."""
    repo_name = subscription.split(os.sep)[-1]
    subs_name = subscription.split(os.sep)[-2]
    if subs_name in NESTED:
        project = f"{subs_name}-{repo_name}"
    else:
        project = repo_name

    return project


def get_repo_user_pass(prot: str, project: str) -> Tuple[str, str]:
    """Return the repo user/pass if prot if http or https."""
    repo_user = ""
    repo_pass = ""
    if prot in ("http", "https"):
        repo_user = os.popen((
            f"vault read -field=repo_user "
            f"secret/continuous/{project}")).read()
        repo_pass = os.popen((
            f"vault read -field=repo_pass "
            f"secret/continuous/{project}")).read()
        repo_pass = urllib.parse.quote_plus(repo_pass)

    return repo_user, repo_pass


def parse_config(
        subscription: str) -> Tuple[List[Tuple[Any, Any]], str, str, str]:
    """Parse the config.yml."""
    with open(f"{subscription}/config/config.yml", "r") as config_file:
        yml_file = yaml.load(config_file)

    config = yml_file.get("code", None)
    if config is None:
        print(f"ERROR|{subscription}|no code tag in yml|")
        raise BadConfigYml

    git_type = config.get("git-type", "")
    path_branch: List[Tuple[Any, Any]] = [
        (pb.rsplit("/", 1)[0], pb.rsplit("/", 1)[1])
        for pb in config.get("branches", [])
    ]

    # get url from the config.yml
    url = str(config.get("url")[0])

    # get vpn
    vpn_soft = yml_file.get('vpn', {}).get('software', "")

    return path_branch, url, git_type, vpn_soft


def execute(clone: str, update: str, target_repo: str, do_print=True) -> int:
    """Execute the clone or update."""
    nrepos_change: int = 0

    if not os.path.isdir(target_repo):
        if do_print:
            print(f"clone: {clone}")
        if not os.system(clone):
            nrepos_change = 1
        elif PORCELAIN:
            exit(1)
    else:
        os.chdir(target_repo)
        if do_print:
            print(f"clone: {update}")
        if not os.system(update):
            nrepos_change = 1
        elif PORCELAIN:
            exit(1)

    return nrepos_change


def process_subscriptions() -> JSON:
    """Process a subscription."""
    # pylint: disable = too-many-locals, too-many-statements, too-many-branches

    branches_json: JSON = {}
    for subscription in iterate_subscriptions():
        nrepos = 0
        os.chdir(subscription)

        project = get_project_name(subscription)

        try:
            path_branch, url, git_type, vpn_soft = parse_config(subscription)
        except BadConfigYml:
            continue

        # get needed parameters
        prot, user, host, port, host_port, rest = filter_url(url)
        repo_user, repo_pass = get_repo_user_pass(prot, project)

        print(f"INFO|YML|{subscription}|{url}|{path_branch}|")
        print(f"INFO|URL|{prot}|{user}|{host}|{port}|{rest}|")

        if vpn_soft == "forticlient":
            vpn_repo_user = os.popen((
                f"vault read -field=repo_user "
                f"secret/continuous/{project}")).read()
            vpn_repo_pass = os.popen((
                f"vault read -field=repo_pass "
                f"secret/continuous/{project}")).read()
            vpn_user = os.popen((
                f"vault read -field=vpn_user_1 "
                f"secret/continuous/{project}")).read()
            vpn_pass = os.popen((
                f"vault read -field=vpn_pass_1 "
                f"secret/continuous/{project}")).read()
            vpn_secret = os.popen((
                f"vault read -field=vpn_secret_1 "
                f"secret/continuous/{project}")).read()
            os.system(
                f"echo 'username = {vpn_user}' >> forti_config")
            os.system(
                f"echo 'password = {vpn_pass}' >> forti_config")
            os.system(
                f"echo 'trusted-cert = {vpn_secret}' >> forti_config")
            proccess = subprocess.Popen(
                ["bash", "-c", "openfortivpn -c forti_config > forti_log"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)
            print("waiting 10 seconds", proccess)
            time.sleep(10)

        once = True
        branches_json[project] = {}
        for path, branch in path_branch:
            repo = path.replace("/", "-")
            branches_json[project][repo] = branch
            restpath = f"{rest}/{path}" if rest else path
            target_repo = f"{TARGET}/{project}/{repo}"

            if repo in USEAUTH2:
                repo_user2 = os.popen((
                    f"vault read -field=repo_user_2 "
                    f"secret/continuous/{project}")).read()
                repo_pass2 = os.popen((
                    f"vault read -field=repo_pass_2 "
                    f"secret/continuous/{project}")).read()
                repo_pass2 = urllib.parse.quote_plus(repo_pass2)

                uri = (
                    f"{prot}://{repo_user2}:{repo_pass2}@{host_port}/"
                    f"{restpath}")
                uri = uri if "codecommit" in host_port else f"{uri}.git"
                clone = (
                    f"git clone -b {branch} "
                    f"--single-branch {uri} {target_repo}")
                update = f"cd {target_repo}; git pull origin {branch}"
            elif prot in ("http", "https"):
                uri = (
                    f"{prot}://{repo_user}:{repo_pass}@{host_port}/"
                    f"{restpath}")
                uri = uri if "codecommit" in host_port else f"{uri}.git"
                uri = uri.replace(
                    "<user>",
                    vpn_repo_user) if vpn_soft == "forticlient" else uri
                uri = uri.replace(
                    "<pass>",
                    vpn_repo_pass) if vpn_soft == "forticlient" else uri
                clone = (
                    f"git clone -b {branch} "
                    f"--single-branch {uri} {target_repo}")
                update = f"cd {target_repo}; git pull origin {branch}"
            else:
                if "codecommit" in git_type:
                    uri = f"ssh://{user}@{host_port}/{restpath}"
                else:
                    uri = f"{user}@{host_port}/{restpath}"

                if once:
                    once = False
                    add_ssh_key(project)

                clone = (
                    f"ssh-agent sh -c \""
                    f"ssh-keyscan {host} >> ~/.ssh/known_hosts;"
                    f"ssh-add ~/.ssh/{project};"
                    f"git clone -b {branch} "
                    f"--single-branch {uri} {target_repo}\"")
                update = (
                    f"ssh-agent sh -c \""
                    f"ssh-keyscan {host} >> ~/.ssh/known_hosts;"
                    f"ssh-add ~/.ssh/{project};"
                    f"git pull origin {branch}\"")

            os.system("cat forti_log")
            nrepos += execute(clone, update, target_repo)

        os.system("pkill openfortivpn")

        print(f"INFO|STATS|{subscription}|{nrepos}|")

    return branches_json


def main() -> None:
    """Usual entry point."""
    branches = process_subscriptions()

    with open(f"{TARGET}/../branches.json", "w") as file:
        json.dump(branches, file, indent=2)


if __name__ == "__main__":
    main()
