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
    block_id = args.graph.nodes[args.n_id]["block_id"]
    args.graph.add_edge(
        args.n_id,
        args.generic(args.fork(block_id, args.nxt_id)),
        label_cfg="CFG",
    )
    return args.n_id
