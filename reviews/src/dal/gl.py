from dal.model import (
    PullRequest,
)
from functools import (
    partial,
)
from gitlab import (
    Gitlab,
)
from gitlab.v4.objects import (
    MergeRequest,
    Project,
    ProjectMergeRequest,
    ProjectPipeline,
)


def get_project(url: str, token: str, project_id: str) -> Project:
    session: Gitlab = Gitlab(url, private_token=token)
    return session.projects.get(project_id)


def get_pull_request(project: Project, pull_request_id: str) -> PullRequest:
    raw: MergeRequest = project.mergerequests.get(pull_request_id, lazy=False)
    return PullRequest(
        type="gitlab",
        id=raw.iid,
        title=raw.title,
        state=raw.state,
        author=raw.author,
        description=raw.description,
        source_branch=raw.source_branch,
        target_branch=raw.target_branch,
        commits=raw.commits,
        changes=raw.changes,
        pipelines=partial(get_pipelines, project, raw),
        raw=raw,
    )


def get_pull_requests(project: Project) -> dict[str, PullRequest]:
    raws: list[ProjectMergeRequest] = project.mergerequests.list(
        state="opened"
    )
    return {raw.iid: get_pull_request(project, raw.iid) for raw in raws}


def get_pipelines(
    project: Project, pull_request: MergeRequest
) -> list[ProjectPipeline]:
    return [
        project.pipelines.get(pipeline.id)
        for pipeline in pull_request.pipelines.list()
    ]


def close_pr(pull_request: PullRequest) -> None:
    pull_request.raw.state_event = "close"
    pull_request.raw.save()
