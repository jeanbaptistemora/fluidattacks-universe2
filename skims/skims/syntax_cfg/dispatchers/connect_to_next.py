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
    if args.nxt_id:
        args.graph.add_edge(args.n_id, args.nxt_id, label_cfg="CFG")
    elif (
        args.graph.nodes[args.n_id].get("label_type") == "VariableDeclaration"
    ) and (
        child_n_id := g.match_ast_d(args.graph, args.n_id, "MethodDeclaration")
    ):
        args.graph.add_edge(
            args.n_id,
            args.generic(args.fork(child_n_id, args.nxt_id)),
            label_cfg="CFG",
        )
    return args.n_id
