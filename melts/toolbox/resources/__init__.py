"""Main module to update resources"""


from alive_progress import (
    alive_bar,
    config_handler,
)
import base64
from contextlib import (
    suppress,
)
from datetime import (
    datetime,
)
from fa_purity import (
    FrozenList,
    Maybe,
    Result,
    ResultE,
)
from git.cmd import (
    Git,
)
from git.exc import (
    GitCommandError,
    GitError,
)
from git.repo import (
    Repo,
)
import json
from multiprocessing import (
    cpu_count,
)
from multiprocessing.pool import (
    ThreadPool,
)
import os
from pathlib import (
    Path,
)
import re
from shlex import (
    quote as shq,
)
import shutil
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
from toolbox.logger import (
    LOGGER,
)
from toolbox.resources.core import (
    FormatRepoProblem,
    GitRoot,
    LazyCloningResult,
    RepoType,
    RootState,
)
from toolbox.utils import (
    last_sync,
)
from toolbox.utils.integrates import (
    get_git_root_credentials,
    get_git_roots,
)
from typing import (
    Any,
    Dict,
    List,
    Optional,
)
from urllib3.exceptions import (
    LocationParseError,
)
from urllib3.util.url import (
    parse_url,
)
import urllib.parse
import uuid

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
    remote = Git()
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
            "ssh"
            " -o UserKnownHostsFile=/dev/null"
            " -o StrictHostKeyChecking=no"
            " -o IdentitiesOnly=yes"
            " -o HostkeyAlgorithms=+ssh-rsa"
            " -o PubkeyAcceptedAlgorithms=+ssh-rsa"
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


def repo_url(group_name: str, root_id: str, baseurl: str) -> str:
    """return the repo url"""
    error = ""
    repo_user: Optional[str] = None
    repo_pass: Optional[str] = None
    repo_token: Optional[str] = None

    parsed_url = parse_url(baseurl)
    if credentials := get_git_root_credentials(group_name, root_id):
        repo_user = credentials.get("user")
        repo_pass = credentials.get("password")
        repo_token = credentials.get("token")
    if repo_token:
        repo_token = urllib.parse.quote_plus(repo_token)
        url = str(parsed_url._replace(auth=f"{repo_token}"))
    elif repo_user and repo_pass:
        repo_user = urllib.parse.quote_plus(repo_user)
        repo_pass = urllib.parse.quote_plus(repo_pass)
        url = str(parsed_url._replace(auth=f"{repo_user}:{repo_pass}"))
    else:
        return "fatal: missing credentials"

    # check if the user has permissions in the repo
    remote = ls_remote(url)
    if remote.get("ok"):
        return url
    error = remote["error"]["message"]

    return error


def _ssh_ls_remote(group_name: str, root: GitRoot) -> Optional[str]:
    repo_url_ = root.url
    if "source.developers.google" not in repo_url_:
        repo_url_ = repo_url_.replace("ssh://", "")

    branch = urllib.parse.unquote(root.branch)

    try:
        parsed_url = urllib.parse.urlparse(repo_url_)
    except LocationParseError:
        return None
    raw_root_url = repo_url_
    if "source.developers.google" not in raw_root_url:
        raw_root_url = repo_url_.replace(f"{parsed_url.scheme}://", "")

    with tempfile.TemporaryDirectory() as temp_dir:
        ssh_file_name: str = os.path.join(temp_dir, str(uuid.uuid4()))
        with open(
            os.open(ssh_file_name, os.O_CREAT | os.O_WRONLY, 0o400),
            "w",
            encoding="utf-8",
        ) as ssh_file:
            if credential_key := get_git_root_credentials(
                group_name, root.root_id
            ):
                ssh_file.write(
                    base64.b64decode(credential_key.get("key") or "").decode()
                )
        with subprocess.Popen(
            args=("git", "ls-remote", raw_root_url, branch),
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
            env={
                **os.environ.copy(),
                "GIT_SSH_COMMAND": (
                    f"ssh -i {ssh_file_name}"
                    " -o UserKnownHostsFile=/dev/null"
                    " -o StrictHostKeyChecking=no"
                    " -o IdentitiesOnly=yes"
                    " -o HostkeyAlgorithms=+ssh-rsa"
                    " -o PubkeyAcceptedAlgorithms=+ssh-rsa"
                ),
            },
        ) as proc:
            stdout, stderr = proc.communicate()

            if stderr and proc.returncode != 0:
                LOGGER.error(
                    "failed git ls-remote",
                    extra=dict(
                        extra={
                            "error": stderr.decode(),
                            "repo_url": repo_url_,
                        }
                    ),
                )

            os.remove(ssh_file_name)

            if proc.returncode != 0:
                return None

            return stdout.decode().split("\t", maxsplit=1)[0]


