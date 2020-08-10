# Standard libraries
from typing import Any, List

# Third party libraries
from gitlab import Gitlab


def required_vars() -> List[str]:
    return [
        'CI_MERGE_REQUEST_IID',
        'CI_PROJECT_ID',
        'REVIEWS_TOKEN',
    ]


def login(url: str, token: str) -> Gitlab:
    return Gitlab(url, private_token=token)


def get_project(session: Gitlab, project_id: str) -> Any:
    return session.projects.get(project_id)


def get_mr(session: Gitlab, project_id: str, mr_iid: str) -> Any:
    project: Any = get_project(session, project_id)
    mr_info: Any = project.mergerequests.get(mr_iid, lazy=False)
    return mr_info


def close_mr(mr_info: Any) -> None:
    mr_info.state_event = 'close'
    mr_info.save()
