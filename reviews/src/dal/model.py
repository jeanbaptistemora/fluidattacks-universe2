from collections.abc import (
    Callable,
)
from gitlab.v4.objects import (
    MergeRequest,
    Project as GitlabProject,
)
from gql import (
    Client as GqlClient,
)
from typing import (
    Any,
    NamedTuple,
)


class Project(NamedTuple):
    rest: GitlabProject
    gql: GqlClient


class Pipeline(NamedTuple):
    id: str
    status: str
    url: str


class PullRequest(NamedTuple):
    author: dict[str, str]
    commits: Callable[[], Any]
    description: str
    deltas: int
    id: str
    pipelines: Callable[[], list[Pipeline]]
    raw: MergeRequest
    source_branch: str
    state: Callable[[], str]
    target_branch: str
    title: str
    type: str
    url: str


class Syntax(NamedTuple):
    user_regex: str


class TestData(NamedTuple):
    config: dict[str, Any]
    pull_request: PullRequest
    syntax: Syntax


class MissingEnvironmentVariable(Exception):
    pass
