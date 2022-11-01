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
from utils.string import (
    complete_attrs_on_set,
)


def crypto_js_credentials(
    shard_db: ShardDb,  # NOSONAR # pylint: disable=unused-argument
    graph_db: GraphDB,
) -> Vulnerabilities:
    danger_methods = complete_attrs_on_set(
        {
            "CryptoJS.enc.Base64.parse",
            "CryptoJS.enc.Utf16.parse",
            "CryptoJS.enc.Utf16LE.parse",
            "CryptoJS.enc.Hex.parse",
            "CryptoJS.enc.Latin1.parse",
            "CryptoJS.enc.Utf8.parse",
        }
    )

    def n_ids() -> Iterable[GraphShardNode]:
        for shard in graph_db.shards_by_language(
            GraphLanguage.JAVASCRIPT,
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph
            for n_id in g.filter_nodes(
                graph,
                nodes=graph.nodes,
                predicate=g.pred_has_labels(label_type="MethodInvocation"),
            ):
                n_attrs = graph.nodes[n_id]
                if (
                    n_attrs["expression"] in danger_methods
                    and (al_id := n_attrs.get("arguments_id"))
                    and (child := g.match_ast_d(graph, al_id, "Literal"))
                    and graph.nodes[child]["value_type"] == "string"
                    and graph.nodes[child]["value"] not in {'""', "''"}
                ):
                    yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f009.crypto_js_credentials.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=MethodsEnum.JS_CRYPTO_CREDENTIALS,
    )
