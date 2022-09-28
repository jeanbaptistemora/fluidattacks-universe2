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
    "target_snowflake": (
        "cli",
        "db_clients",
        "schema",
        "table",
        "column",
        ("data_type", "sql_client"),
        ("_assert", "_logger"),
    ),
    "target_snowflake.db_clients": (
        ("_table", "_table_ops"),
        ("_encode", "_decode"),
    ),
    "target_snowflake.sql_client": (
        "_connection",
        "_cursor",
        "_query",
        ("_inner", "_identifier", "_primitive"),
    ),
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
