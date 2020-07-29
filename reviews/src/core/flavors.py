# Standard libraries
import os
from typing import Any, List, Dict, Callable
from functools import partial

# Third party libraries
import gitlab

# Local libraries
from core.tests import (
    test_skip_ci,
    test_mr_under_max_deltas,
    test_all_pipelines_successful,
    test_mr_message,
    test_branch_equals_to_user,
    test_most_relevant_type,
    test_commits_user,
    test_mr_user,
    test_one_commit_per_mr,
    test_close_issue_directive,
)
from utils.logs import (
    log
)


GITLAB_URL: str = 'https://gitlab.com'
REGEX_COMMIT_USER: str = r'^[A-Z][a-z]+ [A-Z][a-z]+$'
RELEVANCES: Dict[str, int] = {
    'rever': 1,
    'feat': 2,
    'perf': 3,
    'fix': 4,
    'refac': 5,
    'test': 6,
    'style': 7,
}


def get_mr(session: Any, project_id: str, mr_iid: str) -> Any:
    project: Any = session.projects.get(project_id)
    mr_info: Any = project.mergerequests.get(mr_iid, lazy=False)
    return mr_info


def required_env() -> bool:
    variables: List[str] = [
        'MR_TEST_MAX_DELTAS',
        'CI_PROJECT_ID',
        'CI_MERGE_REQUEST_IID',
        'MR_TEST_TOKEN',
    ]
    success: bool = True
    for variable in variables:
        if variable not in os.environ:
            success = False
            log('error',
                '%s must be set',
                variable)
    return success


def run_flavor(
        fail_tests: List[str],
        warn_tests: List[str],
        regex_mr_title: str) -> bool:
    success: bool = required_env()

    if success:
        max_deltas: int = int(str(os.environ.get('MR_TEST_MAX_DELTAS')))
        project_id: str = str(os.environ.get('CI_PROJECT_ID'))
        mr_iid: str = str(os.environ.get('CI_MERGE_REQUEST_IID'))
        token: str = str(os.environ.get('MR_TEST_TOKEN'))
        session: Any = gitlab.Gitlab(GITLAB_URL, private_token=token)
        mr_info: Any = get_mr(session, project_id, mr_iid)
        mr_commit_msg: str = f'{mr_info.title}\n\n{mr_info.description}'

    if success and not test_skip_ci(mr_info):
        tests: Dict[str, Callable[[], bool]] = {
            'mr_under_max_deltas':
                partial(test_mr_under_max_deltas, mr_info, max_deltas),
            'all_pipelines_successful':
                partial(test_all_pipelines_successful, mr_info),
            'mr_message':
                partial(test_mr_message, mr_commit_msg),
            'branch_equals_to_user':
                partial(test_branch_equals_to_user, mr_info),
            'most_relevant_type':
                partial(test_most_relevant_type, mr_info,
                        regex_mr_title, RELEVANCES),
            'commits_user':
                partial(test_commits_user, mr_info, REGEX_COMMIT_USER),
            'mr_user':
                partial(test_mr_user, mr_info, REGEX_COMMIT_USER),
            'one_commit_per_mr':
                partial(test_one_commit_per_mr, mr_info),
            'close_issue_directive':
                partial(test_close_issue_directive, mr_info, regex_mr_title)
        }

        # Run tests that produce failure
        for test in fail_tests:
            success = tests[test]() and success

        for test in warn_tests:
            tests[test]()

    return success
