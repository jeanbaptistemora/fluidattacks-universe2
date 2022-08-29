from gitlab.v4.objects import (
    MergeRequest,
)
from typing import (
    Any,
    Callable,
    NamedTuple,
)


class PullRequest(NamedTuple):
    author: dict[str, str]
    changes: Callable[[], Any]
    commits: Callable[[], Any]
    description: str
    id: str
    pipelines: Callable[[], list[dict[str, str]]]
    raw: MergeRequest
    source_branch: str
    state: str
    target_branch: str
    title: str
    type: str
    url: str


class Syntax(NamedTuple):
    match_groups: dict[str, int]
    regex: str
    user_regex: str


class TestData(NamedTuple):
    config: dict[str, Any]
    pull_request: PullRequest
    syntax: Syntax


class MissingEnvironmentVariable(Exception):
    pass
