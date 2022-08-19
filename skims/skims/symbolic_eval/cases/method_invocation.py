from model.core_model import (
    FindingEnum,
)
from model.graph_model import (
    Graph,
    NId,
)
from symbolic_eval.context.method import (
    solve_invocation,
)
from symbolic_eval.f211.method_invocation import (
    evaluate as evaluate_parameter_f211,
)
from symbolic_eval.f338.method_invocation import (
    evaluate as evaluate_parameter_f338,
)
from symbolic_eval.types import (
    BadMethodInvocation,
    Evaluator,
    SymbolicEvalArgs,
    SymbolicEvaluation,
)
from symbolic_eval.utils import (
    get_inv_forward_paths,
    iter_backward_paths,
)
from typing import (
    cast,
    Dict,
)
from utils import (
    graph as g,
    logs,
)

FINDING_EVALUATORS: Dict[FindingEnum, Evaluator] = {
    FindingEnum.F211: evaluate_parameter_f211,
    FindingEnum.F338: evaluate_parameter_f338,
}


def _get_invocation_eval(
    graph: Graph, evaluation: Dict[NId, bool], md_id: NId, mi_id: NId
) -> Dict[NId, bool]:
    invocation_eval: Dict[NId, bool] = {}

    al_id = graph.nodes[mi_id].get("arguments_id")
    pl_id = graph.nodes[md_id].get("parameters_id")

    if not al_id:
        raise BadMethodInvocation(f"No aguments in {mi_id} to use in {md_id}")

    if not pl_id:
        raise BadMethodInvocation(f"No parameters in {md_id} for call {mi_id}")

    p_ids = g.adj_ast(graph, pl_id)
    a_ids = g.adj_ast(graph, al_id)

    if len(p_ids) != len(a_ids):
        raise BadMethodInvocation(
            f"Can not assign parameters in {pl_id} with arguments in {al_id}"
        )

    for p_id, a_id in zip(p_ids, a_ids):
        invocation_eval[p_id] = evaluation[a_id]

    return invocation_eval


def evaluate(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    if al_id := args.graph.nodes[args.n_id].get("arguments_id"):
        d_arguments = args.generic(args.fork_n_id(al_id)).danger
    else:
        d_arguments = False

    expr_id = args.graph.nodes[args.n_id]["expression_id"]
    if md_id := solve_invocation(args.graph, args.path, expr_id):
        try:
            invoc_eval = _get_invocation_eval(
                args.graph, args.evaluation, md_id, mi_id=args.n_id
            )
        except BadMethodInvocation as error:
            logs.log_blocking("warning", cast(str, error))
            invoc_eval = {}

        eb_id = args.graph.nodes[md_id]["block_id"]

        d_expression = any(
            args.generic(
                args.fork(n_id=eb_id, path=fwd + bck, evaluation=invoc_eval)
            ).danger
            for fwd in get_inv_forward_paths(args.graph, eb_id)
            for _, *bck in iter_backward_paths(args.graph, eb_id)
        )
    else:
        d_expression = args.generic(args.fork_n_id(expr_id)).danger

    args.evaluation[args.n_id] = d_expression or d_arguments

    if finding_evaluator := FINDING_EVALUATORS.get(args.method.value.finding):
        args.evaluation[args.n_id] = finding_evaluator(args).danger

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
