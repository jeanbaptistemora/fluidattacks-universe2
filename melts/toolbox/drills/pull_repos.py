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
import requests  # type: ignore
import shutil
import subprocess
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
from toolbox.utils.integrates import (
    get_filter_rules,
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
        for path in utils.file.iter_rel_paths(path_to_repo):
            if match_file(spec_ignore.patterns, path):
                if path.startswith(".git/"):
                    continue
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

    with requests.get(root["downloadUrl"], stream=True) as handler:
        handler.raise_for_status()
        with open(file_path, "wb") as file:
            for chunk in handler.iter_content(8192):
                file.write(chunk)

    if progress_bar:
        progress_bar()

    code, _, stderr = utils.generic.run_command(
        cmd=["tar", "-xf", f"{nickname}.tar.gz"],
        cwd=f"groups/{group_name}/fusion/",
        env={},
    )

    if code != 0:
        LOGGER.error(stderr)
        os.remove(file_path)
        return False

    os.remove(file_path)
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
            return True
        LOGGER.error("Expand repositories has failed:")
        LOGGER.info("Repository: %s", local_path)
        LOGGER.info(exc)
        LOGGER.info("\n")
        failed = True
    return not failed


@shield(retries=1)
def main(subs: str, repository_name: str) -> bool:
    """
    Clone all repos for a group

    param: subs: group to work with
    """
    bucket: str = "continuous-repositories"
    passed: bool = True

    utils.generic.aws_login(f"continuous-{subs}")
    roots = [
        root for root in get_git_roots(group=subs) if root["state"] == "ACTIVE"
    ]
    if not roots:
        return False

    zip_roots = [root for root in roots if root.get("downloadUrl") is not None]
    pull_roots = (
        [root for root in roots if root.get("downloadUrl") is None]
        if repository_name == "*"
        else [{"nickname": repository_name}]
    )

    with alive_bar(
        len(zip_roots) + len(pull_roots), enrich_print=False
    ) as progress_bar:
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
            LOGGER.info("Sync from s3")
            pull = list(
                executor.map(
                    pull_repos_s3_to_fusion,
                    [subs for _ in range(len(pull_roots))],
                    [root["nickname"] for root in pull_roots],
                    [progress_bar for _ in range(len(pull_roots))],
                )
            )
            passed = passed and all(pull) if pull_roots else True

    if not drills_generic.s3_path_exists(bucket, f"{subs}/"):
        LOGGER.info("group %s does not have repos uploaded to s3", subs)
    else:
        LOGGER.info("Computing last upload date")
        days: int = drills_generic.calculate_days_ago(
            drills_generic.get_last_upload(bucket, f"{subs}/")
        )

        passed = delete_out_of_scope_files(subs) and passed

        LOGGER.info("Data for %s was uploaded to S3 %i days ago", subs, days)

    return passed
