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
from utils.graph import (
    match_ast,
)


def reader(args: SyntaxGraphArgs) -> NId:
    n_attrs = args.ast_graph.nodes[args.n_id]
    block_id = n_attrs["label_field_body"]

    parameters_id = n_attrs["label_field_parameters"]
    if parameters_id and "__0__" not in match_ast(
        args.ast_graph, parameters_id, "(", ")"
    ):
        parameters_id = None

    children_nid = {"parameters_id": parameters_id}

    return build_method_declaration_node(args, None, block_id, children_nid)
