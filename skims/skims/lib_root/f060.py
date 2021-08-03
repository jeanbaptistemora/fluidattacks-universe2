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
from utils.graph.transformation import (
    build_qualified_name,
)
from utils.string import (
    complete_attrs_on_set,
)


def java_declaration_of_throws_for_generic_exception(
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


def c_sharp_insecure_exceptions(
    graph_db: graph_model.GraphDB,
) -> core_model.Vulnerabilities:
    def n_ids() -> graph_model.GraphShardNodes:
        insecure_exceptions: Set[str] = {
            # Generic
            "Exception",
            "ApplicationException",
            "SystemException",
            "System.Exception",
            "System.ApplicationException",
            "System.SystemException",
            # Unrecoverable
            "NullReferenceException",
            "system.NullReferenceException",
        }
        for shard in graph_db.shards_by_language(
            graph_model.GraphShardMetadataLanguage.CSHARP,
        ):
            graph = shard.graph

            for catch_declaration in g.filter_nodes(
                graph,
                nodes=graph.nodes,
                predicate=g.pred_has_labels(label_type="catch_declaration"),
            ):
                match_identifiers = g.match_ast_group(
                    graph, catch_declaration, "identifier", "qualified_name"
                )
                if _qualified := match_identifiers["qualified_name"]:
                    qualified = _qualified.pop()
                    exception = build_qualified_name(graph, qualified)
                    if exception in insecure_exceptions:
                        yield shard, qualified
                else:
                    exceptions = {
                        n_id
                        for n_id in match_identifiers["identifier"] or set()
                        if graph.nodes[n_id]["label_text"]
                        in insecure_exceptions
                    }
                    if exceptions:
                        yield shard, exceptions.pop()

    return get_vulnerabilities_from_n_ids(
        cwe=("396",),
        desc_key="src.lib_path.f060.insecure_exceptions.description",
        desc_params=dict(lang="CSharp"),
        finding=FINDING,
        graph_shard_nodes=n_ids(),
    )


def c_sharp_throws_for_generic_exception(
    graph_db: graph_model.GraphDB,
) -> core_model.Vulnerabilities:
    def n_ids() -> graph_model.GraphShardNodes:
        insecure_exceptions: Set[str] = {
            "Exception",
            "System.Exception",
            "SystemException",
            "System.SystemException",
            "NullReferenceException",
            "System.NullReferenceException",
            "IndexOutOfRangeException",
            "System.IndexOutOfRangeException",
        }
        for shard in graph_db.shards_by_language(
            graph_model.GraphShardMetadataLanguage.CSHARP,
        ):
            graph = shard.graph

            for catch_declaration in g.filter_nodes(
                graph,
                nodes=graph.nodes,
                predicate=g.pred_has_labels(label_type="throw_statement"),
            ):
                match_type_id = g.match_ast_group(
                    graph, catch_declaration, "throw", "__0__"
                )
                type_name = g.match_ast(
                    graph,
                    match_type_id["__0__"],
                    "identifier",
                    "qualified_name",
                )
                if _qualified := type_name["qualified_name"]:
                    exception = build_qualified_name(graph, _qualified)
                else:
                    exception = graph.nodes[type_name["identifier"]][
                        "label_text"
                    ]

                if exception in insecure_exceptions:
                    yield shard, _qualified

    return get_vulnerabilities_from_n_ids(
        cwe=("397",),
        desc_key="src.lib_path.f060.insecure_exceptions.description",
        desc_params=dict(lang="CSharp"),
        finding=FINDING,
        graph_shard_nodes=n_ids(),
    )


def java_insecure_exceptions(
    graph_db: graph_model.GraphDB,
) -> core_model.Vulnerabilities:
    def n_ids() -> graph_model.GraphShardNodes:
        insecure_exceptions: Set[str] = complete_attrs_on_set(
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
                        in insecure_exceptions
                    ):
                        yield shard, scoped_id

                for type_id in match_identifiers["type_identifier"]:
                    if (
                        graph.nodes[type_id].get("label_text")
                        in insecure_exceptions
                    ):
                        yield shard, type_id

    return get_vulnerabilities_from_n_ids(
        cwe=("396",),
        desc_key="src.lib_path.f060.insecure_exceptions.description",
        desc_params=dict(lang="Java"),
        finding=FINDING,
        graph_shard_nodes=n_ids(),
    )


def kotlin_generic_exceptions(
    graph_db: graph_model.GraphDB,
) -> core_model.Vulnerabilities:
    def n_ids() -> graph_model.GraphShardNodes:
        for shard in graph_db.shards_by_language(
            graph_model.GraphShardMetadataLanguage.KOTLIN
        ):
            for catch_clause in g.filter_nodes(
                shard.graph,
                shard.graph.nodes,
                g.pred_has_labels(label_type="catch_block"),
            ):
                exception_type_node = g.get_ast_childs(
                    shard.graph, catch_clause, "user_type"
                )
                exception_type = (
                    g.get_ast_childs(
                        shard.graph, exception_type_node[0], "type_identifier"
                    )
                    if exception_type_node
                    else tuple()
                )
                if exception_type and shard.graph.nodes[exception_type[0]][
                    "label_text"
                ] in {"Error", "Exception", "Throwable"}:
                    yield shard, catch_clause

    return get_vulnerabilities_from_n_ids(
        cwe=("397",),
        desc_key="src.lib_path.f060.insecure_exceptions.description",
        desc_params=dict(lang="Kotlin"),
        finding=FINDING,
        graph_shard_nodes=n_ids(),
    )


# Constants
FINDING: core_model.FindingEnum = core_model.FindingEnum.F060
QUERIES: graph_model.Queries = (
    (FINDING, java_declaration_of_throws_for_generic_exception),
    (FINDING, c_sharp_insecure_exceptions),
    (FINDING, c_sharp_throws_for_generic_exception),
    (FINDING, java_insecure_exceptions),
    (FINDING, kotlin_generic_exceptions),
)
