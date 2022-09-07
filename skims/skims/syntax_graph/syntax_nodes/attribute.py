# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def build_attribute_node(
    args: SyntaxGraphArgs,
    attr_name: str,
) -> NId:
    args.syntax_graph.add_node(
        args.n_id,
        name=attr_name,
        label_type="Attribute",
    )

    return args.n_id
