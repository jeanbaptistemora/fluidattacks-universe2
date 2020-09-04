import os
import re
import time
from array import ArrayType
from typing import List, Match, Optional, Tuple

import git
import numpy as np
import pandas as pd
from git.cmd import Git
from git.exc import GitCommandError
from pandas import DataFrame, Series
from pydriller.metrics.process.hunks_count import HunksCount


def df_get_file_commits_authors(row: Series) -> Tuple[int, int]:
    """
    Get the commit and authors information for each file in the DataFrame
    """
    repo: str = row['repo']
    file_: str = row['file']
    return get_file_commits_authors(repo, file_)


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


def fill_model_commit_features(base_df: DataFrame) -> DataFrame:
    """
    Takes a base DataFrame that has at least the following columns:
    [commit, hour, repo]
    Based on these columns, it extracts more features in adds them to the
    DataFrame
    """
    print('Extracting model commit features...')
    start = time.time()
    features_df: DataFrame = pd.DataFrame()
    features_df['hunks'] = base_df.apply(df_get_hunks, axis=1)
    print(f'Hunks added after {time.time() - start} secods.')
    start = time.time()
    features_df[['additions', 'deletions', 'deltas', 'touched']] = base_df\
        .apply(df_get_deltas, axis=1, result_type='expand')
    print(f'Deltas information was added after {time.time() - start}')
    start = time.time()
    files_df = base_df.apply(df_get_files, axis=1)
    features_df['touched_files'] = files_df.apply(len)
    features_df['max_other_touchers'] = files_df.apply(
        lambda x: max(x) if x.size else 0
    )
    features_df['touches_busy_file'] = features_df.max_other_touchers.apply(
        lambda x: 1 if x > 9 else 0
    )
    features_df['authored_hour'] = base_df['hour']
    print(f'File information was added after {time.time() - start}')
    return pd.concat([base_df, features_df], axis=1)


def fill_model_file_features(base_df: DataFrame) -> DataFrame:
    """
    Takes a base DataFrame that has at least the following columns:
    [file, repo]
    Based on these columns, it extracts file-related features and adds them
    to the DataFrame
    """
    print('Extracting model file features...')
    timer: float = time.time()
    features_df: DataFrame = pd.DataFrame()
    features_df[['num_commits', 'num_unique_authors']] = base_df.apply(
        df_get_file_commits_authors,
        axis=1,
        result_type='expand'
    )
    print(
        f'Commit/Authors information extracted after '
        f'{time.time() - timer:.2f} seconds'
    )
    return pd.concat([base_df, features_df], axis=1)


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


def get_file_commits_authors(repo: str, file_: str) -> Tuple[int, int]:
    """
    Given a file in a repository, extract the number of commits that have
    modified it, as well as the number of different authors
    """
    commits_authors: Tuple[int, int] = (0, 0)
    try:
        git_repo: Git = git.Git(repo)
        file_relative_path = os.path.sep.join(file_.split(os.path.sep)[1:])
        file_history = git_repo.log(
            '--follow',
            '--pretty=%H,%ae',
            file_relative_path
        ).split('\n')
        commits_authors = (
            len(file_history),
            len({x.split(',')[1] for x in file_history})
        )
    except GitCommandError:
        print('Error extracting the commits/authors that modified a file')
    return commits_authors


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
