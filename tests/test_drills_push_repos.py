# Standrd libraries
import os
from typing import List
from pathlib import Path
from shutil import rmtree

# Third party libraries
import boto3

# Local libraries
from toolbox.utils import generic
from toolbox.drills import (
    push_repos
)


BUCKET: str = 'continuous-repositories'
SUBS: str = 'continuoustests3'
AWS_LOGIN: bool = False
SUBS_PATH: str = f'subscriptions/{SUBS}'
SUBS_FUSION: str = f'{SUBS_PATH}/fusion'
LOCALSTACK_ENDPOINT: str = \
    'localstack' if generic.is_env_ci() else 'localhost'
ENDPOINT_URL: str = f'http://{LOCALSTACK_ENDPOINT}:4566'

EXPECTED_ACTIVE_REPOS: List[str] = ['repo2', 'repo3', 'repo4']
EXPECTED_INACTIVE_REPOS: List[str] = ['repo1']


def test_drills_push_repos(relocate, prepare_s3_continuous_repositories):
    """
    This tests does the following:

    1. repo1 changes from active to inactive
    2. repo2 changes from inactive to active
    3. repo3 stays active (already uploaded)
    4. repo4 becomes active (it is uploaded)
    """


    def create_repo(path: str):
        files: List[str] = ['file1', 'file2', 'file3']
        os.mkdir(path)
        for filename in files:
            file_path: str = f'{path}/{filename}'
            Path(file_path).touch()


    def set_up_repos():
        repos: List[str] = ['repo1', 'repo2', 'repo3']
        os.makedirs(SUBS_FUSION, exist_ok=True)
        create_repo(f'{SUBS_FUSION}/repo4')
        for repo in repos:
            repo_path: str = f'{SUBS_FUSION}/{repo}'
            create_repo(repo_path)
            status : str = 'active' if repo != 'repo2' else 'inactive'
            push_repos.s3_upload(
                BUCKET,
                f'{SUBS_FUSION}/{repo}/',
                f'{SUBS}/{status}/{repo}/',
                ENDPOINT_URL
            )
        rmtree(f'{SUBS_FUSION}/repo1')


    try:
        set_up_repos()
        push_repos.main(SUBS, BUCKET, AWS_LOGIN, '', ENDPOINT_URL)
        active_repos: List[str] = \
            push_repos.s3_get_repos(BUCKET, SUBS, 'active', ENDPOINT_URL)
        inactive_repos: List[str] = \
            push_repos.s3_get_repos(BUCKET, SUBS, 'inactive', ENDPOINT_URL)
        assert sorted(active_repos) == sorted(EXPECTED_ACTIVE_REPOS)
        assert sorted(inactive_repos) == sorted(EXPECTED_INACTIVE_REPOS)
    finally:
        rmtree(SUBS_PATH)
