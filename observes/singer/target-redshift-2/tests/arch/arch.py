# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

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
    "target_redshift": (
        "cli",
        "loader",
        "data_schema",
        "errors",
        "_logger",
    ),
    "target_redshift.loader": (
        "_handlers",
        "_grouper",
        "_strategy",
        "_s3_loader",
        "_truncate",
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
