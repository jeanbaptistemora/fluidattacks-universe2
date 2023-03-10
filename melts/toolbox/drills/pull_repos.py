from alive_progress import (
    alive_bar,
)
from concurrent.futures import (
    ThreadPoolExecutor,
)
from contextlib import (
    suppress,
)
from git.cmd import (
    Git,
)
from git.exc import (
    GitError,
)
from git.repo import (
    Repo,
)
import os
from pathlib import (
    Path,
)
import pathspec
from pathspec.patterns.gitwildmatch import (
    GitWildMatchPattern,
)
import shutil
import tarfile
from toolbox import (
    utils,
)
from toolbox.drills import (
    generic as drills_generic,
)
from toolbox.logger import (
    LOGGER,
)
from toolbox.resources import (
    get_head_commit,
)
from toolbox.utils.function import (
    shield,
)
from toolbox.utils.generic import (
    rfc3339_str_to_date_obj,
)
from toolbox.utils.integrates import (
    get_filter_rules,
    get_git_root_download_url,
    get_git_roots,
)
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Set,
)
import urllib.parse
from urllib.request import (
    urlretrieve,
)


def notify_out_of_scope(
    nickname: str,
    gitignore: str,
) -> bool:
    LOGGER.info("Please remember the scope for : %s", nickname)
    for line in gitignore:
        LOGGER.info("    - %s", line)

    LOGGER.info("\n")

    return True


def get_repo_from_url(url: str) -> str:
    # Parse the URL
    url_obj = urllib.parse.urlparse(url)

    # Unquote the path portion, it may contain URL encoded characters
    url_path = urllib.parse.unquote_plus(url_obj.path)

    # Return the last component of the path
    repo = os.path.basename(url_path)

    # It may end with .git
    if repo.endswith(".git"):
        repo = repo[0:-4]

    return repo


def match_file(patterns: List[GitWildMatchPattern], file: str) -> bool:
    matches = []
    for pattern in patterns:
        if pattern.include is not None:
            if file in pattern.match((file,)):
                matches.append(pattern.include)
            elif not pattern.include:
                matches.append(True)

    return all(matches) if matches else False


def delete_out_of_scope_files(group: str) -> bool:
    expected_repositories: Set[str] = set()
    path_to_fusion: str = os.path.join("groups", group, "fusion")
    all_roots = get_filter_rules(group)
    active_roots_nicknames = [
        root["nickname"] for root in all_roots if root["state"] == "ACTIVE"
    ]
    all_roots = sorted(
        all_roots,
        key=lambda x: 1 if x["state"] == "ACTIVE" else 0,
        reverse=True,
    )
    processed_nicknames = []
    for root in all_roots:
        # Get the expected repo name from the URL
        nickname = root["nickname"]
        if nickname in processed_nicknames:
            continue
        expected_repositories.add(nickname)

        spec_ignore = pathspec.PathSpec.from_lines(
            "gitwildmatch", root["gitignore"]
        )

        # Display to the user the Scope
        notify_out_of_scope(
            nickname,
            root["gitignore"],
        )

        # Compute what files should be deleted according to the scope rules
        path_to_repo = os.path.join("groups", group, "fusion", nickname)
        with suppress(FileNotFoundError):
            if (
                root["state"] == "INACTIVE"
                and root["nickname"] not in active_roots_nicknames
            ) or not os.listdir(path_to_repo):
                shutil.rmtree(path_to_repo)
                continue

        for path in spec_ignore.match_files(
            (
                path
                for path in utils.file.iter_rel_paths(path_to_repo)
                if not path.startswith(".git/")
            )
        ):
            path_to_delete = os.path.join(path_to_fusion, nickname, path)
            if os.path.isfile(path_to_delete):
                with suppress(FileNotFoundError):
                    os.unlink(path_to_delete)
            elif os.path.isdir(path_to_delete):
                shutil.rmtree(path_to_delete, ignore_errors=True)
        processed_nicknames.append(root["nickname"])

    # Delete cloned repositories that are not expected to be cloned
    cloned_repositories: Set[str] = set()
    with suppress(FileNotFoundError):
        os.makedirs(path_to_fusion, exist_ok=True)
        cloned_repositories = set(os.listdir(path_to_fusion))
    bad_repositories: Set[str] = cloned_repositories - expected_repositories

    if bad_repositories:
        LOGGER.error("We cloned repositories that are not on Integrates")
        LOGGER.error("This is very likely a bug, please notify the manager")
        for repository in bad_repositories:
            LOGGER.warning("  Deleting, out of scope: %s", repository)
            path_to_delete = os.path.join(path_to_fusion, repository)
            if os.path.isfile(path_to_delete):
                os.remove(path_to_delete)
            else:
                shutil.rmtree(path_to_delete)

    return True