def _ssh_repo_cloning(
    group_name: str,
    root: GitRoot,
) -> ResultE[None]:
    raw_root_url = root.url
    branch = urllib.parse.unquote(root.branch)
    nickname = root.nickname

    folder = nickname
    problem: Optional[FormatRepoProblem] = None
    if "source.developers.google" not in raw_root_url:
        raw_root_url = raw_root_url.replace(
            f"{urllib.parse.urlparse(raw_root_url).scheme}://", ""
        )
    with tempfile.TemporaryDirectory() as temp_dir:
        ssh_file_name: str = os.path.join(temp_dir, str(uuid.uuid4()))
        with open(
            os.open(ssh_file_name, os.O_CREAT | os.O_WRONLY, 0o400),
            "w",
            encoding="utf-8",
        ) as ssh_file:
            if credential_key := get_git_root_credentials(
                group_name, root.root_id
            ):
                ssh_file.write(
                    base64.b64decode(credential_key.get("key") or "").decode()
                )
        with subprocess.Popen(
            args=(
                "git",
                *(
                    ("pull", "origin", branch)
                    if os.path.isdir(folder)
                    else (
                        "clone",
                        "--single-branch",
                        "--branch",
                        branch,
                        raw_root_url,
                    )
                ),
                *(() if os.path.isdir(folder) else (folder,)),
            ),
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
            env={
                **os.environ.copy(),
                "GIT_SSH_COMMAND": (
                    f"ssh -i {ssh_file_name}"
                    " -o UserKnownHostsFile=/dev/null"
                    " -o StrictHostKeyChecking=no"
                    " -o IdentitiesOnly=yes"
                    " -o HostkeyAlgorithms=+ssh-rsa"
                    " -o PubkeyAcceptedAlgorithms=+ssh-rsa"
                ),
            },
            cwd=(os.path.abspath(folder) if os.path.isdir(folder) else None),
        ) as proc:
            _, stderr = proc.communicate()

            os.remove(ssh_file_name)
            if proc.returncode != 0:
                problem = FormatRepoProblem(nickname, branch, stderr.decode())
                problem.log(LOGGER)

            if problem:
                message = format_problem_message(problem.raw()["problem"])
                utils.integrates.update_root_cloning_status(
                    group_name,
                    root.root_id,
                    "FAILED",
                    message,
                )
    return Maybe.from_optional(problem).to_result().swap()  # type: ignore


def _http_ls_remote(
    group_name: str, root: GitRoot
) -> Result[Optional[str], FormatRepoProblem]:
    baseurl = repo_url(group_name, root.root_id, root.url)
    if "fatal" not in baseurl:
        command_ls = ["git", "ls-remote", shq(baseurl), root.branch]
        cmd = cmd_execute(command_ls)
        if len(cmd[0]) > 0:
            return Result.success(cmd[0].split("\t")[0])
        return Result.success(None)
    problem = FormatRepoProblem(root.nickname, root.branch, baseurl)
    return Result.failure(problem)


def get_head_commit(path_to_repo: Path, branch: str) -> Optional[str]:
    try:
        return (
            Repo(path_to_repo.resolve(), search_parent_directories=True)
            .heads[branch]
            .object.hexsha
        )
    except GitError:
        return None


def _http_repo_cloning(
    group_name: str,
    root: GitRoot,
) -> Result[None, FormatRepoProblem]:
    """cloning or updated a repository https"""
    # Needed to avoid SSL certificate problem
    os.environ["GIT_SSL_NO_VERIFY"] = "False"
    # script does not support vpns atm
    baseurl = root.url
    nickname = root.nickname

    branch = root.branch

    problem: Optional[FormatRepoProblem] = None
    # check if user has access to current repository
    baseurl = repo_url(group_name, root.root_id, root.url)

    if "fatal:" in baseurl:
        problem = FormatRepoProblem(nickname, branch, baseurl)
        problem.log(LOGGER)

    branch = root.branch
    folder = nickname

    if os.path.isdir(folder):
        # Update already existing repo
        try:
            git_repo = Repo(folder, search_parent_directories=True)
            git_repo.remotes.origin.pull()
        except GitError as exc:
            problem = FormatRepoProblem(nickname, branch, str(exc))
            problem.log(LOGGER)
    # validate if there is no problem with the baseurl
    elif not problem:
        try:
            Repo.clone_from(
                baseurl,
                folder,
                multi_options=[f"-b {branch}", "--single-branch"],
            )
        except GitError as exc:
            problem = FormatRepoProblem(nickname, branch, str(exc))
            problem.log(LOGGER)

    if problem:
        message = format_problem_message(problem.raw()["problem"])
        utils.integrates.update_root_cloning_status(
            group_name,
            root.root_id,
            "FAILED",
            message,
        )
    return Maybe.from_optional(problem).to_result().swap()


