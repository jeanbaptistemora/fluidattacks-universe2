# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from dal.model import (
    Pipeline,
    Project,
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
)
from gql import (
    Client,
    gql,
)
from gql.transport.aiohttp import (
    AIOHTTPTransport,
)
from typing import (
    Any,
)


def get_project(*, url: str, token: str, project_id: str) -> Project:
    rest_session: Gitlab = Gitlab(url, private_token=token)
    gql_transport = AIOHTTPTransport(
        url=f"{url}/api/graphql",
        headers={"Authorization": token},
    )
    return Project(
        rest=rest_session.projects.get(project_id),
        gql=Client(transport=gql_transport, fetch_schema_from_transport=True),
    )


def get_pull_request(*, project: Project, pull_request_id: str) -> PullRequest:
    raw: MergeRequest = project.rest.mergerequests.get(
        pull_request_id, lazy=False
    )
    return PullRequest(
        type="gitlab",
        title=raw.title,
        state=raw.state,
        author=raw.author,
        id=raw.id,
        deltas=get_deltas(gql_session=project.gql, pull_request_id=raw.id),
        description=raw.description,
        source_branch=raw.source_branch,
        target_branch=raw.target_branch,
        commits=raw.commits,
        pipelines=partial(get_pipelines, pull_request=raw),
        raw=raw,
        url=raw.web_url,
    )


def get_deltas(*, gql_session: Client, pull_request_id: str) -> int:
    query: str = gql(
        """
        query getDeltas ($id: MergeRequestID!){
            mergeRequest(id: $id) {
                diffStatsSummary {
                    changes
                }
            }
        }
        """
    )
    result: dict[str, Any] = gql_session.execute(
        query,
        variable_values={"id": f"gid://gitlab/MergeRequest/{pull_request_id}"},
    )
    return result["mergeRequest"]["diffStatsSummary"]["changes"]


def get_pipelines(*, pull_request: MergeRequest) -> list[Pipeline]:
    return [
        Pipeline(id=raw.iid, status=raw.status, url=raw.web_url)
        for raw in pull_request.pipelines.list(get_all=True)
    ]


def close_pr(*, pull_request: PullRequest) -> None:
    pull_request.raw.state_event = "close"
    pull_request.raw.save()
