import boto3
from concurrent.futures.thread import (
    ThreadPoolExecutor,
)
from contextlib import (
    suppress,
)
import git
from git.exc import (
    GitCommandError,
    GitError,
)
import glob
import json
import os
from pathlib import (
    Path,
)
import requests  # type: ignore
import shutil
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
from toolbox.utils.integrates import (
    get_git_root_upload_url,
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
    LOGGER.info("Git files: %s", tuple(x.name for x in git_files))
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
    root_id: str,
    upload_url: str,
) -> bool:
    append_root_metadata(group_name, root_nickname)

    fusion_dir: str = f"groups/{group_name}/fusion"
    base_path = os.getcwd()
    repo_path = f"{base_path}/{fusion_dir}/{root_nickname}"

    if not generic.is_env_ci():
        git_optimize_all(f"{base_path}/{fusion_dir}/{root_nickname}/")

    # Allow upload empty folders to keep .git structure
    # and avoid errors
    fill_empty_folders(fusion_dir)

    _, zip_output_path = tempfile.mkstemp()
    code, _, stderr = generic.run_command(
        cmd=[
            "tar",
            "czf",
            zip_output_path,
            "--transform",
            f"flags=r;s/./{root_nickname}/",
            ".",
        ],
        cwd=repo_path,
        env={},
    )
    if code != 0:
        LOGGER.error("Failed to comppres root \n %s", stderr)

    with open(zip_output_path, "rb") as object_file:
        object_text = object_file.read()
        response = requests.put(upload_url, data=object_text)
        response.raise_for_status()

    with suppress(GitError, AttributeError):
        utils.integrates.update_root_cloning_status(
            group_name,
            root_id,
            "OK",
            "Cloned successfully",
            commit=git.Repo(
                repo_path, search_parent_directories=True
            ).head.object.hexsha,
        )
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
    aws_login: bool = True,
    aws_profile: str = "continuous-admin",
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
    roots_dict_by_id = {
        root["id"]: root
        for root in repo_request.data["group"]["roots"]
        if root.get("state", "") == "ACTIVE"
    }
    with ThreadPoolExecutor() as executor:
        roots_ulrs_dict = dict(
            executor.map(
                get_git_root_upload_url,
                [subs for _ in range(len(roots_dict))],
                roots_dict_by_id.keys(),
            )
        )
    for root_id, download_url in roots_ulrs_dict.items():
        roots_dict[roots_dict_by_id[root_id]["nickname"]][
            "uploadUrl"
        ] = download_url

    LOGGER.info("Syncing repositories")
    repos = os.listdir(f"groups/{subs}/fusion")
    with ThreadPoolExecutor() as executor:
        for repo in repos:
            if (root := roots_dict.get(repo)) and (
                local_commit := get_head_commit(
                    f"groups/{subs}/fusion/{repo}", root["branch"]
                )
            ):
                if force or (
                    local_commit
                    and local_commit
                    != root.get("cloningStatus", {}).get("commit")
                ):
                    LOGGER.info(
                        (
                            "Syncing %s to s3, local commit: %s,"
                            " remote commit: %s"
                        ),
                        root["nickname"],
                        local_commit,
                        root.get("cloningStatus", {}).get("commit"),
                    )
                    executor.submit(
                        s3_sync_fusion_to_s3,
                        subs,
                        root["nickname"],
                        root["id"],
                        root["uploadUrl"],
                    )
                else:
                    LOGGER.info("%s is already in S3", repo)
            else:
                passed = False
    if passed and (
        (generic.is_env_ci() and generic.is_branch_master())
        or not generic.is_env_ci()
    ):
        if aws_login:
            generic.aws_login(aws_profile)
        update_last_sync_date("last_sync_date", subs)
    if passed and subs != TEST_SUBS:
        utils.integrates.refresh_toe_lines(subs)

    return passed
