from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)
from utils import (
    graph as g,
)


def java_host_key_checking(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    args.evaluation[args.n_id] = False
    n_attr = args.graph.nodes[args.n_id]
    if (
        n_attr["expression"] in {"add", "put", "push"}
        and (al_list := n_attr.get("arguments_id"))
        and (args_nodes := g.adj_ast(args.graph, al_list))
        and len(args_nodes) == 2
    ):
        eval_1 = args.generic(
            args.fork(
                n_id=args_nodes[0],
                evaluation={},
                triggers=set(),
            )
        )
        eval_2 = args.generic(
            args.fork(
                n_id=args_nodes[1],
                evaluation={},
                triggers=set(),
            )
        )
        if (
            eval_1
            and eval_2
            and eval_1.triggers == {"hostkey"}
            and eval_2.triggers == {"no"}
        ):
            args.evaluation[args.n_id] = True

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
