# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from model.graph_model import (
    NId,
)
from syntax_cfg.types import (
    SyntaxCfgArgs,
)


def build(args: SyntaxCfgArgs) -> NId:
    val_id = args.graph.nodes[args.n_id].get("value_id")
    if val_id and args.graph.nodes[val_id]["label_type"] == "LambdaExpression":
        args.graph.add_edge(
            args.n_id,
            args.generic(args.fork(val_id, args.nxt_id)),
            label_cfg="CFG",
        )

    return args.n_id
