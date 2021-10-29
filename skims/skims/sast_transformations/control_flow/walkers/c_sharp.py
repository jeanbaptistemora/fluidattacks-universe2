from sast_transformations.control_flow.c_sharp import (
    lambda_expression as c_sharp_lambda_expression,
    switch_statement as c_sharp_switch_statement,
    using_statement as c_sharp_using_statement,
)
from sast_transformations.control_flow.common import (
    catch_statement as common_catch_statement,
    if_statement as common_if_statement,
    link_to_last_node as common_link_to_last_node,
    loop_statement as common_loop_statement,
    step_by_step as common_step_by_step,
    try_statement as common_try_statement,
)
from sast_transformations.control_flow.types import (
    Walker,
    Walkers,
)

CSHARP_WALKERS: Walkers = (
    Walker(
        applicable_node_label_types={
            "block",
            "constructor_body",
            "expression_statement",
        },
        walk_fun=common_step_by_step,
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
            "switch_statement",
        },
        walk_fun=c_sharp_switch_statement,
    ),
    Walker(
        applicable_node_label_types={
            "using_statement",
        },
        walk_fun=c_sharp_using_statement,
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
            "if_statement",
        },
        walk_fun=common_if_statement,
    ),
    Walker(
        applicable_node_label_types={
            "try_statement",
        },
        walk_fun=common_try_statement,
    ),
    Walker(
        applicable_node_label_types={
            "for_statement",
            "do_statement",
            "while_statement",
            "for_each_statement",
        },
        walk_fun=common_loop_statement,
    ),
    Walker(
        applicable_node_label_types={
            "lambda_expression",
        },
        walk_fun=c_sharp_lambda_expression,
    ),
)
