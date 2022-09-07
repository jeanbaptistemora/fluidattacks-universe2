# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def build_symbol_type_node(args: SyntaxGraphArgs, symbol_type: str) -> NId:
    args.syntax_graph.add_node(
        args.n_id,
        symbol_type=symbol_type,
        label_type="SymbolType",
    )

    return args.n_id
