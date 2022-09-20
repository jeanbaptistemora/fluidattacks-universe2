# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.using_statement import (
    build_using_statement_node,
)
from syntax_graph.types import (
    MissingCaseHandling,
    SyntaxGraphArgs,
)
from utils.graph import (
    match_ast,
)


def reader(args: SyntaxGraphArgs) -> NId:
    block_id = args.ast_graph.nodes[args.n_id].get("label_field_body")
    if not block_id:
        raise MissingCaseHandling(
            f"Bad using statement handling in {args.n_id}"
        )
    children = match_ast(args.ast_graph, args.n_id, "variable_declaration")
    declaration_id = children.get("variable_declaration")
    return build_using_statement_node(args, block_id, declaration_id)
