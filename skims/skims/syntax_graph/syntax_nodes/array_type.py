# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def build_array_type_node(
    args: SyntaxGraphArgs,
    type_name: str,
) -> NId:
    args.syntax_graph.add_node(
        args.n_id,
        array_type=type_name,
        label_type="ArrayType",
    )

    return args.n_id
