# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    SyntaxStep,
    SyntaxStepAttributeAccess,
    SyntaxStepMeta,
)
from sast_syntax_readers.types import (
    MissingCaseHandling,
    SyntaxReaderArgs,
)
from typing import (
    Iterator,
)
from utils import (
    graph as g,
)


def reader(args: SyntaxReaderArgs) -> Iterator[SyntaxStep]:
    match = g.match_ast(args.graph, args.n_id, "navigation_suffix")
    attribute = g.get_ast_childs(
        args.graph, str(match["navigation_suffix"]), "simple_identifier"
    )
    if attribute:
        yield SyntaxStepAttributeAccess(
            attribute=args.graph.nodes[attribute[0]]["label_text"],
            meta=SyntaxStepMeta.default(
                n_id=args.n_id,
                dependencies=[
                    args.generic(args.fork_n_id(str(match["__0__"])))
                ],
            ),
        )
    else:
        raise MissingCaseHandling(args)
