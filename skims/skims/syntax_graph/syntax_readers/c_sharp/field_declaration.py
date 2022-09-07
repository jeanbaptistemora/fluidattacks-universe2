# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils import (
    graph as g,
)


def reader(args: SyntaxGraphArgs) -> NId:
    match_var = g.match_ast(args.ast_graph, args.n_id, "variable_declaration")
    var = match_var["variable_declaration"]
    return args.generic(args.fork_n_id(str(var)))
