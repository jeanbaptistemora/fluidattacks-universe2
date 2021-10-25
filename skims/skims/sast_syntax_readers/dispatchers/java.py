from sast_syntax_readers.common import (
    binary_expression as common_binary_expression,
    cast_expression as common_cast_expression,
    identifier as common_identifier,
    literal as common_literal,
    noop as common_noop,
    object_creation_expression as common_object_creation_expression,
    parenthesized_expression as common_parenthesized_expression,
    return_statement as common_return_statement,
    unary_expression as common_unary_expression,
    while_statement as common_while_statement,
)
from sast_syntax_readers.java import (
    array_access as java_array_access,
    array_creation_expression as java_array_creation_expression,
    array_initializer as java_array_initializer,
    assignment_expression as java_assignment_expression,
    catch_clause as java_catch_clause,
    enhanced_for_statement as java_enhanced_for_statement,
    for_statement as java_for_statement,
    if_statement as java_if_statement,
    instanceof_expression as java_instanceof_expression,
    lambda_expression as java_lambda_expression,
    local_variable_declaration as java_local_variable_declaration,
    method_declaration as java_method_declaration,
    method_invocation as java_method_invocation,
    resource as java_resource,
    switch_expression as java_switch_expression,
    switch_label as java_switch_label,
    ternary_expression as java_ternary_expression,
    this as java_this,
)
from sast_syntax_readers.types import (
    Dispatcher,
    Dispatchers,
)

JAVA_DISPATCHERS: Dispatchers = (
    Dispatcher(
        applicable_node_label_types={
            "array_access",
        },
        syntax_reader=java_array_access.reader,
    ),
    Dispatcher(
        applicable_node_label_types={
            "array_creation_expression",
        },
        syntax_reader=java_array_creation_expression.reader,
    ),
    Dispatcher(
        applicable_node_label_types={
            "array_initializer",
        },
        syntax_reader=java_array_initializer.reader,
    ),
    Dispatcher(
        applicable_node_label_types={
            "assignment_expression",
        },
        syntax_reader=java_assignment_expression.reader,
    ),
    Dispatcher(
        applicable_node_label_types={
            "binary_expression",
        },
        syntax_reader=common_binary_expression.reader,
    ),
    Dispatcher(
        applicable_node_label_types={
            "cast_expression",
        },
        syntax_reader=common_cast_expression.reader,
    ),
    Dispatcher(
        applicable_node_label_types={
            "catch_clause",
        },
        syntax_reader=java_catch_clause.reader,
    ),
    Dispatcher(
        applicable_node_label_types={
            "constructor_declaration",
            "method_declaration",
        },
        syntax_reader=java_method_declaration.reader,
    ),
    Dispatcher(
        applicable_node_label_types={
            "enhanced_for_statement",
        },
        syntax_reader=java_enhanced_for_statement.reader,
    ),
    Dispatcher(
        applicable_node_label_types={
            "field_access",
            "identifier",
            "simple_identifier",
        },
        syntax_reader=common_identifier.reader,
    ),
    Dispatcher(
        applicable_node_label_types={"for_statement"},
        syntax_reader=java_for_statement.reader,
    ),
    Dispatcher(
        applicable_node_label_types={
            "if_statement",
        },
        syntax_reader=java_if_statement.reader,
    ),
    Dispatcher(
        applicable_node_label_types={
            "instanceof_expression",
        },
        syntax_reader=java_instanceof_expression.reader,
    ),
    Dispatcher(
        applicable_node_label_types={
            "lambda_expression",
        },
        syntax_reader=java_lambda_expression.reader,
    ),
    Dispatcher(
        applicable_node_label_types={
            "local_variable_declaration",
        },
        syntax_reader=java_local_variable_declaration.reader,
    ),
    Dispatcher(
        applicable_node_label_types={
            "method_invocation",
        },
        syntax_reader=java_method_invocation.reader,
    ),
    Dispatcher(
        applicable_node_label_types={
            "object_creation_expression",
        },
        syntax_reader=common_object_creation_expression.reader,
    ),
    Dispatcher(
        applicable_node_label_types={
            "parenthesized_expression",
        },
        syntax_reader=common_parenthesized_expression.reader,
    ),
    Dispatcher(
        applicable_node_label_types={
            "resource",
        },
        syntax_reader=java_resource.reader,
    ),
    Dispatcher(
        applicable_node_label_types={
            "return_statement",
        },
        syntax_reader=common_return_statement.reader,
    ),
    Dispatcher(
        applicable_node_label_types={
            "switch_expression",
        },
        syntax_reader=java_switch_expression.reader,
    ),
    Dispatcher(
        applicable_node_label_types={
            "switch_label",
        },
        syntax_reader=java_switch_label.reader,
    ),
    Dispatcher(
        applicable_node_label_types={
            "ternary_expression",
        },
        syntax_reader=java_ternary_expression.reader,
    ),
    Dispatcher(
        applicable_node_label_types={
            "this",
            "this_expression",
        },
        syntax_reader=java_this.reader,
    ),
    Dispatcher(
        applicable_node_label_types={
            "unary_expression",
        },
        syntax_reader=common_unary_expression.reader,
    ),
    Dispatcher(
        applicable_node_label_types={
            "while_statement",
        },
        syntax_reader=common_while_statement.reader,
    ),
    Dispatcher(
        applicable_node_label_types={
            "boolean_literal",
            "character_literal",
            "composite_literal",
            "decimal_integer_literal",
            "false",
            "floating_point_type",
            "int_literal",
            "integer_literal",
            "interpreted_string_literal",
            "line_string_literal",
            "nil",
            "null",
            "null_literal",
            "number",
            "raw_string_literal",
            "real_literal",
            "string",
            "string_literal",
            "true",
            "undefined",
            "verbatim_string_literal",
        },
        syntax_reader=common_literal.reader,
    ),
    Dispatcher(
        applicable_node_label_types={
            "else_clause",
            "block",
            "statement_block",
            "break_statement",
            "class_body",
            "class_declaration",
            "constructor_body",
            "continue_statement",
            "comment",
            "expression_statement",
            "finally_clause",
            "resource_specification",
            "try_statement",
            "try_with_resources_statement",
            "throw_statement",
            "update_expression",
            "argument_list",
            ";",
            "-",
            "+",
            "*",
            "/",
            "%",
            "(",
            ")",
            ".",
            "{",
            "}",
            "program",
        },
        syntax_reader=common_noop.reader,
    ),
)
