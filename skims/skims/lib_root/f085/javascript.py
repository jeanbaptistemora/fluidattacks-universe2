# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from lib_root.utilities.javascript import (
    yield_method_invocation,
)
from lib_sast.types import (
    ShardDb,
)
from model import (
    core_model,
    graph_model,
)
import re
from sast.query import (
    get_vulnerabilities_from_n_ids,
)
from sast_syntax_readers.utils_generic import (
    get_dependencies,
)
from typing import (
    Set,
    Tuple,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def _could_be_boolean(key: str) -> bool:
    prefixes = {"is", "has", "es"}
    match = re.search("[a-z]", key, re.I)
    if match:
        _key = key[match.start() :]
        return any(_key.startswith(prefix) for prefix in prefixes)
    return False


def client_storage(
    shard_db: ShardDb,  # pylint: disable=unused-argument
    graph_db: graph_model.GraphDB,
) -> core_model.Vulnerabilities:
    conditions: Tuple[Set[str], ...] = (
        # All items in the set must be present to consider it sensitive info
        {"auth"},
        {"credential"},
        {"documento", "usuario"},
        {"jwt"},
        {"password"},
        {"sesion", "data"},
        {"sesion", "id"},
        {"sesion", "token"},
        {"session", "data"},
        {"session", "id"},
        {"session", "token"},
        {"token", "access"},
        {"token", "app"},
        {"token", "id"},
        {"name", "user"},
        {"nombre", "usuario"},
        {"mail", "user"},
    )

    def n_ids() -> graph_model.GraphShardNodes:
        for (
            shard,
            syntax_steps,
            invocation_step,
            step_index,
        ) in yield_method_invocation(graph_db):
            method = invocation_step.method
            if method not in {
                "localStorage.setItem",
                "localStorage.getItem",
                "sessionStorage.setItem",
                "sessionStorage.getItem",
            }:
                continue

            dependencies = get_dependencies(step_index, syntax_steps)
            store_key = dependencies[0]

            key_str = ""
            if store_key.type == "SyntaxStepLiteral":
                key_str = store_key.value
            elif store_key.type == "SyntaxStepMemberAccessExpression":
                key_str = node_to_str(shard.graph, store_key.meta.n_id)
            elif store_key.type == "SyntaxStepSymbolLookup":
                key_str = store_key.symbol
            key_str = key_str.lower()

            if _could_be_boolean(key_str):
                continue
            if any(
                all(smell in key_str for smell in smells)
                for smells in conditions
            ):
                yield shard, invocation_step.meta.n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f085.client_storage.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=core_model.MethodsEnum.JS_CLIENT_STORAGE,
    )
