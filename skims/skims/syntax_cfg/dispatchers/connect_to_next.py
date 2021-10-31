from syntax_cfg.types import (
    Stack,
    SyntaxCfgArgs,
)


def build(args: SyntaxCfgArgs, stack: Stack) -> None:
    next_id = stack.pop() if stack else None
    if next_id:
        args.graph.add_edge(args.n_id, next_id, label_cfg="CFG")
