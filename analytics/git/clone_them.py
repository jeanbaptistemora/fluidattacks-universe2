"""Clone or update repos in continuous.

Automatically reads every config.yml.
"""

# temporal until next commit
# pylint: disable=redefined-outer-name, duplicate-code

import os
import re
import json
import base64
import urllib.parse

from typing import Iterable, Tuple, Any

import yaml

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

# repos with problems
IGNORE = (
    "caphec",       # URL returned 403 (does repo exist?)
    "aldak",        # no link to clone (no 'code' tag in config.yml)
    "bowky",        # bad private key (bad auth or auth declined)
    "yarumossac",   # Could not resolve host: serdev.gco.com.co
    "stebbins",     # Could not resolve host: inboggit01.suramericana.com.co
    "valvanera",    # Field "repo_key" not present in secret
    "villasilvia",  # Field "repo_key" not present in secret, unreachable
    "volantin",     # Field "repo_key" not present in secret, unreachable
)

# repos to ignore when found inside subscriptions
IGNORE_WHEN_INSIDE = (
    "asserts",
    "integrates"
)


def iterate_subscriptions() -> Iterable[str]:
    """Yields paths of the subscriptions in the continuous repo.
    """

    for subscription in os.listdir(f"{SOURCE}/subscriptions"):
        subscription_path = f"{SOURCE}/subscriptions/{subscription}"
        if subscription in IGNORE:
            continue
        elif subscription in NESTED:
            for sub in os.listdir(subscription_path):
                if sub not in IGNORE_WHEN_INSIDE:
                    yield f"{subscription_path}/{sub}"
        else:
            if subscription not in IGNORE_WHEN_INSIDE:
                yield subscription_path


def add_ssh_key(project: str) -> None:
    """Adds the ssh key of a project to the current enviroment.
    """

    data = base64.b64decode(
        os.popen(
            f"vault read -field=repo_key secret/continuous/{project}").read())
    os.system(f"rm -rf ~/.ssh/{project}")
    with open(os.path.expanduser(f'~/.ssh/{project}'), "wb") as file:
        file.write(data)
    os.system(f"chmod 0400 ~/.ssh/{project}")



def filter_url(url: str) -> Tuple[str, str, str, str, str]:
    """Filter the parts of a url.
    """

    groups = re.match(r"(.*?)://(.*?)@(.*?)/(.*)", url).groups() # type: ignore
    prot, user = groups[0], groups[1]
    if groups[3]:
        rest = groups[3][0:-1] if groups[3][-1] == "/" else groups[3]
    else:
        rest = ""
    groups = groups[2].split(":")
    host, port = groups[0], groups[1] if len(groups) == 2 else ""

    return prot, user, host, port, rest


def process_subscriptions():
    """Process a subscription.
    """

    return {}

BRANCHES: Any = {}
for subscription in iterate_subscriptions():
    nrepos = 0
    os.chdir(subscription)

    repo_name = subscription.split(os.sep)[-1]
    subs_name = subscription.split(os.sep)[-2]
    if subs_name in NESTED:
        project = f"{subs_name}-{repo_name}"
    else:
        project = repo_name

    with open(f"{subscription}/config.yml", "r") as config_file:
        config = yaml.load(config_file).get("code", None)

    if config is None:
        print(f"ERROR|{subscription}|no code tag in yml|")
        continue

    url = str(config.get("url")[0])
    rsplit = lambda rb, x: rb.rsplit("/", 1)[x]
    path_branch = [(rsplit(pb, 0), rsplit(pb, 1).lower()) for pb in config.get("branches", [])]
    git_type = config.get("git-type", "")

    # filter the url into canonical parts
    groups = re.match(r"(.*?)://(.*?)@(.*?)/(.*)", url).groups()  # type: ignore
    prot, user = groups[0], groups[1]
    if groups[3]:
        rest = groups[3][0:-1] if groups[3][-1] == "/" else groups[3]
    else:
        rest = ""
    groups = groups[2].split(":")
    host, port = groups[0], groups[1] if len(groups) == 2 else ""
    host_port = f"{host}:{port}" if port else host

    print(f"INFO|YML|{subscription}|{url}|{path_branch}|")
    print(f"INFO|URL|{prot}|{user}|{host}|{port}|{rest}|")

    repo_user = ""
    repo_pass = ""
    if prot in ("http", "https"):
        repo_user = os.popen((f"vault read -field=repo_user "
                              f"secret/continuous/{project}")).read()
        repo_pass = os.popen((f"vault read -field=repo_pass "
                              f"secret/continuous/{project}")).read()
        repo_pass = urllib.parse.quote_plus(repo_pass)

    once = True
    BRANCHES[project] = {}
    for path, branch in path_branch:
        repo = path.replace("/", "-")
        BRANCHES[project][repo] = branch
        restpath = f"{rest}/{path}" if rest else path
        target_repo = f"{TARGET}/{project}/{repo}"

        if repo in USEAUTH2:
            repo_user2 = os.popen((f"vault read -field=repo_user_2 "
                                   f"secret/continuous/{project}")).read()
            repo_pass2 = os.popen((f"vault read -field=repo_pass_2 "
                                   f"secret/continuous/{project}")).read()
            repo_pass2 = urllib.parse.quote_plus(repo_pass2)
            uri = f"{prot}://{repo_user2}:{repo_pass2}@{host_port}/{restpath}.git"
            clone = f"git clone -b {branch} --single-branch {uri} {target_repo}"
            update = f"cd {target_repo}; git pull origin {branch}"
        elif prot in ("http", "https"):
            uri = f"{prot}://{repo_user}:{repo_pass}@{host_port}/{restpath}.git"
            clone = f"git clone -b {branch} --single-branch {uri} {target_repo}"
            update = f"cd {target_repo}; git pull origin {branch}"
        else:
            if git_type == "ssh-codecommit":
                uri = f"ssh://{user}@{host_port}/{restpath}"
            else:
                uri = f"{user}@{host_port}/{restpath}"

            if once:
                once = False
                key = os.popen(f"vault read -field=repo_key secret/continuous/{project}").read()
                data = base64.b64decode(key)
                os.system(f"rm -rf ~/.ssh/{project}")
                with open(os.path.expanduser(f'~/.ssh/{project}'), "wb") as file:
                    file.write(data)
                os.system(f"chmod 0400 ~/.ssh/{project}")

            clone = (f"ssh-agent sh -c \""
                     f"ssh-keyscan {host} >> ~/.ssh/known_hosts;"
                     f"ssh-add ~/.ssh/{project};"
                     f"git clone -b {branch} --single-branch {uri} {target_repo}\"")
            update = (f"ssh-agent sh -c \""
                      f"ssh-keyscan {host} >> ~/.ssh/known_hosts;"
                      f"ssh-add ~/.ssh/{project};"
                      f"git pull origin {branch}\"")

        if not os.path.isdir(f"{target_repo}"):
            if not os.system(clone):
                nrepos += 1
            elif PORCELAIN:
                exit(1)
        else:
            os.chdir(target_repo)
            if not os.system(update):
                nrepos += 1
            elif PORCELAIN:
                exit(1)

    print(f"INFO|STATS|{subscription}|{nrepos}|")


def main():
    """Usual entry point.
    """

    branches = process_subscriptions()

    with open(f"{TARGET}/../branches.json", "w") as file:
        json.dump(branches, file, indent=2)


if __name__ == "__main__":
    main()
