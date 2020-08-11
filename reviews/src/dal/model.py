from typing import NamedTuple, List, Dict, Callable, Any


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
