# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.argument import (
    build_argument_node,
)
from syntax_graph.syntax_nodes.named_argument import (
    build_named_argument_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    adj_ast,
    match_ast_d,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    c_ids = adj_ast(args.ast_graph, args.n_id)
    if len(c_ids) > 1 and (label_id := match_ast_d(graph, args.n_id, "label")):
        var_id = adj_ast(graph, label_id)[0]
        return build_named_argument_node(args, var_id, c_ids[1])

    return build_argument_node(args, iter(c_ids))
