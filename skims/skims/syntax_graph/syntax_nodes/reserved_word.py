# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def build_reserved_word_node(args: SyntaxGraphArgs, value: str) -> NId:
    args.syntax_graph.add_node(
        args.n_id,
        value=value,
        label_type="ReservedWord",
    )

    return args.n_id
