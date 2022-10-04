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
    List,
    Optional,
)


def build_switch_section_node(
    args: SyntaxGraphArgs,
    cases_ids: Optional[List[NId]],
    execution_ids: List[NId],
) -> NId:
    args.syntax_graph.add_node(
        args.n_id,
        label_type="SwitchSection",
    )

    if cases_ids:
        for case_id in cases_ids:
            args.syntax_graph.add_edge(
                args.n_id,
                args.generic(args.fork_n_id(case_id)),
                label_ast="AST",
            )

    for statement_id in execution_ids:
        args.syntax_graph.add_edge(
            args.n_id,
            args.generic(args.fork_n_id(statement_id)),
            label_ast="AST",
        )

    return args.n_id
