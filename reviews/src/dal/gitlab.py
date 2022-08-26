from dal.model import (
    PullRequest,
)
from functools import (
    partial,
)
from gitlab import (
    Gitlab,
)
from typing import (
    Any,
)


def login(url: str, token: str) -> Gitlab:
    return Gitlab(url, private_token=token)


def get_project(session: Gitlab, project_id: str) -> Any:
    return session.projects.get(project_id)


def get_pipelines(project: Any, raw_pr: Any) -> list[Any]:
    return [
        project.pipelines.get(pipeline.id)
        for pipeline in raw_pr.pipelines.list()
    ]


def close_pr(pull_request: PullRequest) -> None:
    pull_request.raw.state_event = "close"
    pull_request.raw.save()


def get_pr(session: Gitlab, project_id: str, pr_iid: str) -> PullRequest:
    project: Any = get_project(session, project_id)
    raw_pr: Any = project.mergerequests.get(pr_iid, lazy=False)
    return PullRequest(
        type="gitlab",
        id=raw_pr.id,
        iid=raw_pr.iid,
        title=raw_pr.title,
        state=raw_pr.state,
        author=raw_pr.author,
        description=raw_pr.description,
        source_branch=raw_pr.source_branch,
        target_branch=raw_pr.target_branch,
        commits=raw_pr.commits,
        changes=raw_pr.changes,
        pipelines=partial(get_pipelines, project, raw_pr),
        raw=raw_pr,
    )


def get_prs(session: Gitlab, project_id: str, state: str) -> list[PullRequest]:
    project: Any = get_project(session, project_id)
    prs: list[Any] = project.mergerequests.list(state=state)
    return [get_pr(session, project_id, pr.iid) for pr in prs]
