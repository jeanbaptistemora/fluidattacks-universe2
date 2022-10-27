# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    SyntaxStep,
    SyntaxStepDeclaration,
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
    parameters = (
        node
        for node in g.adj_ast(args.graph, args.n_id)[1:-1]
        if args.graph.nodes[node]["label_type"] not in {",", "comment"}
    )
    for parameter in parameters:
        yield from _yield_parameter(args.fork_n_id(parameter))


def _yield_parameter(args: SyntaxReaderArgs) -> Iterator[SyntaxStep]:
    node_attrs = args.graph.nodes[args.n_id]
    if node_attrs["label_type"] == "identifier":
        yield SyntaxStepDeclaration(
            meta=SyntaxStepMeta.default(args.n_id),
            var=node_attrs["label_text"],
            modifiers=set(),
        )
    elif node_attrs["label_type"] == "assignment_pattern":
        yield SyntaxStepDeclaration(
            meta=SyntaxStepMeta.default(
                args.n_id,
                [
                    args.generic(
                        args.fork_n_id(node_attrs["label_field_right"])
                    ),
                ],
            ),
            var=args.graph.nodes[node_attrs["label_field_left"]]["label_text"],
            modifiers=set(),
        )
    else:
        raise MissingCaseHandling(args)
