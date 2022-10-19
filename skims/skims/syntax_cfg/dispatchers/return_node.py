# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    NId,
)
from syntax_cfg.types import (
    SyntaxCfgArgs,
)
from utils import (
    graph as g,
)


def build(args: SyntaxCfgArgs) -> NId:
    childs = g.match_ast(args.graph, args.n_id, "LambdaExpression")
    if val_id := childs.get("LambdaExpression"):
        args.graph.add_edge(
            args.n_id,
            args.generic(args.fork(val_id, args.nxt_id)),
            label_cfg="CFG",
        )

    return args.n_id
