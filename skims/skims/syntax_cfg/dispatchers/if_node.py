from syntax_cfg.types import (
    SyntaxCfgArgs,
)


def build(args: SyntaxCfgArgs) -> None:
    true_id = args.graph.nodes[args.n_id]["true_id"]
    args.graph.add_edge(args.n_id, true_id, label_cfg="CFG")
    args.generic(args.fork(true_id, args.nxt_id))

    if false_id := args.graph.nodes[args.n_id].get("false_id"):
        args.graph.add_edge(args.n_id, false_id, label_cfg="CFG")
        args.generic(args.fork(false_id, args.nxt_id))
    else:
        args.graph.add_edge(args.n_id, args.nxt_id, label_cfg="CFG")
