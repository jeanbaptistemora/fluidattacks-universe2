from arch_lint.dag.core import (
    DAG,
    new_dag,
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
)

_dag: Dict[str, FrozenList[FrozenList[str] | str]] = {
    "code_etl": (
        "cli",
        ("init_tables", "compute_bills", "upload_repo", "migration"),
        "amend",
        ("client", "arm"),
        ("factories", "mailmap"),
        "objs",
        ("_logger", "_patch", "_utils", "str_utils", "time_utils", "parallel"),
    ),
    "code_etl.compute_bills": (
        "_keeper",
        "_report",
        "_getter",
        ("core", "_retry"),
    ),
    "code_etl.client": (
        "_delta_update",
        "_raw",
        ("encoder", "_query", "decoder"),
        "_raw_file_commit",
        ("_raw_objs", "_assert"),
    ),
    "code_etl.amend": (
        "actions",
        "core",
    ),
    "code_etl.arm": (
        "_ignored_paths",
        "_raw_client",
    ),
    "code_etl.client._raw_file_commit": (
        "_client",
        ("_encode", "_decode", "_factory"),
    ),
    "code_etl.upload_repo": ("actions", ("extractor", "_ignored")),
}


def project_dag() -> DAG:
    return new_dag(_dag)


def forbidden_allowlist() -> Dict[FullPathModule, FrozenSet[FullPathModule]]:
    _raw: Dict[str, FrozenSet[str]] = {}
    return {
        FullPathModule.from_raw(k): frozenset(
            FullPathModule.from_raw(i) for i in v
        )
        for k, v in _raw.items()
    }
