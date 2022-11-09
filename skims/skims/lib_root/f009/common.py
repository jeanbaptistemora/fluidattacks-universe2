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
from utils.string import (
    complete_attrs_on_set,
)


def crypto_credentials(graph: Graph) -> List[NId]:
    vuln_nodes: List[NId] = []
    danger_methods = complete_attrs_on_set(
        {
            "CryptoJS.enc.Base64.parse",
            "CryptoJS.enc.Utf16.parse",
            "CryptoJS.enc.Utf16LE.parse",
            "CryptoJS.enc.Hex.parse",
            "CryptoJS.enc.Latin1.parse",
            "CryptoJS.enc.Utf8.parse",
        }
    )
    for n_id in g.filter_nodes(
        graph,
        nodes=graph.nodes,
        predicate=g.pred_has_labels(label_type="MethodInvocation"),
    ):
        n_attrs = graph.nodes[n_id]
        if (
            n_attrs["expression"] in danger_methods
            and (al_id := n_attrs.get("arguments_id"))
            and (child := g.match_ast_d(graph, al_id, "Literal"))
            and graph.nodes[child]["value_type"] == "string"
            and graph.nodes[child]["value"] not in {'""', "''"}
        ):

            vuln_nodes.append(n_id)

    return vuln_nodes
