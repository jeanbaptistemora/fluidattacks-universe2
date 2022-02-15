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
from toolbox.resources import (
    get_head_commit,
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

# Constants
TEST_SUBS: str = "continuoustest"


def s3_ls(
    bucket: str,
    path: str,
    endpoint_url: Optional[str] = None,
) -> List[str]:
    client = boto3.client("s3", endpoint_url=endpoint_url)

    path = f"{path}/" if not path.endswith("/") else path

    response = client.list_objects_v2(
        Bucket=bucket,
        Delimiter="/",
        Prefix=path,
    )
    try:
        return [x["Prefix"] for x in response.get("CommonPrefixes", [])]
    except KeyError as key_error:
        LOGGER.error("Looks like response does not have Common Prefixes:")
        LOGGER.error(key_error)
    except json.decoder.JSONDecodeError as json_decode_error:
        LOGGER.error("Looks like response was not parseable")
        LOGGER.error(json_decode_error)
    return []


def fill_empty_folders(path: str) -> None:
    empty_folders = [
        root for root, dirs, files in os.walk(path) if not dirs and not files
    ]
    for folder in empty_folders:
        LOGGER.info("Adding .keep at %s", folder)
        Path(folder, ".keep").touch()


def git_optimize_all(path: str) -> None:
    git_files = tuple(Path(path).glob("**/.git"))
    LOGGER.info("Git files: %s", git_files)
    git_folders = {x.parent for x in git_files}
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


def append_root_metadata(
    subs: str, root_nickname: Optional[str] = None
) -> None:
    # We'll be appending a small metadata file to each repository so
    # downstream components know important values about the data
    upload_dates: Dict[str, str] = get_root_upload_dates(subs)
    if root_nickname:
        if _upload_date := upload_dates.get(root_nickname):
            with open(
                (
                    f"groups/{subs}/fusion/"
                    f"{root_nickname}/.git/fluidattacks_metadata"
                ),
                "w",
                encoding="utf8",
            ) as file:
                json.dump({"date": _upload_date}, file, indent=2)
    else:
        for root in glob.glob(f"groups/{subs}/fusion/*"):
            root_nickname = os.path.basename(root)
            if _upload_date := upload_dates.get(root_nickname):
                with open(
                    f"{root}/.git/fluidattacks_metadata", "w", encoding="utf8"
                ) as file:
                    json.dump({"date": _upload_date}, file, indent=2)


def s3_sync_fusion_to_s3(
    group_name: str,
    root_nickname: str,
    bucket: str = "continuous-repositories",
    endpoint_url: Optional[str] = None,
) -> bool:
    append_root_metadata(group_name, root_nickname)

    fusion_dir: str = f"groups/{group_name}/fusion"
    s3_subs_repos_path: str = group_name
    kwargs = (
        {}
        if generic.is_env_ci()
        else dict(
            stdout=None,
            stderr=None,
        )
    )
    base_path = os.getcwd()
    aws_sync_command: List[str] = [
        "aws",
        "s3",
        "sync",
        "--delete",
        "--sse",
        "AES256",
        "--exclude",
        f"{base_path}/{fusion_dir}/{root_nickname}/*",
        "--include",
        f"{base_path}/{fusion_dir}/{root_nickname}/.git/*",
        f"{base_path}/{fusion_dir}/{root_nickname}",
        f"s3://{bucket}/{s3_subs_repos_path}/{root_nickname}/",
    ]

    if not generic.is_env_ci():
        git_optimize_all(fusion_dir)

    # Allow upload empty folders to keep .git structure
    # and avoid errors
    fill_empty_folders(fusion_dir)

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
# pylint: disable=too-many-arguments
def main(
    subs: str,
    bucket: str = "continuous-repositories",
    aws_login: bool = True,
    aws_profile: str = "continuous-admin",
    endpoint_url: Optional[str] = None,
    force: bool = False,
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
    permissions = utils.integrates.get_group_permissions(subs)
    if "api_mutations_refresh_toe_lines_mutate" not in permissions:
        LOGGER.error("Must have permission to refresh the surface lines")
        return False
    if not (generic.does_subs_exist(subs) and generic.does_fusion_exist(subs)):
        LOGGER.error("Either the subs or the fusion folder does not exist")
        return False

    if aws_login:
        generic.aws_login(aws_profile)

    repo_request = integrates.Queries.git_roots(
        API_TOKEN,
        subs,
    )
    if not repo_request.ok:
        LOGGER.error(repo_request.errors)
        return False

    roots_dict = {
        root["nickname"]: root
        for root in repo_request.data["group"]["roots"]
        if root.get("state", "") == "ACTIVE"
    }

    LOGGER.info("Syncing repositories")
    repos = os.listdir(f"groups/{subs}/fusion")
    for repo in repos:
        if (root := roots_dict.get(repo)) and (
            local_commit := get_head_commit(
                f"groups/{subs}/fusion/{repo}", root["branch"]
            )
        ):
            if force or local_commit != root.get("cloningStatus", {}).get(
                "commit"
            ):
                passed = s3_sync_fusion_to_s3(
                    subs, root["nickname"], bucket, endpoint_url
                )
            else:
                LOGGER.info("%s is already in S3", repo)
        else:
            passed = False
    if passed and (
        (generic.is_env_ci() and generic.is_branch_master())
        or not generic.is_env_ci()
    ):
        update_last_sync_date("last_sync_date", subs)
    if passed and subs != TEST_SUBS:
        utils.integrates.refresh_toe_lines(subs)

    return passed
