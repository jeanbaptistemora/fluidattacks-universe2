from dal.model import (
    PullRequest,
    TestData,
)
import os
from pygit2 import (
    GitError,
    Repository,
)
import re
import subprocess
from time import (
    sleep,
)
from typing import (
    Any,
    Dict,
    List,
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
    """PR under max_deltas if commit is not solution"""
    success: bool = True
    should_fail: bool = data.config["fail"]
    err_log: str = get_err_log(should_fail)
    repo_path = (
        "." if data.config["repo_path"] is None else data.config["repo_path"]
    )
    max_deltas: int = data.config["max_deltas"]
    try:
        repo: Any = Repository(repo_path)
    except GitError as exc:
        log(
            err_log,
            "You must be in the repo path in order to run this test",
        )
        raise exc
    skip_deltas: bool = "- no-deltas-test" in data.pull_request.description
    base_sha: str = str(data.pull_request.changes()["diff_refs"]["base_sha"])
    head_sha: str = str(data.pull_request.changes()["diff_refs"]["head_sha"])
    base_commit: Any = repo.revparse_single(base_sha)
    head_commit: Any = repo.revparse_single(head_sha)
    diff: Any = repo.diff(base_commit, head_commit)
    diff.find_similar()
    deltas: int = diff.stats.deletions + diff.stats.insertions
    if not skip_deltas and deltas > max_deltas:
        log(
            err_log,
            "PR should be under or equal to %s deltas. You PR has %s deltas",
            max_deltas,
            deltas,
        )
        success = False
    return success or not should_fail


def all_pipelines_successful(*, data: TestData) -> bool:
    """Test if all previous pipelines were successful"""
    should_fail: bool = data.config["fail"]
    err_log: str = get_err_log(should_fail)
    success: bool = True
    index: int = 0
    while index < len(data.pull_request.pipelines()):
        pipeline: Any = data.pull_request.pipelines()[index]
        p_jobs: Any = pipeline.jobs.list()
        p_jobs_names: List[str] = [job.name for job in p_jobs]
        if data.config["job_name"] not in p_jobs_names:
            for p_job in p_jobs:
                if p_job.status in ("success", "manual"):
                    # Nothing to assigned
                    pass
                elif p_job.status in ("pending", "running", "created"):
                    sleep(5)
                    index = -1
                else:
                    log(
                        err_log,
                        "Pipeline: %s\n"
                        "has the job: %s\n"
                        "with status: %s\n",
                        pipeline.web_url,
                        p_job.name,
                        p_job.status,
                    )
                    success = False
        index += 1
    return success or not should_fail


def pr_message_syntax(*, data: TestData) -> bool:
    """Run commitlint on PR message"""
    success: bool = True
    should_fail: bool = data.config["fail"]
    err_log: str = get_err_log(should_fail)
    pr_commit_msg: str = (
        f"{data.pull_request.title}\n\n{data.pull_request.description}"
    )
    command: List[str] = [
        "commitlint",
        "--parser-preset",
        os.path.abspath(data.config["parser"]),
        "--config",
        os.path.abspath(data.config["config"]),
    ]
    proc: Any = subprocess.run(
        command, input=pr_commit_msg, encoding="ascii", check=False
    )
    if proc.returncode != 0:
        log(
            err_log,
            "Commitlint tests failed. "
            "PR Message should be syntax compliant.",
        )
        success = False
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


def most_relevant_type(*, data: TestData) -> bool:
    """Test if PR message uses the most relevant type of all its commits"""
    success: bool = True
    should_fail: bool = data.config["fail"]
    err_log: str = get_err_log(should_fail)
    pr_match: Any = re.match(data.syntax.regex, data.pull_request.title)
    success = pr_match is not None
    pr_type: str = (
        pr_match.group(data.syntax.match_groups["type"]) if success else ""
    )
    relevances: Dict[str, int] = data.config["relevances"]
    highest_type: str = list(relevances.keys())[-1]
    commits: Any = data.pull_request.commits()
    for commit in commits:
        commit_match: Any = re.match(data.syntax.regex, commit.title)
        if commit_match is None:
            log(
                err_log,
                "Commit title is not syntax compliant:\n%s",
                commit.title,
            )
            success = False
            continue
        commit_type = commit_match.group(data.syntax.match_groups["type"])
        if (
            commit_type in relevances.keys()
            and relevances[commit_type] < relevances[highest_type]
        ):
            highest_type = commit_type
    if success and pr_type not in highest_type:
        log(
            err_log,
            "The most relevant type of all commits "
            "included in your PR is: %s\n"
            "The type used in your PR title is: %s\n"
            "Please make sure to change it.\n\n"
            "The relevance order is (from highest to lowest):\n\n%s",
            highest_type,
            pr_type,
            relevances,
        )
        success = False
    return success or not should_fail


def commits_user_syntax(*, data: TestData) -> bool:
    """Test if usernames of all commits associated to PR are compliant"""
    success: bool = True
    should_fail: bool = data.config["fail"]
    err_log: str = get_err_log(should_fail)
    failed_user: str = ""
    commits: Any = data.pull_request.commits()
    for commit in commits:
        if not re.match(data.syntax.user_regex, commit.author_name):
            failed_user = commit.author_name
            success = False
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
                failed_user,
            )
            break
    return success or not should_fail


