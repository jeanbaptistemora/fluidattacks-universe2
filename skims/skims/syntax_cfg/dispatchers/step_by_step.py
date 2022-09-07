# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    NId,
)
from syntax_cfg.types import (
    SyntaxCfgArgs,
)
from syntax_cfg.utils import (
    iter_with_next,
)
from utils import (
    graph as g,
)


def build(args: SyntaxCfgArgs) -> NId:
    if c_ids := g.adj_ast(args.graph, args.n_id):
        first_child, *_ = c_ids
        args.graph.add_edge(args.n_id, first_child, label_cfg="CFG")

        for c_id, nxt_id in iter_with_next(list(c_ids), args.nxt_id):
            args.generic(args.fork(c_id, nxt_id))

    return args.n_id
