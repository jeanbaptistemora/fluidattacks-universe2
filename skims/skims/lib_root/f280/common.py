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
    Dict,
    List,
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


def _has_dangerous_literal(graph: Graph, args: Dict) -> bool:
    sensitive_params = {'"Set-Cookie"', '"connect.sid"'}
    if (
        len(args) == 2
        and (first_param := graph.nodes[args["__0__"]])
        and (first_param.get("label_type") == "Literal")
        and (first_param.get("value") in sensitive_params)
    ):
        return True
    return False


def has_dangerous_param(graph: Graph) -> List[NId]:
    vuln_nodes: List[NId] = []
    sensitive_methods = {"res.setHeader", "res.cookie"}

    for member in g.matching_nodes(graph, label_type="MethodInvocation"):
        if (
            graph.nodes[member].get("expression") in sensitive_methods
            and (args_id := graph.nodes[member].get("arguments_id"))
            and (args := g.match_ast(graph, args_id))
            and (_has_dangerous_literal(graph, args))
        ):
            vuln_nodes.append(member)

    return vuln_nodes
