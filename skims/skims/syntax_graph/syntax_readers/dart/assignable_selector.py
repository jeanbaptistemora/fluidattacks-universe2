# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.assignable_selector import (
    build_assignable_selector_node,
)
from syntax_graph.types import (
    MissingCaseHandling,
    SyntaxGraphArgs,
)
from utils.graph import (
    adj_ast,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    _, *c_ids, _ = adj_ast(graph, args.n_id)
    if c_ids := [
        child
        for child in c_ids
        if args.ast_graph.nodes[child]["label_type"] != "."
    ]:
        return build_assignable_selector_node(args, iter(c_ids))

    raise MissingCaseHandling(
        f"Bad assignable selector handling in {args.n_id}"
    )
