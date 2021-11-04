from symbolic_eval.types import (
    SymbolicSearchArgs,
)
from typing import (
    Optional,
)


def search(args: SymbolicSearchArgs) -> Optional[str]:
    condition_id = args.graph.nodes[args.target_id]["condition_id"]
    return args.generic(args.fork_target_id(condition_id))
