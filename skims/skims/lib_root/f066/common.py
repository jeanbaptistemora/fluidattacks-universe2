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


def nid_uses_console_log(graph: Graph) -> List[NId]:
    vuln_nodes: List[NId] = []
    for n_id in g.filter_nodes(
        graph,
        graph.nodes,
        predicate=g.pred_has_labels(label_type="MethodInvocation"),
    ):
        if graph.nodes[n_id].get("expression") == "console.log":
            vuln_nodes.append(n_id)
    return vuln_nodes
