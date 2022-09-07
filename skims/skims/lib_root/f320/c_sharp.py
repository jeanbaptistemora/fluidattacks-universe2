# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from lib_root.utilities.c_sharp import (
    yield_syntax_graph_member_access,
    yield_syntax_graph_object_creation,
)
from lib_sast.types import (
    ShardDb,
)
from model import (
    core_model,
)
from model.graph_model import (
    GraphDB,
    GraphShardMetadataLanguage,
    GraphShardNodes,
)
from sast.query import (
    get_vulnerabilities_from_n_ids,
)
from symbolic_eval.evaluate import (
    evaluate,
)
from symbolic_eval.utils import (
    get_backward_paths,
)
from utils import (
    graph as g,
)


def ldap_connections_authenticated(
    shard_db: ShardDb,  # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> core_model.Vulnerabilities:
    method = core_model.MethodsEnum.CS_LDAP_CONN_AUTH

    def n_ids() -> GraphShardNodes:
        for shard in graph_db.shards_by_language(
            GraphShardMetadataLanguage.CSHARP,
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for nid in yield_syntax_graph_object_creation(
                graph, {"DirectoryEntry"}
            ):
                var = {graph.nodes[g.pred(graph, nid)[0]].get("variable")}
                if set(yield_syntax_graph_member_access(graph, var)):
                    continue
                args_nid = graph.nodes[nid].get("arguments_id")
                test_nid = g.adj_ast(graph, args_nid)[3]
                for path in get_backward_paths(graph, test_nid):
                    evaluation = evaluate(method, graph, path, test_nid)
                    if evaluation and evaluation.danger:
                        yield shard, nid

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f320.authenticated_ldap_connections",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
