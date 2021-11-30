from model.core_model import (
    FindingEnum,
)
from symbolic_eval.context.search import (
    search_until_def,
)
from symbolic_eval.types import (
    Evaluator,
    SymbolicEvalArgs,
)
from symbolic_eval.utils import (
    get_lookup_path,
)
from typing import (
    Dict,
)
from utils import (
    graph as g,
)

FINDING_EVALUATORS: Dict[FindingEnum, Evaluator] = {}


def evaluate(args: SymbolicEvalArgs) -> bool:
    graph = args.graph
    symbol_id = args.n_id
    symbol = args.graph.nodes[args.n_id]["symbol"]
    path = get_lookup_path(graph, args.path, symbol_id)
    refs_search_order = list(search_until_def(graph, path, symbol))
    refs_exec_order = reversed(refs_search_order)

    for ref_id in refs_exec_order:
        cfg_id = g.lookup_first_cfg_parent(graph, ref_id)
        args.generic(args.fork_n_id(cfg_id))
        graph.nodes[symbol_id]["danger"] = args.graph.nodes[ref_id]["danger"]

    if finding_evaluator := FINDING_EVALUATORS.get(args.finding):
        args.graph.nodes[args.n_id]["danger"] = finding_evaluator(args)

    return graph.nodes[symbol_id]["danger"]
