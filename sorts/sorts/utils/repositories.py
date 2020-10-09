# Standard libraries
import os
from typing import List

# Third-party libraries
import git
from git.cmd import Git
from git.exc import GitCommandError


def get_bad_repos(fusion_path: str) -> List[str]:
    """Filters repositories which have issues running git commands"""
    return [
        repo
        for repo in os.listdir(fusion_path)
        if not test_repo(os.path.join(fusion_path, repo))
    ]


def get_file_authors_history(git_repo: Git, file: str) -> List[str]:
    """Returns a list with the author of every commit that modified a file"""
    file_history: str = git_repo.log(
        '--no-merges',
        '--follow',
        '--pretty=%ae',
        file
    )
    return file_history.split('\n')


def get_file_commit_history(git_repo: Git, file: str) -> List[str]:
    """Returns a list with the hashes of the commits that touched a file"""
    file_history: str = git_repo.log(
        '--no-merges',
        '--follow',
        '--pretty=%H',
        file
    )
    return file_history.split('\n')


def get_file_date_history(git_repo: Git, file: str) -> List[str]:
    """Returns a list with dates in ISO format of every commit the file has"""
    file_history: str = git_repo.log(
        '--no-merges',
        '--follow',
        '--pretty=%aI',
        file
    )
    return file_history.split('\n')


def get_repository_files(repo_path: str) -> List[str]:
    """Lists all the files inside a repository relative to the repository"""
    return [
        os.path.join(path, filename).replace(
            f'{os.path.dirname(repo_path)}/',
            ''
        )
        for path, _, files in os.walk(repo_path)
        for filename in files
    ]


def test_repo(repo_path: str) -> bool:
    """Checks correct configuration of a repository by running `git log`"""
    git_repo: Git = git.Git(repo_path)
    is_repo_ok: bool = True
    try:
        git_repo.log()
    except GitCommandError:
        is_repo_ok = False
    return is_repo_ok
