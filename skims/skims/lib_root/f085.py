from model import (
    core_model,
    graph_model,
)
from sast.query import (
    get_vulnerabilities_from_n_ids,
)
from typing import (
    Set,
    Tuple,
)
from utils import (
    graph as g,
)


def javascript_client_storage(
    graph_db: graph_model.GraphDB,
) -> core_model.Vulnerabilities:
    conditions: Tuple[Set[str], ...] = (
        # All items in the set must be present to consider it sensitive info
        {"auth"},
        {"credential"},
        {"documento", "usuario"},
        {"jwt"},
        {"password"},
        {"sesion", "data"},
        {"sesion", "id"},
        {"sesion", "token"},
        {"session", "data"},
        {"session", "id"},
        {"session", "token"},
        {"token", "access"},
        {"token", "app"},
        {"token", "id"},
        {"name", "user"},
        {"nombre", "usuario"},
        {"mail", "user"},
    )

    def n_ids() -> graph_model.GraphShardNodes:
        for shard in [
            *graph_db.shards_by_langauge(
                graph_model.GraphShardMetadataLanguage.JAVASCRIPT,
            ),
            *graph_db.shards_by_langauge(
                graph_model.GraphShardMetadataLanguage.TSX,
            ),
        ]:
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
                if member_id := match["member_expression"]:
                    match_identifier = g.match_ast(
                        graph, member_id, "identifier", "property_identifier"
                    )
                else:
                    continue

                if (
                    (identifier_id := match_identifier["identifier"])
                    and (
                        property_id := match_identifier["property_identifier"]
                    )
                    and graph.nodes[identifier_id]["label_text"]
                    in {
                        "localStorage",
                        "sessionStorage",
                    }
                    and graph.nodes[property_id]["label_text"]
                    in {
                        "setItem",
                        "getItem",
                    }
                ):
                    match_arguments = g.match_ast_group(
                        graph,
                        match["arguments"],
                        "string",
                        "identifier",
                        "property_identifier",
                        depth=-1,
                    )
                    arguments = [
                        graph.nodes[argument_id]["label_text"].lower()
                        for argument_id in [
                            *match_arguments["string"],
                            *match_arguments["identifier"],
                            *match_arguments["property_identifier"],
                        ]
                    ]
                    if any(
                        all(smell in argument for smell in smells)
                        for argument in arguments
                        for smells in conditions
                    ):
                        yield shard, call_expression

    return get_vulnerabilities_from_n_ids(
        cwe=("922",),
        desc_key="src.lib_path.f085.client_storage.description",
        desc_params={},
        finding=FINDING,
        graph_shard_nodes=n_ids(),
    )


# Constants
FINDING: core_model.FindingEnum = core_model.FindingEnum.F085
QUERIES: graph_model.Queries = ((FINDING, javascript_client_storage),)
