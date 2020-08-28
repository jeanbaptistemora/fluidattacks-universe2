import re

import git
import numpy as np
from git.exc import GitCommandError
from pydriller.metrics.process.hunks_count import HunksCount


def df_get_deltas(row):
    """
    Get deltas information for an entire dataframe
    """
    repo = row['repo']
    commit = row['commit']
    return get_deltas(repo, commit)


def df_get_files(row):
    """
    Get information about modified files for an entire dataframe
    """
    repo = row['repo']
    commit = row['commit']
    return get_files(repo, commit)


def df_get_hunks(row):
    """
    Get number of hunks for an entire dataframe
    """
    repo = row['repo']
    commit = row['commit']
    return get_hunks(repo, commit)


def get_deltas(repo, commit):
    """
    Evaluate a commit and get the number of lines that were added and deleted,
    plus the number of deltas
    """
    deltas_info = (np.nan) * 4
    try:
        gitrepo = git.Git(repo)
        shortstat = gitrepo.show('--shortstat', '--pretty=format:', commit)
        match = re.search(r'(\d+) ins', shortstat)
        add = int(match.group(1) if match else 0)
        match = re.search(r'(\d+) del', shortstat)
        rem = int(match.group(1) if match else 0)
        net = add - rem
        tou = add + rem
        deltas_info = add, rem, net, tou
    except GitCommandError:
        print(f'error with repo {repo}')
        print('commit', commit)
    except IndexError:
        print('shortstat error:', shortstat)
    return deltas_info


def get_files(repo, commit):
    touchers = []
    try:
        gitrepo = git.Git(repo)
        filenames = gitrepo.show('--name-only', '--pretty=format:', commit)
        for file_ in filenames.split('\n'):
            authors = gitrepo.log('--follow', '--pretty=%aE', '--', file_)
            num_file_touchers = len(set(authors.split('\n')))
            touchers.append(num_file_touchers)
        touchers = np.array(touchers)
    except GitCommandError:
        print(f'Error with repo {repo}')
        print('Commit', commit)
    except IndexError:
        print('Shortstat error:', repo)
    return np.array(touchers)


def get_hunks(repo, commit):
    """Get number of hunks introduced by given commit in given repo"""
    metric = HunksCount(path_to_repo=repo,
                        from_commit=commit, to_commit=commit)
    files = metric.count()
    hunks = sum(files.values())
    return hunks
