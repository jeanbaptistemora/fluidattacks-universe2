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


def insecure_file_upload_size(
    shard_db: ShardDb,  # NOSONAR # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> Vulnerabilities:
    def n_ids() -> Iterable[GraphShardNode]:

        danger_objs = {"CommonsMultipartResolver", "MultipartConfigFactory"}

        for shard in graph_db.shards_by_language(
            GraphLanguage.JAVA,
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for n_id in g.filter_nodes(
                graph,
                nodes=graph.nodes,
                predicate=g.pred_has_labels(label_type="ObjectCreation"),
            ):

                n_name = graph.nodes[n_id].get("name")

                if n_name in danger_objs:
                    parent = g.pred_ast(graph, n_id)[0]
                    yield shard, parent

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f354.java_upload_size_limit",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=MethodsEnum.JAVA_UPLOAD_SIZE_LIMIT,
    )
