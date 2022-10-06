# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from syntax_graph.syntax_readers.javascript import (
    arguments as javascript_arguments,
    arrow_function as javascript_arrow_function,
    assignment_expression as javascript_assignment_expression,
    binary_expression as javascript_binary_expression,
    boolean_literal as javascript_boolean_literal,
    call_expression as javascript_call_expression,
    comment as javascript_comment,
    expression_statement as javascript_expression_statement,
    identifier as javascript_identifier,
    if_statement as javascript_if_statement,
    member_expression as javascript_member_expression,
    method_declaration as javascript_method_declaration,
    number_literal as javascript_number_literal,
    object as javascript_object,
    pair as javascript_pair,
    parameter_list as javascript_parameter_list,
    parenthesized_expression as javascript_parenthesized_expression,
    program as javascript_program,
    return_statement as javascript_return_statement,
    statement_block as javascript_statement_block,
    string_literal as javascript_string_literal,
    subscript_expression as javascript_subscript_expression,
    switch_body as javascript_switch_body,
    switch_case as javascript_switch_case,
    switch_statement as javascript_switch_statement,
    variable_declaration as javascript_variable_declaration,
)
from syntax_graph.syntax_readers.typescript import (
    ambient_declaration as typescript_ambient_declaration,
    array as typescript_array,
    as_expression as typescript_as_expression,
    enum_assignment as typescript_enum_assignment,
    enum_body as typescript_enum_body,
    enum_declaration as typescript_enum_declaration,
    function_signature as typescript_function_signature,
    function_type as typescript_function_type,
    interface_declaration as typescript_interface_declaration,
    intersection_type as typescript_intersection_type,
    predefined_type as typescript_predefined_type,
    property_signature as typescript_property_signature,
    required_parameter as typescript_required_parameter,
    rest_pattern as typescript_rest_pattern,
    ternary_expression as typescript_ternary_expression,
    tuple_type as typescript_tuple_type,
    type_alias_declaration as typescript_type_alias_declaration,
    type_annotation as typescript_type_annotation,
    union_type as typescript_union_type,
    void as typescript_void,
)
from syntax_graph.types import (
    Dispatcher,
    Dispatchers,
)

