# Standard libraries
import os
import re
from typing import (
    Dict,
    List,
    Tuple,
)

# Third-party libraries
import git
from git.cmd import Git
from git.exc import GitCommandError


STAT_REGEX = re.compile(
    r'([0-9]+ files? changed)?'
    r'(, (?P<insertions>[0-9]+) insertions\(\+\))?'
    r'(, (?P<deletions>[0-9]+) deletions\(\-\))?'
)


def get_bad_repos(fusion_path: str) -> List[str]:
    """Filters repositories which have issues running git commands"""
    return [
        repo
        for repo in os.listdir(fusion_path)
        if not test_repo(os.path.join(fusion_path, repo))
    ]


def get_file_authors_history(git_repo: Git, file: str) -> List[str]:
    """Returns a list with the author of every commit that modified a file"""
    author_history: str = git_repo.log(
        '--no-merges',
        '--follow',
        '--pretty=%ae',
        file
    )
    return author_history.split('\n')


def get_file_commit_history(git_repo: Git, file: str) -> List[str]:
    """Returns a list with the hashes of the commits that touched a file"""
    commit_history: str = git_repo.log(
        '--no-merges',
        '--follow',
        '--pretty=%H',
        file
    )
    return commit_history.split('\n')


def get_file_date_history(git_repo: Git, file: str) -> List[str]:
    """Returns a list with dates in ISO format of every commit the file has"""
    date_history: str = git_repo.log(
        '--no-merges',
        '--follow',
        '--pretty=%aI',
        file
    )
    return date_history.split('\n')


def get_file_stat_history(git_repo: Git, file: str) -> List[str]:
    """Returns a list with the amount of changed lines each commit has"""
    stat_history: str = git_repo.log(
        '--no-merges',
        '--follow',
        '--shortstat',
        '--pretty=',
        file
    )
    return stat_history.split('\n')


def get_repository_files(repo_path: str) -> List[str]:
    """Lists all the files inside a repository relative to the repository"""
    ignore_dirs: List[str] = ['.git']
    return [
        os.path.join(path, filename).replace(
            f'{os.path.dirname(repo_path)}/',
            ''
        )
        for path, _, files in os.walk(repo_path)
        for filename in files
        if all([dir_ not in path for dir_ in ignore_dirs])
    ]


def parse_git_shortstat(stat: str) -> Tuple[int, int]:
    insertions: int = 0
    deletions: int = 0
    match = re.match(STAT_REGEX, stat.strip())
    if match:
        groups: Dict[str, str] = match.groupdict()
        if groups['insertions']:
            insertions = int(groups['insertions'])
        if groups['deletions']:
            insertions = int(groups['deletions'])
    return insertions, deletions


def test_repo(repo_path: str) -> bool:
    """Checks correct configuration of a repository by running `git log`"""
    git_repo: Git = git.Git(repo_path)
    is_repo_ok: bool = True
    try:
        git_repo.log()
    except GitCommandError:
        is_repo_ok = False
    return is_repo_ok
