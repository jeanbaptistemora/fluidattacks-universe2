# pylint: disable=unused-argument
# Standrd libraries
import os
from pathlib import (
    Path,
)
from shutil import (
    rmtree,
)
from toolbox.drills import (
    push_repos,
)
from toolbox.utils import (
    generic,
)
from typing import (
    Any,
    List,
)

BUCKET: str = "continuous-repositories"
SUBS: str = "continuoustest"
AWS_LOGIN: bool = False
SUBS_PATH: str = f"groups/{SUBS}"
SUBS_FUSION: str = f"{SUBS_PATH}/fusion"
LOCALSTACK_ENDPOINT: str = "localstack" if generic.is_env_ci() else "localhost"
# FP: the endpoint is hosted in a local environment
ENDPOINT_URL: str = f"http://{LOCALSTACK_ENDPOINT}:4566"  # NOSONAR

EXPECTED_REPOS: List[str] = [f"{SUBS}/services/"]


def test_drills_push_repos(
    relocate: Any,
    prepare_s3_continuous_repositories: Any,
) -> None:
    """
    This tests does the following:

    - repo2 and repo3 are uploaded
    """

    def create_repo(path: str) -> None:
        files: List[str] = ["file1", "file2", "file3"]
        os.makedirs(f"{path}/.git", exist_ok=True)
        for filename in files:
            file_path: str = f"{path}/.git/{filename}"
            Path(file_path).touch()

    def set_up_repos() -> None:
        repos: List[str] = ["services"]
        os.makedirs(SUBS_FUSION, exist_ok=True)

        for repo in repos:
            repo_path: str = f"{SUBS_FUSION}/{repo}"
            create_repo(repo_path)
            push_repos.s3_sync_fusion_to_s3(SUBS, repo, BUCKET, ENDPOINT_URL)

    try:
        set_up_repos()
        push_repos.main(SUBS, BUCKET, AWS_LOGIN, "", ENDPOINT_URL)
        repos: List[str] = push_repos.s3_ls(BUCKET, f"{SUBS}/", ENDPOINT_URL)
        assert sorted(repos) == sorted(EXPECTED_REPOS)
    finally:
        rmtree(SUBS_PATH)
