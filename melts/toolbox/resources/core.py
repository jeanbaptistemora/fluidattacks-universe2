from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
)
from enum import (
    Enum,
)
from typing import (
    Any,
    Dict,
)


class RepoType(Enum):
    SSH = "SSH"
    HTTPS = "HTTPS"


class RootStatus(Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"


@dataclass(frozen=True)
class _GitRoot:
    url: str
    branch: str
    repo_type: RepoType
    head_commit: str
    state: RootStatus
    nickname: str


@dataclass(frozen=True)
class GitRoot(_GitRoot):
    def __init__(self, obj: _GitRoot) -> None:
        super().__init__(**obj.__dict__)

    @staticmethod
    def new(raw: Dict[str, Any]) -> GitRoot:
        url = str(raw["url"])
        draft = _GitRoot(
            url,
            str(raw["branch"]),
            RepoType.SSH if url.startswith("ssh") else RepoType.HTTPS,
            str(raw["cloningStatus"]["commit"]),
            RootStatus(raw["status"]),
            str(raw["nickname"]),
        )
        return GitRoot(draft)
