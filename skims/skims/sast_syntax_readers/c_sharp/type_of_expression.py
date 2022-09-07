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
    method_parts = ["typeof", "(", ")"]
    c_ids = [
        c_id
        for c_id in g.adj_ast(args.graph, args.n_id)
        if args.graph.nodes[c_id]["label_type"] not in method_parts
    ]

    yield graph_model.SyntaxStepMethodInvocation(
        meta=graph_model.SyntaxStepMeta.default(
            args.n_id,
            [args.generic(args.fork_n_id(c_id)) for c_id in c_ids],
        ),
        method="typeof",
        current_instance=graph_model.CurrentInstance(fields={}),
    )
