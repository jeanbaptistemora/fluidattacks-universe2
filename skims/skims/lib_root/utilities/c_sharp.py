from model.graph_model import (
    Graph,
    NId,
)
from typing import (
    Any,
    Iterator,
    Optional,
    Set,
)
from utils import (
    graph as g,
)


def yield_syntax_graph_member_access(
    graph: Graph, members: Set[str]
) -> Iterator[NId]:
    for nid in g.filter_nodes(
        graph,
        nodes=graph.nodes,
        predicate=g.pred_has_labels(label_type="MemberAccess"),
    ):
        if graph.nodes[nid].get("expression") in members:
            yield nid


def yield_syntax_graph_object_creation(
    graph: Graph, members: Set[str]
) -> Iterator[NId]:
    for nid in g.filter_nodes(
        graph,
        nodes=graph.nodes,
        predicate=g.pred_has_labels(label_type="ObjectCreation"),
    ):
        if graph.nodes[nid].get("name") in members:
            yield nid


def get_first_member_syntax_graph(graph: Graph, n_id: str) -> Optional[str]:
    member: Any = g.match_ast(graph, n_id, "MemberAccess")
    if member.get("MemberAccess") == "None":
        return n_id
    while member.get("MemberAccess"):
        member = member.get("MemberAccess")
        member = g.match_ast(graph, member, "MemberAccess")
    return member["__0__"]
