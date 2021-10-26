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
from toolbox import (
    utils,
)
from toolbox.drills import (
    generic as drills_generic,
)
from toolbox.logger import (
    LOGGER,
)
from toolbox.utils.function import (
    shield,
)
from toolbox.utils.integrates import (
    get_filter_rules,
)
from typing import (
    List,
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
            shutil.rmtree(os.path.join(path_to_fusion, repository))

    return True


def pull_repos_s3_to_fusion(subs: str, repository_name: str) -> bool:
    """
    Download repos from s3 to a provided path

    param: subs: group to work with
    param: local_path: Path to store downloads
    """

    if repository_name == "*":
        bucket: str = f"s3://continuous-repositories/{subs}"
        local_path: str = f"groups/{subs}/fusion"
    else:
        bucket = f"s3://continuous-repositories/{subs}/{repository_name}"
        local_path = f"groups/{subs}/fusion/{repository_name}"

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
            stdout=None,
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

    failed = False
    for folder in os.listdir(f"groups/{subs}/fusion"):
        repo_path = f"groups/{subs}/fusion/{folder}"
        try:
            repo = Repo(repo_path)
            repo.git.reset("--hard", "HEAD")
        except GitError as exc:
            LOGGER.error("Expand repositories has failed:")
            LOGGER.info("Repository: %s", folder)
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
    if not utils.generic.does_subs_exist(subs):
        LOGGER.error("group %s does not exist on services.", subs)
        passed = False
        return passed

    utils.generic.aws_login(f"continuous-{subs}")

    if not drills_generic.s3_path_exists(bucket, f"{subs}/"):
        LOGGER.info("group %s does not have repos uploaded to s3", subs)
    else:
        LOGGER.info("Computing last upload date")
        days: int = drills_generic.calculate_days_ago(
            drills_generic.get_last_upload(bucket, f"{subs}/")
        )

        passed = (
            passed
            and pull_repos_s3_to_fusion(subs, repository_name)
            and delete_out_of_scope_files(subs)
        )

        LOGGER.info("Data for %s was uploaded to S3 %i days ago", subs, days)

    return passed
