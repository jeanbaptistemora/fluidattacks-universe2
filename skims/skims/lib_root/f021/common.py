from lib_root.utilities.common import (
    search_method_invocation_naive,
)
from lib_root.utilities.javascript import (
    file_imports_module,
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


def get_eval_danger(graph: Graph, n_id: NId, method: MethodsEnum) -> bool:
    for path in get_backward_paths(graph, n_id):
        evaluation = evaluate(method, graph, path, n_id)
        if (
            evaluation
            and evaluation.danger
            and evaluation.triggers == {"userparameters"}
        ):
            return True
    return False


def insecure_dynamic_xpath(graph: Graph, method: MethodsEnum) -> list[NId]:
    vuln_nodes: list[NId] = []
    danger_methods = {"select", "parse"}
    if not (
        file_imports_module(graph, "fs")
        and file_imports_module(graph, "xpath")
    ):
        return vuln_nodes
    for n_id in search_method_invocation_naive(graph, danger_methods):
        if (
            (al_id := graph.nodes[n_id].get("arguments_id"))
            and (args_ids := g.adj_ast(graph, al_id))
            and len(args_ids) >= 1
            and get_eval_danger(graph, args_ids[0], method)
        ):
            vuln_nodes.append(n_id)
    return vuln_nodes
