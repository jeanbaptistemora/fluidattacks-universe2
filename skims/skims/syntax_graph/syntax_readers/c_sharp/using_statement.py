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
    match_ast_d,
)


def reader(args: SyntaxGraphArgs) -> NId:
    if match := match_ast_d(args.ast_graph, args.n_id, "variable_declaration"):
        return build_using_statement_node(args, match)

    raise MissingCaseHandling(f"Bad using statement handling in {args.n_id}")
