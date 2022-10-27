# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    SyntaxStep,
)
from more_itertools import (
    flatten,
)
from sast_syntax_readers.types import (
    SyntaxReaderArgs,
)
from typing import (
    Iterator,
)
from utils import (
    graph as g,
)


def reader(args: SyntaxReaderArgs) -> Iterator[SyntaxStep]:
    match = g.match_ast_group(
        args.graph,
        args.n_id,
        "__0__",
        "variable_declarator",
        ";",
    )
    declarators = list(
        flatten(
            args.generic(args.fork_n_id(declarator))
            for declarator in match["variable_declarator"]
        )
    )
    assignment_value = declarators[-1].meta.dependencies
    for declarator in declarators:
        declarator.meta.dependencies = assignment_value

    yield from declarators
