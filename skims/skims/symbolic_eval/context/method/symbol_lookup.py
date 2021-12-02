from symbolic_eval.context.method.types import (
    SolverArgs,
)
from symbolic_eval.context.search import (
    definition_search,
)
from symbolic_eval.utils import (
    get_lookup_path,
)
from typing import (
    Optional,
)


def solve(args: SolverArgs) -> Optional[str]:
    symbol = args.graph.nodes[args.n_id]["symbol"]
    search_path = get_lookup_path(args.graph, args.path, args.n_id)
    return definition_search(args.graph, search_path, symbol)
