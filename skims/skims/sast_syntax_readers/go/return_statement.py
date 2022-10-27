# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    SyntaxStep,
    SyntaxStepMeta,
    SyntaxStepReturn,
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
    c_id = g.get_ast_childs(args.graph, args.n_id, "expression_list")

    if c_id:
        yield SyntaxStepReturn(
            meta=SyntaxStepMeta.default(
                args.n_id,
                [
                    args.generic(args.fork_n_id(r_id))
                    for r_id in g.adj_ast(args.graph, c_id[0])
                    if args.graph.nodes[r_id]["label_type"] != ","
                ],
            )
        )
