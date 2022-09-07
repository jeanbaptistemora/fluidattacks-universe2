# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from lib_sast.types import (
    ShardDb,
)
from model.core_model import (
    MethodsEnum,
    Vulnerabilities,
)
from model.graph_model import (
    GraphDB,
    GraphShardMetadataLanguage as GraphLanguage,
    GraphShardNodes,
)
from sast.query import (
    get_vulnerabilities_from_n_ids,
)
from symbolic_eval.utils import (
    get_object_identifiers,
    get_value_member_access,
)


def disabled_http_header_check(
    shard_db: ShardDb,  # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.CS_DISABLED_HTTP_HEADER_CHECK
    c_sharp = GraphLanguage.CSHARP

    def n_ids() -> GraphShardNodes:
        for shard in graph_db.shards_by_language(c_sharp):
            if shard.syntax_graph is None:
                continue

            s_graph = shard.syntax_graph
            http_obj = {"HttpRuntimeSection"}
            for ident in get_object_identifiers(s_graph, http_obj):
                if (
                    value := get_value_member_access(
                        s_graph, ident, "EnableHeaderChecking"
                    )
                ) and s_graph.nodes[value].get("value") == "false":
                    yield shard, value

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_path.f414.disabled_http_header_check",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