def _reset_repo(repo_path: str) -> bool:
    try:
        Git().execute(
            [
                "git",
                "config",
                "--global",
                "--add",
                "safe.directory",
                str(repo_path),
            ]
        )
    except GitError as exc:
        LOGGER.error("Failed to add safe directory:")
        LOGGER.info("Repository: %s", repo_path)
        LOGGER.info(exc)
        LOGGER.info("\n")

    try:
        repo = Repo(repo_path)
        repo.git.reset("--hard", "HEAD")
    except GitError as exc:
        LOGGER.error("Expand repositories has failed:")
        LOGGER.info("Repository: %s", repo_path)
        LOGGER.info(exc)
        LOGGER.info("\n")
        return False
    return True


def download_repo_from_s3(
    group_name: str,
    nickname: str,
    root: Dict[str, Any],
    progress_bar: Optional[Any] = None,
) -> bool:
    repo_path = Path("groups") / group_name / Path("fusion") / nickname

    with suppress(GitError):
        if (
            (commit := root.get("cloningStatus", {}).get("commit"))
            and (branch := root.get("branch"))
            and (local_commit := get_head_commit(repo_path, branch))
            and (local_commit == commit)
        ):
            LOGGER.info("%s  repository already exists", nickname)
            if progress_bar:
                progress_bar()
            return True

    os.makedirs(repo_path.parent, exist_ok=True)
    file_path = repo_path.with_suffix(".tar.gz")

    urlretrieve(root["downloadUrl"], file_path)

    if not file_path.exists():
        return False

    if progress_bar:
        progress_bar()

    try:
        shutil.rmtree(repo_path, ignore_errors=True)
        with tarfile.open(file_path, "r:gz") as tar_handler:
            tar_handler.extractall(file_path.parent, numeric_owner=True)
    except PermissionError:
        LOGGER.error("filed to unzip %s", nickname)

    os.remove(file_path)

    return _reset_repo(str(repo_path.resolve()))


@shield(retries=1)
def main(subs: str, repository_name: Optional[str] = None) -> bool:
    """
    Clone all repos for a group

    param: subs: group to work with
    """
    passed: bool = True
    roots = get_git_roots(group=subs)
    if roots is None:
        return False

    git_roots_dict = {
        root["id"]: root
        for root in roots
        if root.get("state") == "ACTIVE"
        and (
            root["nickname"] == repository_name
            if repository_name is not None
            else True
        )
    }
    if not git_roots_dict:
        LOGGER.info("Git roots not found")
        return True

    with ThreadPoolExecutor() as executor:
        for root_id, download_url in executor.map(
            get_git_root_download_url,
            [subs for _ in range(len(git_roots_dict))],
            git_roots_dict.keys(),
        ):
            git_roots_dict[root_id]["downloadUrl"] = download_url

    zip_roots = [
        root
        for root in git_roots_dict.values()
        if root.get("downloadUrl") is not None
    ]

    with alive_bar(len(zip_roots), enrich_print=False) as progress_bar:
        with ThreadPoolExecutor() as executor:
            LOGGER.info("Downloading .tar files")
            passed = (
                passed
                and all(
                    executor.map(
                        download_repo_from_s3,
                        [subs for _ in range(len(zip_roots))],
                        [root["nickname"] for root in zip_roots],
                        zip_roots,
                        [progress_bar for _ in range(len(zip_roots))],
                    )
                )
                if zip_roots
                else True
            )

    for root in git_roots_dict.values():
        if date := root.get("lastCloningStatusUpdate"):
            LOGGER.info(
                "Data for %s was uploaded to S3 %i days ago",
                root["nickname"],
                drills_generic.calculate_days_ago(
                    rfc3339_str_to_date_obj(date)
                ),
            )
        else:
            LOGGER.info(
                "root %s does not have repos uploaded to s3", root["nickname"]
            )
    passed = delete_out_of_scope_files(subs) and passed

    return passed
