# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.constructor_declaration import (
    build_constructor_declaration_node,
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
    method = args.ast_graph.nodes[args.n_id]
    name_id = method["label_field_name"]
    parameters_id = method["label_field_parameters"]
    block_id = method["label_field_body"]
    name = node_to_str(args.ast_graph, name_id)
    if "__0__" not in match_ast(args.ast_graph, parameters_id, "(", ")"):
        parameters_id = None
    return build_constructor_declaration_node(
        args, name, block_id, parameters_id
    )
