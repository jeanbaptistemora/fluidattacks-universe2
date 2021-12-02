from model.core_model import (
    FindingEnum,
)
from symbolic_eval.context.method import (
    solve_invocation,
)
from symbolic_eval.types import (
    Evaluator,
    SymbolicEvalArgs,
)
from symbolic_eval.utils import (
    get_inv_forward_paths,
    iter_backward_paths,
)
from typing import (
    Dict,
)
from utils import (
    graph as g,
)

FINDING_EVALUATORS: Dict[FindingEnum, Evaluator] = {}


def evaluate(args: SymbolicEvalArgs) -> bool:
    expr_id = args.graph.nodes[args.n_id]["expression_id"]
    al_id = args.graph.nodes[args.n_id]["arguments_id"]

    d_arguments = args.generic(args.fork_n_id(al_id))

    if md_id := solve_invocation(args.graph, args.path, expr_id):
        invoc_eval = {}
        graph = args.graph

        pl_id = graph.nodes[md_id]["parameters_id"]
        for p_id, a_id in zip(
            g.adj_ast(graph, pl_id), g.adj_ast(graph, al_id)
        ):
            invoc_eval[p_id] = args.evaluation[a_id]

        eb_id = args.graph.nodes[md_id]["block_id"]

        d_expression = any(
            args.generic(
                args.fork(n_id=eb_id, path=fwd + bck, evaluation=invoc_eval)
            )
            for fwd in get_inv_forward_paths(args.graph, eb_id)
            for _, *bck in iter_backward_paths(args.graph, eb_id)
        )
    else:
        d_expression = args.generic(args.fork_n_id(expr_id))

    args.evaluation[args.n_id] = d_expression or d_arguments

    if finding_evaluator := FINDING_EVALUATORS.get(args.finding):
        args.evaluation[args.n_id] = finding_evaluator(args)

    return args.evaluation[args.n_id]
