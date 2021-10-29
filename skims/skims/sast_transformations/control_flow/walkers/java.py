from sast_transformations.control_flow.common import (
    catch_statement as common_catch_statement,
    if_statement as common_if_statement,
    link_to_last_node as common_link_to_last_node,
    loop_statement as common_loop_statement,
    step_by_step as common_step_by_step,
    try_statement as common_try_statement,
)
from sast_transformations.control_flow.java import (
    lambda_expression as java_lambda_expression,
    method_invocation as java_method_invocation,
    switch_expression as java_switch_expression,
    try_with_resources_statement as java_try_with_resources_statement,
)
from sast_transformations.control_flow.types import (
    Walker,
    Walkers,
)

JAVA_WALKERS: Walkers = (
    Walker(
        applicable_node_label_types={
            "block",
            "constructor_body",
            "expression_statement",
            "resource_specification",
        },
        walk_fun=common_step_by_step,
    ),
    Walker(
        applicable_node_label_types={
            "catch_clause",
            "finally_clause",
        },
        walk_fun=common_catch_statement,
    ),
    Walker(
        applicable_node_label_types={
            "for_statement",
            "enhanced_for_statement",
            "while_statement",
            "do_statement",
        },
        walk_fun=common_loop_statement,
    ),
    Walker(
        applicable_node_label_types={
            "if_statement",
        },
        walk_fun=common_if_statement,
    ),
    Walker(
        applicable_node_label_types={
            "switch_expression",
        },
        walk_fun=java_switch_expression,
    ),
    Walker(
        applicable_node_label_types={
            "method_invocation",
        },
        walk_fun=java_method_invocation,
    ),
    Walker(
        applicable_node_label_types={
            "lambda_expression",
        },
        walk_fun=java_lambda_expression,
    ),
    Walker(
        applicable_node_label_types={
            "constructor_declaration",
            "method_declaration",
        },
        walk_fun=common_link_to_last_node,
    ),
    Walker(
        applicable_node_label_types={
            "try_statement",
        },
        walk_fun=common_try_statement,
    ),
    Walker(
        applicable_node_label_types={
            "try_with_resources_statement",
        },
        walk_fun=java_try_with_resources_statement,
    ),
)
