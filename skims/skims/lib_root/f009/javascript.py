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
from utils.graph.text_nodes import (
    node_to_str,
)
from utils.string import (
    complete_attrs_on_set,
)


def crypto_js_credentials(
    graph_db: graph_model.GraphDB,
) -> core_model.Vulnerabilities:
    def n_ids() -> graph_model.GraphShardNodes:
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
        for shard in graph_db.shards_by_language(
            graph_model.GraphShardMetadataLanguage.JAVASCRIPT,
        ):
            graph = shard.graph
            for call_expression in g.filter_nodes(
                graph,
                nodes=graph.nodes,
                predicate=g.pred_has_labels(label_type="call_expression"),
            ):
                match = g.match_ast(
                    graph,
                    call_expression,
                    "member_expression",
                    "arguments",
                )
                if member_expression_id := match["member_expression"]:
                    method_name = node_to_str(graph, member_expression_id)
                    if method_name in danger_methods:
                        match_arguments = g.match_ast_group(
                            graph,
                            match["arguments"],
                            "string",
                            "template_string",
                        )
                        if (
                            match_arguments["string"]
                            or match_arguments["template_string"]
                        ):
                            yield shard, call_expression

    return get_vulnerabilities_from_n_ids(
        cwe=("798",),
        desc_key="src.lib_path.f009.crypto_js_credentials.description",
        desc_params={},
        finding=FINDING,
        graph_shard_nodes=n_ids(),
    )


FINDING: core_model.FindingEnum = core_model.FindingEnum.F009
