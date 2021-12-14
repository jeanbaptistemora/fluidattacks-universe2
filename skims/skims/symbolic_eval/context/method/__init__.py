from model.graph_model import (
    Graph,
    NId,
)
from symbolic_eval.context.method import (
    symbol_lookup,
)
from symbolic_eval.context.method.types import (
    Solver,
    SolverArgs,
)
from symbolic_eval.types import (
    Path,
)
from typing import (
    Dict,
    Optional,
)

SOLVERS: Dict[str, Solver] = {
    "SymbolLookup": symbol_lookup.solve,
}


def generic(args: SolverArgs) -> Optional[NId]:
    node_type = args.graph.nodes[args.n_id]["label_type"]
    if solver := SOLVERS.get(node_type):
        return solver(args)
    return None


def solve_invocation(graph: Graph, path: Path, n_id: NId) -> Optional[NId]:
    return generic(SolverArgs(generic, graph, path, n_id))
