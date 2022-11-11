# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.method_invocation import (
    build_method_invocation_node,
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
    graph = args.ast_graph
    qualified_id = match_ast_d(graph, args.n_id, "qualified")
    params_id = match_ast_d(graph, args.n_id, "formal_parameter_list")
    if qualified_id and (
        identifier_id := match_ast_d(graph, qualified_id, "identifier")
    ):
        name = node_to_str(graph, identifier_id)
        return build_method_invocation_node(
            args, name, identifier_id, params_id, None
        )

    raise MissingCaseHandling(
        f"Bad constant constructor handling in {args.n_id}"
    )
