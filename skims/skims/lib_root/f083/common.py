from model.core_model import (
    MethodsEnum,
)
from model.graph_model import (
    Graph,
)
from symbolic_eval.evaluate import (
    get_node_evaluation_results,
)
from utils import (
    graph as g,
)
from utils.string import (
    split_on_last_dot,
)


def get_vuln_nodes(graph: Graph, method: MethodsEnum) -> list[str]:
    vuln_nodes: list[str] = []
    for nid in g.matching_nodes(graph, label_type="MethodInvocation"):
        f_name: tuple[str, str] = split_on_last_dot(
            graph.nodes[nid]["expression"]
        )
        if f_name[-1] == "parseXmlString":
            if args := g.match_ast_d(graph, nid, "ArgumentList"):
                childs = g.adj_ast(graph, args)
                if len(childs) > 1 and get_node_evaluation_results(
                    method, graph, childs[1], set()
                ):
                    vuln_nodes.append(nid)

    return vuln_nodes
