"""
Produce a dataframe with commit metadata for a subscription in CSV format
out of open vulnerabilities json from integrates API
"""

import os
import random
import time
from itertools import filterfalse
from typing import Dict, List, Tuple, Set, Union

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
from toolbox.sorts.utils import (
    fill_model_commit_features,
    fill_model_file_features
)


PATH_DELIMITER = os.path.sep
MAX_RETRIES = 15

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


def build_vulnerabilities_df(
    group: str,
    fusion_path: str,
    scope: str
) -> DataFrame:
    """
    Creates a DataFrame with vulnerable and safe files/commits extracted
    from the Integrates API and the subscription repositories
    """
    print('Building vulnerabilities DataFrame...')
    timer: float = time.time()
    vuln_files, _, vuln_repos = get_unique_vuln_files(group)
    vuln_files, vuln_repos = filter_vuln_files(
        vuln_files, vuln_repos, fusion_path
    )
    print(
        f'Vulnerable files extracted after {time.time() - timer:.2f} seconds'
    )
    timer = time.time()
    if scope == 'file':
        safe_files = get_safe_files(vuln_files, vuln_repos, fusion_path)
        print(f'Safe files extracted after {time.time() - timer:.2f} seconds')
        vulns_df = pd.concat([
            pd.DataFrame(
                map(lambda x: (x, 1), vuln_files),
                columns=['file', 'is_vuln']
            ),
            pd.DataFrame(
                map(lambda x: (x, 0), safe_files),
                columns=['file', 'is_vuln']
            ),
        ])
    if scope == 'commit':
        vulns_files_df = pd.DataFrame(vuln_files, columns=['file'])
        vulns_files_df[['commit', 'hour']] = vulns_files_df.apply(
            get_intro_commit,
            args=(fusion_path,),
            axis=1,
            result_type='expand'
        )
        vuln_commits_df = make_commit_df(vulns_files_df)
        safe_commits_df = get_safe_commits_df(
            vuln_commits_df, vuln_repos, fusion_path
        )
        print(
            f'Safe commits extracted after {time.time() - timer:.2f} seconds'
        )
        vulns_df = pd.concat([vuln_commits_df, safe_commits_df])
        vulns_df['is_vuln'] = vulns_df['vulns'].apply(np.sign)
    vulns_df['repo'] = vulns_df['file'].apply(
        lambda filename: os.path.join(
            fusion_path, filename.split(PATH_DELIMITER)[0]
        )
    )
    vulns_df.reset_index(drop=True, inplace=True)
    return vulns_df


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


def get_safe_commits_df(
    vuln_commits_df: DataFrame,
    vuln_repos: List[str],
    fusion_path: str
) -> DataFrame:
    """
    Balance the dataset by adding as many 'safe' commits as there are
    vulnerable commits in the given dataset, chosen at random
    """
    safe_commits: List[List[Union[int, str]]] = []
    retries: int = 0
    while len(safe_commits) < len(vuln_commits_df):
        if retries > MAX_RETRIES:
            print('Could not find safe commit that matches all conditions')
            break
        repo = random.choice(vuln_repos)
        git_repo: Git = git.Git(os.path.join(fusion_path, repo))
        try:
            commits: List[str] = git_repo.log(
                '--pretty=%H,%aI'
            ).split('\n')
            rand_commit: str = random.choice(commits)
            commit_hash: str = rand_commit.split(',')[0]
            commit_hour: str = rand_commit.split(',')[1].split('T')[1]\
                .split(':')[0]
            commit_files: List[str] = git_repo.show(
                '--name-only',
                '--pretty=format:',
                commit_hash
            ).split('\n')
            file_: str = random.choice(commit_files)
            if not file_.strip():
                continue  # ok, just make another random choice
            if commit_hash not in vuln_commits_df['commit'].values:
                file_ = os.path.join(repo, file_)
                safe_commits.append([commit_hash, file_, 0, commit_hour])
                retries = 0
        except CommandError:
            continue  # ok, just make another random choice
        retries += 1
    safe_commits_df: DataFrame = pd.DataFrame(
        safe_commits,
        columns=['commit', 'file', 'vulns', 'hour']
    )
    return safe_commits_df


def get_safe_files(
    vuln_files: List[str],
    vuln_repos: List[str],
    fusion_path: str
) -> List[str]:
    safe_files: Set[str] = set()
    retries: int = 0
    extensions = read_lst(f'{os.path.dirname(__file__)}/extensions.lst')
    composites = read_lst(f'{os.path.dirname(__file__)}/composites.lst')
    repo_files: Dict[str, List[str]] = {}
    while len(safe_files) < len(vuln_files):
        if retries > MAX_RETRIES:
            print('Could not find a safe file that matches the conditions')
            break
        repo = random.choice(vuln_repos)
        if repo not in repo_files.keys():
            repo_files[repo] = [
                os.path.join(path, filename).replace(
                    f'{fusion_path}{PATH_DELIMITER}', ''
                )
                for path, _, files in os.walk(os.path.join(fusion_path, repo))
                for filename in files
            ]
        file_ = random.choice(repo_files[repo]) if repo_files[repo] else ''
        if (
            file_ and
            file_ not in vuln_files and
            file_ not in composites and
            os.path.splitext(file_)[1].strip('.') in extensions
        ):
            safe_files.add(file_)
            retries = 0
        retries += 1
    return sorted(safe_files)


