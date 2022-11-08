# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def build_for_each_statement_node(
    args: SyntaxGraphArgs, var_node: NId, iterable_item: NId, block: NId
) -> NId:

    args.syntax_graph.add_node(
        args.n_id,
        block_id=block,
        iterable_item_id=iterable_item,
        variable_id=var_node,
        label_type="ForEachStatement",
    )

    args.syntax_graph.add_edge(
        args.n_id,
        args.generic(args.fork_n_id(var_node)),
        label_ast="AST",
    )

    args.syntax_graph.add_edge(
        args.n_id,
        args.generic(args.fork_n_id(iterable_item)),
        label_ast="AST",
    )

    args.syntax_graph.add_edge(
        args.n_id,
        args.generic(args.fork_n_id(block)),
        label_ast="AST",
    )

    return args.n_id
