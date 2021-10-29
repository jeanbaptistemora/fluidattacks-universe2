from sast_transformations.control_flow.common import (
    link_to_last_node as common_link_to_last_node,
    step_by_step as common_step_by_step,
)
from sast_transformations.control_flow.kotlin import (
    class_statements as kotlin_class_statements,
    if_statement as kotlin_if_statement,
    loop_statement as kotlin_loop_statement,
    try_catch_statement as kotlin_try_catch_statement,
    when_statement as kotlin_when_statement,
)
from sast_transformations.control_flow.types import (
    Walker,
    Walkers,
)

KOTLIN_WALKERS: Walkers = (
    Walker(
        applicable_node_label_types={
            "class_body",
        },
        walk_fun=kotlin_class_statements,
    ),
    Walker(
        applicable_node_label_types={
            "for_statement",
            "while_statement",
        },
        walk_fun=kotlin_loop_statement,
    ),
    Walker(
        applicable_node_label_types={
            "function_body",
            "statements",
        },
        walk_fun=common_step_by_step,
    ),
    Walker(
        applicable_node_label_types={
            "class_declaration",
            "function_declaration",
            "companion_object",
        },
        walk_fun=common_link_to_last_node,
    ),
    Walker(
        applicable_node_label_types={
            "if_expression",
        },
        walk_fun=kotlin_if_statement,
    ),
    Walker(
        applicable_node_label_types={
            "try_catch_expression",
        },
        walk_fun=kotlin_try_catch_statement,
    ),
    Walker(
        applicable_node_label_types={
            "when_expression",
        },
        walk_fun=kotlin_when_statement,
    ),
)
