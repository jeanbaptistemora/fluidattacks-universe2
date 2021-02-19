# Standard libraries
from typing import (
    Any,
    Callable,
    Dict,
    List,
    NamedTuple,
)


class PullRequest(NamedTuple):
    type: str
    id: str
    iid: str
    title: str
    state: str
    author: Dict[str, str]
    description: str
    source_branch: str
    target_branch: str
    commits: Callable[[], Any]
    changes: Callable[[], Any]
    pipelines: Callable[[], List[Dict[str, str]]]
    raw: Any


class Syntax(NamedTuple):
    regex: str
    match_groups: Dict[str, int]


class TestData(NamedTuple):
    config: Dict[str, Any]
    pull_request: PullRequest
    syntax: Syntax
