from concurrent.futures.thread import (
    ThreadPoolExecutor,
)
from contextlib import (
    suppress,
)
import git
from git.exc import (
    GitError,
)
import glob
import json
import os
import requests  # type: ignore
import tarfile
import tempfile
from toolbox import (
    utils,
)
from toolbox.logger import (
    LOGGER,
)
from toolbox.resources import (
    get_head_commit,
)
from toolbox.utils import (
    generic,
    last_sync,
)
from toolbox.utils.function import (
    shield,
)
from toolbox.utils.integrates import (
    get_git_root_upload_url,
    get_git_roots,
)
from typing import (
    Dict,
    Optional,
)

# Constants
TEST_SUBS: str = "continuoustest"


def create_git_root_tar_file(
    root_nickname: str, repo_path: str, output_path: Optional[str] = None
) -> bool:
    git_dir = os.path.normpath(f"{repo_path}/.git")
    with tarfile.open(
        output_path or f"{root_nickname}.tar.gz", "w:gz"
    ) as tar_handler:
        if os.path.exists(git_dir):
            tar_handler.add(
                git_dir, arcname=f"{root_nickname}/.git", recursive=True
            )
            return True
        return False


def get_root_upload_dates(subs: str) -> Dict[str, str]:
    return {
        root["nickname"]: root["lastCloningStatusUpdate"]
        for root in get_git_roots(subs)
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

    _, zip_output_path = tempfile.mkstemp()

    if not create_git_root_tar_file(
        root_nickname, repo_path, output_path=zip_output_path
    ):
        LOGGER.error("Failed to comppres root \n %s", root_nickname)

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

    roots = get_git_roots(subs)

    roots_dict = {
        root["nickname"]: root
        for root in roots
        if root.get("state", "") == "ACTIVE"
    }
    roots_dict_by_id = {
        root["id"]: root for root in roots if root.get("state", "") == "ACTIVE"
    }
    with ThreadPoolExecutor() as executor:
        for root_id, download_url in executor.map(
            get_git_root_upload_url,
            [subs for _ in range(len(roots_dict))],
            roots_dict_by_id.keys(),
        ):
            roots_dict[roots_dict_by_id[root_id]["nickname"]][
                "uploadUrl"
            ] = download_url

    LOGGER.info("Syncing repositories")
    with ThreadPoolExecutor() as executor:
        for repo in os.listdir(f"groups/{subs}/fusion"):
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
        LOGGER.info("Update sync date in DB")
        if aws_login:
            generic.aws_login(aws_profile)
        last_sync.update_last_sync_date("last_sync_date", subs)
    if passed and subs != TEST_SUBS:
        utils.integrates.refresh_toe_lines(subs)

    return passed
