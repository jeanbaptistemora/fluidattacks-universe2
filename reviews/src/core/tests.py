# Standard libraries
import os
import re
import subprocess
from time import sleep
from typing import Any, List, Dict
from git import Repo, InvalidGitRepositoryError

# Local libraries
from utils.logs import (
    log
)


def get_err_log(should_fail: bool) -> str:
    err_log: str = 'error' if should_fail else 'warn'
    return err_log


def skip_ci(mr_info: Any) -> bool:
    return '[skip ci]' in mr_info.title


def mr_under_max_deltas(mr_info: Any, config: Dict[str, Any]) -> bool:
    """MR under max_deltas if commit is not solution"""

    def get_commit_by_sha(sha: str, repo: Any) -> Any:
        commits: Any = list(repo.iter_commits())
        found_commit: Any = None
        for commit in commits:
            if commit.hexsha in sha:
                found_commit = commit
                break
        return found_commit

    success: bool = True
    should_fail: bool = config['fail']
    err_log: str = get_err_log(should_fail)
    repo_path = '.' if config['repo_path'] is None else config['repo_path']
    max_deltas: int = config['max_deltas']
    try:
        repo: Any = Repo(repo_path)
    except InvalidGitRepositoryError:
        log('error',
            'You must be in the repo path in order '
            'to run this test')
        raise InvalidGitRepositoryError
    skip_deltas: bool = '- no-deltas-test' in mr_info.description
    commit: Any = get_commit_by_sha(mr_info.changes()['sha'], repo)
    deltas: int = int(commit.stats.total['lines'])
    if not skip_deltas and deltas > max_deltas:
        log(err_log,
            'MR should be under or equal to %s deltas',
            max_deltas)
        success = False
    return success or not should_fail


def all_pipelines_successful(mr_info: Any, config: Dict[str, Any]) -> bool:
    """Test if all previous pipelines were successful"""
    success: bool = True
    should_fail: bool = config['fail']
    err_log: str = get_err_log(should_fail)
    current_p_id: str = str(os.environ.get('CI_PIPELINE_ID'))
    index: int = 0
    while index < len(mr_info.pipelines()):
        pipeline: Dict[str, str] = mr_info.pipelines()[index]
        p_id: str = str(pipeline['id'])
        p_status: str = str(pipeline['status'])
        if p_id not in current_p_id:
            if p_status in ('success', 'manual'):
                pass
            elif p_status in ('pending', 'running'):
                sleep(5)
                index = -1
            else:
                log(err_log,
                    'Pipeline with ID %s '
                    'finished with status: %s, please '
                    'make sure to have all the pipelines associated '
                    'to your MR in green before re-running MR tests.',
                    p_id,
                    p_status)
                success = False
        index += 1
    return success or not should_fail


def mr_message_syntax(mr_info: Any, config: Dict[str, Any]) -> bool:
    """Run commitlint on MR message"""
    success: bool = True
    should_fail: bool = config['fail']
    err_log: str = get_err_log(should_fail)
    mr_commit_msg: str = f'{mr_info.title}\n\n{mr_info.description}'
    command: List[str] = ['commitlint']
    proc: Any = subprocess.run(command, input=mr_commit_msg,
                               encoding='ascii', check=False)
    if proc.returncode != 0:
        log(err_log,
            'Commitlint tests failed. '
            'MR Message should be syntax compliant.')
        success = False
    return success or not should_fail


def branch_equals_to_user(mr_info: Any, config: Dict[str, Any]) -> bool:
    """Test if branch name differs from user name"""
    success: bool = True
    should_fail: bool = config['fail']
    err_log: str = get_err_log(should_fail)
    if mr_info.source_branch not in mr_info.author['username']:
        log(err_log,
            'Your branch name should be equal to your gitlab user.\n\n'
            'Branch name: %s\n'
            'Gitlab user: %s',
            mr_info.source_branch,
            mr_info.author['username'])
        success = False
    return success or not should_fail


