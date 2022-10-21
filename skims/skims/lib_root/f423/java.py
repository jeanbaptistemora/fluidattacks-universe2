# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from lib_root.utilities.java import (
    yield_method_invocation_syntax_graph,
)
from lib_sast.types import (
    ShardDb,
)
from model import (
    core_model,
)
from model.graph_model import (
    Graph,
    GraphDB,
    GraphShardMetadataLanguage,
    GraphShardNode,
)
from sast.query import (
    get_vulnerabilities_from_n_ids,
)
from typing import (
    Iterable,
)
from utils import (
    graph as g,
)


def get_parent_method_name(graph: Graph, n_id: str) -> str:
    parent = g.pred_ast(graph, n_id)[0]
    while graph.nodes[parent].get("label_type") != "MethodDeclaration":
        get_nodes = g.pred_ast(graph, parent)
        if get_nodes:
            parent = get_nodes[0]
        else:
            return "no_method_found"

    return graph.nodes[parent]["name"]


def uses_exit_method(
    shard_db: ShardDb,  # NOSONAR # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> core_model.Vulnerabilities:
    method = core_model.MethodsEnum.JAVA_USES_SYSTEM_EXIT
    exit_methods = {
        "System.exit",
        "Runtime.getRuntime.exit",
        "Runtime.getRuntime.halt",
    }

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(
            GraphShardMetadataLanguage.JAVA,
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for m_id, m_name in yield_method_invocation_syntax_graph(graph):
                if (
                    get_parent_method_name(graph, m_id) != "main"
                    and m_name in exit_methods
                ):
                    yield shard, m_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f423.uses_system_exit",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
