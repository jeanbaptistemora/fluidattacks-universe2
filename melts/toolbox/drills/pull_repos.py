from alive_progress import (
    alive_bar,
)
from concurrent.futures import (
    ThreadPoolExecutor,
)
from contextlib import (
    suppress,
)
from git import (
    Repo,
)
from git.exc import (
    GitError,
)
import os
import pathspec
from pathspec.patterns.gitwildmatch import (
    GitWildMatchPattern,
)
import shutil
import subprocess
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

    for root in get_filter_rules(group):
        # Get the expected repo name from the URL
        nickname = root["nickname"]
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
            if root["state"] == "INACTIVE" or not os.listdir(path_to_repo):
                shutil.rmtree(path_to_repo)
                continue

        for path in (
            path
            for path in utils.file.iter_rel_paths(path_to_repo)
            if not path.startswith(".git/")
        ):
            if match_file(spec_ignore.patterns, path):
                path_to_delete = os.path.join(path_to_fusion, nickname, path)
                if os.path.isfile(path_to_delete):
                    os.unlink(path_to_delete)
                elif os.path.isdir(path_to_delete):
                    shutil.rmtree(path_to_delete)

    # Delete cloned repositories that are not expected to be cloned
    cloned_repositories: Set[str] = set(os.listdir(path_to_fusion))
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


def download_repo_from_s3(
    group_name: str,
    nickname: str,
    root: Dict[str, Any],
    progress_bar: Optional[Any] = None,
) -> bool:
    repo_path = f"groups/{group_name}/fusion/{nickname}"

    with suppress(GitError):
        if (
            (commit := root.get("cloningStatus", {}).get("commit"))
            and (branch := root.get("branch"))
            and (local_commit := get_head_commit(repo_path, branch))
        ):
            if local_commit == commit:
                LOGGER.info("%s  repository already exists", nickname)
                if progress_bar:
                    progress_bar()
                return True

    os.makedirs(f"groups/{group_name}/fusion/", exist_ok=True)
    file_path = f"groups/{group_name}/fusion/{nickname}.tar.gz"

    urlretrieve(root["downloadUrl"], file_path)

    if not os.path.exists(file_path):
        return False

    if progress_bar:
        progress_bar()

    try:
        shutil.rmtree(
            f"groups/{group_name}/fusion/{nickname}", ignore_errors=True
        )
        with tarfile.open(file_path, "r:gz") as tar_handler:
            tar_handler.extractall(
                f"groups/{group_name}/fusion/", numeric_owner=True
            )
    except PermissionError:
        LOGGER.error("filed to unzip %s", nickname)

    os.remove(file_path)

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


def pull_repos_s3_to_fusion(
    subs: str,
    repository_name: str,
    progress_bar: Optional[Any] = None,
) -> bool:
    """
    Download repos from s3 to a provided path

    param: subs: group to work with
    param: local_path: Path to store downloads
    """

    if repository_name == "*":
        raise Exception("A valid repository name is required")

    bucket = f"s3://continuous-repositories/{subs}/{repository_name}/"
    local_path = f"groups/{subs}/fusion/{repository_name}/"

    os.makedirs(local_path, exist_ok=True)

    aws_sync_command: List[str] = [
        "aws",
        "s3",
        "sync",
        "--delete",
        "--sse",
        "AES256",
        "--exact-timestamps",
        bucket,
        local_path,
    ]

    LOGGER.info("Downloading %s from %s to %s", subs, bucket, local_path)

    # Passing None to stdout and stderr shows the s3 progress
    # We want the CI to be as quiet as possible to have clean logs
    kwargs = (
        {}
        if utils.generic.is_env_ci()
        else dict(
            stdout=subprocess.DEVNULL,
            stderr=None,
        )
    )

    status, stdout, stderr = utils.generic.run_command(
        cmd=aws_sync_command,
        cwd=".",
        env={},
        **kwargs,  # type: ignore
    )

    if status:
        if not os.listdir(local_path):
            shutil.rmtree(local_path)
        LOGGER.debug("pull status: %s", status)
        LOGGER.error("Sync from bucket has failed:")
        LOGGER.info(stdout)
        LOGGER.info(stderr)
        LOGGER.info("\n")
        return False

    if progress_bar:
        progress_bar()

    failed = False

    try:
        repo = Repo(local_path)
        repo.git.reset("--hard", "HEAD")
    except GitError as exc:
        if not os.listdir(local_path):
            shutil.rmtree(local_path)
            return True
        LOGGER.error("Expand repositories has failed:")
        LOGGER.info("Repository: %s", local_path)
        LOGGER.info(exc)
        LOGGER.info("\n")
        failed = True
    return not failed


@shield(retries=1)
def main(subs: str, repository_name: Optional[str] = None) -> bool:
    """
    Clone all repos for a group

    param: subs: group to work with
    """
    passed: bool = True

    roots_dict = {
        root["id"]: root
        for root in get_git_roots(group=subs)
        if root.get("state") == "ACTIVE"
        and (
            root["nickname"] == repository_name
            if repository_name is not None
            else True
        )
    }
    if not roots_dict:
        return False

    with ThreadPoolExecutor() as executor:
        for root_id, download_url in executor.map(
            get_git_root_download_url,
            [subs for _ in range(len(roots_dict))],
            roots_dict.keys(),
        ):
            roots_dict[root_id]["downloadUrl"] = download_url

    zip_roots = [
        root
        for root in roots_dict.values()
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

    for root in roots_dict.values():
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
