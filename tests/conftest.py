# Standard library
import os
import sys
import shlex
import contextlib

# Third parties libraries
import boto3
import pytest
import unittest.mock

# Local libraries
import toolbox.toolbox
from toolbox import logger
from toolbox.utils import generic
from toolbox import resources

# Constants
SUBS: str = 'continuoustest'


@contextlib.contextmanager
def _relocate(path: str = '../'):
    """Change temporarily the working directory."""
    # The toolbox need to be run in the root of the repository
    current_dir: str = os.getcwd()
    try:
        os.chdir(path)
        logger.info('yield', os.getcwd())
        yield os.getcwd()
    finally:
        # Return to where we were
        logger.info('finally', current_dir)
        os.chdir(current_dir)


@pytest.fixture(scope='function')
def relocate(request):
    """Change temporarily the working directory."""
    with _relocate() as new_path:
        yield new_path


@pytest.fixture(scope='function')
def relocate_to_cloned_repo(request):
    """Change temporarily the working directory."""
    with _relocate(path=f'../groups/{SUBS}/fusion/continuous') as new_path:
        yield new_path


@pytest.fixture(scope='function')
def prepare_s3_continuous_repositories(request):
    """Create empty continuous-repositories s3 bucket"""
    localstack_endpoint: str = \
        'localstack' if generic.is_env_ci() else 'localhost'
    endpoint_url: str = f'http://{localstack_endpoint}:4566'
    bucket_name: str = 'continuous-repositories'
    s3_client = boto3.client('s3', endpoint_url=endpoint_url)
    s3_client.create_bucket(Bucket=bucket_name)


@pytest.fixture(scope='session', autouse=True)
def prepare(request):
    """Prepare the environment by cloning the test repository."""
    with _relocate():
        os.system(
            f'git -C groups/{SUBS}/fusion/continuous reset --hard HEAD'
        )
        assert resources.repo_cloning(SUBS)
