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
    split_on_last_dot,
)


def get_eval_danger(graph: Graph, n_id: NId, method: MethodsEnum) -> bool:
    for path in get_backward_paths(graph, n_id):
        evaluation = evaluate(method, graph, path, n_id)
        if evaluation and evaluation.danger:
            return True
    return False


def get_vuln_nodes(graph: Graph, method: MethodsEnum) -> List[str]:
    vuln_nodes: List[str] = []
    for nid in g.filter_nodes(
        graph,
        graph.nodes,
        predicate=g.pred_has_labels(label_type="MethodInvocation"),
    ):
        f_name: Tuple[str, str] = split_on_last_dot(
            graph.nodes[nid]["expression"]
        )
        if f_name[-1] == "parseXmlString":
            if args := g.match_ast_d(graph, nid, "ArgumentList"):
                childs = g.adj_ast(graph, args)
                if len(childs) > 1 and get_eval_danger(
                    graph, childs[1], method
                ):
                    vuln_nodes.append(nid)

    return vuln_nodes
