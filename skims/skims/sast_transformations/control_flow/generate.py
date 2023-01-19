from sast_transformations.control_flow.types import (
    CfgArgs,
    Stack,
)


def generic(args: CfgArgs, stack: Stack) -> None:
    node_type = args.graph.nodes[args.n_id]["label_type"]
    stack.append(dict(type=node_type))
    stack.pop()
