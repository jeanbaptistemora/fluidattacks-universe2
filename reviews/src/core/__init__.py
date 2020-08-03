# Standard libraries
import os
from functools import partial
from typing import Any, List, Callable

# Third party libraries
from gitlab import Gitlab
from dynaconf import Dynaconf

# Local libraries
from core import tests
from utils.logs import log


def run_tests(config: Dynaconf) -> bool:

    def get_mr(session: Gitlab, project_id: str, mr_iid: str) -> Any:
        project: Any = session.projects.get(project_id)
        mr_info: Any = project.mergerequests.get(mr_iid, lazy=False)
        return mr_info

    def required_env() -> bool:
        variables: List[str] = [
            'CI_MERGE_REQUEST_IID',
            'CI_PROJECT_ID',
            'REVIEWS_TOKEN',
        ]
        success: bool = True
        for variable in variables:
            if variable not in os.environ:
                success = False
                log('error',
                    '%s must be set',
                    variable)
        return success

    success: bool = required_env()
    if success:
        gitlab_url: str = config['gitlab_url']
        project_id: str = str(os.environ.get('CI_PROJECT_ID'))
        mr_iid: str = str(os.environ.get('CI_MERGE_REQUEST_IID'))
        token: str = str(os.environ.get('REVIEWS_TOKEN'))
        session: Gitlab = Gitlab(gitlab_url, private_token=token)
        mr_info: Any = get_mr(session, project_id, mr_iid)

    if success and not tests.skip_ci(mr_info):
        for name, args in config['tests'].items():
            test: Callable[[], bool] = \
                partial(getattr(tests, name), mr_info=mr_info, config=args)
            log('info', f'Running tests.{name}')
            success = test() and success

    return success
