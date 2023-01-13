from arch_lint.dag.core import (
    DAG,
    new_dag,
)
from arch_lint.graph import (
    FullPathModule,
)
from typing import (
    Dict,
    FrozenSet,
    Tuple,
    Union,
)

_dag: Dict[str, Tuple[Union[Tuple[str, ...], str], ...]] = {
    "tap_mandrill": (
        "cli",
        ("streams", "singer"),
        "api",
        ("_logger", "_files", "_utils"),
    ),
    "tap_mandrill.api": (
        "export",
        ("_api_key", "objs"),
        "_utils",
    ),
    "tap_mandrill.api.export": (
        "_api_1",
        "_core",
    ),
    "tap_mandrill.api.export._api_1": (
        ("_activity", "_download", "_get_job"),
        "_decode",
    ),
    "tap_mandrill.singer": (
        "activity",
        "core",
    ),
    "tap_mandrill._files": (
        "_zip_file",
        "_csv_file",
        "_str_file",
        "_bin_file",
    ),
}


def project_dag() -> DAG:
    return new_dag(_dag)


def forbidden_allowlist() -> Dict[FullPathModule, FrozenSet[FullPathModule]]:
    _raw: Dict[str, FrozenSet[str]] = {
        "dateutil": frozenset(["tap_mandrill._utils"]),
        "mailchimp_transactional": frozenset(
            [
                "tap_mandrill.api.export._api_1._activity",
                "tap_mandrill.api.export._api_1._get_job",
                "tap_mandrill.api.export._api_1",
                "tap_mandrill.api._utils",
            ]
        ),
    }
    return {
        FullPathModule.from_raw(k): frozenset(
            FullPathModule.from_raw(i) for i in v
        )
        for k, v in _raw.items()
    }
