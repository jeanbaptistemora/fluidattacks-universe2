from model.graph_model import (
    Graph,
    NId,
)
from utils import (
    graph as g,
)


def crypto_credentials(graph: Graph) -> list[NId]:
    vuln_nodes: list[NId] = []
    danger_methods = {
        "cryptojs.enc.base64.parse",
        "cryptojs.enc.utf16.parse",
        "cryptojs.enc.utf16le.parse",
        "cryptojs.enc.hex.parse",
        "cryptojs.enc.latin1.parse",
        "cryptojs.enc.utf8.parse",
        "enc.base64.parse",
        "enc.utf16.parse",
        "enc.utf16le.parse",
        "enc.hex.parse",
        "enc.latin1.parse",
        "enc.utf8.parse",
    }

    for n_id in g.matching_nodes(
        graph,
        label_type="MethodInvocation",
    ):
        n_attrs = graph.nodes[n_id]
        m_name = n_attrs.get("expression")
        al_id = n_attrs.get("arguments_id")

        if not (m_name and al_id):
            continue

        arg_childs = g.adj_ast(graph, al_id)
        if (
            m_name.lower() in danger_methods
            and len(arg_childs) == 1
            and graph.nodes[arg_childs[0]].get("value_type") == "string"
            and graph.nodes[arg_childs[0]].get("value") not in {'""', "''"}
        ):
            vuln_nodes.append(n_id)

    return vuln_nodes
