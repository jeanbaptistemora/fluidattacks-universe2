# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    Graph,
    NId,
)
from typing import (
    List,
)
from utils import (
    graph as g,
)


def is_argument_literal(graph: Graph, n_id: NId) -> bool:
    if (args := g.match_ast(graph, n_id)) and (
        len(args) == 1
        and graph.nodes[args.get("__0__")]["label_type"] == "Literal"
    ):
        return True
    return False


def has_eval(graph: Graph) -> List[NId]:
    vuln_nodes: List[NId] = []
    sensitive_methods = {"eval", "Function"}

    for member in g.filter_nodes(
        graph,
        graph.nodes,
        predicate=g.pred_has_labels(label_type="MethodInvocation"),
    ):
        if (args_id := graph.nodes[member].get("arguments_id")) and (
            graph.nodes[member].get("expression") in sensitive_methods
            and not is_argument_literal(graph, args_id)
        ):
            vuln_nodes.append(member)

    return vuln_nodes
