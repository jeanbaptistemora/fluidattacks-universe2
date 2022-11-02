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
from fa_purity import (
    FrozenList,
)
from typing import (
    Dict,
    FrozenSet,
)

_dag: Dict[str, FrozenList[FrozenList[str] | str]] = {
    "tap_checkly": (
        "cli",
        "streams",
        "state",
        ("singer", "api"),
        ("objs", "_utils"),
    ),
    "tap_checkly.api": (
        ("alert_channels", "checks", "groups", "report"),
        ("_raw", "_utils"),
    ),
    "tap_checkly.api.alert_channels": (
        "_client",
        "_decode",
    ),
    "tap_checkly.api.checks": (
        "_client",
        "_decode",
        ("results", "status"),
    ),
    "tap_checkly.api.checks.results": ("_client", "_decode", "time_range"),
    "tap_checkly.api.checks.results._decode": (("_api_result", "_browser"),),
    "tap_checkly.api.checks.status": (
        "_client",
        "_decode",
    ),
    "tap_checkly.api.groups": (
        "_client",
        "_decode",
    ),
    "tap_checkly.api.report": (
        "_client",
        "_decode",
    ),
    "tap_checkly.singer": (
        ("_alert_channels", "_groups", "_report", "_checks"),
        ("_core", "_encoder"),
    ),
    "tap_checkly.singer._checks": (
        "_encoders",
        ("results", "status"),
    ),
    "tap_checkly.streams": (("_state", "_objs"),),
    "tap_checkly.objs": (
        "_root",
        "_report",
        "_group",
        "_subscriptions",
        ("_check", "_alert", "_dashboard", "result"),
        "_id_objs",
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
