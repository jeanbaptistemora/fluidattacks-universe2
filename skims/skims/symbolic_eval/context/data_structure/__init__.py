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
    obj_id = n_attrs.get("object_id")
    al_id = n_attrs.get("arguments_id")

    if not (obj_id and al_id):
        return None

    var_name = graph.nodes[n_attrs["object_id"]].get("symbol") or ""
    access_id = g.adj_ast(graph, al_id)[0]
    m_path = get_lookup_path(graph, path, method_id)
    access_nid = graph.nodes[access_id]
    if access_nid.get("value_type") == "number":
        with suppress(ValueError):
            access_val = int(access_nid.get("value"))
            return get_element_by_idx(graph, m_path, var_name, access_val)
    elif access_nid.get("value_type") == "string":
        access_key = str(access_nid["value"])
        el_id = get_element_by_key(graph, m_path, var_name, access_key)
        return el_id

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
            and (al_id := n_attrs.get("arguments_id"))
            and (arg_id := g.match_ast(graph, al_id).get("__0__"))
        ):
            if n_attrs.get("expression") in {"add", "push"}:
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


def get_element_by_key(
    graph: Graph, path: Path, var_name: str, access_key: str
) -> Optional[NId]:
    for n_id in path:
        n_attrs = graph.nodes[n_id]
        if (
            n_attrs["label_type"] != "MethodInvocation"
            or not n_attrs.get("object_id")
            or n_attrs.get("expression") not in {"put"}
        ):
            continue

        if (
            graph.nodes[n_attrs["object_id"]].get("symbol") == var_name
            and (al_id := n_attrs.get("arguments_id"))
            and (arg_ids := g.adj_ast(graph, al_id))
            and len(arg_ids) >= 2
            and graph.nodes[arg_ids[0]].get("value") == access_key
        ):
            return arg_ids[1]
    return None
