from typing import NamedTuple, List, Dict, Union, Any


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
    commits: Dict[str, Dict[str, str]]
    changes: Dict[str, Any]
    pipelines: List[Dict[str, str]]
    raw: Any
