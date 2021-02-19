# Standard libraries
from typing import (
    Any,
    Callable,
    Dict,
    List,
    NamedTuple,
)


class PullRequest(NamedTuple):
    author: Dict[str, str]
    changes: Callable[[], Any]
    commits: Callable[[], Any]
    description: str
    id: str
    iid: str
    pipelines: Callable[[], List[Dict[str, str]]]
    raw: Any
    source_branch: str
    state: str
    target_branch: str
    title: str
    type: str


class Syntax(NamedTuple):
    match_groups: Dict[str, int]
    regex: str
    user_regex: str


class TestData(NamedTuple):
    config: Dict[str, Any]
    pull_request: PullRequest
    syntax: Syntax
