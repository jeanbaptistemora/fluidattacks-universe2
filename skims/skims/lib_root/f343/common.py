from lib_root.utilities.javascript import (
    get_default_alias,
)
from model.graph_model import (
    Graph,
    NId,
)
from typing import (
    Set,
)
from utils import (
    graph as g,
)


def is_vuln_node(graph: Graph, n_id: NId) -> bool:
    return bool(
        (key_n_id := graph.nodes[n_id].get("key_id"))
        and (graph.nodes[key_n_id].get("symbol") == "algorithm")
        and (value_n_id := graph.nodes[n_id].get("value_id"))
        and (graph.nodes[value_n_id].get("value") == '"' + "gzip" + '"')
    )


def webpack_insecure_compression(graph: Graph) -> Set[NId]:
    vuln_nodes: Set[NId] = set()
    if dangerous_library := get_default_alias(
        graph, "compression-webpack-plugin"
    ):
        for n_id in g.matching_nodes(
            graph, label_type="ObjectCreation", name=dangerous_library
        ):
            for p_id in g.get_nodes_by_path(
                graph, n_id, [], "ArgumentList", "Object", "Pair"
            ):
                if is_vuln_node(graph, p_id):
                    vuln_nodes.add(p_id)
    return vuln_nodes
