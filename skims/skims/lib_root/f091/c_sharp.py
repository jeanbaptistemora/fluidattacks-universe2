from itertools import (
    chain,
)
from lib_sast.types import (
    ShardDb,
)
from model import (
    core_model,
    graph_model,
)
from model.graph_model import (
    Graph,
    GraphShardMetadataLanguage as GraphLanguage,
)
from sast.query import (
    get_vulnerabilities_from_n_ids,
)
from symbolic_eval.evaluate import (
    evaluate,
)
from symbolic_eval.utils import (
    get_backward_paths,
)
from typing import (
    List,
)
from utils import (
    graph as g,
)


def get_insecure_vars(graph: Graph) -> List[str]:
    object_methods = {"GetLogger", "GetCurrentClassLogger"}
    object_names = {
        "FileLogger",
        "DBLogger",
        "EventLogger",
        "EventLog",
        "StreamWriter",
        "TraceSource",
    }
    insecure_vars = []
    for nid in chain(
        g.filter_nodes(
            graph,
            graph.nodes,
            g.pred_has_labels(label_type="MethodInvocation"),
        ),
        g.filter_nodes(
            graph,
            graph.nodes,
            g.pred_has_labels(label_type="ObjectCreation"),
        ),
    ):
        if (
            graph.nodes[nid].get("label_type") == "MethodInvocation"
            and graph.nodes[nid].get("expression").split(".")[-1]
            in object_methods
        ) or (
            graph.nodes[nid].get("label_type") == "ObjectCreation"
            and graph.nodes[nid].get("name") in object_names
        ):
            var_nid = g.pred_ast(graph, nid)[0]
            if graph.nodes[var_nid].get("label_type") == "VariableDeclaration":
                insecure_vars.append(graph.nodes[var_nid].get("variable"))
    return insecure_vars


def insecure_logging(
    shard_db: ShardDb,  # pylint: disable=unused-argument
    graph_db: graph_model.GraphDB,
) -> core_model.Vulnerabilities:
    method = core_model.MethodsEnum.CS_INSECURE_LOGGING
    c_sharp = GraphLanguage.CSHARP
    logging_methods = {
        "Info",
        "Log",
        "WriteLine",
        "WriteEntry",
        "TraceEvent",
        "Debug",
    }
    sanitize = {"\\n", "\\t", "\\r"}

    def n_ids() -> graph_model.GraphShardNodes:
        for shard in graph_db.shards_by_language(c_sharp):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph
            insecure_vars = get_insecure_vars(graph)

            for nid in g.filter_nodes(
                graph,
                graph.nodes,
                g.pred_has_labels(label_type="MemberAccess"),
            ):
                if not (
                    graph.nodes[nid].get("member") in logging_methods
                    and graph.nodes[nid].get("expression") in insecure_vars
                ):
                    continue
                al_id = graph.nodes[g.pred(graph, nid)[0]].get("arguments_id")
                if test_node := g.match_ast(graph, al_id).get("__0__"):
                    for path in get_backward_paths(graph, test_node):
                        evaluation = evaluate(method, graph, path, test_node)
                        if (
                            evaluation
                            and evaluation.danger
                            and not (
                                "Replace" in evaluation.triggers
                                and all(
                                    char in evaluation.triggers
                                    for char in sanitize
                                )
                            )
                        ):
                            yield shard, nid

    return get_vulnerabilities_from_n_ids(
        desc_key="criteria.vulns.091.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
