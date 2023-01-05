from dal.model import (
    Pipeline,
    PullRequest,
    TestData,
)
import re
from typing import (
    Any,
)
from utils.logs import (
    log,
)


def get_err_log(should_fail: bool) -> str:
    err_log: str = "error" if should_fail else "warn"
    return err_log


def skip_ci(pull_request: PullRequest) -> bool:
    return "[skip ci]" in pull_request.title


def pr_under_max_deltas(*, data: TestData) -> bool:
    """PR deltas under max_deltas"""
    success: bool = False
    should_fail: bool = data.config["fail"]
    err_log: str = get_err_log(should_fail)
    skip_deltas: bool = "- no-deltas-test" in data.pull_request.description
    if skip_deltas:
        success = True
    else:
        deltas: int = data.pull_request.deltas
        max_deltas: int = data.config["max_deltas"]
        success = deltas <= max_deltas
        if not success:
            log(
                err_log,
                "PRs should be under or equal to %s deltas.\n"
                "This one has %s deltas.\n"
                "You can run 'git diff --stat' locally "
                "to know the staged deltas.\n"
                "You can also add the '- no-deltas-test' "
                "directive to your commit message "
                "in case skipping this test is mandatory.",
                max_deltas,
                deltas,
            )
    return success or not should_fail


def first_pipeline_successful(*, data: TestData) -> bool:
    """Test if first pipeline was successful"""
    success: bool = False
    should_fail: bool = data.config["fail"]
    err_log: str = get_err_log(should_fail)
    pipelines: list[Pipeline] = data.pull_request.pipelines()
    if len(pipelines) < 1:
        log(
            err_log,
            "This pull request does not have any associated pipelines.",
        )
    else:
        first: Pipeline = pipelines[-1]
        success = first.status in ("success", "manual")
        if not success:
            log(
                err_log,
                "Pipeline: %s\n Has status: %s\n",
                first.url,
                first.status,
            )
    return success or not should_fail


def pr_message_equals_commit_message(*, data: TestData) -> bool:
    """PR message equals commit message"""
    should_fail: bool = data.config["fail"]
    err_log: str = get_err_log(should_fail)
    pr_msg: str = (
        f"{data.pull_request.title}\n\n{data.pull_request.description}\n"
    )
    commit_msg: str = list(data.pull_request.commits())[0].message
    success: bool = pr_msg == commit_msg
    if not success:
        log(
            err_log,
            "PR message is not equal to commit message. \n\n"
            "PR message:\n"
            "%s\n\n"
            "Commit message:\n"
            "%s\n\n",
            pr_msg,
            commit_msg,
        )
    return success or not should_fail


def branch_equals_to_user(*, data: TestData) -> bool:
    """Test if branch name differs from user name"""
    success: bool = True
    should_fail: bool = data.config["fail"]
    err_log: str = get_err_log(should_fail)
    source_branch: str = data.pull_request.source_branch
    author: str = data.pull_request.author["username"]
    if source_branch not in author:
        log(
            err_log,
            "Your branch name should be equal to your gitlab user.\n\n"
            "Branch name: %s\n"
            "Gitlab user: %s",
            source_branch,
            author,
        )
        success = False
    return success or not should_fail


def commit_user_syntax(*, data: TestData) -> bool:
    """Test if username of commit associated to PR is compliant"""
    should_fail: bool = data.config["fail"]
    err_log: str = get_err_log(should_fail)
    commit: Any = list(data.pull_request.commits())[0]
    success: bool = bool(re.match(data.syntax.user_regex, commit.author_name))
    if not success:
        log(
            err_log,
            "All commits should have a valid commit user. \n\n"
            "A commit had user %s.\n"
            "Please make sure to use the following syntax: \n"
            "Capitalized name, space and capitalized lastname "
            "(avoid accents and ñ). \n"
            "For example: Aureliano Buendia \n"
            "You can change your git user by running: \n"
            'git config --global user.name "Aureliano Buendia"',
            commit.author_name,
        )
    return success or not should_fail


def pr_user_syntax(*, data: TestData) -> bool:
    """Test if username of PR author is compliant"""
    should_fail: bool = data.config["fail"]
    err_log: str = get_err_log(should_fail)
    author: str = data.pull_request.author["name"]
    success: bool = bool(re.match(data.syntax.user_regex, author))
    if not success:
        log(
            err_log,
            "Your gitlab user name is %s. \n"
            "Please make sure to use the following syntax: \n"
            "Capitalized name, space and capitalized lastname "
            "(avoid accents and ñ). \n"
            "For example: Aureliano Buendia. \n"
            "You can change your gitlab user name here: \n"
            "https://gitlab.com/-/profile",
            author,
        )
    return success or not should_fail


def pr_max_commits(*, data: TestData) -> bool:
    """Only max_commits per PR"""
    success: bool = True
    should_fail: bool = data.config["fail"]
    err_log: str = get_err_log(should_fail)
    max_commits: int = data.config["max_commits"]
    commit_number: int = len(list(data.pull_request.commits()))
    if commit_number > max_commits:
        success = False
        log(
            err_log,
            "This PR adds %s commits.\n"
            "A maximum of %s commits per PR are recommended.\n"
            "Make sure to use git squash",
            commit_number,
            max_commits,
        )
    return success or not should_fail
