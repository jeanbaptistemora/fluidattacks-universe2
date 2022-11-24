from lib_root.f052.common import (
    split_function_name,
)
from model.core_model import (
    MethodsEnum,
)
from model.graph_model import (
    Graph,
    NId,
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


def is_logger_unsafe(graph: Graph, n_id: str, method: MethodsEnum) -> bool:
    if test_node := graph.nodes[n_id].get("arguments_id"):
        for path in get_backward_paths(graph, test_node):
            evaluation = evaluate(method, graph, path, test_node)
            if (
                evaluation
                and evaluation.danger
                and not (
                    "sanitized" in evaluation.triggers
                    and "characters" in evaluation.triggers
                )
            ):
                return True

    return False


def insecure_logging(graph: Graph, method: MethodsEnum) -> List[NId]:
    vuln_nodes: List[NId] = []
    danger_objects = {
        "console",
        "logger",
        "log",
    }
    danger_methods = {
        "info",
        "warn",
        "error",
        "trace",
        "debug",
    }

    for n_id in g.filter_nodes(
        graph,
        graph.nodes,
        predicate=g.pred_has_labels(label_type="MethodInvocation"),
    ):
        f_name = graph.nodes[n_id]["expression"]
        obj, funct = split_function_name(f_name)
        if (
            obj.lower() in danger_objects
            and funct in danger_methods
            and is_logger_unsafe(graph, n_id, method)
        ):
            vuln_nodes.append(n_id)
    return vuln_nodes
