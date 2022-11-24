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
    childs = g.match_ast(args.graph, args.n_id)
    true_id = args.graph.nodes[args.n_id].get("true_id")
    if true_id and (match_true := childs.get("__1__")):
        args.graph.add_edge(
            args.n_id,
            args.generic(args.fork(match_true, args.nxt_id)),
            label_cfg="CFG",
        )

    if args.graph.nodes[args.n_id].get("false_id") and (
        match_false := childs.get("__2__")
    ):
        args.graph.add_edge(
            args.n_id,
            args.generic(args.fork(match_false, args.nxt_id)),
            label_cfg="CFG",
        )
    elif args.nxt_id:
        args.graph.add_edge(args.n_id, args.nxt_id, label_cfg="CFG")

    return args.n_id
