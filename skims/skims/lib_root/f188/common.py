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
    triggers = [
        {"WindowOriginChecked", "TypeOriginChecked"},
        {"WindowOriginChecked"},
        {"TypeOriginChecked"},
    ]
    for path in get_backward_paths(graph, n_id):
        evaluation = evaluate(method, graph, path, n_id)
        if evaluation and evaluation.triggers not in triggers:
            return True
    return False


def is_message_on_args(
    graph: Graph,
    n_id: NId,
) -> bool:
    arg_list = g.adj_ast(graph, n_id, label_type="ArgumentList")[0]
    args_childs = g.adj_ast(graph, arg_list)
    if (
        graph.nodes[args_childs[0]]["value"] == "'message'"
        and graph.nodes[args_childs[1]]["label_type"] == "MethodDeclaration"
    ):
        return True
    return False


def has_dangerous_param(graph: Graph) -> list[NId]:
    vuln_nodes: list[NId] = []
    sensitive_methods = {"window.addEventListener"}
    method = MethodsEnum.TSX_LACK_OF_VALIDATION_EVENT_LISTENER
    for member in g.matching_nodes(graph, label_type="MethodInvocation"):
        if (
            graph.nodes[member].get("expression") in sensitive_methods
            and is_message_on_args(graph, member)
            and is_insec_invocation(graph, member, method)
        ):
            vuln_nodes.append(member)

    return vuln_nodes