def pr_user_syntax(*, data: TestData) -> bool:
    """Test if username of PR author is compliant"""
    success: bool = True
    should_fail: bool = data.config["fail"]
    err_log: str = get_err_log(should_fail)
    author: str = data.pull_request.author["name"]
    if not re.match(data.syntax.user_regex, author):
        success = False
        log(
            err_log,
            "Your gitlab user name is %s. \n"
            "Please make sure to use the following syntax: \n"
            "Capitalized name, space and capitalized lastname "
            "(avoid accents and ñ). \n"
            "For example: Aureliano Buendia. \n"
            "You can change your gitlab user name here: \n"
            "https://gitlab.com/profile",
            author,
        )
    return success or not should_fail


def pr_max_commits(*, data: TestData) -> bool:
    """Only one commit per PR"""
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


def close_issue_directive(*, data: TestData) -> bool:
    """Test if a PR has an issue different from #0 without a Close directive"""
    success: bool = True
    should_fail: bool = data.config["fail"]
    err_log: str = get_err_log(should_fail)
    pr_match: Any = re.match(data.syntax.regex, data.pull_request.title)
    pr_issue: str = pr_match.group(data.syntax.match_groups["issue"])
    if pr_match is None:
        success = False
    if (
        success
        and pr_issue not in "#0"
        and f"Closes {pr_issue}" not in data.pull_request.description
    ):
        log(
            err_log,
            "This PR is referencing issue %s "
            "but it does not have a: Close %s "
            "in its footer. Was this intentional?",
            pr_issue,
            pr_issue,
        )
        success = False
    return success or not should_fail


def pr_only_one_product(*, data: TestData) -> bool:
    """Test if a PR only contains commits for its product"""
    success: bool = True
    should_fail: bool = data.config["fail"]
    err_log: str = get_err_log(should_fail)
    pr_match: Any = re.match(data.syntax.regex, data.pull_request.title)
    pr_product: str = pr_match.group(data.syntax.match_groups["product"])
    if pr_match is None:
        log(
            err_log,
            "PR title is not syntax compliant: %s",
            data.pull_request.title,
        )
        success = False
    else:
        commits: Any = data.pull_request.commits()
        for commit in commits:
            commit_match: Any = re.match(data.syntax.regex, commit.title)
            if commit_match is None:
                log(
                    err_log,
                    "Commit title is not syntax compliant:\n%s",
                    commit.title,
                )
                success = False
            else:
                commit_product: str = commit_match.group(
                    data.syntax.match_groups["product"]
                )
                if commit_product not in pr_product:
                    log(
                        err_log,
                        "All associated commits must "
                        "have the same product as the PR.\n"
                        "PR product: %s\n"
                        "Commit product: %s",
                        pr_product,
                        commit_product,
                    )
                    success = False
    return success or not should_fail
