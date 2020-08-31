import re
from array import ArrayType
from typing import List, Match, Optional, Tuple

import git
import numpy as np
from git.cmd import Git
from git.exc import GitCommandError
from pandas import Series
from pydriller.metrics.process.hunks_count import HunksCount


def df_get_deltas(row: Series) -> Tuple[int, int, int, int]:
    """
    Get deltas information for an entire dataframe
    """
    repo: str = row['repo']
    commit: str = row['commit']
    return get_deltas(repo, commit)


def df_get_files(row: Series) -> ArrayType:
    """
    Get information about modified files for an entire dataframe
    """
    repo: str = row['repo']
    commit: str = row['commit']
    return get_files(repo, commit)


def df_get_hunks(row: Series) -> float:
    """
    Get number of hunks for an entire dataframe
    """
    repo: str = row['repo']
    commit: str = row['commit']
    return get_hunks(repo, commit)


def get_deltas(repo: str, commit: str) -> Tuple[int, int, int, int]:
    """
    Evaluate a commit and get the number of lines that were added and deleted,
    plus the number of deltas
    """
    deltas_info: Tuple[int, int, int, int] = (0, 0, 0, 0)
    try:
        gitrepo: Git = git.Git(repo)
        shortstat: str = gitrepo.show(
            '--shortstat',
            '--pretty=format:',
            commit
        )
        match: Optional[Match[str]] = re.search(r'(\d+) ins', shortstat)
        add: int = int(match.group(1) if match else 0)
        match = re.search(r'(\d+) del', shortstat)
        rem: int = int(match.group(1) if match else 0)
        net: int = add - rem
        tou: int = add + rem
        deltas_info = add, rem, net, tou
    except GitCommandError:
        print(f'error with repo {repo}')
        print('commit', commit)
    except IndexError:
        print('shortstat error:', shortstat)
    return deltas_info


def get_files(repo: str, commit: str) -> ArrayType:
    touchers: List[int] = []
    try:
        gitrepo: Git = git.Git(repo)
        filenames: str = gitrepo.show(
            '--name-only',
            '--pretty=format:',
            commit
        )
        for file_ in filenames.split('\n'):
            authors: str = gitrepo.log('--follow', '--pretty=%aE', '--', file_)
            num_file_touchers: int = len(set(authors.split('\n')))
            touchers.append(num_file_touchers)
    except GitCommandError:
        print(f'Error with repo {repo}')
        print('Commit', commit)
    except IndexError:
        print('Shortstat error:', repo)
    touchers_array: ArrayType = np.array(touchers)
    return touchers_array


def get_hunks(repo: str, commit: str) -> float:
    """
    Get number of hunks introduced by given commit in given repo
    """
    metric = HunksCount(
        path_to_repo=repo,
        from_commit=commit,
        to_commit=commit
    )
    files = metric.count()
    hunks = sum(files.values())
    return hunks
