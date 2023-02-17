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

SOLVERS: dict[str, Solver] = {
    "SymbolLookup": symbol_lookup.solve,
}


def generic(args: SolverArgs) -> NId | None:
    if args.n_id not in args.graph.nodes:
        return None
    node_type = args.graph.nodes[args.n_id]["label_type"]
    if solver := SOLVERS.get(node_type):
        return solver(args)
    return None


def solve_invocation(graph: Graph, path: Path, n_id: NId) -> NId | None:
    return generic(SolverArgs(generic, graph, path, n_id))
