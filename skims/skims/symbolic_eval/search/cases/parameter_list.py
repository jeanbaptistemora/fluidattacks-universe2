from symbolic_eval.types import (
    SymbolicSearchArgs,
)
from typing import (
    Optional,
)
from utils import (
    graph as g,
)


def search(args: SymbolicSearchArgs) -> Optional[str]:
    for param_id in g.adj_ast(args.graph, args.target_id):
        if parameter_id := args.generic(args.fork_target_id(param_id)):
            return parameter_id
    return None
