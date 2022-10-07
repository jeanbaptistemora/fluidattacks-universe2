# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from contextlib import (
    suppress,
)
from model.graph_model import (
    Graph,
    NId,
)
from symbolic_eval.types import (
    Path,
)
from symbolic_eval.utils import (
    get_lookup_path,
)
from typing import (
    List,
    Optional,
)
from utils import (
    graph as g,
)


def search_data_element(
    graph: Graph, path: Path, method_id: NId
) -> Optional[NId]:
    n_attrs = graph.nodes[method_id]
    var_name = graph.nodes[n_attrs["object_id"]].get("symbol")
    access_id = g.match_ast(graph, n_attrs["arguments_id"]).get("__0__")

    if not (var_name and access_id):
        return None

    m_path = get_lookup_path(graph, path, method_id)

    if graph.nodes[access_id].get("value_type") == "number":
        with suppress(ValueError):
            access_val = int(graph.nodes[access_id].get("value"))
            return get_element_by_idx(graph, m_path, var_name, access_val)

    return None


def get_element_by_idx(
    graph: Graph, path: Path, var_name: str, access_val: int
) -> Optional[NId]:
    d_nodes: List[str] = []
    for n_id in reversed(path):
        n_attrs = graph.nodes[n_id]
        if (
            n_attrs["label_type"] == "MethodInvocation"
            and (object_id := n_attrs.get("object_id"))
            and graph.nodes[object_id].get("symbol") == var_name
            and (al_id := n_attrs["arguments_id"])
            and (arg_id := g.match_ast(graph, al_id).get("__0__"))
        ):
            if n_attrs.get("expression") in {"add", "push", "put"}:
                d_nodes.append(arg_id)
            elif n_attrs.get("expression") in {"remove"} and (
                idx := graph.nodes[arg_id].get("value")
            ):
                try:
                    d_nodes.pop(int(idx))
                except ValueError:
                    d_nodes.pop()

    if len(d_nodes) >= access_val:
        return d_nodes[access_val]

    return None
