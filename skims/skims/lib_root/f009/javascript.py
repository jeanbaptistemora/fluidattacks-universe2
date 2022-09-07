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
from utils.string import (
    complete_attrs_on_set,
)


def crypto_js_credentials(
    shard_db: ShardDb,  # pylint: disable=unused-argument
    graph_db: graph_model.GraphDB,
) -> core_model.Vulnerabilities:
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

    def n_ids() -> graph_model.GraphShardNodes:
        for shard in graph_db.shards_by_language(
            graph_model.GraphShardMetadataLanguage.JAVASCRIPT,
        ):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph
            for n_id in g.filter_nodes(
                graph,
                nodes=graph.nodes,
                predicate=g.pred_has_labels(label_type="CallExpression"),
            ):
                if (
                    graph.nodes[n_id]["function_name"] in danger_methods
                    and (
                        al_id := g.match_ast(graph, n_id, "ArgumentList").get(
                            "ArgumentList"
                        )
                    )
                    and (
                        child := g.match_ast(graph, al_id, "Literal").get(
                            "Literal"
                        )
                    )
                    and graph.nodes[child]["value_type"] == "string"
                ):
                    yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f009.crypto_js_credentials.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=core_model.MethodsEnum.JS_CRYPTO_CREDENTIALS,
    )
