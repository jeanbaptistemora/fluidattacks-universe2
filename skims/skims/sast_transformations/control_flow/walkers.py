from functools import (
    partial,
)
from model.graph_model import (
    GraphShardMetadataLanguage,
)
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
from sast_transformations.control_flow.go import (
    switch_statement as go_switch_statement,
)
from sast_transformations.control_flow.java import (
    lambda_expression as java_lambda_expression,
    method_invocation as java_method_invocation,
    switch_expression as java_switch_expression,
    try_with_resources_statement as java_try_with_resources_statement,
)
from sast_transformations.control_flow.javascript import (
    function_declaration as javascript_function_declaration,
    if_statement as javascript_if_statement,
    switch_statement as javascript_switch_statement,
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
)
from typing import (
    Dict,
    Tuple,
)

CSHARP_WALKERS: Tuple[Walker, ...] = (
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
        applicable_node_label_types={"catch_clause", "finally_clause"},
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


GO_WALKERS: Tuple[Walker, ...] = (
    Walker(
        applicable_node_label_types={"block"},
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
        applicable_node_label_types={"if_statement"},
        walk_fun=common_if_statement,
    ),
    Walker(
        applicable_node_label_types={"for_statement"},
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


JAVA_WALKERS: Tuple[Walker, ...] = (
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
        applicable_node_label_types={"catch_clause", "finally_clause"},
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
        applicable_node_label_types={"if_statement"},
        walk_fun=common_if_statement,
    ),
    Walker(
        applicable_node_label_types={"switch_expression"},
        walk_fun=java_switch_expression,
    ),
    Walker(
        applicable_node_label_types={"method_invocation"},
        walk_fun=java_method_invocation,
    ),
    Walker(
        applicable_node_label_types={"lambda_expression"},
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
        applicable_node_label_types={"try_statement"},
        walk_fun=common_try_statement,
    ),
    Walker(
        applicable_node_label_types={"try_with_resources_statement"},
        walk_fun=java_try_with_resources_statement,
    ),
)


JAVASCRIPT_WALKERS: Tuple[Walker, ...] = (
    Walker(
        applicable_node_label_types={
            "statement_block",
            "expression_statement",
            "program",
        },
        walk_fun=common_step_by_step,
    ),
    Walker(
        applicable_node_label_types={"catch_clause", "finally_clause"},
        walk_fun=common_catch_statement,
    ),
    Walker(
        applicable_node_label_types={"if_statement"},
        walk_fun=javascript_if_statement,
    ),
    Walker(
        applicable_node_label_types={"function_declaration"},
        walk_fun=javascript_function_declaration,
    ),
    Walker(
        applicable_node_label_types={"switch_statement"},
        walk_fun=javascript_switch_statement,
    ),
    Walker(
        applicable_node_label_types={"try_statement"},
        walk_fun=partial(
            common_try_statement,
            language=GraphShardMetadataLanguage.JAVASCRIPT,
        ),
    ),
    Walker(
        applicable_node_label_types={
            "for_statement",
            "do_statement",
            "while_statement",
            "for_each_statement",
            "for_in_statement",
            "for_of_statement",
        },
        walk_fun=partial(
            common_loop_statement,
            language=GraphShardMetadataLanguage.JAVASCRIPT,
        ),
    ),
)


KOTLIN_WALKERS: Tuple[Walker, ...] = (
    Walker(
        applicable_node_label_types={"class_body"},
        walk_fun=kotlin_class_statements,
    ),
    Walker(
        applicable_node_label_types={"for_statement", "while_statement"},
        walk_fun=kotlin_loop_statement,
    ),
    Walker(
        applicable_node_label_types={"function_body", "statements"},
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
        applicable_node_label_types={"if_expression"},
        walk_fun=kotlin_if_statement,
    ),
    Walker(
        applicable_node_label_types={"try_catch_expression"},
        walk_fun=kotlin_try_catch_statement,
    ),
    Walker(
        applicable_node_label_types={"when_expression"},
        walk_fun=kotlin_when_statement,
    ),
)


WALKERS_BY_LANG: Dict[GraphShardMetadataLanguage, Tuple[Walker, ...]] = {
    GraphShardMetadataLanguage.CSHARP: CSHARP_WALKERS,
    GraphShardMetadataLanguage.GO: GO_WALKERS,
    GraphShardMetadataLanguage.JAVA: JAVA_WALKERS,
    GraphShardMetadataLanguage.JAVASCRIPT: JAVASCRIPT_WALKERS,
    GraphShardMetadataLanguage.KOTLIN: KOTLIN_WALKERS,
}
