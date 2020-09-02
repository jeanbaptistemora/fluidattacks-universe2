"""
Produce a dataframe with commit metadata for a subscription in CSV format
out of open vulnerabilities json from integrates API
"""

import os
import random
from typing import List, Tuple, Set, Union

import git
import numpy as np
import pandas as pd
from git.cmd import Git
from git.exc import CommandError
from mypy_extensions import TypedDict
from pandas import DataFrame, Series
from pandas.core.groupby import GroupBy

from toolbox.api import integrates
from toolbox.constants import API_TOKEN
from toolbox.sorts.utils import fill_model_features


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


def get_unique_wheres(group: str) -> Tuple[List[str], int, Set[str]]:
    """
    Given vulnerabilities in graphQL format, return a sorted set
    containing the vulnerable files and the total number of vulnerabilities
    reported as open in the project.
    """
    wheres_uniq: Set[str] = set()
    total_wheres: int = 0
    repos: Set[str] = set()
    response = integrates.Queries.wheres(API_TOKEN, group)
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


def test_repo(repo_name: str, fusion_path: str) -> bool:
    """
    Test if a repo is ok by executing a single `git log` on it.
    """
    path: str = fusion_path + repo_name
    repo: Git = git.Git(path)
    rpok: bool = True
    try:
        repo.log()
    except CommandError:
        rpok = False
    return rpok


def get_bad_repos(repos: Set[str], fusion_path: str) -> List[str]:
    """Filter a list of repos, returning the bad ones"""
    filt: List[str] = list(
        filter(lambda x: not test_repo(x, fusion_path), repos)
    )
    return filt


def filter_code_files(wheres: List[str], bad_repos: List[str]) -> DataFrame:
    """
    Filter files that comply with certain extensions and remove
    binaries and those that are stored in bad repositories
    """
    wheres_code: List[str] = []
    extensions = read_lst(f'{os.path.dirname(__file__)}/extensions.lst')
    composites = read_lst(f'{os.path.dirname(__file__)}/composites.lst')
    for file_ in wheres:
        repo: str = file_.split('/')[0]
        name: str = file_.split('/')[-1]
        if repo not in bad_repos:
            extn: str = file_.split('.')[-1]
            if extn in extensions or name in composites:
                wheres_code.append(file_)
    wheres_code_df: DataFrame = pd.DataFrame(wheres_code, columns=['file'])
    return wheres_code_df


def get_intro_commit(row: Series, fusion_path: str) -> Tuple[str, str]:
    """
    Given a vulnerable file, return the commit that introduced it,
    understood as the first commit that added that file
    (this rationale is subject to change).
    Obtained by doing a `git log` on the file and taking the last commit hash.
    """
    file_: str = row.file
    repo_name: str = file_.split('/')[0]
    file_rest: str = '/'.join(file_.split('/')[1:])
    intro_commit = ('', '')
    try:
        # this could be done after grouping by repo, not per-file
        git_repo: Git = git.Git(fusion_path + repo_name)
        hashes_log: str = git_repo.log(
            '--pretty=%H,%aI',
            '--follow',
            '--',
            file_rest
        )
        hashes_list: List[str] = hashes_log.split('\n')
        last_commit_info = hashes_list[-1].split(',')
        intro_commit = (
            last_commit_info[0],
            last_commit_info[1].split('T')[1].split(':')[0]
        )
    except FileNotFoundError:
        intro_commit = 'file_not_found', ''
    return intro_commit


def make_commit_df(files_df: DataFrame) -> DataFrame:
    """
    Turn the wheres dataframe into a commit dataframe by grouping
    by commit, keeping one sample filename per commit, and the number
    of vulnerable files introduced by the commit.
    """
    groups: GroupBy = files_df.groupby('commit')
    # np.min to get a sample file per commit, discard  the rest
    # np.size = # of files tainted by commit < number of vulns (many per file)
    commit_df: DataFrame = pd.DataFrame(groups.agg([np.min, np.size]))
    commit_df.reset_index(inplace=True)
    commit_df.columns = ['commit', 'file', 'vulns', 'hour', 'size']
    # Last column is not necessary since it's a duplicated
    # from the 'vulns' column
    commit_df = commit_df.drop(columns=['size'])
    return commit_df


def balance_df(vuln_df: DataFrame, fusion_path: str) -> DataFrame:
    """
    Balance the dataset by adding as many 'safe' commits as there are
    vulnerable commits in the given dataset, chosen at random
    """
    df_skel: List[List[Union[int, str]]] = []
    count: int = 0
    goal: int = len(vuln_df)
    repos_dirs: List[str] = os.listdir(fusion_path)
    while count < goal:
        rand_repo: str = random.choice(repos_dirs)
        rand_repo_git: Git = git.Git(fusion_path + rand_repo)
        try:
            commits: List[str] = rand_repo_git.log(
                '--pretty=%H,%aI'
            ).split('\n')
            rand_commit: str = random.choice(commits)
            rand_hash: str = rand_commit.split(',')[0]
            rand_hour: str = rand_commit.split(',')[1].split('T')[1]\
                .split(':')[0]
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
                df_skel.append([rand_hash, samp_file, 0, rand_hour])
                count += 1
        except CommandError:
            continue  # ok, just make another random choice
    safe_commits: DataFrame = pd.DataFrame(
        df_skel,
        columns=['commit', 'file', 'vulns', 'hour']
    )
    return safe_commits


def get_project_data(subscription_path: str) -> None:
    """
    Produce a dataframe with commit metadata for a project in csv format
    out of open vulnerabilities json from integrates API
    """
    group: str = subscription_path.split('/')[-1]
    fusion_path: str = f'{subscription_path}/fusion/'
    wheres_uniq, _, repos = get_unique_wheres(group)
    bad_repos = get_bad_repos(repos, fusion_path)
    wheres_code = filter_code_files(wheres_uniq, bad_repos)
    wheres_code[['commit', 'hour']] = wheres_code.apply(
        get_intro_commit,
        args=(fusion_path,),
        axis=1,
        result_type='expand'
    )
    vuln_commits = make_commit_df(wheres_code)
    safe_commits = balance_df(vuln_commits, fusion_path)
    balanced_commits: DataFrame = pd.concat([vuln_commits, safe_commits])
    balanced_commits.reset_index(drop=True, inplace=True)
    balanced_commits['repo'] = balanced_commits['file'].apply(
        lambda filename: f'{fusion_path}{filename.split("/")[0]}'
    )
    balanced_commits['is_vuln'] = balanced_commits['vulns'].apply(np.sign)
    complete_df = fill_model_features(balanced_commits)
    complete_df.to_csv(f'{group}_commits_df.csv', index=False)
