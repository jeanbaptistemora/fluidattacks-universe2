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
    l_id, _, r_id = g.adj_ast(args.graph, args.n_id)

    yield graph_model.SyntaxStepAttributeAccess(
        attribute=args.graph.nodes[r_id]["label_text"],
        meta=graph_model.SyntaxStepMeta.default(
            args.n_id,
            [
                args.generic(args.fork_n_id(l_id)),
            ],
        ),
    )
