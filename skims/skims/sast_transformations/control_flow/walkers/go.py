from sast_transformations.control_flow.common import (
    if_statement as common_if_statement,
    link_to_last_node as common_link_to_last_node,
    loop_statement as common_loop_statement,
    step_by_step as common_step_by_step,
)
from sast_transformations.control_flow.go import (
    switch_statement as go_switch_statement,
)
from sast_transformations.control_flow.types import (
    Walker,
    Walkers,
)

GO_WALKERS: Walkers = (
    Walker(
        applicable_node_label_types={
            "block",
        },
        walk_fun=common_step_by_step,
    ),
    Walker(
        applicable_node_label_types={
            "function_declaration",
            "method_declaration",
        },
        walk_fun=common_link_to_last_node,
    ),
    Walker(
        applicable_node_label_types={
            "if_statement",
        },
        walk_fun=common_if_statement,
    ),
    Walker(
        applicable_node_label_types={
            "for_statement",
        },
        walk_fun=common_loop_statement,
    ),
    Walker(
        applicable_node_label_types={
            "expression_switch_statement",
            "type_switch_statement",
        },
        walk_fun=go_switch_statement,
    ),
)
