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

EXPECTED_REPOS: List[str] = [
    f'{SUBS}/inactive/repo1/',
    f'{SUBS}/active/repo2/',
    f'{SUBS}/active/repo3/'
]


def test_drills_push_repos(relocate, prepare_s3_continuous_repositories):
    """
    This tests does the following:

    1. repo1 changes from active to inactive
    2. repo2 and repo3 are uploaded
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

        for repo in repos:
            repo_path: str = f'{SUBS_FUSION}/{repo}'
            create_repo(repo_path)
        push_repos.s3_sync_fusion_to_s3(SUBS, BUCKET, ENDPOINT_URL)
        rmtree(f'{SUBS_FUSION}/repo1')

    try:
        set_up_repos()
        push_repos.main(SUBS, BUCKET, AWS_LOGIN, '', ENDPOINT_URL)
        repos: List[str] = push_repos.s3_ls(BUCKET, f'{SUBS}/active/', ENDPOINT_URL)
        repos += push_repos.s3_ls(BUCKET, f'{SUBS}/inactive/', ENDPOINT_URL)
        assert sorted(repos) == sorted(EXPECTED_REPOS)
    finally:
        rmtree(SUBS_PATH)
