from collections.abc import (
    Iterator,
)
from itertools import (
    chain,
)
from model.core_model import (
    MethodsEnum,
    Vulnerabilities,
)
from model.graph_model import (
    Graph,
    GraphDB,
    GraphShardMetadataLanguage as GraphLanguage,
    GraphShardNode,
    NId,
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
from utils import (
    graph as g,
)


def get_insecure_vars(graph: Graph) -> list[str]:
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
        g.matching_nodes(graph, label_type="MethodInvocation"),
        g.matching_nodes(graph, label_type="ObjectCreation"),
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


def is_insecure_logging(graph: Graph, n_id: NId) -> bool:
    method = MethodsEnum.CS_INSECURE_LOGGING
    sanitize = {"\\n", "\\t", "\\r"}

    al_id = graph.nodes[g.pred(graph, n_id)[0]].get("arguments_id")
    if test_node := g.match_ast(graph, al_id).get("__0__"):
        for path in get_backward_paths(graph, test_node):
            evaluation = evaluate(method, graph, path, test_node)
            if (
                evaluation
                and evaluation.danger
                and not (
                    "Replace" in evaluation.triggers
                    and all(char in evaluation.triggers for char in sanitize)
                )
            ):
                return True
    return False


def insecure_logging(
    graph_db: GraphDB,
) -> Vulnerabilities:
    c_sharp = GraphLanguage.CSHARP
    logging_methods = {
        "Info",
        "Log",
        "WriteLine",
        "WriteEntry",
        "TraceEvent",
        "Debug",
    }

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(c_sharp):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph
            insecure_vars = get_insecure_vars(graph)

            for nid in g.matching_nodes(graph, label_type="MemberAccess"):
                if (
                    graph.nodes[nid].get("member") in logging_methods
                    and graph.nodes[nid].get("expression") in insecure_vars
                    and is_insecure_logging(graph, nid)
                ):
                    yield shard, nid

    return get_vulnerabilities_from_n_ids(
        desc_key="criteria.vulns.091.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=MethodsEnum.CS_INSECURE_LOGGING,
    )
