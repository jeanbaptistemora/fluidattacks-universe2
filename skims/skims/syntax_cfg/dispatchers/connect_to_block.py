from syntax_cfg.types import (
    SyntaxCfgArgs,
)


def build(args: SyntaxCfgArgs) -> None:
    block_id = args.graph.nodes[args.n_id]["block_id"]
    args.graph.add_edge(args.n_id, block_id, label_cfg="CFG")
    args.generic(args.fork(block_id, args.nxt_id))
