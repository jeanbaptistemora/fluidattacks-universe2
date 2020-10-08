# Standard libraries
import os
from typing import List

# Third-party libraries
import git
from git.cmd import Git
from git.exc import GitCommandError


def get_bad_repos(fusion_path: str, repos: List[str]) -> List[str]:
    """
    Filter a list of repos, returning the bad ones
    """
    are_repos_ok = [test_repo(fusion_path, repo) for repo in repos]
    return [
        repo
        for idx, repo in enumerate(repos)
        if are_repos_ok[idx] is False
    ]


def test_repo(fusion_path: str, repo: str) -> bool:
    """
    Test if a repository is ok by executing a single `git log` on it.
    """
    repo_path: str = os.path.join(fusion_path, repo)
    git_repo: Git = git.Git(repo_path)
    repo_ok: bool = True
    try:
        git_repo.log()
    except GitCommandError:
        repo_ok = False
    return repo_ok
