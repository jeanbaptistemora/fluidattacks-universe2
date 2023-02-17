from model.core_model import (
    FindingEnum,
)
from symbolic_eval.context.search import (
    search_until_def,
)
from symbolic_eval.f085.symbol_lookup import (
    evaluate as evaluate_symbol_f085,
)
from symbolic_eval.f343.symbol_lookup import (
    evaluate as evaluate_symbol_f343,
)
from symbolic_eval.types import (
    Evaluator,
    SymbolicEvalArgs,
    SymbolicEvaluation,
)
from symbolic_eval.utils import (
    get_lookup_path,
)
from utils import (
    graph as g,
)

FINDING_EVALUATORS: dict[FindingEnum, Evaluator] = {
    FindingEnum.F085: evaluate_symbol_f085,
    FindingEnum.F343: evaluate_symbol_f343,
}

OUTSIDEPATH_TYPES = {
    "Parameter",
    "FieldDeclaration",
    "VariableDeclaration",
    "MethodInvocation",
    "MethodDeclaration",
}


def evaluate(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    symbol_id = args.n_id
    symbol = args.graph.nodes[args.n_id]["symbol"]

    try:
        path = get_lookup_path(args.graph, args.path, symbol_id)
    except ValueError:
        path = args.path

    refs_search_order = list(search_until_def(args.graph, path, symbol))
    refs_exec_order = reversed(refs_search_order)

    args.evaluation[symbol_id] = False
    refs_dangers = []
    for ref_id in refs_exec_order:
        if args.graph.nodes[ref_id]["label_type"] in OUTSIDEPATH_TYPES:
            args.generic(args.fork_n_id(ref_id))
        elif ref_id in args.path:
            cfg_id = g.lookup_first_cfg_parent(args.graph, ref_id)
            args.generic(args.fork_n_id(cfg_id))

        if ref_id in args.evaluation:
            refs_dangers.append(args.evaluation[ref_id])

    args.evaluation[symbol_id] = any(refs_dangers)

    if finding_evaluator := FINDING_EVALUATORS.get(args.method.value.finding):
        args.evaluation[args.n_id] = finding_evaluator(args).danger

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
