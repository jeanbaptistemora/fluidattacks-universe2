# Standard libraries
import os
import re
import subprocess
from time import sleep
from typing import Any, List, Dict

# Third party libraries
from pygit2 import Repository, GitError

# Local libraries
from dal.model import PullRequest
from utils.logs import log


def get_err_log(should_fail: bool) -> str:
    err_log: str = 'error' if should_fail else 'warn'
    return err_log


def skip_ci(pull_request: PullRequest) -> bool:
    return '[skip ci]' in pull_request.title


def mr_under_max_deltas(pull_request: PullRequest, config: Dict[str, Any]) -> bool:
    """MR under max_deltas if commit is not solution"""
    success: bool = True
    should_fail: bool = config['fail']
    err_log: str = get_err_log(should_fail)
    repo_path = '.' if config['repo_path'] is None else config['repo_path']
    max_deltas: int = config['max_deltas']
    try:
        repo: Any = Repository(repo_path)
    except GitError:
        log('error',
            'You must be in the repo path in order '
            'to run this test')
        raise GitError
    skip_deltas: bool = '- no-deltas-test' in pull_request.description
    base_sha: str = str(pull_request.changes()['diff_refs']['base_sha'])
    head_sha: str = str(pull_request.changes()['diff_refs']['head_sha'])
    base_commit: Any = repo.revparse_single(base_sha)
    head_commit: Any = repo.revparse_single(head_sha)
    diff: Any = repo.diff(base_commit, head_commit)
    diff.find_similar()
    deltas: int = diff.stats.deletions + diff.stats.insertions
    if not skip_deltas and deltas > max_deltas:
        log(err_log,
            'MR should be under or equal to %s deltas. You MR has %s deltas',
            max_deltas,
            deltas)
        success = False
    return success or not should_fail


def all_pipelines_successful(pull_request: PullRequest, config: Dict[str, Any]) -> bool:
    """Test if all previous pipelines were successful"""

    def passed_first_pipeline_before_mr() -> bool:
        success: bool = True
        if config['passed_first_pipeline_before_mr']:
            first_pipeline: Any = pull_request.pipelines()[-1]
            if first_pipeline.status not in ('success', 'manual'):
                log(err_log,
                    'The Dev pipeline should pass before you open an MR.\n'
                    'Specifically, you opened your MR before %s passed.',
                    first_pipeline.web_url)
                success = False
        return success

    should_fail: bool = config['fail']
    err_log: str = get_err_log(should_fail)
    success: bool = passed_first_pipeline_before_mr()
    index: int = 0
    while index < len(pull_request.pipelines()):
        pipeline: Any = pull_request.pipelines()[index]
        p_id: str = str(pipeline.id)
        p_status: str = str(pipeline.status)
        p_job_names: List[str] = [ job.name for job in pipeline.jobs.list() ]
        if config['job_name'] not in p_job_names:
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


def mr_message_syntax(pull_request: PullRequest, config: Dict[str, Any]) -> bool:
    """Run commitlint on MR message"""
    success: bool = True
    should_fail: bool = config['fail']
    err_log: str = get_err_log(should_fail)
    mr_commit_msg: str = f'{pull_request.title}\n\n{pull_request.description}'
    command: List[str] = ['commitlint']
    proc: Any = subprocess.run(command, input=mr_commit_msg,
                               encoding='ascii', check=False)
    if proc.returncode != 0:
        log(err_log,
            'Commitlint tests failed. '
            'MR Message should be syntax compliant.')
        success = False
    return success or not should_fail


def branch_equals_to_user(pull_request: PullRequest, config: Dict[str, Any]) -> bool:
    """Test if branch name differs from user name"""
    success: bool = True
    should_fail: bool = config['fail']
    err_log: str = get_err_log(should_fail)
    if pull_request.source_branch not in pull_request.author['username']:
        log(err_log,
            'Your branch name should be equal to your gitlab user.\n\n'
            'Branch name: %s\n'
            'Gitlab user: %s',
            pull_request.source_branch,
            pull_request.author['username'])
        success = False
    return success or not should_fail


def most_relevant_type(pull_request: PullRequest, config: Dict[str, Any]) -> bool:
    """Test if MR message uses the most relevant type of all its commits"""
    success: bool = True
    should_fail: bool = config['fail']
    err_log: str = get_err_log(should_fail)
    commit_regex: str = config['commit_regex']
    relevances: Dict[str, int] = config['relevances']
    mr_title_match: Any = re.match(commit_regex, pull_request.title)
    if mr_title_match is None:
        success = False
    else:
        mr_title_matches: List[str] = list(mr_title_match.groups())
    commits: Any = pull_request.commits()
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


def commits_user_syntax(pull_request: PullRequest, config: Dict[str, Any]) -> bool:
    """Test if usernames of all commits associated to MR are compliant"""
    success: bool = True
    should_fail: bool = config['fail']
    err_log: str = get_err_log(should_fail)
    user_regex: str = config['user_regex']
    failed_user: str = ''
    commits: Any = pull_request.commits()
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


def mr_user_syntax(pull_request: PullRequest, config: Dict[str, Any]) -> bool:
    """Test if username of mr author is compliant"""
    success: bool = True
    should_fail: bool = config['fail']
    err_log: str = get_err_log(should_fail)
    user_regex: str = config['user_regex']
    if not re.match(user_regex, pull_request.author['name']):
        success = False
        log(err_log,
            'Your gitlab user name is %s. \n'
            'Please make sure to use the following syntax: \n'
            'Capitalized name, space and capitalized lastname '
            '(avoid accents and ñ). \n'
            'For example: Aureliano Buendia. \n'
            'You can change your gitlab user name here: \n'
            'https://gitlab.com/profile',
            pull_request.author['name'])
    return success or not should_fail


def max_commits_per_mr(pull_request: PullRequest, config: Dict[str, Any]) -> bool:
    """Only one commit per MR"""
    success: bool = True
    should_fail: bool = config['fail']
    err_log: str = get_err_log(should_fail)
    max_commits: int = config['max_commits']
    commit_number: int = len(list(pull_request.commits()))
    if commit_number > max_commits:
        success = False
        log(err_log,
            'This MR adds %s commits.\n'
            'A maximum of %s commits per MR are recommended.\n'
            'Make sure to use git squash',
            commit_number,
            max_commits)
    return success or not should_fail


def close_issue_directive(pull_request: PullRequest, config: Dict[str, Any]) -> bool:
    """Test if a MR has an issue different from #0 without a Close directive"""
    success: bool = True
    should_fail: bool = config['fail']
    err_log: str = get_err_log(should_fail)
    mr_title_regex: str = config['mr_title_regex']
    mr_title_match: Any = re.match(mr_title_regex, pull_request.title)
    if mr_title_match is None:
        success = False
    else:
        mr_title_matches: List[str] = list(mr_title_match.groups())
    if success and mr_title_matches[2] not in '#0' \
            and 'Closes #' not in pull_request.description:
        log(err_log,
            'This MR is referencing issue %s '
            'but it does not have a: Close %s '
            'in its footer. Was this intentional?',
            mr_title_matches[2],
            mr_title_matches[2])
        success = False
    return success or not should_fail