def already_in_s3(
    group_name: str,
    root: GitRoot,
) -> Result[bool, FormatRepoProblem]:
    if root.repo_type is RepoType.SSH:
        return Result.success(
            _ssh_ls_remote(group_name, root) == root.head_commit
        )
    return _http_ls_remote(group_name, root).map(
        lambda c: c == root.head_commit
    )


def _clone_repo(
    group_name: str, root: GitRoot
) -> Result[None, FormatRepoProblem]:
    return (
        _ssh_repo_cloning(group_name, root)  # type: ignore
        if root.repo_type is RepoType.SSH
        else _http_repo_cloning(group_name, root)
    )


def _lazy_cloning(
    git_root: Dict[str, Any],
    group_name: str,
    progress_bar: Any,
    force: bool = False,
) -> Result[LazyCloningResult, FormatRepoProblem]:
    root = GitRoot.new(git_root)
    # check if current repo is active
    if root.state is not RootState.ACTIVE:
        return Result.success(LazyCloningResult.SKIPPED)

    def _notify() -> ResultE[LazyCloningResult]:
        LOGGER.info(
            "the last version of %s has already in s3",
            root.nickname,
        )
        return Result.success(LazyCloningResult.CACHED)

    problem = already_in_s3(group_name, root).bind(  # type: ignore
        lambda b: _clone_repo(group_name, root).map(  # type: ignore
            lambda _: LazyCloningResult.UPDATED
        )
        if (not b) or force
        else _notify()
    )
    progress_bar()
    return problem


def _report_success(
    group: str,
    results: FrozenList[Result[LazyCloningResult, FormatRepoProblem]],
) -> None:
    if all(
        map(
            lambda r: r.map(
                lambda v: v
                in (LazyCloningResult.SKIPPED, LazyCloningResult.CACHED)
            ).value_or(False),
            results,
        )
    ):
        last_sync.update_last_sync_date("last_sync_date", group)
        LOGGER.info("Last sync date of %s updated!", group)


def repo_cloning(subs: str, repo_name: str, force: bool = False) -> bool:
    """cloning or updated a repository"""

    success = True
    problems: list = []
    original_dir: str = os.getcwd()
    destination_folder = f"groups/{subs}/fusion"
    repositories: List[Dict[str, str]] = []

    os.makedirs(destination_folder, exist_ok=True)
    os.chdir(destination_folder)

    roots = get_git_roots(subs) or []

    if repo_name == "*":
        repositories = list(
            root for root in roots if root.get("state", "") == "ACTIVE"
        )
        manage_repo_diffs(repositories)
    else:
        repositories = list(
            root
            for root in roots
            if root.get("state", "") == "ACTIVE"
            and root["nickname"] == repo_name
        )
    if not repositories:
        LOGGER.error("There is no %s repository in %s", repo_name, subs)
        return False

    with alive_bar(len(repositories), enrich_print=False) as progress_bar:
        with ThreadPool(processes=cpu_count()) as worker:
            results = tuple(
                worker.map(
                    lambda x: _lazy_cloning(
                        x, subs, progress_bar, force=force
                    ),
                    repositories,
                )
            )
            problems.extend(
                (
                    problem.raw()
                    for problem in map(lambda r: r.to_union(), results)
                    if isinstance(problem, FormatRepoProblem)
                )
            )

    if problems:
        LOGGER.error("Some problems occured: \n")

        for problem in problems:
            print(f'Repository: {problem["repo"]}')
            print(f'Description: {problem["problem"]}')
        success = False
    os.chdir(original_dir)

    return success


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
        git_repo = Repo(f"{path}/{repo}", search_parent_directories=True)
        hashr = git_repo.head.commit.hexsha
        date = datetime.fromtimestamp(git_repo.head.commit.authored_date)
        max_date = max_date or date
        if date >= max_date:
            max_date = date
            max_hash = hashr
        results.append((repo, hashr, date.isoformat()))
    if not results:
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
