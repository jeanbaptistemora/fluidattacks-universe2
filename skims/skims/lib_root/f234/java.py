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


def java_method_invoc_to_str(graph: graph_model.Graph, method_inv: str) -> str:
    ids = g.match_ast_group(graph, method_inv, "identifier")["identifier"]
    return ".".join([graph.nodes[i]["label_text"] for i in ids])


def info_leak_stacktrace(
    graph_db: graph_model.GraphDB,
) -> core_model.Vulnerabilities:
    def n_ids() -> graph_model.GraphShardNodes:
        for shard in graph_db.shards_by_language(
            graph_model.GraphShardMetadataLanguage.JAVA,
        ):
            graph = shard.graph
            for catch in g.filter_nodes(
                graph,
                nodes=graph.nodes,
                predicate=g.pred_has_labels(label_type="catch_clause"),
            ):
                param = g.match_ast_d(graph, catch, "catch_formal_parameter")
                exception_id = g.match_ast_d(graph, param, "identifier")

                if exception_id is None:
                    continue

                exception = graph.nodes[exception_id]["label_text"]
                block = g.match_ast_d(graph, catch, "block")
                for method_inv_id in g.filter_nodes(
                    graph,
                    nodes=g.adj_ast(graph, block, depth=-1),
                    predicate=g.pred_has_labels(
                        label_type="method_invocation"
                    ),
                ):
                    method_inv = java_method_invoc_to_str(graph, method_inv_id)
                    if method_inv == f"{exception}.printStackTrace":
                        yield shard, method_inv_id

    return get_vulnerabilities_from_n_ids(
        cwe=("209",),
        desc_key="src.lib_root.f234.java_info_leak_stacktrace",
        desc_params=dict(lang="Java"),
        finding=FINDING,
        graph_shard_nodes=n_ids(),
    )


FINDING: core_model.FindingEnum = core_model.FindingEnum.F234
