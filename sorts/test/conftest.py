# Standard libraries
import os
import tempfile
from typing import Iterator

# Third-party libraries
import git
import pytest
from git.cmd import Git

# Local libraries
from integrates.graphql import (
    create_session,
    end_session,
)


@pytest.fixture(autouse=True, scope='session')
def test_clone_repo() -> Iterator[str]:
    with tempfile.TemporaryDirectory() as tmp_dir:
        repo_path: str = os.path.join(tmp_dir, 'requests')
        repo_url: str = 'https://github.com/psf/requests.git'
        repo_version: str = 'v2.24.0'
        git.Repo.clone_from(repo_url, repo_path)
        git_repo: Git = git.Git(repo_path)
        git_repo.checkout(repo_version)
        yield tmp_dir


@pytest.fixture(autouse=True, scope='session')
def test_integrates_api_token() -> Iterator[str]:
    yield os.environ['INTEGRATES_API_TOKEN']


@pytest.fixture(scope='function')
def test_integrates_session(test_integrates_api_token: str) -> Iterator[None]:
    token = create_session(api_token=test_integrates_api_token)
    try:
        yield
    finally:
        end_session(token)
