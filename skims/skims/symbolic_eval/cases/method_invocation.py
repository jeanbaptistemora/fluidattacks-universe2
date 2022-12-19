from model.core_model import (
    FindingEnum,
)
from model.graph_model import (
    Graph,
    NId,
)
from symbolic_eval.context.data_structure import (
    search_data_element,
)
from symbolic_eval.context.method import (
    solve_invocation,
)
from symbolic_eval.f004.method_invocation import (
    evaluate as evaluate_method_f004,
)
from symbolic_eval.f008.method_invocation import (
    evaluate as evaluate_method_f008,
)
from symbolic_eval.f015.method_invocation import (
    evaluate as evaluate_method_f015,
)
from symbolic_eval.f021.method_invocation import (
    evaluate as evaluate_method_f021,
)
from symbolic_eval.f034.method_invocation import (
    evaluate as evaluate_method_f034,
)
from symbolic_eval.f059.method_invocation import (
    evaluate as evaluate_method_f059,
)
from symbolic_eval.f091.method_invocation import (
    evaluate as evaluate_method_f091,
)
from symbolic_eval.f107.method_invocation import (
    evaluate as evaluate_method_f107,
)
from symbolic_eval.f192.method_invocation import (
    evaluate as evaluate_method_f192,
)
from symbolic_eval.f211.method_invocation import (
    evaluate as evaluate_method_f211,
)
from symbolic_eval.f338.method_invocation import (
    evaluate as evaluate_method_f338,
)
from symbolic_eval.f368.method_invocation import (
    evaluate as evaluate_method_f368,
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
    Set,
)
from utils import (
    graph as g,
    logs,
)

FINDING_EVALUATORS: Dict[FindingEnum, Evaluator] = {
    FindingEnum.F004: evaluate_method_f004,
    FindingEnum.F008: evaluate_method_f008,
    FindingEnum.F015: evaluate_method_f015,
    FindingEnum.F034: evaluate_method_f034,
    FindingEnum.F021: evaluate_method_f021,
    FindingEnum.F059: evaluate_method_f059,
    FindingEnum.F091: evaluate_method_f091,
    FindingEnum.F107: evaluate_method_f107,
    FindingEnum.F192: evaluate_method_f192,
    FindingEnum.F211: evaluate_method_f211,
    FindingEnum.F338: evaluate_method_f338,
    FindingEnum.F368: evaluate_method_f368,
}

MODIFYING_METHODS: Set[str] = {"add", "push", "put", "get"}


def get_invocation_eval(
    graph: Graph, evaluation: Dict[NId, bool], md_id: NId, mi_id: NId
) -> Dict[NId, bool]:
    invocation_eval: Dict[NId, bool] = {}

    al_id = graph.nodes[mi_id].get("arguments_id")
    pl_id = graph.nodes[md_id].get("parameters_id")

    if not al_id:
        raise BadMethodInvocation(f"No arguments in {mi_id} to use in {md_id}")

    if not pl_id:
        raise BadMethodInvocation(f"No parameters in {md_id} for call {mi_id}")

    p_ids = g.adj_ast(graph, pl_id)
    a_ids = g.adj_ast(graph, al_id)

    if len(p_ids) != len(a_ids):
        raise BadMethodInvocation(
            f"Can not assign parameters in {md_id} with arguments in {mi_id}"
        )

    for p_id, a_id in zip(p_ids, a_ids):
        invocation_eval[p_id] = evaluation[a_id]

    return invocation_eval


def evaluate_method_expression(
    args: SymbolicEvalArgs,
    expr_id: NId,
) -> bool:
    if args.graph.nodes[expr_id].get("symbol") in MODIFYING_METHODS:
        return False

    if md_id := solve_invocation(args.graph, args.path, expr_id):
        try:
            invoc_eval = get_invocation_eval(
                args.graph, args.evaluation, md_id, mi_id=args.n_id
            )
        except BadMethodInvocation as error:
            logs.log_blocking("warning", cast(str, error))
            invoc_eval = {}

        eb_id = args.graph.nodes[md_id].get("block_id")

        if eb_id:
            d_expression = any(
                args.generic(
                    args.fork(
                        n_id=eb_id, path=fwd + bck, evaluation=invoc_eval
                    )
                ).danger
                for fwd in get_inv_forward_paths(args.graph, eb_id)
                for _, *bck in iter_backward_paths(args.graph, eb_id)
            )
        else:
            d_expression = args.generic(args.fork_n_id(md_id)).danger
    else:
        d_expression = args.generic(args.fork_n_id(expr_id)).danger

    return d_expression


def evaluate(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    n_attrs = args.graph.nodes[args.n_id]

    if n_attrs.get("expression") == "get" and (
        el_id := search_data_element(args.graph, args.path, args.n_id)
    ):
        args.evaluation[args.n_id] = args.generic(args.fork_n_id(el_id)).danger
    else:
        if al_id := n_attrs.get("arguments_id"):
            d_arguments = args.generic(args.fork_n_id(al_id)).danger
        else:
            d_arguments = False

        d_expression = evaluate_method_expression(
            args, n_attrs["expression_id"]
        )

        if obj_id := n_attrs.get("object_id"):
            d_object = args.generic(args.fork_n_id(obj_id)).danger
        else:
            d_object = False

        args.evaluation[args.n_id] = d_expression or d_arguments or d_object

    if finding_evaluator := FINDING_EVALUATORS.get(args.method.value.finding):
        args.evaluation[args.n_id] = finding_evaluator(args).danger

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
