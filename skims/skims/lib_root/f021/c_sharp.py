# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from lib_root.utilities.c_sharp import (
    get_first_member_syntax_graph,
)
from lib_root.utilities.common import (
    search_method_invocation_naive,
)
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
from symbolic_eval.evaluate import (
    evaluate,
)
from symbolic_eval.utils import (
    get_backward_paths,
    get_object_identifiers,
)


def xpath_injection(
    shard_db: ShardDb,  # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.CS_XPATH_INJECTION
    c_sharp = GraphLanguage.CSHARP
    danger_meths = {"SelectSingleNode"}

    def n_ids() -> GraphShardNodes:
        for shard in graph_db.shards_by_language(c_sharp):
            if shard.syntax_graph is None:
                continue

            graph = shard.syntax_graph
            xpath_obj = get_object_identifiers(graph, {"XPathNavigator"})

            for n_id in search_method_invocation_naive(graph, danger_meths):
                if (
                    memb := get_first_member_syntax_graph(graph, n_id)
                ) and graph.nodes[memb].get("symbol") in xpath_obj:
                    for path in get_backward_paths(graph, n_id):
                        if (
                            evaluation := evaluate(method, graph, path, n_id)
                        ) and evaluation.danger:
                            yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f021.xpath_injection",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
