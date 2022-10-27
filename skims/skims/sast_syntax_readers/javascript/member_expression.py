# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    SyntaxStep,
    SyntaxStepMemberAccessExpression,
    SyntaxStepMeta,
)
from sast_syntax_readers.types import (
    SyntaxReaderArgs,
)
from typing import (
    Iterator,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxReaderArgs) -> Iterator[SyntaxStep]:
    node_attrs = args.graph.nodes[args.n_id]
    expression_id = node_attrs["label_field_object"]
    member_id = node_attrs["label_field_property"]

    yield SyntaxStepMemberAccessExpression(
        meta=SyntaxStepMeta.default(
            args.n_id,
            [args.generic(args.fork_n_id(expression_id))],
        ),
        member=node_to_str(args.graph, member_id),
        expression=node_to_str(args.graph, expression_id),
    )
