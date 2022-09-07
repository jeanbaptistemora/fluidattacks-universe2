# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.package_declaration import (
    build_package_declaration_node,
)
from syntax_graph.types import (
    MissingCaseHandling,
    SyntaxGraphArgs,
)
from utils.graph import (
    match_ast_d,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:
    c_id = match_ast_d(args.ast_graph, args.n_id, "scoped_identifier")
    if not c_id:
        raise MissingCaseHandling(
            f"Bad package expression handling in {args.n_id}"
        )
    expression = node_to_str(args.ast_graph, c_id)
    return build_package_declaration_node(args, expression)
