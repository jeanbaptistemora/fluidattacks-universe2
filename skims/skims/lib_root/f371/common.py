# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from lib_root.utilities.c_sharp import (
    yield_syntax_graph_member_access,
)
from model.graph_model import (
    Graph,
    GraphShard,
    GraphShardNode,
)
from typing import (
    Iterable,
    List,
)
from utils import (
    graph as g,
)


def has_innerhtml(shard: GraphShard) -> Iterable[GraphShardNode]:
    if shard.syntax_graph is not None:
        graph = shard.syntax_graph
        for nid in yield_syntax_graph_member_access(graph, {"innerHTML"}):
            yield shard, nid


def has_bypass_sec(graph: Graph) -> List[str]:
    vuln_nodes: List[str] = []
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
