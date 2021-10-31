from contextlib import (
    suppress,
)
from sast_transformations.control_flow.types import (
    CfgArgs,
    Stack,
)
from utils import (
    graph as g,
)


def next_declaration(args: CfgArgs, stack: Stack) -> None:
    with suppress(IndexError):
        # check if a following stmt is pending in parent entry of the stack
        next_id = stack[-2].pop("next_id", None)

        # if there was a following stament, it does not have the current one
        # as child and they are not the same
        if (
            next_id
            and args.n_id != next_id
            and args.n_id not in g.adj_cfg(args.graph, next_id)
        ):
            # check that the next node is not already part of this cfg branch
            for statement in g.pred_cfg_lazy(args.graph, args.n_id, depth=-1):
                if statement == next_id:
                    break
            else:
                # add following statement to cfg
                args.graph.add_edge(args.n_id, next_id, **g.ALWAYS)
