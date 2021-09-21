from model import (
    core_model,
    graph_model,
)
from sast.query import (
    get_vulnerabilities_from_n_ids,
)
from typing import (
    Set,
)
from utils import (
    graph as g,
)
from utils.string import (
    complete_attrs_on_set,
)


def throws_generic_exception(
    graph_db: graph_model.GraphDB,
) -> core_model.Vulnerabilities:
    def n_ids() -> graph_model.GraphShardNodes:
        for shard in graph_db.shards_by_language(
            graph_model.GraphShardMetadataLanguage.JAVA,
        ):
            graph = shard.graph

            for method_declaration_id in g.filter_nodes(
                graph,
                nodes=graph.nodes,
                predicate=g.pred_has_labels(label_type="method_declaration"),
            ):
                for throws_id in g.filter_nodes(
                    graph,
                    nodes=g.adj_ast(graph, method_declaration_id),
                    predicate=g.pred_has_labels(label_type="throws"),
                ):
                    c_ids = g.adj_ast(graph, throws_id)

                    for identifier_id in g.filter_nodes(
                        graph,
                        nodes=c_ids,
                        predicate=g.pred_has_labels(
                            label_type="type_identifier",
                        ),
                    ) + g.filter_nodes(
                        graph,
                        nodes=c_ids,
                        predicate=g.pred_has_labels(
                            label_type="scoped_type_identifier",
                        ),
                    ):
                        if graph.nodes[identifier_id]["label_text"] in {
                            "Exception",
                            "Throwable",
                            "lang.Exception",
                            "lang.Throwable",
                            "java.lang.Exception",
                            "java.lang.Throwable",
                        }:
                            yield shard, identifier_id

    return get_vulnerabilities_from_n_ids(
        cwe=("397",),
        desc_key="src.lib_path.f060.insecure_exceptions.description",
        desc_params=dict(lang="Java"),
        finding=FINDING,
        graph_shard_nodes=n_ids(),
    )


def insecure_exceptions(
    graph_db: graph_model.GraphDB,
) -> core_model.Vulnerabilities:
    def n_ids() -> graph_model.GraphShardNodes:
        insec_exceptions: Set[str] = complete_attrs_on_set(
            {
                # Unrecoverable
                "java.lang.RuntimeException",
                # Don't do this
                "java.lang.NullPointerException",
                # Generics
                "java.lang.Exception",
                "java.lang.Throwable",
            }
        )
        for shard in graph_db.shards_by_language(
            graph_model.GraphShardMetadataLanguage.JAVA,
        ):
            graph = shard.graph

            for catch_type in g.filter_nodes(
                graph,
                nodes=graph.nodes,
                predicate=g.pred_has_labels(label_type="catch_type"),
            ):
                match_identifiers = g.match_ast_group(
                    graph,
                    catch_type,
                    "scoped_type_identifier",
                    "type_identifier",
                )
                for scoped_id in match_identifiers["scoped_type_identifier"]:
                    if (
                        graph.nodes[scoped_id].get("label_text")
                        in insec_exceptions
                    ):
                        yield shard, scoped_id

                for type_id in match_identifiers["type_identifier"]:
                    if (
                        graph.nodes[type_id].get("label_text")
                        in insec_exceptions
                    ):
                        yield shard, type_id

    return get_vulnerabilities_from_n_ids(
        cwe=("396",),
        desc_key="src.lib_path.f060.insecure_exceptions.description",
        desc_params=dict(lang="Java"),
        finding=FINDING,
        graph_shard_nodes=n_ids(),
    )


FINDING: core_model.FindingEnum = core_model.FindingEnum.F060
