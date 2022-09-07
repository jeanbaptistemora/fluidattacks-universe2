# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model import (
    graph_model,
)
from sast_syntax_readers.types import (
    SyntaxReaderArgs,
)
from typing import (
    Iterator,
    Union,
)


def reader(args: SyntaxReaderArgs) -> graph_model.SyntaxStepsLazy:
    assignments = tuple(_expression(args, args.n_id))
    last_assignment = assignments[-1]
    for var_identifier_id in assignments[:-1]:
        yield graph_model.SyntaxStepAssignment(
            meta=last_assignment.meta,  # type: ignore
            var=args.graph.nodes[var_identifier_id]["label_text"],
        )
    yield last_assignment


def _expression(
    args: SyntaxReaderArgs, expression_id: str
) -> Iterator[Union[str, graph_model.SyntaxStepAssignment]]:
    node_attrs = args.graph.nodes[expression_id]
    left = node_attrs["label_field_left"]
    right = node_attrs["label_field_right"]
    if args.graph.nodes[right]["label_type"] == "assignment_expression":
        yield left
        yield from _expression(args, right)
    else:
        yield graph_model.SyntaxStepAssignment(
            meta=graph_model.SyntaxStepMeta.default(
                args.n_id,
                [
                    args.generic(args.fork_n_id(right)),
                ],
            ),
            var=args.graph.nodes[left].get("label_text"),
        )
