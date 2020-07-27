# Standard libraries
import os
import re
import subprocess
from time import sleep
from typing import Any, List, Dict
from git import Repo

# Local libraries
from utils.logs import (
    log
)


def get_commit_by_sha(sha: str, repo: Any) -> Any:
    commits: Any = list(repo.iter_commits())
    found_commit: Any = None
    for commit in commits:
        if commit.hexsha in sha:
            found_commit = commit
            break
    return found_commit


def test_skip_ci(mr_info: Any) -> bool:
    return '[skip ci]' in mr_info.title


def test_mr_under_max_deltas(
        mr_info: Any,
        max_deltas: int,
        repo_path: str = '.') -> bool:
    """MR under max_deltas if commit is not solution"""
    log('info', 'Running test_mr_under_max_deltas')
    success: bool = True
    repo: Any = Repo(repo_path)
    skip_deltas: bool = '- no-deltas-test' in mr_info.description
    commit: Any = get_commit_by_sha(mr_info.changes()['sha'], repo)
    deltas: int = int(commit.stats.total['lines'])
    if not skip_deltas and deltas > max_deltas:
        log('error',
            'MR must be under or equal to %s deltas',
            max_deltas)
        success = False
    return success


def test_all_pipelines_successful(mr_info: Any) -> bool:
    """Test if all previous pipelines were successful"""
    log('info', 'Running test_all_pipelines_successful')
    success: bool = True
    current_p_id: str = str(os.environ.get('CI_PIPELINE_ID'))
    index: int = 0
    while index < len(mr_info.pipelines()):
        pipeline: Dict[str, str] = mr_info.pipelines()[index]
        p_id: str = str(pipeline['id'])
        p_status: str = str(pipeline['status'])
        if p_id not in current_p_id:
            if p_status in 'pending' or p_status in 'running':
                sleep(5)
                index = -1
            elif p_status not in 'success':
                log('error',
                    'Pipeline with ID %s '
                    'finished with status: %s, please '
                    'make sure to have all the pipelines associated '
                    'to your MR in green before re-running MR tests.',
                    p_id,
                    p_status)
                success = False
        index += 1
    return success


def test_mr_message(mr_commit_msg: str) -> bool:
    """Run commitlint on MR message"""
    log('info', 'Running test_mr_message')
    success: bool = True
    command: List[str] = ['commitlint']
    proc: Any = subprocess.run(command, input=mr_commit_msg,
                               encoding='ascii', check=False)
    if proc.returncode != 0:
        log('error',
            'Commitlint tests failed. '
            'MR Message must be syntax compliant.')
        success = False
    return success


def test_branch_equals_to_user(mr_info: Any) -> bool:
    """Test if branch name differs from user name"""
    log('info', 'Running test_branch_equals_to_user')
    success: bool = True
    if mr_info.source_branch not in mr_info.author['username']:
        log('error',
            'Your branch name must be equal to your gitlab user.\n\n'
            'Branch name: %s\n'
            'Gitlab user: %s',
            mr_info.source_branch,
            mr_info.author['username'])
        success = False
    return success


def test_most_relevant_type(
        mr_info: Any,
        mr_title_regex: str,
        relevances: Dict[str, int]) -> bool:
    """Test if MR message uses the most relevant type of all its commits"""
    log('info', 'Running test_most_relevant_type')
    success: bool = True
    mr_title_match: Any = re.match(mr_title_regex, mr_info.title)
    if mr_title_match is None:
        success = False
    else:
        mr_title_matches: List[str] = list(mr_title_match.groups())
    commits: Any = mr_info.commits()
    mr_title_type: str = mr_title_matches[0] if success else ''
    most_relevant_type: str = list(relevances.keys())[-1]
    for commit in commits:
        commit_title_match: Any = re.match(mr_title_regex, commit.title)
        if commit_title_match is None:
            log('error',
                'Commit title is not syntax compliant:\n%s',
                commit.title)
            success = False
            continue
        commit_title_type = commit_title_match.group(1)
        if commit_title_type in relevances.keys() and \
                relevances[commit_title_type] < relevances[most_relevant_type]:
            most_relevant_type = commit_title_type
    if success and mr_title_type not in most_relevant_type:
        log('error',
            'The most relevant type of all commits '
            'included in your MR is: %s\n'
            'The type used in your MR title is: %s\n'
            'Please make sure to change it.\n\n'
            'The relevance order is (from highest to lowest):\n\n%s',
            most_relevant_type,
            mr_title_type,
            relevances)
        success = False
    return success


def test_commits_user(mr_info: Any, commit_user_regex: str) -> bool:
    """Test if usernames of all commits associated to MR are compliant"""
    log('info', 'Running test_commits_user')
    success: bool = True
    failed_user: str = ''
    commits: Any = mr_info.commits()
    for commit in commits:
        if not re.match(commit_user_regex, commit.author_name):
            failed_user = commit.author_name
            success = False
            log('error',
                'All commits must have a valid commit user. \n\n'
                'A commit had user %s.\n'
                'Please make sure to use the following syntax: \n'
                'Capitalized name, space and capitalized lastname '
                '(avoid accents and ñ). \n'
                'For example: Aureliano Buendia \n'
                'You can change your git user by running: \n'
                'git config --global user.name "Aureliano Buendia"',
                failed_user)
            break
    return success


def test_mr_user(mr_info: Any, commit_user_regex: str) -> bool:
    """Test if gitlab username of mr author is compliant"""
    log('info', 'Running test_mr_user')
    success: bool = True
    if not re.match(commit_user_regex, mr_info.author['name']):
        success = False
        log('error',
            'Your gitlab user name is %s. \n'
            'Please make sure to use the following syntax: \n'
            'Capitalized name, space and capitalized lastname. \n'
            'For example: Aureliano Buendia. \n'
            'You can change your gitlab user name here: \n'
            'https://gitlab.com/profile',
            mr_info.author['name'])
    return success


def test_one_commit_per_mr(mr_info: Any) -> bool:
    """Only one commit per MR"""
    log('info', 'Running test_one_commit_per_mr')
    success: bool = True
    commit_number: int = len(list(mr_info.commits()))
    if commit_number > 1:
        success = False
        log('error',
            'This MR adds %s commits.'
            'Only one commit per MR is recommended.'
            'Make sure to use git squash',
            commit_number)
    return success


def test_close_issue_directive(mr_info: Any, mr_title_regex: str) -> bool:
    """Test if a MR has an issue different from #0 without a Closes directive"""
    log('info', 'Running test_close_issue_directive')
    success: bool = True
    mr_title_match: Any = re.match(mr_title_regex, mr_info.title)
    if mr_title_match is None:
        success = False
    else:
        mr_title_matches: List[str] = list(mr_title_match.groups())
    if success and mr_title_matches[2] not in '#0' \
            and 'Closes #' not in mr_info.description:
        log('error',
            'This MR is referencing issue %s '
            'but it does not have a: Close %s '
            'in its footer. Was this intentional?',
            mr_title_matches[2],
            mr_title_matches[2])
        success = False
    return success
