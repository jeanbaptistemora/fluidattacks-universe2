# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

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
from symbolic_eval.evaluate import (
    evaluate,
)
from symbolic_eval.utils import (
    get_backward_paths,
)
from typing import (
    Set,
    Tuple,
)
from utils import (
    graph as g,
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
    method = core_model.MethodsEnum.JS_CLIENT_STORAGE
    danger_names = {
        "localStorage.getItem",
        "localStorage.setItem",
        "sessionStorage.getItem",
        "sessionStorage.setItem",
    }

    def n_ids() -> graph_model.GraphShardNodes:
        for shard in graph_db.shards_by_language(
            graph_model.GraphShardMetadataLanguage.JAVASCRIPT,
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in g.filter_nodes(
                graph,
                graph.nodes,
                predicate=g.pred_has_labels(label_type="CallExpression"),
            ):
                f_name = graph.nodes[nid]["function_name"]
                al_id = g.match_ast(graph, nid, "ArgumentList").get(
                    "ArgumentList"
                )
                if f_name not in danger_names or not al_id:
                    continue

                opc_nid = g.match_ast(graph, al_id)

                if "getItem" in f_name.split("."):
                    test_node = opc_nid.get("__0__")
                else:
                    test_node = opc_nid.get("__1__")

                if not test_node:
                    continue

                for path in get_backward_paths(graph, test_node):
                    if (
                        evaluation := evaluate(method, graph, path, test_node)
                    ) and any(
                        all(smell in key_str.lower() for smell in smells)
                        and not _could_be_boolean(key_str.lower())
                        for key_str in evaluation.triggers
                        for smells in conditions
                    ):
                        yield shard, nid

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f085.client_storage.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
