from syntax_cfg.types import (
    Stack,
    SyntaxCfgArgs,
)
from syntax_cfg.utils import (
    iter_with_next,
)
from utils import (
    graph as g,
)


def build(args: SyntaxCfgArgs, stack: Stack) -> None:
    c_ids = list(g.adj_ast(args.graph, args.n_id))
    following_node = stack.pop() if stack else None

    first_child, *_ = c_ids
    args.graph.add_edge(args.n_id, first_child, label_cfg="CFG")

    for c_id, nxt_id in iter_with_next(c_ids, following_node):
        if nxt_id:
            stack.append(nxt_id)

        args.generic(args.fork_n_id(c_id), stack)
