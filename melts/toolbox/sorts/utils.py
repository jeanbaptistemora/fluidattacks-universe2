import os
import re
import time
from array import ArrayType
from datetime import datetime
from functools import partial
from typing import Dict, List, Match, NamedTuple, Optional, Set, Tuple

import git
import numpy as np
import pandas as pd
import pytz
from git.cmd import Git
from git.exc import GitCommandError
from pandas import DataFrame, Series
from pydriller.metrics.process.hunks_count import HunksCount


class FileFeatures(NamedTuple):
    num_commits: int
    num_unique_authors: int
    file_age: int
    midnight_commits: int
    risky_commits: int
    seldom_contributors: int


def count_loc(file_path: str) -> int:
    result: int = 0
    try:
        file_ = open(file_path, 'rb')
        bufgen = iter(
            partial(file_.raw.read, 1024 * 1024), b''  # type: ignore
        )
        result = sum(buf.count(b'\n') for buf in bufgen)
    except FileNotFoundError:
        print(f'File {file_path} not found. ')
    return result


def df_get_deltas(row: Series) -> Tuple[int, int, int, int]:
    """
    Get deltas information for an entire dataframe
    """
    repo: str = row['repo']
    commit: str = row['commit']
    return get_deltas(repo, commit)


def df_get_file_features(row: Series) -> FileFeatures:
    """
    Get the commit and authors information for each file in the DataFrame
    """
    repo: str = row['repo']
    file_: str = row['file']
    return get_file_features(repo, file_)


def df_get_file_loc(row: Series) -> int:
    """
    Get the number of lines for each file in the DataFrame
    """
    repo: str = row['repo']
    file_: str = row['file']
    return get_file_loc(repo, file_)


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
    features_df[[
        'additions',
        'deletions',
        'deltas',
        'touched'
    ]] = base_df.apply(df_get_deltas, axis=1, result_type='expand')
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
    features_df[[
        'num_commits',
        'num_unique_authors',
        'file_age',
        'midnight_commits',
        'risky_commits',
        'seldom_contributors'
    ]] = base_df.apply(
        df_get_file_features,
        axis=1,
        result_type='expand'
    )
    features_df['num_lines'] = base_df.apply(df_get_file_loc, axis=1)
    features_df['commit_frequency'] = features_df.apply(
        lambda x: round(float(x['num_commits']) / float(x['file_age']), 3)
        if x['file_age'] else 0,
        axis=1
    )
    features_df['busy_file'] = features_df['num_unique_authors'].apply(
        lambda x: 1 if x > 9 else 0
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


def get_file_features(repo: str, file_: str) -> FileFeatures:
    """
    Given a file in a repository, extract features by analizing its
    history of commits
    """
    num_commits: int = 0
    num_unique_authors: int = 0
    file_age: int = 0
    midnight_commits: int = 0
    risky_commits: int = 0
    seldom_contributors: Set[str] = set()
    today = datetime.now(tz=pytz.timezone('America/Bogota'))

    try:
        git_repo: Git = git.Git(repo)
        file_relative_path = os.path.sep.join(file_.split(os.path.sep)[1:])
        authors_contribution, mean_contribution = \
            get_repo_author_contributions(git_repo)

        # History is retrieved in the following format from git:
        #     commit_hash, commit_author, commit_date_iso_format\n
        #     \n
        #     deltas_info
        # We translate it to:
        #     commit_hash, commit_author, commit_date_iso_format, deltas_info
        file_history = git_repo.log(
            '--shortstat',
            '--follow',
            '--pretty=%H,%ae,%aI',
            file_relative_path
        ).replace('\n\n', ',').split('\n')

        # Filter empty commits
        file_history = list(filter(None, file_history))

        if file_history:
            num_commits = len(file_history)
            num_unique_authors = len({x.split(',')[1] for x in file_history})

            date_first_commit: str = file_history[-1].split(',')[2]
            file_age = (
                today - datetime.fromisoformat(date_first_commit)
            ).days
            for record in file_history:
                record_as_list = record.split(',')

                # Usually deltas info has the following format:
                #     # files changed, # lines added, # lines deleted
                # Sometimes there aren't either lines added or removed, so we
                # fill that information with 0
                while len(record_as_list) != 6:
                    record_as_list.append('0')

                if datetime.fromisoformat(record_as_list[2]).hour < 6:
                    midnight_commits += 1

                lines_added = int(record_as_list[4].strip().split(' ')[0])
                lines_removed = int(record_as_list[5].strip().split(' ')[0])
                if lines_added + lines_removed > 200:
                    risky_commits += 1

                if authors_contribution[record_as_list[1]] < mean_contribution:
                    seldom_contributors.add(record_as_list[1])
    except GitCommandError:
        print('Error extracting the commits/authors that modified a file')
    return FileFeatures(
        num_commits=num_commits,
        num_unique_authors=num_unique_authors,
        file_age=file_age,
        midnight_commits=midnight_commits,
        risky_commits=risky_commits,
        seldom_contributors=len(seldom_contributors)
    )


def get_file_loc(repo: str, file_: str) -> int:
    file_relative_path: str = os.path.sep.join(file_.split(os.path.sep)[1:])
    file_path: str = os.path.join(repo, file_relative_path)
    return count_loc(file_path)


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


def get_repo_author_contributions(repo: Git) -> Tuple[Dict[str, float], float]:
    """
    Analyzes a git repository's history and returns a tuple containing:
        - A dictionary with the repo's authors and the percentage of commits
          they contributed.
        - The mean contribution value taken from all the authors.
    """
    authors_commit_contribution: Dict[str, int] = {}
    repo_history: List[str] = repo.log('--pretty=%ae').split('\n')
    total_commits: int = len(repo_history)
    for author_email in repo_history:
        if author_email in authors_commit_contribution:
            authors_commit_contribution[author_email] += 1
        else:
            authors_commit_contribution[author_email] = 1
    authors_percentage_contribution: Dict[str, float] = {
        author: round(commit * 100 / total_commits, 3)
        for author, commit in authors_commit_contribution.items()
    }
    percentages: List[float] = list(authors_percentage_contribution.values())
    mean_contribution: float = round(sum(percentages) / len(percentages), 3)
    return authors_percentage_contribution, mean_contribution
