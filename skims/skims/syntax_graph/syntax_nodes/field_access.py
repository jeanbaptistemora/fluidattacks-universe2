# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def build_field_access_node(args: SyntaxGraphArgs, field_text: str) -> NId:
    args.syntax_graph.add_node(
        args.n_id,
        field_text=field_text,
        label_type="FieldAccess",
    )

    return args.n_id