def get_unique_vuln_files(group: str) -> Tuple[List[str], int, List[str]]:
    """
    Given vulnerabilities in JSON format, return a sorted list
    containing the vulnerable files, the total number of open vulnerabilities
    reported in the project, and a sorted list of the vulnerable repositories.
    """
    unique_vuln_files: Set[str] = set()
    unique_vuln_repos: Set[str] = set()
    total_vulns: int = 0
    query = integrates.Queries.wheres(API_TOKEN, group)
    if query.ok:
        response: ResponseType = query.data
        for finding in response['project']['findings']:
            vulns: List[VulnerabilityType] = [
                vuln for vuln in finding['vulnerabilities']
                if vuln['vulnType'] == 'lines'
            ]
            if vulns:
                total_vulns += len(vulns)
                for vuln in vulns:
                    vuln_file: str = vuln['where']
                    vuln_repo: str = vuln_file.split(PATH_DELIMITER)[0]
                    unique_vuln_files.add(vuln_file)
                    unique_vuln_repos.add(vuln_repo)
    else:
        print(f'There was an error fetching vulnerabilities for group {group}')
    return sorted(unique_vuln_files), total_vulns, sorted(unique_vuln_repos)


def test_repo(fusion_path: str, repo: str) -> bool:
    """
    Test if a repository is ok by executing a single `git log` on it.
    """
    repo_path: str = os.path.join(fusion_path, repo)
    git_repo: Git = git.Git(repo_path)
    repo_ok: bool = True
    try:
        git_repo.log()
    except CommandError:
        repo_ok = False
    return repo_ok


def get_bad_repos(fusion_path: str, repos: List[str]) -> List[str]:
    """
    Filter a list of repos, returning the bad ones
    """
    bad_repos: List[str] = list(
        filterfalse(lambda x: test_repo(fusion_path, x), repos)
    )
    return bad_repos


def filter_vuln_files(
    vuln_files: List[str],
    vuln_repos: List[str],
    fusion_path: str
) -> DataFrame:
    """
    Filter files that comply with certain extensions and remove
    binaries and those that are stored in bad repositories
    """
    filtered_vuln_files: List[str] = []
    extensions = read_lst(f'{os.path.dirname(__file__)}/extensions.lst')
    composites = read_lst(f'{os.path.dirname(__file__)}/composites.lst')
    bad_repos = get_bad_repos(fusion_path, vuln_repos)
    for vuln_file in vuln_files:
        vuln_repo: str = vuln_file.split(PATH_DELIMITER)[0]
        vuln_file_name: str = os.path.basename(vuln_file)
        if vuln_repo not in bad_repos:
            vuln_file_extension: str = os.path.splitext(vuln_file_name)[1]\
                .strip('.')
            if vuln_file_extension in extensions or \
                    vuln_file_name in composites:
                filtered_vuln_files.append(vuln_file)
    return (
        filtered_vuln_files,
        [repo for repo in vuln_repos if repo not in bad_repos]
    )


def get_intro_commit(row: Series, fusion_path: str) -> Tuple[str, str]:
    """
    Given a vulnerable file, return the commit that introduced it,
    understood as the first commit that added that file
    (this rationale is subject to change).
    Obtained by doing a `git log` on the file and taking the last commit hash.
    """
    file_: str = row.file
    repo_name: str = file_.split(PATH_DELIMITER)[0]
    file_rest: str = '/'.join(file_.split(PATH_DELIMITER)[1:])
    intro_commit = ('', '')
    try:
        # this could be done after grouping by repo, not per-file
        git_repo: Git = git.Git(os.path.join(fusion_path, repo_name))
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


def get_project_data(subscription_path: str, scope: str) -> None:
    """
    Produce a dataframe with commit metadata for a project in csv format
    out of open vulnerabilities json from integrates API
    """
    if scope == 'commit':
        get_project_commit_data(subscription_path)
    if scope == 'file':
        get_project_file_data(subscription_path)


def get_project_commit_data(subscription_path: str) -> None:
    """
    Produce a DataFrame with commit metadata from a subscription,
    out of open vulnerabilities extracted from Integrates API.
    Export DataFrame to CSV file.
    """
    group: str = subscription_path.split(PATH_DELIMITER)[-1]
    fusion_path: str = os.path.join(subscription_path, 'fusion')
    vulns_df = build_vulnerabilities_df(group, fusion_path, 'commit')
    complete_df = fill_model_commit_features(vulns_df)
    complete_df.to_csv(f'{group}_commits_df.csv', index=False)


def get_project_file_data(subscription_path: str) -> None:
    """
    Produce a DataFrame with file metadata from a subscription,
    out of open vulnerabilities extracted from Integrates API.
    Export DataFrame to CSV file.
    """
    group: str = os.path.basename(os.path.normpath(subscription_path))
    fusion_path: str = os.path.join(subscription_path, 'fusion')
    vulns_df = build_vulnerabilities_df(group, fusion_path, 'file')
    if not vulns_df.empty:
        complete_df = fill_model_file_features(vulns_df, fusion_path)
        complete_df.to_csv(f'{group}_files_metadata.csv', index=False)
    else:
        print(f'Group {group} has an empty vulnerabilities DataFrame')
