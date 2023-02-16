from lib_root.utilities.c_sharp import (
    yield_syntax_graph_member_access,
)
from model.graph_model import (
    Graph,
    NId,
)
from utils import (
    graph as g,
)


def has_innerhtml(graph: Graph) -> list[NId]:
    vuln_nodes: list[NId] = []
    for nid in yield_syntax_graph_member_access(graph, {"innerHTML"}):
        vuln_nodes.append(nid)
    return vuln_nodes


def has_bypass_sec(graph: Graph) -> list[NId]:
    vuln_nodes: list[NId] = []
    risky_methods = {
        "bypassSecurityTrustHtml",
        "bypassSecurityTrustScript",
        "bypassSecurityTrustStyle",
        "bypassSecurityTrustUrl",
        "bypassSecurityTrustResourceUrl",
    }
    for nid in g.matching_nodes(graph, label_type="MemberAccess"):
        f_name = graph.nodes[nid]["expression"]
        if f_name in risky_methods:
            vuln_nodes.append(nid)

    return vuln_nodes


def has_set_inner_html(graph: Graph) -> list[NId]:
    vuln_nodes: list[NId] = []
    for nid in g.matching_nodes(graph, label_type="JsxElement"):
        ast_childs = g.match_ast(graph, nid, "VariableDeclaration")
        child = ast_childs.get("VariableDeclaration")
        if (
            child
            and graph.nodes[child]["variable"] == "dangerouslySetInnerHTML"
        ):
            vuln_nodes.append(child)

    return vuln_nodes
