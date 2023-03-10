from model.core_model import (
    MethodsEnum,
)
from model.graph_model import (
    Graph,
    NId,
)
from symbolic_eval.evaluate import (
    get_node_evaluation_results,
)
from utils import (
    graph as g,
)


def remote_command_exec_nodes(graph: Graph, method: MethodsEnum) -> list[NId]:
    vuln_nodes: list[NId] = []
    danger_methods = {"execSync", "exec"}
    for n_id in g.matching_nodes(graph, label_type="MethodInvocation"):
        m_expr = graph.nodes[n_id]["expression"]
        m_name = m_expr.split(".")[-1]
        if (m_name in danger_methods or m_expr == "execa.command") and (
            al_id := graph.nodes[n_id].get("arguments_id")
        ):
            args_ids = g.adj_ast(graph, al_id)
            if len(args_ids) > 0 and get_node_evaluation_results(
                method, graph, args_ids[0], set()
            ):
                vuln_nodes.append(args_ids[0])
    return vuln_nodes
