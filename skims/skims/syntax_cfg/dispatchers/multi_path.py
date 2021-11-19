from syntax_cfg.types import (
    SyntaxCfgArgs,
)
from utils import (
    graph as g,
)


def build(args: SyntaxCfgArgs) -> None:
    for c_id in g.adj_ast(args.graph, args.n_id):
        args.graph.add_edge(args.n_id, c_id, label_cfg="CFG")
        args.generic(args.fork(c_id, args.nxt_id))
