"""
Produce a dataframe with commit metadata for a subscription in CSV format
out of open vulnerabilities json from integrates API
"""

import os
import random
from typing import Dict, List, Tuple, Set, Union

import git
import numpy as np
import pandas as pd
from git.exc import CommandError
from git.cmd import Git
from mypy_extensions import TypedDict
from pandas import DataFrame
from pandas.core.groupby import GroupBy
from pydriller.metrics.process.hunks_count import HunksCount

from toolbox.api import integrates
from toolbox.constants import API_TOKEN
from toolbox.sorts.utils import df_get_hunks


BASE_DIR: str = ''
INCL_PATH: str = os.path.dirname(__file__)


VulnerabilityType = TypedDict('VulnerabilityType', {
    'vulnType': str,
    'where': str
})
FindingType = TypedDict('FindingType', {
    'id': str,
    'vulnerabilities': List[VulnerabilityType],
})
ProjectType = TypedDict('ProjectType', {
    'findings': List[FindingType],
})
ResponseType = TypedDict('ResponseType', {
    'project': ProjectType
})


def read_lst(path: str) -> List[str]:
    """
    Read file and return a list of its contents
    """
    lst: List[str] = []
    with open(path) as lstfile:
        lst = lstfile.read().split('\n')
        if '' in lst:
            lst.remove('')
    return lst


def get_unique_wheres(subs: str) -> Tuple[List[str], int, Set[str]]:
    """
    Given vulnerabilities in graphQL format, return a sorted set
    containing the vulnerable files and the total number of vulnerabilities
    reported as open in the project.
    """
    wheres_uniq: Set[str] = set()
    total_wheres: int = 0
    repos: Set[str] = set()

    response = integrates.Queries.wheres(API_TOKEN, subs)
    wheres_dict: ResponseType = response.data
    for finding in wheres_dict['project']['findings']:
        vulns: List[VulnerabilityType] = [
            vuln for vuln in finding['vulnerabilities']
            if vuln['vulnType'] == 'lines'
        ]
        total_wheres += len(vulns)
        if vulns:
            for vuln in vulns:
                where: str = vuln['where']
                # could test each where here
                repo: str = where.split('/')[0]
                # but testing each repo here would be redundant
                repos.add(repo)
                wheres_uniq.add(where)
    sorted_wheres_uniq: List[str] = sorted(list(wheres_uniq))
    return sorted_wheres_uniq, total_wheres, repos


def test_repo(repo_name: str) -> bool:
    """
    Test if a repo is ok by executing a single `git log` on it.
    """
    path: str = BASE_DIR + repo_name
    repo: Git = git.Git(path)
    rpok: bool = True
    try:
        repo.log()
    except CommandError:
        rpok = False
    return rpok


def get_bad_repos(repos: Set[str]) -> List[str]:
    """Filter a list of repos, returning the bad ones"""
    filt: List[str] = list(filter(lambda x: not test_repo(x), repos))
    return filt


def filter_code_files(wheres: List[str], bad_repos: List[str]) -> DataFrame:
    """
    Filter files that comply with certain extensions and remove
    binaries and those that are stored in bad repositories
    """
    wheres_code: List[str] = []
    extensions = read_lst(f'{INCL_PATH}/extensions.lst')
    composites = read_lst(f'{INCL_PATH}/composites.lst')
    for file_ in wheres:
        repo: str = file_.split('/')[0]
        name: str = file_.split('/')[-1]
        if repo not in bad_repos:
            extn: str = file_.split('.')[-1]
            if extn in extensions or name in composites:
                wheres_code.append(file_)
    wheres_code_df: DataFrame = pd.DataFrame(wheres_code, columns=['file'])
    return wheres_code_df


def get_intro_commit(file_: str) -> str:
    """
    Given a vulnerable file, return the commit that introduced it,
    understood as the first commit that added that file
    (this rationale is subject to change).
    Obtained by doing a `git log` on the file and taking the last commit hash.
    """
    repo_name: str = file_.split('/')[0]
    file_rest: str = '/'.join(file_.split('/')[1:])
    intro_commit: str = ''
    repo_ok = test_repo(repo_name)
    if repo_ok:
        try:
            # this could be done after grouping by repo, not per-file
            git_repo: Git = git.Git(BASE_DIR + repo_name)
            hashes_log: str = git_repo.log(
                '--pretty=%H',
                '--follow',
                '--',
                file_rest
            )
            hashes_list: List[str] = hashes_log.split('\n')
            intro_commit = hashes_list[-1]
        except FileNotFoundError:
            intro_commit = 'file_not_found'
    else:
        intro_commit = 'repo_not_found'
    return intro_commit


def make_commit_df(files_df: DataFrame) -> DataFrame:
    """
    Turn the wheres dataframe into a commit dataframe by grouping
    by commit, keeping one sample filename per commit, and the number
    of vulnerable files introduced by the commit.
    """
    groups: GroupBy = files_df.groupby('commit')
    # np.min on the 'file' column just to get a sample file, discard rest
    # np.size = #files tainted by commit < number of vulns (many per file)
    commit_df: DataFrame = pd.DataFrame(groups['file'].agg([np.min, np.size]))
    commit_df.reset_index(inplace=True)
    commit_df.rename(columns={'amin': 'file', 'size': 'vulns'}, inplace=True)
    return commit_df


def balance_df(vuln_df: DataFrame) -> DataFrame:
    """
    Balance the dataset by adding as many 'safe' commits as there are
    vulnerable commits in the given dataset, chosen at random
    """
    df_skel: List[List[Union[int, str]]] = []
    count: int = 0
    goal: int = len(vuln_df)
    repos_dirs: List[str] = os.listdir(BASE_DIR)

    while count < goal:
        rand_repo: str = random.choice(repos_dirs)
        rand_repo_git: Git = git.Git(BASE_DIR + rand_repo)
        try:
            hashes: List[str] = rand_repo_git.log('--pretty=%H').split('\n')
            rand_hash: str = random.choice(hashes)
            samp_files: List[str] = rand_repo_git.show(
                '--name-only',
                '--pretty=format:',
                rand_hash
            ).split('\n')
            samp_file: str = random.choice(samp_files)
            if not samp_file.strip():
                continue  # ok, just make another random choice
            if rand_hash not in vuln_df['commit'].values:
                samp_file = rand_repo + '/' + samp_file
                df_skel.append([rand_hash, samp_file, 0])
                count += 1
        except CommandError:
            continue  # ok, just make another random choice
    safe_commits: DataFrame = pd.DataFrame(
        df_skel,
        columns=['commit', 'file', 'vulns']
    )
    return safe_commits


def get_project_data(subs: str) -> None:
    """
    Produce a dataframe with commit metadata for a project in csv format
    out of open vulnerabilities json from integrates API
    """
    global BASE_DIR  # pylint: disable=global-statement
    BASE_DIR = f'groups/{subs}/fusion/'
    wheres_uniq, _, repos = get_unique_wheres(subs)
    bad_repos = get_bad_repos(repos)
    wheres_code = filter_code_files(wheres_uniq, bad_repos)
    wheres_code['commit'] = wheres_code['file'].apply(get_intro_commit)
    vuln_commits = make_commit_df(wheres_code)
    safe_commits = balance_df(vuln_commits)
    balanced_commits: DataFrame = pd.concat([vuln_commits, safe_commits])
    balanced_commits.reset_index(drop=True, inplace=True)
    balanced_commits['hunks'] = balanced_commits.apply(df_get_hunks, axis=1)
    balanced_commits.to_csv(f'{subs}_commits_df.csv',
                            index=False)
