# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.switch_case import (
    build_switch_case_node,
)
from syntax_graph.syntax_nodes.switch_default import (
    build_switch_default_node,
)
from syntax_graph.types import (
    MissingCaseHandling,
    SyntaxGraphArgs,
)
from utils.graph import (
    match_ast,
)


def reader(args: SyntaxGraphArgs) -> NId:
    match_childs = match_ast(
        args.ast_graph,
        args.n_id,
        "case",
        "default",
    )
    default = match_childs.get("default")
    case = match_childs.get("case")

    if default:
        return build_switch_default_node(args, None)

    if case and (expr := match_childs["__0__"]):
        return build_switch_case_node(args, expr, "case")

    raise MissingCaseHandling(f"Bad switch label handling in {args.n_id}")
