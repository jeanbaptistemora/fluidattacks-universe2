# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model import (
    graph_model,
)
from sast_syntax_readers.types import (
    MissingCaseHandling,
    SyntaxReaderArgs,
)
from utils import (
    graph as g,
)


def reader(args: SyntaxReaderArgs) -> graph_model.SyntaxStepsLazy:
    # switch parenthesized_expression switch_block
    match = g.match_ast(args.graph, args.n_id, "__2__", "switch_body")
    switch_block = match["switch_body"]
    switch_pred_id = match["__2__"]
    if not switch_block or not switch_pred_id:
        raise MissingCaseHandling(args)

    switch_cases = tuple(
        _case
        for c_id in g.adj_ast(
            args.graph, switch_block, label_type="switch_section"
        )
        for _case in g.adj_ast(
            args.graph, c_id, label_type="case_switch_label"
        )
    )

    yield graph_model.SyntaxStepSwitch(
        meta=graph_model.SyntaxStepMeta.default(
            args.n_id,
            [
                args.generic(args.fork_n_id(switch_label_id))
                for switch_label_id in reversed(switch_cases)
            ]
            + [
                args.generic(args.fork_n_id(switch_pred_id)),
            ],
        ),
    )
