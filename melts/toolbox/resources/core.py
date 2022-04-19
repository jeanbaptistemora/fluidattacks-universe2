from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
)
from enum import (
    Enum,
)
from logging import (
    Logger,
)
from typing import (
    Any,
    Dict,
)


class RepoType(Enum):
    SSH = "SSH"
    HTTPS = "HTTPS"


class RootState(Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"


@dataclass(frozen=True)
class _GitRoot:
    root_id: str
    url: str
    branch: str
    repo_type: RepoType
    head_commit: str
    state: RootState
    nickname: str


@dataclass(frozen=True)
class FormatRepoProblem(Exception):
    nickname: str
    branch: str
    problem: str

    def log(self, logger: Logger) -> None:
        logger.error("%s/%s failed", self.nickname, self.branch)
        logger.error(self.problem)

    def raw(self) -> Dict[str, str]:
        return {"repo": self.nickname, "problem": self.problem}


@dataclass(frozen=True)
class GitRoot(_GitRoot):
    def __init__(self, obj: _GitRoot) -> None:
        super().__init__(**obj.__dict__)

    @staticmethod
    def new(raw: Dict[str, Any]) -> GitRoot:
        url = str(raw["url"])
        draft = _GitRoot(
            str(raw["id"]),
            url,
            str(raw["branch"]),
            RepoType.SSH if url.startswith("ssh") else RepoType.HTTPS,
            str(raw["cloningStatus"]["commit"]),
            RootState(raw["state"]),
            str(raw["nickname"]),
        )
        return GitRoot(draft)
