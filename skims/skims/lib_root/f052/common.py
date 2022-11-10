# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

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
    Tuple,
)
from utils import (
    graph as g,
)
from utils.string import (
    complete_attrs_on_set,
)


def split_function_name(f_names: str) -> Tuple[str, str]:
    name_l = f_names.lower().split(".")
    if len(name_l) < 2:
        return "", name_l[-1]
    return name_l[-2], name_l[-1]


def get_eval_danger(graph: Graph, n_id: str, method: MethodsEnum) -> bool:
    for path in get_backward_paths(graph, n_id):
        evaluation = evaluate(method, graph, path, n_id)
        if evaluation and evaluation.danger:
            return True
    return False


def insecure_create_cipher(graph: Graph, method: MethodsEnum) -> List[NId]:
    vuln_nodes: List[NId] = []
    ciphers_methods = {
        "createdecipher",
        "createcipher",
        "createdecipheriv",
        "createcipheriv",
    }
    for n_id in g.filter_nodes(
        graph,
        nodes=graph.nodes,
        predicate=g.pred_has_labels(label_type="MethodInvocation"),
    ):
        f_name = graph.nodes[n_id]["expression"]
        _, crypt = split_function_name(f_name)
        if (
            crypt in ciphers_methods
            and (al_id := graph.nodes[n_id].get("arguments_id"))
            and (args := g.adj_ast(graph, al_id))
            and len(args) > 0
            and get_eval_danger(graph, args[0], method)
        ):
            vuln_nodes.append(n_id)

    return vuln_nodes


def insecure_hash(graph: Graph, method: MethodsEnum) -> List[NId]:
    vuln_nodes: List[NId] = []
    danger_methods = complete_attrs_on_set({"crypto.createHash"})

    for n_id in g.filter_nodes(
        graph,
        nodes=graph.nodes,
        predicate=g.pred_has_labels(label_type="MethodInvocation"),
    ):
        if (
            graph.nodes[n_id]["expression"] in danger_methods
            and (al_id := graph.nodes[n_id].get("arguments_id"))
            and (test_node := g.match_ast(graph, al_id).get("__0__"))
            and get_eval_danger(graph, test_node, method)
        ):
            vuln_nodes.append(n_id)
    return vuln_nodes
