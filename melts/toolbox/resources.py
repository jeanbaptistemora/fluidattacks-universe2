"""Main module to update resources"""


from alive_progress import (
    alive_bar,
    config_handler,
)
import base64
from contextlib import (
    contextmanager,
    suppress,
)
from datetime import (
    datetime,
)
import git
from git import (
    Repo,
)
from git.exc import (
    GitCommandError,
    GitError,
)
import json
from multiprocessing import (
    cpu_count,
)
from multiprocessing.pool import (
    ThreadPool,
)
import os
import re
from shlex import (
    quote as shq,
)
import shutil
import stat
import subprocess
from subprocess import (
    DEVNULL,
    PIPE,
    Popen,
)
import tempfile
from toolbox import (
    utils,
)
from toolbox.api import (
    integrates,
)
from toolbox.constants import (
    API_TOKEN,
)
from toolbox.logger import (
    LOGGER,
)
from typing import (
    Any,
    Dict,
    Iterator,
    List,
    Optional,
)
import urllib.parse

config_handler.set_global(length=25)


def format_repo_problem(
    nickname: str,
    branch: str,
    problem: str,
) -> Dict[str, str]:
    LOGGER.error("%s/%s failed", nickname, branch)
    LOGGER.error(problem)
    return {"repo": nickname, "problem": problem}


def format_problem_message(problem: str) -> str:
    fatal = re.search("(fatal:(.\n*)+)", problem)
    message = fatal.groups()[0] if fatal else problem
    if len(message) >= 400:
        return message[:399]
    return message


def manage_repo_diffs(repositories: List[Dict[str, str]]) -> None:
    repo_fusion = os.listdir(".")

    repo_nicknames = [repo["nickname"] for repo in repositories]

    repo_difference = set(repo_fusion).difference(set(repo_nicknames))

    # delete repositories of fusion that are not in the config
    for repo_dif in repo_difference:
        LOGGER.info("Deleting %s", repo_dif)
        shutil.rmtree(repo_dif)


def ls_remote(url: str) -> Dict[str, Any]:
    remote_refs = {}
    remote = git.cmd.Git()
    try:
        for ref in remote.ls_remote(url).split("\n"):
            hash_ref_list = ref.split("\t")
            with suppress(IndexError):
                remote_refs[hash_ref_list[1]] = hash_ref_list[0]
        return {"ok": remote_refs}
    except GitCommandError as exc:
        return {"error": {"message": exc.stderr, "status": exc.status}}


def cmd_execute(cmnd: List[str], folder: str = ".") -> List[str]:
    """Execute a cmd command in the folder"""
    env_vars: Dict[str, str] = {
        "GIT_SSL_NO_VERIFY": "1",
        "GIT_SSH_COMMAND": (
            "ssh -o "
            "UserKnownHostsFile=/dev/null -o "
            "StrictHostKeyChecking=no"
        ),
    }
    process = Popen(  # pylint: disable=consider-using-with
        cmnd,
        stdin=DEVNULL,
        stdout=PIPE,
        stderr=PIPE,
        cwd=folder,
        env={**os.environ.copy(), **env_vars},
    )
    return list(
        map(lambda x: x.decode("utf-8", "ignore"), process.communicate())
    )


def print_problems(
    problems: List[Dict[str, str]],
    branches: List[str],
) -> None:
    """print problems in the repos"""
    LOGGER.info(
        "Problems with the following repositories: [%i/%i]\n\n",
        len(problems),
        len(branches),
    )
    for problem in problems:
        LOGGER.info("%s\n", problem["repo"])
        LOGGER.info(problem["problem"])


def has_vpn(code: Dict[str, str], subs: str) -> None:
    """check if the group has a vpn"""
    does_have_vpn = code.get("vpn")
    if does_have_vpn:
        LOGGER.info("%s needs VPN. ", subs)
        LOGGER.info("Make sure to run your VPN software before cloning.\n")