def most_relevant_type(mr_info: Any, config: Dict[str, Any]) -> bool:
    """Test if MR message uses the most relevant type of all its commits"""
    success: bool = True
    should_fail: bool = config['fail']
    err_log: str = get_err_log(should_fail)
    commit_regex: str = config['commit_regex']
    relevances: Dict[str, int] = config['relevances']
    mr_title_match: Any = re.match(commit_regex, mr_info.title)
    if mr_title_match is None:
        success = False
    else:
        mr_title_matches: List[str] = list(mr_title_match.groups())
    commits: Any = mr_info.commits()
    mr_title_type: str = mr_title_matches[0] if success else ''
    most_relevant_type: str = list(relevances.keys())[-1]
    for commit in commits:
        commit_title_match: Any = re.match(commit_regex, commit.title)
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
        log(err_log,
            'The most relevant type of all commits '
            'included in your MR is: %s\n'
            'The type used in your MR title is: %s\n'
            'Please make sure to change it.\n\n'
            'The relevance order is (from highest to lowest):\n\n%s',
            most_relevant_type,
            mr_title_type,
            relevances)
        success = False
    return success or not should_fail


def commits_user_syntax(mr_info: Any, config: Dict[str, Any]) -> bool:
    """Test if usernames of all commits associated to MR are compliant"""
    success: bool = True
    should_fail: bool = config['fail']
    err_log: str = get_err_log(should_fail)
    user_regex: str = config['user_regex']
    failed_user: str = ''
    commits: Any = mr_info.commits()
    for commit in commits:
        if not re.match(user_regex, commit.author_name):
            failed_user = commit.author_name
            success = False
            log(err_log,
                'All commits should have a valid commit user. \n\n'
                'A commit had user %s.\n'
                'Please make sure to use the following syntax: \n'
                'Capitalized name, space and capitalized lastname '
                '(avoid accents and ñ). \n'
                'For example: Aureliano Buendia \n'
                'You can change your git user by running: \n'
                'git config --global user.name "Aureliano Buendia"',
                failed_user)
            break
    return success or not should_fail


def mr_user_syntax(mr_info: Any, config: Dict[str, Any]) -> bool:
    """Test if gitlab username of mr author is compliant"""
    success: bool = True
    should_fail: bool = config['fail']
    err_log: str = get_err_log(should_fail)
    user_regex: str = config['user_regex']
    if not re.match(user_regex, mr_info.author['name']):
        success = False
        log(err_log,
            'Your gitlab user name is %s. \n'
            'Please make sure to use the following syntax: \n'
            'Capitalized name, space and capitalized lastname '
            '(avoid accents and ñ). \n'
            'For example: Aureliano Buendia. \n'
            'You can change your gitlab user name here: \n'
            'https://gitlab.com/profile',
            mr_info.author['name'])
    return success or not should_fail


def max_commits_per_mr(mr_info: Any, config: Dict[str, Any]) -> bool:
    """Only one commit per MR"""
    success: bool = True
    should_fail: bool = config['fail']
    err_log: str = get_err_log(should_fail)
    max_commits: int = config['max_commits']
    commit_number: int = len(list(mr_info.commits()))
    if commit_number > max_commits:
        success = False
        log(err_log,
            'This MR adds %s commits.\n'
            'A maximum of %s commits per MR are recommended.\n'
            'Make sure to use git squash',
            commit_number,
            max_commits)
    return success or not should_fail


def close_issue_directive(mr_info: Any, config: Dict[str, Any]) -> bool:
    """Test if a MR has an issue different from #0 without a Close directive"""
    success: bool = True
    should_fail: bool = config['fail']
    err_log: str = get_err_log(should_fail)
    mr_title_regex: str = config['mr_title_regex']
    mr_title_match: Any = re.match(mr_title_regex, mr_info.title)
    if mr_title_match is None:
        success = False
    else:
        mr_title_matches: List[str] = list(mr_title_match.groups())
    if success and mr_title_matches[2] not in '#0' \
            and 'Closes #' not in mr_info.description:
        log(err_log,
            'This MR is referencing issue %s '
            'but it does not have a: Close %s '
            'in its footer. Was this intentional?',
            mr_title_matches[2],
            mr_title_matches[2])
        success = False
    return success or not should_fail
