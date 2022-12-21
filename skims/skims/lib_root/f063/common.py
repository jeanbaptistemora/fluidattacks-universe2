from lib_root.utilities.common import (
    search_method_invocation_naive,
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


def get_eval_danger(graph: Graph, n_id: NId, method: MethodsEnum) -> bool:
    for path in get_backward_paths(graph, n_id):
        evaluation = evaluate(method, graph, path, n_id)
        if (
            evaluation
            and evaluation.danger
            and evaluation.triggers != {"resolve", "sanitize"}
        ):
            return True
    return False


def require_fs_library(graph: Graph) -> bool:
    for n_id in g.matching_nodes(graph, label_type="MethodInvocation"):
        m_name = graph.nodes[n_id]["expression"]
        if (
            m_name == "require"
            and (al_id := graph.nodes[n_id].get("arguments_id"))
            and (arg_id := g.match_ast(graph, al_id).get("__0__"))
            and (import_module := graph.nodes[arg_id].get("value"))
            and import_module[1:-1] == "fs"
        ):
            return True
    return False


def import_fs_library(graph: Graph) -> bool:
    for n_id in g.matching_nodes(graph, label_type="Import"):
        if (
            import_module := graph.nodes[n_id].get("expression")
        ) and import_module[1:-1] == "fs":
            return True
    return False


def insecure_path_traversal(graph: Graph, method: MethodsEnum) -> List[NId]:
    vuln_nodes: List[NId] = []
    danger_methods = {
        "readdir",
        "readdirSync",
        "readFile",
        "readFileSync",
        "unlink",
        "unlinkSync",
        "writeFile",
        "writeFileSync",
    }
    if not (import_fs_library(graph) or require_fs_library(graph)):
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
