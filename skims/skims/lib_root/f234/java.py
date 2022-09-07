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
from sast.query import (
    get_vulnerabilities_from_n_ids,
)
from utils import (
    graph as g,
)


def info_leak_stacktrace(
    shard_db: ShardDb,  # pylint: disable=unused-argument
    graph_db: graph_model.GraphDB,
) -> core_model.Vulnerabilities:
    def n_ids() -> graph_model.GraphShardNodes:
        for shard in graph_db.shards_by_language(
            graph_model.GraphShardMetadataLanguage.JAVA,
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for n_id in g.filter_nodes(
                graph,
                nodes=graph.nodes,
                predicate=g.pred_has_labels(label_type="CatchClause"),
            ):
                childs = g.match_ast(
                    graph, n_id, "CatchParameter", "ExecutionBlock"
                )
                param = childs.get("CatchParameter")
                block = childs.get("ExecutionBlock")

                if not (param and block):
                    continue
                exc_name = graph.nodes[param].get("variable_name")

                for m_id in g.filter_nodes(
                    graph,
                    nodes=g.adj_ast(graph, str(block), depth=-1),
                    predicate=g.pred_has_labels(label_type="MethodInvocation"),
                ):
                    m_node = graph.nodes[m_id]
                    if (
                        m_node["expression"] == "printStackTrace"
                        and (symbol_id := m_node.get("object_id"))
                        and graph.nodes[symbol_id]["symbol"] == exc_name
                    ):
                        yield shard, m_id

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_root.f234.java_info_leak_stacktrace",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=core_model.MethodsEnum.JAVA_LEAK_STACKTRACE,
    )
