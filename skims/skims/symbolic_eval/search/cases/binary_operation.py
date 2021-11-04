from symbolic_eval.types import (
    SymbolicSearchArgs,
)
from typing import (
    Optional,
)


def search(args: SymbolicSearchArgs) -> Optional[str]:
    op_attr = args.graph.nodes[args.target_id]
    return args.generic(
        args.fork_target_id(op_attr["left_id"])
    ) or args.generic(args.fork_target_id(op_attr["right_id"]))