TYPESCRIPT_DISPATCHERS: Dispatchers = (
    Dispatcher(
        applicable_types={
            "ambient_declaration",
        },
        syntax_reader=typescript_ambient_declaration.reader,
    ),
    Dispatcher(
        applicable_types={
            "arguments",
        },
        syntax_reader=javascript_arguments.reader,
    ),
    Dispatcher(
        applicable_types={
            "array",
        },
        syntax_reader=typescript_array.reader,
    ),
    Dispatcher(
        applicable_types={
            "arrow_function",
        },
        syntax_reader=javascript_arrow_function.reader,
    ),
    Dispatcher(
        applicable_types={
            "as_expression",
        },
        syntax_reader=typescript_as_expression.reader,
    ),
    Dispatcher(
        applicable_types={
            "assignment_expression",
        },
        syntax_reader=javascript_assignment_expression.reader,
    ),
    Dispatcher(
        applicable_types={
            "binary_expression",
        },
        syntax_reader=javascript_binary_expression.reader,
    ),
    Dispatcher(
        applicable_types={
            "call_expression",
        },
        syntax_reader=javascript_call_expression.reader,
    ),
    Dispatcher(
        applicable_types={
            "comment",
        },
        syntax_reader=javascript_comment.reader,
    ),
    Dispatcher(
        applicable_types={
            "enum_assignment",
        },
        syntax_reader=typescript_enum_assignment.reader,
    ),
    Dispatcher(
        applicable_types={
            "enum_body",
        },
        syntax_reader=typescript_enum_body.reader,
    ),
    Dispatcher(
        applicable_types={
            "enum_declaration",
        },
        syntax_reader=typescript_enum_declaration.reader,
    ),
    Dispatcher(
        applicable_types={
            "expression_statement",
        },
        syntax_reader=javascript_expression_statement.reader,
    ),
    Dispatcher(
        applicable_types={
            "formal_parameters",
        },
        syntax_reader=javascript_parameter_list.reader,
    ),
    Dispatcher(
        applicable_types={
            "boolean",
            "false",
            "true",
        },
        syntax_reader=javascript_boolean_literal.reader,
    ),
    Dispatcher(
        applicable_types={
            "function_signature",
        },
        syntax_reader=typescript_function_signature.reader,
    ),
    Dispatcher(
        applicable_types={
            "function_type",
        },
        syntax_reader=typescript_function_type.reader,
    ),
    Dispatcher(
        applicable_types={
            "identifier",
            "property_identifier",
            "shorthand_property_identifier",
            "shorthand_property_identifier_pattern",
            "type_identifier",
        },
        syntax_reader=javascript_identifier.reader,
    ),
    Dispatcher(
        applicable_types={
            "if_statement",
        },
        syntax_reader=javascript_if_statement.reader,
    ),
    Dispatcher(
        applicable_types={
            "interface_declaration",
        },
        syntax_reader=typescript_interface_declaration.reader,
    ),
    Dispatcher(
        applicable_types={
            "intersection_type",
        },
        syntax_reader=typescript_intersection_type.reader,
    ),
    Dispatcher(
        applicable_types={
            "member_expression",
        },
        syntax_reader=javascript_member_expression.reader,
    ),
    Dispatcher(
        applicable_types={
            "function_declaration",
        },
        syntax_reader=javascript_method_declaration.reader,
    ),
    Dispatcher(
        applicable_types={
            "number",
        },
        syntax_reader=javascript_number_literal.reader,
    ),
    Dispatcher(
        applicable_types={
            "object",
            "object_type",
        },
        syntax_reader=javascript_object.reader,
    ),
    Dispatcher(
        applicable_types={
            "pair",
        },
        syntax_reader=javascript_pair.reader,
    ),
    Dispatcher(
        applicable_types={
            "parenthesized_expression",
        },
        syntax_reader=javascript_parenthesized_expression.reader,
    ),
    Dispatcher(
        applicable_types={
            "program",
        },
        syntax_reader=javascript_program.reader,
    ),
    Dispatcher(
        applicable_types={
            "optional_type",
            "array_type",
            "literal_type",
            "predefined_type",
        },
        syntax_reader=typescript_predefined_type.reader,
    ),
    Dispatcher(
        applicable_types={
            "property_signature",
        },
        syntax_reader=typescript_property_signature.reader,
    ),
    Dispatcher(
        applicable_types={
            "required_parameter",
        },
        syntax_reader=typescript_required_parameter.reader,
    ),
    Dispatcher(
        applicable_types={
            "rest_pattern",
        },
        syntax_reader=typescript_rest_pattern.reader,
    ),
    Dispatcher(
        applicable_types={
            "return_statement",
        },
        syntax_reader=javascript_return_statement.reader,
    ),
    Dispatcher(
        applicable_types={
            "statement_block",
        },
        syntax_reader=javascript_statement_block.reader,
    ),
    Dispatcher(
        applicable_types={
            "string",
        },
        syntax_reader=javascript_string_literal.reader,
    ),
    Dispatcher(
        applicable_types={
            "subscript_expression",
        },
        syntax_reader=javascript_subscript_expression.reader,
    ),
    Dispatcher(
        applicable_types={
            "switch_body",
        },
        syntax_reader=javascript_switch_body.reader,
    ),
    Dispatcher(
        applicable_types={
            "switch_case",
        },
        syntax_reader=javascript_switch_case.reader,
    ),
    Dispatcher(
        applicable_types={
            "switch_statement",
        },
        syntax_reader=javascript_switch_statement.reader,
    ),
    Dispatcher(
        applicable_types={
            "ternary_expression",
        },
        syntax_reader=typescript_ternary_expression.reader,
    ),
    Dispatcher(
        applicable_types={
            "tuple_type",
        },
        syntax_reader=typescript_tuple_type.reader,
    ),
    Dispatcher(
        applicable_types={
            "type_annotation",
        },
        syntax_reader=typescript_type_annotation.reader,
    ),
    Dispatcher(
        applicable_types={
            "type_alias_declaration",
        },
        syntax_reader=typescript_type_alias_declaration.reader,
    ),
    Dispatcher(
        applicable_types={
            "union_type",
        },
        syntax_reader=typescript_union_type.reader,
    ),
    Dispatcher(
        applicable_types={
            "lexical_declaration",
            "variable_declaration",
        },
        syntax_reader=javascript_variable_declaration.reader,
    ),
    Dispatcher(
        applicable_types={
            "void",
        },
        syntax_reader=typescript_void.reader,
    ),
)
