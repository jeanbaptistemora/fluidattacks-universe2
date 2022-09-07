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
    "tap_dynamo": ("cli", "extractor", ("client", "dynamo"), "_logger"),
    "tap_dynamo.dynamo": ("item_factory", "core"),
}


def project_dag() -> DAG:
    return new_dag(_dag)


def forbidden_allowlist() -> Dict[FullPathModule, FrozenSet[FullPathModule]]:
    _raw: Dict[str, FrozenSet[str]] = {
        "boto3": frozenset(
            [
                "tap_dynamo.client",
                "tap_dynamo.dynamo.item_factory",
                "tap_dynamo.dynamo.core",
            ]
        ),
    }
    return {
        FullPathModule.from_raw(k): frozenset(
            FullPathModule.from_raw(i) for i in v
        )
        for k, v in _raw.items()
    }
