from model.core_model import (
    FindingEnum,
)
from symbolic_eval.search import (
    lookup_search,
)
from symbolic_eval.types import (
    Evaluator,
    Path,
    SymbolicEvalArgs,
)
from typing import (
    Dict,
)
from utils import (
    graph as g,
)

FINDING_EVALUATORS: Dict[FindingEnum, Evaluator] = {}


def get_lookup_path(args: SymbolicEvalArgs) -> Path:
    cfg_parent = g.lookup_first_cfg_parent(args.graph, args.n_id)
    cfg_parent_idx = args.path.index(cfg_parent)  # current instruction idx
    return args.path[cfg_parent_idx + 1 :]  # from previus instruction idx


def evaluate(args: SymbolicEvalArgs) -> bool:
    graph = args.graph
    symbol = args.n_id

    if v_id := lookup_search(graph, get_lookup_path(args), symbol):
        graph.nodes[symbol]["danger"] = args.generic(args.fork_n_id(v_id))
    else:
        print("COULD NOT SOLVE SYMBOL LOOKUP", symbol)

    if finding_evaluator := FINDING_EVALUATORS.get(args.finding):
        args.graph.nodes[args.n_id]["danger"] = finding_evaluator(args)

    return graph.nodes[symbol]["danger"]
