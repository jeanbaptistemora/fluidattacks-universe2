# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    GraphDB,
    GraphShardMetadataLanguage as GraphLanguage,
    GraphShardNode,
)
from typing import (
    Iterable,
)
from utils import (
    graph as g,
)


def n_ids_uses_console_fns(
    graph_db: GraphDB, language: GraphLanguage
) -> Iterable[GraphShardNode]:
    for shard in graph_db.shards_by_language(
        language,
    ):
        if shard.syntax_graph is None:
            continue
        graph = shard.syntax_graph
        for n_id in g.filter_nodes(
            graph,
            graph.nodes,
            predicate=g.pred_has_labels(label_type="MethodInvocation"),
        ):
            if graph.nodes[n_id].get("expression") == "console.log":
                yield shard, n_id
