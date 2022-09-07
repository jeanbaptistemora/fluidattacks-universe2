# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.class_decl import (
    build_class_node,
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
    class_node = args.ast_graph.nodes[args.n_id]
    name_id = class_node["label_field_name"]
    block_id = class_node["label_field_body"]
    name = node_to_str(args.ast_graph, name_id)

    match_childs = match_ast(args.ast_graph, args.n_id, "attribute_list")
    attributes = match_childs.get("attribute_list")
    return build_class_node(args, name, block_id, attributes)
