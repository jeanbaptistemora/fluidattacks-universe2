from sast_syntax_readers.c_sharp import (
    argument as c_sharp_argument,
    array_creation_expression as c_sharp_array_creation_expression,
    assignment_expression as c_sharp_assignment_expression,
    case_switch_label as c_sharp_case_switch_label,
    default_switch_label as c_sharp_default_switch_label,
    element_access_expression as c_sharp_element_access_expression,
    for_statement as c_sharp_for_statement,
    initializer_expression as c_sharp_initializer_expression,
    invocation_expression as c_sharp_invocation_expression,
    lambda_expression as c_sharp_lambda_expression,
    local_declaration_statement as c_sharp_local_declaration_statement,
    member_access_expression as c_sharp_member_access_expression,
    method_declaration as c_sharp_method_declaration,
    object_creation_expression as c_sharp_object_creation_expression,
    parameter as c_sharp_parameter,
    prefix_expression as c_sharp_prefix_expression,
    switch_statement as c_sharp_switch_statement,
    type_of_expression as c_sharp_type_of_expression,
    using_statement as c_sharp_using_statement,
    variable_declaration as c_sharp_variable_declaration,
    while_statement as c_sharp_while_statement,
)
from sast_syntax_readers.common import (
    binary_expression as common_binary_expression,
    cast_expression as common_cast_expression,
    identifier as common_identifier,
    if_statement as common_if_statement,
    literal as common_literal,
    noop as common_noop,
    parenthesized_expression as common_parenthesized_expression,
    return_statement as common_return_statement,
)
from sast_syntax_readers.types import (
    Dispatcher,
    Dispatchers,
)

CSHARP_DISPATCHERS: Dispatchers = (
    Dispatcher(
        applicable_node_label_types={
            "argument",
        },
        syntax_reader=c_sharp_argument.reader,
    ),
    Dispatcher(
        applicable_node_label_types={
            "array_creation_expression",
        },
        syntax_reader=c_sharp_array_creation_expression.reader,
    ),
    Dispatcher(
        applicable_node_label_types={
            "assignment_expression",
        },
        syntax_reader=c_sharp_assignment_expression.reader,
    ),
    Dispatcher(
        applicable_node_label_types={
            "binary_expression",
        },
        syntax_reader=common_binary_expression.reader,
    ),
    Dispatcher(
        applicable_node_label_types={
            "case_switch_label",
        },
        syntax_reader=c_sharp_case_switch_label.reader,
    ),
    Dispatcher(
        applicable_node_label_types={
            "cast_expression",
        },
        syntax_reader=common_cast_expression.reader,
    ),
    Dispatcher(
        applicable_node_label_types={
            "constructor_declaration",
            "method_declaration",
        },
        syntax_reader=c_sharp_method_declaration.reader,
    ),
    Dispatcher(
        applicable_node_label_types={
            "default_switch_label",
        },
        syntax_reader=c_sharp_default_switch_label.reader,
    ),
    Dispatcher(
        applicable_node_label_types={
            "element_access_expression",
        },
        syntax_reader=c_sharp_element_access_expression.reader,
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
        syntax_reader=c_sharp_for_statement.reader,
    ),
    Dispatcher(
        applicable_node_label_types={
            "if_statement",
        },
        syntax_reader=common_if_statement.reader,
    ),
    Dispatcher(
        applicable_node_label_types={
            "initializer_expression",
        },
        syntax_reader=c_sharp_initializer_expression.reader,
    ),
    Dispatcher(
        applicable_node_label_types={
            "invocation_expression",
        },
        syntax_reader=c_sharp_invocation_expression.reader,
    ),
    Dispatcher(
        applicable_node_label_types={
            "lambda_expression",
        },
        syntax_reader=c_sharp_lambda_expression.reader,
    ),
    Dispatcher(
        applicable_node_label_types={
            "local_declaration_statement",
        },
        syntax_reader=c_sharp_local_declaration_statement.reader,
    ),
    Dispatcher(
        applicable_node_label_types={
            "member_access_expression",
        },
        syntax_reader=c_sharp_member_access_expression.reader,
    ),
    Dispatcher(
        applicable_node_label_types={
            "object_creation_expression",
        },
        syntax_reader=c_sharp_object_creation_expression.reader,
    ),
    Dispatcher(
        applicable_node_label_types={
            "parameter",
        },
        syntax_reader=c_sharp_parameter.reader,
    ),
    Dispatcher(
        applicable_node_label_types={
            "parenthesized_expression",
        },
        syntax_reader=common_parenthesized_expression.reader,
    ),
    Dispatcher(
        applicable_node_label_types={
            "prefix_unary_expression",
        },
        syntax_reader=c_sharp_prefix_expression.reader,
    ),
    Dispatcher(
        applicable_node_label_types={
            "return_statement",
        },
        syntax_reader=common_return_statement.reader,
    ),
    Dispatcher(
        applicable_node_label_types={
            "switch_statement",
        },
        syntax_reader=c_sharp_switch_statement.reader,
    ),
    Dispatcher(
        applicable_node_label_types={
            "type_of_expression",
        },
        syntax_reader=c_sharp_type_of_expression.reader,
    ),
    Dispatcher(
        applicable_node_label_types={
            "using_statement",
        },
        syntax_reader=c_sharp_using_statement.reader,
    ),
    Dispatcher(
        applicable_node_label_types={
            "variable_declaration",
        },
        syntax_reader=c_sharp_variable_declaration.reader,
    ),
    Dispatcher(
        applicable_node_label_types={
            "while_statement",
        },
        syntax_reader=c_sharp_while_statement.reader,
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
