# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.method_declaration import (
    build_method_declaration_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:
    as_attrs = args.ast_graph.nodes[args.n_id]
    method_name = (
        node_to_str(args.ast_graph, name_id)
        if (name_id := as_attrs.get("label_field_name"))
        else None
    )

    block_id = as_attrs["label_field_body"]
    class_id = as_attrs["label_field_class"]

    return build_method_declaration_node(
        args, method_name, block_id, {"modifiers_id": class_id}
    )
