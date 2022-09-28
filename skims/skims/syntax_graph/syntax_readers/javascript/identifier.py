# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.symbol_lookup import (
    build_symbol_lookup_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def reader(args: SyntaxGraphArgs) -> NId:
    symbol = args.ast_graph.nodes[args.n_id]["label_text"]
    return build_symbol_lookup_node(args, symbol)
