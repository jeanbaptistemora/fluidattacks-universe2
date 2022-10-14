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


def uses_eval(
    shard_db: ShardDb,  # NOSONAR # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.JS_USES_EVAL

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(
            GraphLanguage.JAVASCRIPT,
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for member in g.filter_nodes(
                graph,
                graph.nodes,
                predicate=g.pred_has_labels(label_type="MethodInvocation"),
            ):
                if graph.nodes[member].get("expression") == "eval":
                    yield shard, member

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f143.js_uses_eval",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
