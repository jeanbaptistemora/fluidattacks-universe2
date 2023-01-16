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


def local_storage_from_http(graph: Graph) -> Set[NId]:
    vuln_nodes: Set[NId] = set()
    if dangerous_library := get_default_alias(
        graph, "provisional_placeholder"
    ):
        for n_id in g.matching_nodes(
            graph, label_type="ObjectCreation", name=dangerous_library
        ):
            vuln_nodes.add(n_id)

    return vuln_nodes
