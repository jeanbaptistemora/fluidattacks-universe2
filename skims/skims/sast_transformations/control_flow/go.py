from more_itertools import (
    pairwise,
)
from sast_transformations.control_flow.common import (
    propagate_next_id_from_parent,
    set_next_id,
)
from sast_transformations.control_flow.types import (
    CfgArgs,
    Stack,
)
from utils import (
    graph as g,
)


def switch_statement(args: CfgArgs, stack: Stack) -> None:
    switch_flow = tuple(
        (c_id, args.graph.nodes[c_id])
        for c_id in g.adj_ast(args.graph, args.n_id)
    )

    switch_cases_ids = []
    for (c_id, c_attrs) in switch_flow:
        if c_attrs["label_type"] in [
            "default_case",
            "expression_case",
            "type_case",
        ]:
            switch_cases_ids.append(c_id)

    for case_id in switch_cases_ids:
        args.graph.add_edge(args.n_id, case_id, **g.MAYBE)
        case_steps = tuple(
            node
            for node in g.adj_ast(args.graph, case_id)
            if args.graph.nodes[node].get("label_type") not in [":", "\n"]
        )
        # Remove the `case condition` and `default` nodes
        case_steps = (
            case_steps[2:]
            if args.graph.nodes[case_steps[0]]["label_type"] == "case"
            else case_steps[1:]
        )
        if case_steps:
            for step_a_id, step_b_id in pairwise((case_id, *case_steps)):
                set_next_id(stack, step_b_id)
                args.generic(args.fork_n_id(step_a_id), stack)

            propagate_next_id_from_parent(stack)
            args.generic(args.fork_n_id(case_steps[-1]), stack)
