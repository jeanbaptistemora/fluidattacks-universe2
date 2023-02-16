from itertools import (
    chain,
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
from utils import (
    graph as g,
)


def is_insec_invocation(graph: Graph, n_id: NId, method: MethodsEnum) -> bool:
    for path in get_backward_paths(graph, n_id):
        evaluation = evaluate(method, graph, path, n_id)
        if evaluation and evaluation.danger:
            return True
    return False


def only_one_argument(graph: Graph, n_id: NId) -> bool:
    if (args := g.match_ast(graph, n_id)) and (len(args) == 1):
        return True
    return False


def has_eval(graph: Graph) -> list[NId]:
    vuln_nodes: list[NId] = []
    sensitive_methods = {"eval", "Function"}

    for member in chain(
        g.matching_nodes(graph, label_type="MethodInvocation"),
        g.matching_nodes(graph, label_type="ObjectCreation"),
    ):
        if (
            (
                graph.nodes[member].get("expression") in sensitive_methods
                or graph.nodes[member].get("name") in sensitive_methods
            )
            and (args_id := graph.nodes[member].get("arguments_id"))
            and only_one_argument(graph, args_id)
        ):
            vuln_nodes.append(member)

    return vuln_nodes
