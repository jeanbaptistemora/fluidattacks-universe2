from symbolic_eval.types import (
    SymbolicSearchArgs,
)
from typing import (
    Optional,
)


def search(args: SymbolicSearchArgs) -> Optional[str]:
    expression_id = args.graph.nodes[args.target_id]["expression_id"]
    return args.generic(args.fork_target_id(expression_id))