@contextmanager
def setup_ssh_key() -> Iterator[str]:
    try:
        if credentials := utils.generic.get_sops_secret(
            "repo_key", "../config/secrets-prod.yaml", "continuous-admin"
        ):
            key = base64.b64decode(credentials).decode("utf-8")

            with tempfile.NamedTemporaryFile(delete=False) as keyfile:
                os.chmod(keyfile.name, stat.S_IREAD | stat.S_IWRITE)
                keyfile.write(key.encode())

            os.chmod(keyfile.name, stat.S_IREAD)

            yield keyfile.name
    finally:
        cmd_execute(
            [
                "ssh-agent",
                "sh",
                "-c",
                f"ssh-add -D; rm -f {shq(keyfile.name)}",
            ]
        )


def repo_url(baseurl: str) -> str:
    """return the repo url"""
    error = ""
    for user, passw in ["repo_user", "repo_pass"], [
        "repo_user_2",
        "repo_pass_2",
    ]:
        repo_user: Optional[str] = ""
        repo_pass: Optional[str] = ""
        with open("../config/secrets-prod.yaml", encoding="utf8") as secrets:
            if f"{user}:" in secrets.read():
                repo_user = utils.generic.get_sops_secret(
                    user,
                    "../config/secrets-prod.yaml",
                    "continuous-admin",
                )
                repo_pass = utils.generic.get_sops_secret(
                    passw,
                    "../config/secrets-prod.yaml",
                    "continuous-admin",
                )
                if repo_user and repo_pass:
                    repo_user = urllib.parse.quote_plus(repo_user)
                    repo_pass = urllib.parse.quote_plus(repo_pass)
                    uri = baseurl.replace("<user>", repo_user)
                    uri = uri.replace("<pass>", repo_pass)
                    # check if the user has permissions in the repo
                    remote = ls_remote(uri)
                    if remote.get("ok"):
                        return uri
                    error = remote["error"]["message"]

    return error


def _ssh_ls_remote(git_root: Dict[str, str]) -> Optional[str]:
    baseurl = git_root["url"]
    if "source.developers.google" not in baseurl:
        baseurl = baseurl.replace("ssh://", "")

    branch = urllib.parse.unquote(git_root["branch"])

    with setup_ssh_key() as keyfile:
        command_ls = [
            "ssh-agent",
            "sh",
            "-c",
            f"ssh-add {shq(keyfile)}; git ls-remote {shq(baseurl)} {branch}",
        ]
        cmd = cmd_execute(command_ls)
        if len(cmd[0]) >= 0:
            return cmd[0].split("\t")[0]
    return None


def _ssh_repo_cloning(
    group_name: str,
    git_root: Dict[str, str],
) -> Optional[Dict[str, str]]:
    """cloning or updated a repository ssh"""
    baseurl = git_root["url"]
    if "source.developers.google" not in baseurl:
        baseurl = baseurl.replace("ssh://", "")

    # handle urls special chars in branch names
    branch = urllib.parse.unquote(git_root["branch"])

    problem: Optional[Dict[str, Any]] = None

    nickname = git_root["nickname"]

    folder = nickname

    with setup_ssh_key() as keyfile:
        if os.path.isdir(folder):
            # Update already existing repo
            command = [
                "ssh-agent",
                "sh",
                "-c",
                "ssh-add "
                f"{shq(keyfile)} "
                "git "
                "pull "
                "origin "
                f"{shq(branch)}",
            ]

            cmd = cmd_execute(command, folder)
            if len(cmd[0]) == 0 and "fatal" in cmd[1]:
                problem = format_repo_problem(nickname, branch, cmd[1])
        else:
            # Clone repo:
            command = [
                "ssh-agent",
                "sh",
                "-c",
                "ssh-add "
                f"{shq(keyfile)}; "
                "git "
                "clone "
                "-b "
                f"{shq(branch)} "
                "--single-branch "
                f"{shq(baseurl)} "
                f"{shq(folder)}",
            ]

            cmd = cmd_execute(command)
            if len(cmd[0]) == 0 and "fatal" in cmd[1]:
                problem = format_repo_problem(nickname, branch, cmd[1])

    if problem:
        message = format_problem_message(problem["problem"])
        utils.integrates.update_root_cloning_status(
            group_name,
            git_root["id"],
            "FAILED",
            message,
        )
    return problem


