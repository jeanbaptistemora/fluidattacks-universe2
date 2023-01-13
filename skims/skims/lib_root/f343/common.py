from lib_root.utilities.javascript import (
    get_default_alias,
)
from model.graph_model import (
    Graph,
    NId,
)
from typing import (
    Optional,
    Set,
)
from utils import (
    graph as g,
)


def get_vuln_nodes(graph: Graph, n_id: NId) -> Optional[NId]:
    algorithm_set_flag: bool = False
    for p_id in g.get_nodes_by_path(
        graph, n_id, [], "ArgumentList", "Object", "Pair"
    ):
        if (key_n_id := graph.nodes[p_id].get("key_id")) and (
            graph.nodes[key_n_id].get("symbol") == "algorithm"
        ):
            algorithm_set_flag = True
            if (value_n_id := graph.nodes[p_id].get("value_id")) and (
                graph.nodes[value_n_id].get("value") == '"' + "gzip" + '"'
            ):
                return p_id
    if not algorithm_set_flag:
        return n_id
    return None


def webpack_insecure_compression(graph: Graph) -> Set[NId]:
    vuln_nodes: Set[NId] = set()
    if dangerous_library := get_default_alias(
        graph, "compression-webpack-plugin"
    ):
        for n_id in g.matching_nodes(
            graph, label_type="ObjectCreation", name=dangerous_library
        ):
            if vuln_node := get_vuln_nodes(graph, n_id):
                vuln_nodes.add(vuln_node)

    return vuln_nodes
