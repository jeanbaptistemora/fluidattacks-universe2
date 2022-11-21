# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from lib_root.f052.common import (
    split_function_name,
)
from model.core_model import (
    MethodsEnum,
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


def insecure_logging(graph: Graph, method: MethodsEnum) -> List[NId]:
    vuln_nodes: List[NId] = []
    danger_objects = {
        "console",
        "logger",
        "log",
    }
    danger_methods = {
        "info",
        "warn",
        "error",
        "trace",
        "debug",
    }

    for n_id in g.filter_nodes(
        graph,
        graph.nodes,
        predicate=g.pred_has_labels(label_type="MethodInvocation"),
    ):
        f_name = graph.nodes[n_id]["expression"]
        obj, funct = split_function_name(f_name)
        if (
            obj.lower() in danger_objects
            and funct in danger_methods
            and method
        ):
            vuln_nodes.append(n_id)
    return vuln_nodes
