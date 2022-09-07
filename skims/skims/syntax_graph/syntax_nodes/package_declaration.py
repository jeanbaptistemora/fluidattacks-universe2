# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def build_package_declaration_node(
    args: SyntaxGraphArgs, expression: str
) -> NId:
    args.syntax_graph.add_node(
        args.n_id,
        expression=expression,
        label_type="PackageDeclaration",
    )

    return args.n_id
