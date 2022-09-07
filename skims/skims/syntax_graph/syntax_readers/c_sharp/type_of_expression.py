# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    NId,
)
from syntax_graph.syntax_nodes.typeof import (
    build_typeof_node,
)
from syntax_graph.types import (
    MissingCaseHandling,
    SyntaxGraphArgs,
)
from utils.graph import (
    match_ast,
)


def reader(args: SyntaxGraphArgs) -> NId:
    match = match_ast(args.ast_graph, args.n_id, "typeof", "(", ")")

    if len(match) == 4 and match["typeof"] and match["("] and match[")"]:
        return build_typeof_node(args, argument_id=str(match["__0__"]))

    raise MissingCaseHandling(f"Bad typeof invocation in {args.n_id}")
