from gitlab.v4.objects import (
    MergeRequest,
)
from typing import (
    Any,
    Callable,
    NamedTuple,
)


class Pipeline(NamedTuple):
    id: str
    status: str
    url: str


class PullRequest(NamedTuple):
    author: dict[str, str]
    commits: Callable[[], Any]
    description: str
    pipelines: Callable[[], list[Pipeline]]
    raw: MergeRequest
    source_branch: str
    state: str
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
