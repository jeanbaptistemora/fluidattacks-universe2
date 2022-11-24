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
    childs = g.match_ast(args.graph, args.n_id, "StatementBlock")
    block_id = args.graph.nodes[args.n_id].get("block_id") or childs.get(
        "StatementBlock"
    )
    if block_id:
        args.graph.add_edge(
            args.n_id,
            args.generic(args.fork(block_id, args.nxt_id)),
            label_cfg="CFG",
        )
    return args.n_id
