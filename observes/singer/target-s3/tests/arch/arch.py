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
    "target_s3": (
        "_cli",
        "loader",
        "upload",
        "csv",
        "_splitter",
        "core",
        "in_buffer",
        "_utils",
        "_parallel",
        "_logger",
    ),
    "target_s3.core": (
        "_record_group",
        "_complete_record",
        "_plain_record",
        "_ro_file",
    ),
}


def project_dag() -> DAG:
    return new_dag(_dag)


def forbidden_allowlist() -> Dict[FullPathModule, FrozenSet[FullPathModule]]:
    _raw: Dict[str, FrozenSet[str]] = {
        "pathos": frozenset(["target_s3._parallel"]),
    }
    return {
        FullPathModule.from_raw(k): frozenset(
            FullPathModule.from_raw(i) for i in v
        )
        for k, v in _raw.items()
    }
