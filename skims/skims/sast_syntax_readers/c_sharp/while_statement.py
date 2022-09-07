# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    SyntaxStepLoop,
    SyntaxStepMeta,
    SyntaxStepsLazy,
)
from sast_syntax_readers.types import (
    MissingCaseHandling,
    SyntaxReaderArgs,
)
from sast_syntax_readers.utils_generic import (
    dependencies_from_arguments,
)
from utils import (
    graph as g,
)


def reader(
    args: SyntaxReaderArgs,
) -> SyntaxStepsLazy:
    match = g.match_ast(
        args.graph,
        args.n_id,
        "while",
        "(",
        "__0__",
        ")",
        "block",
    )
    if expression := match["__0__"]:
        yield SyntaxStepLoop(
            meta=SyntaxStepMeta.default(
                args.n_id,
                dependencies_from_arguments(
                    args.fork_n_id(expression),
                ),
            ),
        )
    else:
        raise MissingCaseHandling(args)
