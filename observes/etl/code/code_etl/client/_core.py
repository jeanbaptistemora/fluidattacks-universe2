from __future__ import (
    annotations,
)

from ._delta_update import (
    CommitStampDiff,
)
from code_etl.objs import (
    CommitStamp,
    RepoContex,
    RepoId,
    RepoRegistration,
)
from dataclasses import (
    dataclass,
)
from enum import (
    Enum,
)
from fa_purity import (
    Cmd,
    FrozenList,
    ResultE,
    Stream,
)
from fa_purity.result.factory import (
    ResultFactory,
)
import logging
from typing import (
    Callable,
    Generic,
    Optional,
    TypeVar,
    Union,
)

LOG = logging.getLogger(__name__)
_T = TypeVar("_T")


class Tables(Enum):
    COMMITS = "COMMITS"
    FILES = "FILES"

    @staticmethod
    def from_raw(raw: str) -> ResultE[Tables]:
        factory: ResultFactory[Tables, Exception] = ResultFactory()
        try:
            return factory.success(Tables[raw.upper()])
        except KeyError as err:
            return factory.failure(err)


@dataclass(frozen=True)
class _Patch(Generic[_T]):
    inner: _T


@dataclass(frozen=True)
class Client:
    # interface of exposed utilities from and to DB using not raw objs
    _init_table: _Patch[Callable[[Tables], Cmd[None]]]
    _all_data_count: _Patch[Callable[[Optional[str]], Cmd[ResultE[int]]]]
    _get_context: _Patch[Callable[[RepoId], Cmd[RepoContex]]]
    _register_repos: _Patch[
        Callable[[FrozenList[RepoRegistration]], Cmd[None]]
    ]
    _insert_stamps: _Patch[Callable[[FrozenList[CommitStamp]], Cmd[None]]]
    _namespace_data: _Patch[
        Callable[
            [str], Cmd[Stream[ResultE[Union[CommitStamp, RepoRegistration]]]]
        ]
    ]
    _delta_update: _Patch[Callable[[CommitStampDiff], Cmd[None]]]

    @staticmethod
    def new(
        _init_table: Callable[[Tables], Cmd[None]],
        _all_data_count: Callable[[Optional[str]], Cmd[ResultE[int]]],
        _get_context: Callable[[RepoId], Cmd[RepoContex]],
        _register_repos: Callable[[FrozenList[RepoRegistration]], Cmd[None]],
        _insert_stamps: Callable[[FrozenList[CommitStamp]], Cmd[None]],
        _namespace_data: Callable[
            [str], Cmd[Stream[ResultE[Union[CommitStamp, RepoRegistration]]]]
        ],
        _delta_update: Callable[[CommitStampDiff], Cmd[None]],
    ) -> Client:
        return Client(
            _Patch(_init_table),
            _Patch(_all_data_count),
            _Patch(_get_context),
            _Patch(_register_repos),
            _Patch(_insert_stamps),
            _Patch(_namespace_data),
            _Patch(_delta_update),
        )

    def init_table(self, table: Tables) -> Cmd[None]:
        return self._init_table.inner(table)

    def all_data_count(self, namespace: Optional[str]) -> Cmd[ResultE[int]]:
        return self._all_data_count.inner(namespace)

    def get_context(self, repo: RepoId) -> Cmd[RepoContex]:
        return self._get_context.inner(repo)

    def register_repos(self, reg: FrozenList[RepoRegistration]) -> Cmd[None]:
        return self._register_repos.inner(reg)

    def insert_stamps(self, stamps: FrozenList[CommitStamp]) -> Cmd[None]:
        return self._insert_stamps.inner(stamps)

    def namespace_data(
        self, namespace: str
    ) -> Cmd[Stream[ResultE[Union[CommitStamp, RepoRegistration]]]]:
        return self._namespace_data.inner(namespace)

    def delta_update(self, diff: CommitStampDiff) -> Cmd[None]:
        return self._delta_update.inner(diff)
