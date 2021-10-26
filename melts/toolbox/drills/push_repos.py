import boto3
import git
from git.exc import (
    GitCommandError,
)
import glob
import json
import os
from pathlib import (
    Path,
)
import shutil
from toolbox.api import (
    integrates,
)
from toolbox.constants import (
    API_TOKEN,
)
from toolbox.logger import (
    LOGGER,
)
from toolbox.utils import (
    db_client,
    generic,
)
from toolbox.utils.function import (
    shield,
)
from typing import (
    Dict,
    List,
    Optional,
)


def s3_ls(
    bucket: str,
    path: str,
    endpoint_url: Optional[str] = None,
) -> List[str]:
    client = boto3.client("s3", endpoint_url=endpoint_url)

    if not path.endswith("/"):
        path = f"{path}/"

    response = client.list_objects_v2(
        Bucket=bucket,
        Delimiter="/",
        Prefix=path,
    )
    try:
        return list(map(lambda x: x["Prefix"], response["CommonPrefixes"]))
    except KeyError as key_error:
        LOGGER.error("Looks like response does not have Common Prefixes:")
        LOGGER.error(key_error)
    except json.decoder.JSONDecodeError as json_decode_error:
        LOGGER.error("Looks like response was not parseable")
        LOGGER.error(json_decode_error)
    return []


def fill_empty_folders(path: str) -> None:
    empty_folders = []
    for root, dirs, files in os.walk(path):
        if not dirs and not files:
            empty_folders.append(root)
    for folder in empty_folders:
        LOGGER.info("Adding .keep at %s", folder)
        Path(folder, ".keep").touch()


def git_optimize_all(path: str) -> None:
    git_files = Path(path).glob("**/.git")
    LOGGER.info("Git files: %s", tuple(git_files))
    git_folders = set(map(lambda x: x.parent, git_files))
    for folder in git_folders:
        LOGGER.info("Git optimize at %s", folder)
        try:
            git.Repo(str(folder), search_parent_directories=True).git.gc(
                "--aggressive", "--prune=all"
            )
        except GitCommandError as exc:
            LOGGER.error("Git optimization has failed at %s: ", folder)
            LOGGER.info(exc.stdout)
            LOGGER.info(exc.stderr)
            shutil.rmtree(folder)


def get_root_upload_dates(subs: str) -> Dict[str, str]:
    response = integrates.Queries.git_roots(API_TOKEN, subs)
    if not response.ok:
        LOGGER.error(response.errors)
        raise ValueError("Could not retrieve git roots from Integrates")

    return {
        root["nickname"]: root["lastCloningStatusUpdate"]
        for root in response.data["group"]["roots"]
    }


def append_root_metadata(subs: str) -> None:
    # We'll be appending a small metadata file to each repository so
    # downstream components know important values about the data
    upload_dates: Dict[str, str] = get_root_upload_dates(subs)

    for root in glob.glob(f"groups/{subs}/fusion/*"):
        root_nickname: str = os.path.basename(root)
        with open(
            f"{root}/.git/fluidattacks_metadata", "w", encoding="utf8"
        ) as file:
            json.dump({"date": upload_dates[root_nickname]}, file, indent=2)


def s3_sync_fusion_to_s3(
    subs: str,
    bucket: str = "continuous-repositories",
    endpoint_url: Optional[str] = None,
) -> bool:
    append_root_metadata(subs)

    fusion_dir: str = f"groups/{subs}/fusion"
    s3_subs_repos_path: str = f"{subs}/"
    kwargs = (
        dict()
        if generic.is_env_ci()
        else dict(
            stdout=None,
            stderr=None,
        )
    )

    aws_sync_command: List[str] = [
        "aws",
        "s3",
        "sync",
        "--delete",
        "--sse",
        "AES256",
        "--exclude",
        "*",
        "--include",
        "*/.git/*",
        fusion_dir,
        f"s3://{bucket}/{s3_subs_repos_path}",
    ]
    # Allow upload empty folders to keep .git structure
    # and avoid errors
    fill_empty_folders(fusion_dir)

    if not generic.is_env_ci():
        git_optimize_all(fusion_dir)

    if endpoint_url:
        aws_sync_command.append("--endpoint")
        aws_sync_command.append(endpoint_url)
    if generic.is_env_ci():
        aws_sync_command.append("--quiet")
    status, stdout, stderr = generic.run_command(
        cmd=aws_sync_command,
        cwd=".",
        env={},
        **kwargs,  # type:ignore
    )
    # refer to https://docs.aws.amazon.com/cli/latest/topic/return-codes.html
    if status not in (0, 2):
        LOGGER.debug("push status: %s", status)
        LOGGER.error("Sync from bucket has failed:")
        LOGGER.info("stdout: %s", stdout)
        LOGGER.info("stderr: %s", stderr)
        return False
    return True


def update_last_sync_date(table: str, group: str) -> None:
    db_state = db_client.make_access_point()
    try:
        db_client.confirm_synced_group(db_state, group, table)
    finally:
        db_client.drop_access_point(db_state)


@shield(retries=1)
def main(
    subs: str,
    bucket: str = "continuous-repositories",
    aws_login: bool = True,
    aws_profile: str = "continuous-admin",
    endpoint_url: Optional[str] = None,
) -> bool:
    """
    This function does:

    1. Upload all repos from fusion to s3

    param: subs: group to work with
    param: bucket: Bucket to work with
    param: aws_login: where or not to login to aws
    param: aws_profile: which profile-role to use in case aws_login is true
    param: endpoint_url: aws endpoint to send API requests
    """
    passed: bool = True
    if generic.does_subs_exist(subs) and generic.does_fusion_exist(subs):
        if aws_login:
            generic.aws_login(aws_profile)

        LOGGER.info("Syncing repositories")
        passed = passed and s3_sync_fusion_to_s3(subs, bucket, endpoint_url)
    else:
        LOGGER.error("Either the subs or the fusion folder does not exist")
        passed = False
    if passed and (
        (generic.is_env_ci() and generic.is_branch_master())
        or not generic.is_env_ci()
    ):
        update_last_sync_date("last_sync_date", subs)

    return passed
