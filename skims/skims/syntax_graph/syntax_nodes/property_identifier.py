# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from typing import (
    Optional,
)


def build_property_identifier_node(
    args: SyntaxGraphArgs,
    var_name: Optional[str],
) -> NId:
    args.syntax_graph.add_node(
        args.n_id,
        variable_name=var_name,
        label_type="PropertyIdentifier",
    )

    return args.n_id