def _http_ls_remote(_repo_url: str, git_root: Dict[str, Any]) -> Optional[str]:
    branch = git_root["branch"]
    command_ls = ["git", "ls-remote", shq(_repo_url), branch]
    cmd = cmd_execute(command_ls)
    if len(cmd[0]) >= 0:
        return cmd[0].split("\t")[0]
    return None


def get_head_commit(path_to_repo: str, branch: str) -> Optional[str]:
    try:
        return (
            git.Repo(path_to_repo, search_parent_directories=True)
            .heads[branch]
            .object.hexsha
        )
    except GitError:
        return None


def _http_repo_cloning(
    group_name: str,
    git_root: Dict[str, str],
) -> Optional[Dict[str, str]]:
    """cloning or updated a repository https"""
    # Needed to avoid SSL certificate problem
    os.environ["GIT_SSL_NO_VERIFY"] = "False"
    # script does not support vpns atm
    baseurl = git_root["url"]
    nickname = git_root["nickname"]

    branch = git_root["branch"]

    problem: Optional[Dict[str, Any]] = None

    # check if user has access to current repository
    baseurl = repo_url(git_root["url"])
    if "fatal:" in baseurl:
        problem = format_repo_problem(nickname, branch, baseurl)

    branch = git_root["branch"]
    folder = nickname

    if os.path.isdir(folder):
        # Update already existing repo
        try:
            git_repo = git.Repo(folder, search_parent_directories=True)
            git_repo.remotes.origin.pull()
        except GitError as exc:
            problem = format_repo_problem(nickname, branch, exc.stderr)
    # validate if there is no problem with the baseurl
    elif not problem:
        try:
            Repo.clone_from(
                baseurl,
                folder,
                multi_options=[f"-b {branch}", "--single-branch"],
            )
        except GitError as exc:
            problem = format_repo_problem(nickname, branch, exc.stderr)

    if problem:
        message = format_problem_message(problem["problem"])
        utils.integrates.update_root_cloning_status(
            group_name,
            git_root["id"],
            "FAILED",
            message,
        )
    return problem


def action(
    git_root: Dict[str, Any],
    group_name: str,
    progress_bar: Any,
    force: bool = False,
) -> Optional[Dict[str, Any]]:
    repo_type = "ssh" if git_root["url"].startswith("ssh") else "https"
    problem: Optional[Dict[str, str]] = None

    # check if current repo is active
    if git_root.get("state", "") != "ACTIVE":
        return None

    current_commit = git_root["cloningStatus"]["commit"]
    if repo_type == "ssh":
        if not force and _ssh_ls_remote(git_root) == current_commit:
            LOGGER.info(
                "the las version of %s has already in s3",
                git_root["nickname"],
            )
        else:
            problem = _ssh_repo_cloning(group_name, git_root)
    else:
        baseurl = repo_url(git_root["url"])
        if "fatal" not in baseurl:
            if (
                not force
                and _http_ls_remote(baseurl, git_root) == current_commit
            ):
                LOGGER.info(
                    "the las version of %s has already in s3",
                    git_root["nickname"],
                )
            else:
                problem = _http_repo_cloning(group_name, git_root)
        else:
            problem = format_repo_problem(
                git_root["nickname"], git_root["branch"], baseurl
            )
    if problem:
        return problem
    progress_bar()
    return None


