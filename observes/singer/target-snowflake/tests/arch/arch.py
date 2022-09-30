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
        "loader",
        "data_schema",
        "snowflake_client",
        ("_assert", "_logger"),
    ),
    "target_snowflake.loader": (
        ("_handlers", "_strategy"),
        "_grouper",
    ),
    "target_snowflake.data_schema": (
        "_data_types",
        "_utils",
    ),
    "target_snowflake.data_schema._data_types": (
        ("_integer", "_string", "_number"),
    ),
    "target_snowflake.snowflake_client": (
        "root",
        "db",
        "schema",
        "table",
        "column",
        ("_encode", "_decode"),
        ("data_type", "sql_client"),
    ),
    "target_snowflake.snowflake_client.db": (
        "_manager",
        "_core",
    ),
    "target_snowflake.snowflake_client.schema": (
        "_manager",
        "_core",
    ),
    "target_snowflake.snowflake_client.table": (
        "_manager",
        "_core",
    ),
    "target_snowflake.snowflake_client.sql_client": (
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
