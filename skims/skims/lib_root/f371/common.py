# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from lib_root.utilities.c_sharp import (
    yield_syntax_graph_member_access,
)
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


def has_innerhtml(graph: Graph) -> List[NId]:
    vuln_nodes: List[NId] = []
    for nid in yield_syntax_graph_member_access(graph, {"innerHTML"}):
        vuln_nodes.append(nid)
    return vuln_nodes


def has_bypass_sec(graph: Graph) -> List[NId]:
    vuln_nodes: List[NId] = []
    risky_methods = {
        "bypassSecurityTrustHtml",
        "bypassSecurityTrustScript",
        "bypassSecurityTrustStyle",
        "bypassSecurityTrustUrl",
        "bypassSecurityTrustResourceUrl",
    }
    for nid in g.filter_nodes(
        graph,
        graph.nodes,
        predicate=g.pred_has_labels(label_type="MemberAccess"),
    ):
        f_name = graph.nodes[nid]["expression"]
        if f_name in risky_methods:
            vuln_nodes.append(nid)

    return vuln_nodes


def has_set_inner_html(graph: Graph) -> List[NId]:
    vuln_nodes: List[NId] = []
    for nid in g.filter_nodes(
        graph,
        graph.nodes,
        predicate=g.pred_has_labels(label_type="JsxElement"),
    ):
        ast_childs = g.match_ast(graph, nid, "VariableDeclaration")
        child = ast_childs.get("VariableDeclaration")
        if (
            child
            and graph.nodes[child]["variable"] == "dangerouslySetInnerHTML"
        ):
            vuln_nodes.append(child)

    return vuln_nodes
