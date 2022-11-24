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


def has_not_csfr_protection(
    shard_db: ShardDb,  # NOSONAR # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> Vulnerabilities:
    method = MethodsEnum.CS_HAS_NOT_CSFR_PROTECTION

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(
            GraphLanguage.CSHARP,
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for n_id in g.filter_nodes(
                graph,
                graph.nodes,
                g.pred_has_labels(label_type="Class"),
            ):
                if (
                    (
                        class_filter := g.match_ast(
                            shard.syntax_graph, n_id, "Attribute", depth=2
                        )["Attribute"]
                    )
                    and (attribute_node := graph.nodes[class_filter])
                    and (
                        attribute_node["name"]
                        == "AutoValidateAntiforgeryToken"
                    )
                ):
                    continue

                yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f337.cs_has_not_csfr_protection",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
