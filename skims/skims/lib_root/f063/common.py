# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

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


def eval_insecure_path(graph: Graph, n_id: NId, method: MethodsEnum) -> bool:
    for path in get_backward_paths(graph, n_id):
        evaluation = evaluate(method, graph, path, n_id)
        if evaluation and evaluation.triggers != {"resolve"}:
            return True
    return False


def insecure_path_traversal(graph: Graph, method: MethodsEnum) -> List[NId]:
    vuln_nodes: List[NId] = []

    for n_id in search_method_invocation_naive(graph, {"readFileSync"}):
        if (args_id := graph.nodes[n_id].get("arguments_id")) and (
            (test_id := g.match_ast(graph, args_id).get("__0__"))
            and eval_insecure_path(graph, test_id, method)
        ):
            vuln_nodes.append(n_id)
    return vuln_nodes
