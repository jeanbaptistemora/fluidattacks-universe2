# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model import (
    graph_model,
)
from sast_syntax_readers.types import (
    SyntaxReaderArgs,
)
from utils import (
    graph as g,
)


def reader(args: SyntaxReaderArgs) -> graph_model.SyntaxStepsLazy:
    match = g.match_ast_group(
        args.graph,
        args.n_id,
        "variable_declaration",
    )
    for declaration in match["variable_declaration"] or set():
        yield from args.generic(args.fork_n_id(declaration))
