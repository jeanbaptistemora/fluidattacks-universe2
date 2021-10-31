from syntax_cfg.types import (
    Stack,
    SyntaxCfgArgs,
)


def build(args: SyntaxCfgArgs, stack: Stack) -> None:
    block_id = args.graph.nodes[args.n_id]["block_id"]
    args.graph.add_edge(args.n_id, block_id, label_cfg="CFG")
    args.generic(args.fork_n_id(block_id), stack)
