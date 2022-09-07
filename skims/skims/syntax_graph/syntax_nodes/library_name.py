# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def build_library_name_node(args: SyntaxGraphArgs, expression: str) -> NId:
    args.syntax_graph.add_node(
        args.n_id,
        expression=expression,
        label_type="LibraryName",
    )

    return args.n_id
