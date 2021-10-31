from sast_transformations.control_flow.types import (
    CfgArgs,
    Stack,
)
from sast_transformations.control_flow.utils import (
    next_declaration,
)
from sast_transformations.control_flow.walkers import (
    WALKERS_BY_LANG,
)


def generic(args: CfgArgs, stack: Stack) -> None:
    node_type = args.graph.nodes[args.n_id]["label_type"]

    stack.append(dict(type=node_type))

    for walker in WALKERS_BY_LANG[args.language]:
        if node_type in walker.applicable_node_label_types:
            walker.walk_fun(args, stack)
            break
    else:
        # if there is no walker for the expression, stop the recursion
        # the only thing left is to check if there is a cfg statement following
        next_declaration(args, stack)

    stack.pop()