def repo_cloning(subs: str, repo_name: str, force: bool = False) -> bool:
    """cloning or updated a repository"""

    success = True
    problems: list = []
    original_dir: str = os.getcwd()
    destination_folder = f"groups/{subs}/fusion"
    repositories: List[Dict[str, str]] = []

    os.makedirs(destination_folder, exist_ok=True)
    os.chdir(destination_folder)

    repo_request = integrates.Queries.git_roots(
        API_TOKEN,
        subs,
    )
    if not repo_request.ok:
        LOGGER.error(repo_request.errors)
        return False

    if repo_name == "*":
        repositories = list(
            root
            for root in repo_request.data["group"]["roots"]
            if root.get("state", "") == "ACTIVE"
        )
        manage_repo_diffs(repositories)
    else:
        repositories = list(
            root
            for root in repo_request.data["group"]["roots"]
            if root.get("state", "") == "ACTIVE"
            and root["nickname"] == repo_name
        )
    if not repositories:
        LOGGER.error("There is no %s repository in %s", repo_name, subs)
        return False

    utils.generic.aws_login("continuous-admin")

    with alive_bar(len(repositories), enrich_print=False) as progress_bar:
        with ThreadPool(processes=cpu_count()) as worker:
            _problems = worker.map(
                lambda x: action(x, subs, progress_bar, force=force),
                repositories,
            )
            problems.extend((problem for problem in _problems if problem))

    if problems:
        LOGGER.error("Some problems occured: \n")

        for problem in problems:
            print(f'Repository: {problem["repo"]}')
            print(f'Description: {problem["problem"]}')
        success = False
    os.chdir(original_dir)

    return success


def edit_secrets(group: str, suffix: str, profile: str) -> bool:
    status: bool = True
    secrets_file: str = f"groups/{group}/config/secrets-{suffix}.yaml"
    if not os.path.exists(secrets_file):
        LOGGER.error("secrets-%s.yaml does not exist in %s", suffix, group)
        status = False
    else:
        utils.generic.aws_login(profile)
        subprocess.call(
            f"sops --aws-profile {profile} {secrets_file}", shell=True
        )
    return status


def read_secrets(group: str, suffix: str, profile: str) -> bool:
    status: bool = True
    secrets_file: str = f"groups/{group}/config/secrets-{suffix}.yaml"
    if not os.path.exists(secrets_file):
        LOGGER.error("secrets-%s.yaml does not exist in %s", suffix, group)
        status = False
    else:
        utils.generic.aws_login(profile)
        subprocess.call(
            f"sops --aws-profile {profile} --decrypt {secrets_file}",
            shell=True,
        )
    return status


def get_fingerprint(subs: str) -> bool:
    """Get the hash and date of every folder in fusion"""
    results = []
    max_hash = ""
    max_date = datetime.fromtimestamp(0)
    path = f"groups/{subs}"
    if not os.path.exists(path):
        LOGGER.error("There is no project with the name: %s", subs)
        LOGGER.info("Please run fingerprint inside a project or use subs")
        return False
    path += "/fusion"
    if not os.path.exists(path):
        LOGGER.error("There is no a fusion folder in the group")
        return False
    listpath = os.listdir(f"groups/{subs}/fusion")

    for repo in (r for r in listpath if os.path.isdir(f"{path}/{r}")):
        # com -> commom command
        git_repo = git.Repo(f"{path}/{repo}", search_parent_directories=True)
        hashr = git_repo.head.commit.hexsha
        date = datetime.fromtimestamp(git_repo.head.commit.authored_date)
        max_date = max_date or date
        if date >= max_date:
            max_date = date
            max_hash = hashr
        results.append((repo, hashr, date.isoformat()))
    if results == []:
        LOGGER.error("There is not any folder in fusion - Subs: %s", subs)
        return False
    output_bar = "-" * 84
    output_fmt = "{:^59} {:^7} {:^16}"
    LOGGER.info(output_bar)
    LOGGER.info(output_fmt.format("Repository", "Hash", "Date"))
    LOGGER.info(output_bar)
    for params in sorted(results):
        LOGGER.info(output_fmt.format(*params))
    LOGGER.info(output_bar)
    LOGGER.info(
        output_fmt.format(len(results), max_hash, max_date.isoformat())
    )
    return True


def print_inactive_missing_repos(
    group: str,
    inactive_repos: List[str],
    missing_repos: List[str],
) -> None:
    print(
        json.dumps(
            {
                "stream": "repositories",
                "record": {
                    "subscription": group,
                    "inactive": inactive_repos,
                    "missing": missing_repos,
                },
            }
        )
    )
