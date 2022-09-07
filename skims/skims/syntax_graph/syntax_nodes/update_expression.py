# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def build_update_expression_node(
    args: SyntaxGraphArgs, expression_type: str, identifier_id: str
) -> NId:
    args.syntax_graph.add_node(
        args.n_id,
        expression_type=expression_type,
        identifier_id=identifier_id,
        label_type="UpdateExpression",
    )

    args.syntax_graph.add_edge(
        args.n_id,
        args.generic(args.fork_n_id(identifier_id)),
        label_ast="AST",
    )

    return args.n_id
