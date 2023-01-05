from arch_lint.dag import (
    DagMap,
)
from arch_lint.graph import (
    FullPathModule,
)
from fa_purity import (
    FrozenList,
)
from typing import (
    Dict,
    FrozenSet,
    TypeVar,
)

_T = TypeVar("_T")
_dag: Dict[str, FrozenList[FrozenList[str] | str]] = {
    "job_last_success": (
        "cli",
        "core",
        "db_client",
        ("conf", "_logger"),
    ),
    "job_last_success.db_client": ("_client_1", "_core"),
    "job_last_success.cli": ("_sub_cmds", "_core"),
}


def raise_if_exception(item: _T | Exception) -> _T:
    if isinstance(item, Exception):
        raise item
    return item


def project_dag() -> DagMap:
    return raise_if_exception(DagMap.new(_dag))


def forbidden_allowlist() -> Dict[FullPathModule, FrozenSet[FullPathModule]]:
    _raw: Dict[str, FrozenSet[str]] = {}
    return {
        FullPathModule.assert_module(k): frozenset(
            FullPathModule.assert_module(i) for i in v
        )
        for k, v in _raw.items()
    }