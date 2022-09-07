# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

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
from utils import (
    graph as g,
)


def has_console_functions(
    shard_db: ShardDb,  # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> core_model.Vulnerabilities:
    method = core_model.MethodsEnum.CS_HAS_CONSOLE_FUNCTIONS

    def n_ids() -> GraphShardNodes:
        for shard in graph_db.shards_by_language(
            GraphShardMetadataLanguage.CSHARP,
        ):
            if shard.syntax_graph is None:
                continue
            syntax_graph = shard.syntax_graph
            for nid in g.filter_nodes(
                syntax_graph,
                nodes=syntax_graph.nodes,
                predicate=g.pred_has_labels(label_type="MemberAccess"),
            ):
                pred_nid = g.pred_ast(syntax_graph, nid)[0]
                if (
                    syntax_graph.nodes[pred_nid].get("expression")
                    == "Console.WriteLine"
                ):
                    args = g.get_ast_childs(
                        syntax_graph,
                        pred_nid,
                        "InterpolatedStringExpression",
                        depth=2,
                    )
                    if args:
                        yield shard, nid

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f066.has_console_functions",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
