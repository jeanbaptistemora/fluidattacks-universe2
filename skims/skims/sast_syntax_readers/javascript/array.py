# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    SyntaxStep,
    SyntaxStepMeta,
    SyntaxStepObjectInstantiation,
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
    match = g.match_ast_group(args.graph, args.n_id, ",", "[", "]")
    elements = [
        args.generic(args.fork_n_id(str(value)))[-1]
        for value in match.values()
        if isinstance(value, str)
    ]
    yield from elements
    yield SyntaxStepObjectInstantiation(
        meta=SyntaxStepMeta(
            danger=False, dependencies=[], n_id=args.n_id, value=elements
        ),
        object_type="Array",
    )
