from model.graph_model import (
    Graph,
)
from more_itertools import (
    pairwise,
)
from sast_transformations.control_flow.common import (
    propagate_next_id_from_parent,
    set_next_id,
)
from sast_transformations.control_flow.types import (
    GenericType,
    Stack,
)
from utils import (
    graph as g,
)


def switch_statement(
    graph: Graph,
    n_id: str,
    stack: Stack,
    go_generic: GenericType,
) -> None:
    switch_flow = tuple(
        (c_id, graph.nodes[c_id]) for c_id in g.adj_ast(graph, n_id)
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
        graph.add_edge(n_id, case_id, **g.MAYBE)
        case_steps = tuple(
            node
            for node in g.adj_ast(graph, case_id)
            if graph.nodes[node].get("label_type") not in [":", "\n"]
        )
        # Remove the `case condition` and `default` nodes
        case_steps = (
            case_steps[2:]
            if graph.nodes[case_steps[0]]["label_type"] == "case"
            else case_steps[1:]
        )
        if case_steps:
            for step_a_id, step_b_id in pairwise((case_id, *case_steps)):
                set_next_id(stack, step_b_id)
                go_generic(graph, step_a_id, stack, edge_attrs=g.ALWAYS)

            propagate_next_id_from_parent(stack)
            go_generic(graph, case_steps[-1], stack, edge_attrs=g.ALWAYS)
