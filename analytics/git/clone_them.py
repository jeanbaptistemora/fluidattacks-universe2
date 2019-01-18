""" clone or update repos in continuous """

import os
import re
import json
import base64
import urllib.parse

import yaml # pylint: disable=import-error

SOURCE = "/git/fluidsignal/continuous"
TARGET = "/git"

USEAUTH2 = ("Repo_Alis_Front", )
NESTED = ("banistmo",)

# repos with problems
IGNORE = (
    "bowky",        # fails
    "caphec",       # fails
    "aldak",        # no link to clone
    "valvanera",    # no authorization
    "villasilvia",  # unable to resolve host (or host down)
    "yarumossac",   # unable to resolve host
    "stebbins",     # unable to resolve host
    "vilachuaga",   # unable to resolve host
    "volantin",     # unable to resolve host
    "paitu"         # unable to resolve host
)

SUBSCRIPTIONS = []
for subscription in os.listdir(f"{SOURCE}/subscriptions"):
    if subscription in IGNORE:
        continue
    for multiple in NESTED:
        if subscription == multiple:
            for sub in os.listdir(f"{SOURCE}/subscriptions/{subscription}"):
                if sub in ("asserts",):
                    continue
                SUBSCRIPTIONS.append(f"{SOURCE}/subscriptions/{subscription}/{sub}")
            break
    else:
        if not subscription in ("integrates",):
            SUBSCRIPTIONS.append(f"{SOURCE}/subscriptions/{subscription}")

BRANCHES = {}
for subscription in SUBSCRIPTIONS:
    print(f"===={subscription}")

    os.chdir(subscription)

    repo_name = subscription.split(os.sep)[-1]
    if subscription.split(os.sep)[-2] == "banistmo":
        project = f"banistmo-{repo_name}"
    else:
        project = repo_name

    extension = ".git"
    with open(f"{subscription}/config.yml", "r") as config_file:
        config = yaml.load(config_file).get("code")

    base_url = str(config.get("url")[0])
    list_of_repos = config.get("branches")
    git_type = config.get("git-type", "http://")

    protocol = base_url[:base_url.index("://") + 3]
    host = base_url[base_url.rfind("@"):]
    git_user = base_url[base_url.index("//") + 2 :base_url.index("@")]

    repo_user = ""
    pass_url = ""
    if protocol in ("https://", "http://"):
        repo_user = os.popen((f"vault read -field=repo_user "
                              f"secret/continuous/{project}")).read()
        repo_pass = os.popen((f"vault read -field=repo_pass "
                              f"secret/continuous/{project}")).read()
        pass_url = urllib.parse.quote_plus(repo_pass)

    BRANCHES[project] = {}

    once = True
    for repo in list_of_repos:
        repository = repo.rsplit("/", 1)[0].replace("/", "-")
        branch = repo.rsplit("/", 1)[1]

        BRANCHES[project][repository] = branch

        target_repo = f"{TARGET}/{project}/{repository}"

        if repository in USEAUTH2:
            repo_user_2 = os.popen((f"vault read -field=repo_user_2 "
                                    f"secret/continuous/{project}")).read()
            repo_pass_2 = os.popen((f"vault read -field=repo_pass_2 "
                                    f"secret/continuous/{project}")).read()
            pass_url_2 = urllib.parse.quote_plus(repo_pass_2)
            uri = f"{protocol}{repo_user_2}:{pass_url_2}{host}/{repository}{extension}"
            clone = f"git clone -b {branch} --single-branch {uri} {target_repo}"
            update = f"cd {target_repo}; git pull origin {branch}"
        elif protocol in ("http://", "https://"):
            uri = f"{protocol}{repo_user}:{pass_url}{host}/{repository}{extension}"
            clone = f"git clone -b {branch} --single-branch {uri} {target_repo}"
            update = f"cd {target_repo}; git pull origin {branch}"
        else:
            if git_type == "ssh-codecommit":
                uri = f"{protocol}{git_user}{host}{repository}"
            else:
                uri = f"{git_user}{host}{repository}"
            if "fluid-attacks" not in base_url:
                if once:
                    key = os.popen(f"vault read -field=repo_key secret/continuous/{project}").read()
                    data = base64.b64decode(key)
                    os.system(f"rm -rf ~/.ssh/{project}")
                    with open(os.path.expanduser(f'~/.ssh/{project}'), "wb") as file:
                        file.write(data)
                    os.system(f"chmod 0400 ~/.ssh/{project}")
                    once = False

                # love you very much regexp
                real_host = re.sub(r".*@(.*?)[:/].*", r"\g<1>", host)
                clone = (f"ssh-agent sh -c \""
                         f"ssh-keyscan {real_host} >> ~/.ssh/known_hosts;"
                         f"ssh-add ~/.ssh/{project};"
                         f"git clone -b {branch} --single-branch {uri} {target_repo}\"")
                update = (f"ssh-agent sh -c \""
                          f"ssh-keyscan {real_host} >> ~/.ssh/known_hosts;"
                          f"ssh-add ~/.ssh/{project};"
                          f"git pull origin {branch}\"")
            else:
                clone = f"git clone -b {branch} --single-branch {uri} {target_repo}"
                update = f"git pull origin {branch}"

        if not os.path.isdir(f"{target_repo}"):
            os.makedirs(f"{target_repo}")
            os.system(clone)
        else:
            os.chdir(target_repo)
            os.system(update)

with open(f"{TARGET}/../branches.json", "w") as file:
    json.dump(BRANCHES, file, indent=2)
