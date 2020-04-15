"""Produce a dataframe with commit metadata for a project in csv format
out of open vulnerabilities json from integrates API"""

import json
import os
import random

import git
import numpy as np
from git.exc import CommandError
import pandas as pd
from pydriller.metrics.process.hunks_count import HunksCount

BASE_DIR = f'subscriptions/waggo/fusion/'
INCL_PATH = os.path.dirname(__file__)


def read_lst(path):
    """Read lst file for extensions, etc"""
    with open(path) as lstfile:
        lst = lstfile.read().split('\n')
        if '' in lst:
            lst.remove('')
    return lst


EXTS = read_lst(f'{INCL_PATH}/extensions.lst')
COMP = read_lst(f'{INCL_PATH}/composites.lst')


def get_unique_wheres(wheres):
    """Given wheres in graphQL format, return a sorted list containing the
    vulnerable files and the total number of vulnerabilities
    reported as open in the project."""
    wheres_uniq = set()
    total_wheres = 0
    repos = set()
    for finding in wheres['data']['project']['findings']:
        vulns = finding['vulnerabilities']
        total_wheres += len(vulns)
        if vulns:
            for vuln in vulns:
                where = vuln['where']
                # could test each where here
                repo = where.split('/')[0]
                # but testing each repo here would be redundant
                repos.add(repo)
                wheres_uniq.add(where)
    sorted_wheres_uniq = sorted(list(wheres_uniq))
    return sorted_wheres_uniq, total_wheres, repos


def test_repo(repo_name):
    """Test if a repo is ok by executing a single `git log` on it."""
    path = BASE_DIR + repo_name
    repo = git.Git(path)
    rpok = True
    try:
        repo.log()
    except CommandError:
        rpok = False
    return rpok


def get_bad_repos(repos):
    """Filter a list of repos, returning the bad ones"""
    filt = list(filter(lambda x: not test_repo(x), repos))
    return filt


def filter_code_files(wheres, bad_repos):
    """"Select only code files from a list of wheres, discarding binaries, etc.
    Also skip files from bad_repos.
    """
    wheres_code = []
    for file in wheres:
        repo = file.split('/')[0]
        name = file.split('/')[-1]
        if repo not in bad_repos:
            extn = file.split('.')[-1]
            if extn in EXTS or name in COMP:
                wheres_code.append(file)
    wheres_code_df = pd.DataFrame(wheres_code, columns=['file'])
    return wheres_code_df


def get_intro_commit(file):
    """Given a vulnerable file, return the commit that introduced it,
    understood as the first commit that added that file
    (this rationale is subject to change).
    Obtained by doing a `git log` on the file and taking the last commit hash.
    """
    repo_name = file.split('/')[0]
    file_rest = '/'.join(file.split('/')[1:])
    repo_ok = test_repo(repo_name)
    intro_commit = ''
    if repo_ok:
        try:
            # this could be done after grouping by repo, not per-file
            git_repo = git.Git(BASE_DIR + repo_name)
            hashes_log = git_repo.log('--pretty=%H', '--follow',
                                      '--', file_rest)
            hashes_list = hashes_log.split('\n')
            intro_commit = hashes_list[-1]
        except FileNotFoundError:
            intro_commit = 'file_not_found'
    else:
        intro_commit = 'repo_not_found'
    return intro_commit


def make_commit_df(files_df):
    """Turn the wheres dataframe into a commit dataframe by grouping
    by commit, keeping one sample filename per commit, and the number
    of vulnerable files introduced by the commit.
    """
    groups = files_df.groupby('commit')
    # np.min on the 'file' column just to get a sample file, discard rest
    # np.size = #files tainted by commit < number of vulns (many per file)
    commit_df = pd.DataFrame(groups['file'].agg([np.min, np.size]))
    commit_df.reset_index(inplace=True)
    commit_df.rename(columns={'amin': 'file', 'size': 'vulns'}, inplace=True)
    return commit_df


def get_row_hunks(row):
    """Get number of hunks corresponding to the commit in the given row"""
    repo = row['file'].split('/')[0]
    commit = row['commit']
    return get_hunks(repo, commit)


def get_hunks(repo, commit):
    """Get number of hunks introduced by given commit in given repo"""
    metric = HunksCount(path_to_repo=BASE_DIR + repo,
                        from_commit=commit, to_commit=commit)
    files = metric.count()
    hunks = sum(files.values())
    return hunks


def balance_df(vuln_df):
    """Balance the dataset by adding as many 'safe' commits as there are
    vulnerable commits in the given dataset, chosen at random"""
    df_skel = []
    count = 0
    goal = len(vuln_df)
    repos_dirs = os.listdir(BASE_DIR)
    while count < goal:
        rand_repo = random.choice(repos_dirs)
        rand_repo_git = git.Git(BASE_DIR + rand_repo)
        try:
            hashes = rand_repo_git.log('--pretty=%H').split('\n')
            rand_hash = random.choice(hashes)
            samp_files = rand_repo_git.show('--name-only', '--pretty=format:',
                                            rand_hash).split('\n')
            samp_file = random.choice(samp_files)
            if not samp_file.strip():
                continue  # ok, just make another random choice
            if rand_hash not in vuln_df['commit'].values:
                samp_file = rand_repo + '/' + samp_file
                df_skel.append([rand_hash, samp_file, 0])
                count += 1
        except CommandError:
            continue  # ok, just make another random choice
    safe_commits = pd.DataFrame(df_skel, columns=['commit', 'file', 'vulns'])
    return safe_commits


def get_project_data(subs):
    """Produce a dataframe with commit metadata for a project in csv format
    out of open vulnerabilities json from integrates API"""
    wheres_json = f'{subs}_wheres.json'
    global BASE_DIR  # pylint: disable=global-statement
    BASE_DIR = f'subscriptions/{subs}/fusion/'
    with open(wheres_json) as wheresfile:
        wheres = json.load(wheresfile)
    # wheres json comes from request to integrates api,
    # per project, obtained manually via graphiql
    wheres_uniq, _, repos = get_unique_wheres(wheres)
    bad_repos = get_bad_repos(repos)
    wheres_code = filter_code_files(wheres_uniq, bad_repos)
    wheres_code['commit'] = wheres_code['file'].apply(get_intro_commit)
    vuln_commits = make_commit_df(wheres_code)
    safe_commits = balance_df(vuln_commits)
    balanced_commits = pd.concat([vuln_commits, safe_commits])
    balanced_commits.reset_index(drop=True, inplace=True)
    balanced_commits['hunks'] = balanced_commits.apply(get_row_hunks, axis=1)
    balanced_commits.to_csv(f'{subs}_commits_df.csv',
                            index=False)
