# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.resource import (
    build_resource_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph

    resource = graph.nodes[args.n_id]
    type_id = resource.get("label_field_type")
    value_id = resource.get("label_field_value")
    identifier_id = resource["label_field_name"]

    variable = node_to_str(graph, identifier_id)
    variable_type = None if type_id is None else node_to_str(graph, type_id)

    return build_resource_node(args, variable, variable_type, value_id)
