# Standard libraries
import os
from functools import partial
from typing import Callable

# Third party libraries
from gitlab import Gitlab
from dynaconf import Dynaconf

# Local libraries
from config import load
from core import tests
from dal import (
    gitlab,
    verify_required_vars,
)
from dal.model import (
    Syntax,
    PullRequest,
    TestData,
)
from utils.logs import log


def run_tests(config_path: str) -> bool:
    config: Dynaconf = load(config_path)
    if config['platform'] in 'gitlab':
        success: bool = verify_required_vars(gitlab.required_vars())
        if success:
            endpoint_url: str = config['endpoint_url']
            project_id: str = str(os.environ.get('CI_PROJECT_ID'))
            mr_iid: str = str(os.environ.get('CI_MERGE_REQUEST_IID'))
            token: str = str(os.environ.get('REVIEWS_TOKEN'))
            session: Gitlab = gitlab.login(endpoint_url, token)
            pull_request: PullRequest = \
                gitlab.get_pr(session, project_id, mr_iid)

    if success and not tests.skip_ci(pull_request):
        syntax: Syntax = Syntax(
            regex=config['syntax']['regex'],
            match_groups=config['syntax']['match_groups'],
        )
        for name, args in config['tests'].items():
            data: TestData = TestData(
                config=args,
                pull_request=pull_request,
                syntax=syntax,
            )
            test: Callable[[], bool] = \
                partial(getattr(tests, name), data=data)
            log('info', f'Running tests.{name}')
            success = test() and success
            if not success \
                    and args['close_pr'] \
                    and pull_request.raw.state not in 'closed':
                gitlab.close_pr(pull_request)
                log('error', 'Merge Request closed by: %s', name)

    return success
