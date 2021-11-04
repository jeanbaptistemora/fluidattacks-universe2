from symbolic_eval.types import (
    SymbolicSearchArgs,
)
from typing import (
    Optional,
)


def search(args: SymbolicSearchArgs) -> Optional[str]:
    nodes = args.graph.nodes
    if nodes[args.target_id]["variable"] == nodes[args.symbol]["symbol"]:
        return args.target_id
    return None
