from syntax_cfg.types import (
    Stack,
    SyntaxCfgArgs,
)


def build(args: SyntaxCfgArgs, stack: Stack) -> None:
    following_node = stack.pop() if stack else None

    true_id = args.graph.nodes[args.n_id]["true_id"]
    args.graph.add_edge(args.n_id, true_id, label_cfg="CFG")

    if following_node:
        stack.append(following_node)

    args.generic(args.fork_n_id(true_id), stack)

    if false_id := args.graph.nodes[args.n_id].get("false_id"):
        args.graph.add_edge(args.n_id, false_id, label_cfg="CFG")

        if following_node:
            stack.append(following_node)

        args.generic(args.fork_n_id(false_id), stack)
    else:
        args.graph.add_edge(args.n_id, following_node, label_cfg="CFG")
