from arch_lint.dag import (
    DAG,
    DagMap,
)
from arch_lint.graph import (
    FullPathModule,
)
from typing import (
    Dict,
    FrozenSet,
    Tuple,
    TypeVar,
    Union,
)

_T = TypeVar("_T")


def _raise_or_return(item: _T | Exception) -> _T:
    if isinstance(item, Exception):
        raise item
    return item


_dag: Dict[str, Tuple[Union[Tuple[str, ...], str], ...]] = {
    "target_redshift": (
        "cli",
        ("input", "output"),
        ("loader", "strategy"),
        ("data_schema", "grouper"),
        ("_utils", "_logger"),
    ),
    "target_redshift.loader": (
        "_loaders",
        ("_common", "_s3_loader"),
        "_handlers",
        "_core",
        "_truncate",
    ),
    "target_redshift.strategy": (
        ("_recreate_all", "_per_stream"),
        "_core",
    ),
    "target_redshift.data_schema": (
        "_data_types",
        "_utils",
    ),
    "target_redshift.data_schema._data_types": (
        "_number",
        "_string",
        "_integer",
    ),
    "target_redshift.cli": ("_upload", "_from_s3", "_core"),
}


def project_dag() -> DagMap:
    return _raise_or_return(DagMap.new(_dag))


def forbidden_allowlist() -> Dict[FullPathModule, FrozenSet[FullPathModule]]:
    _raw: Dict[str, FrozenSet[str]] = {
        "fa_singer_io.singer.deserializer": frozenset(
            ["target_redshift.input"]
        )
    }
    return {
        FullPathModule.assert_module(k): frozenset(
            FullPathModule.assert_module(i) for i in v
        )
        for k, v in _raw.items()
    }
