# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.object_creation import (
    build_object_creation_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    match_ast,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:
    node_attr = args.ast_graph.nodes[args.n_id]
    type_id = node_attr["label_field_type"]
    name = node_to_str(args.ast_graph, type_id)

    arguments_id = node_attr["label_field_arguments"]
    if "__0__" not in match_ast(args.ast_graph, arguments_id, "(", ")"):
        arguments_id = None

    return build_object_creation_node(args, name, arguments_id, None)
