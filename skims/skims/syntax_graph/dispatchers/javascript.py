# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from syntax_graph.syntax_readers.common import (
    boolean_literal as common_boolean_literal,
    break_statement as common_break_statement,
    call_expression as common_call_expression,
    class_body as common_class_body,
    class_declaration as common_class_declaration,
    comment as common_comment,
    do_statement as common_do_statement,
    else_clause as common_else_clause,
    export_statement as common_export_statement,
    expression_statement as common_expression_statement,
    finally_clause as common_finally_clause,
    identifier as common_identifier,
    if_statement as common_if_statement,
    method_declaration as common_method_declaration,
    new_expression as common_new_expression,
    null_literal as common_null_literal,
    number_literal as common_number_literal,
    pair as common_pair,
    parameter_list as common_parameter_list,
    parenthesized_expression as common_parenthesized_expression,
    program as common_program,
    return_statement as common_return_statement,
    statement_block as common_statement_block,
    string_literal as common_string_literal,
    switch_body as common_switch_body,
    switch_case as common_switch_case,
    switch_default as common_switch_default,
    switch_statement as common_switch_statement,
    this as common_this,
    throw_statement as common_throw_statement,
    unary_expression as common_unary_expression,
    update_expression as common_update_expression,
    yield_expression as common_yield_expression,
)
from syntax_graph.syntax_readers.javascript import (
    arguments as javascript_arguments,
    array as javascript_array,
    arrow_function as javascript_arrow_function,
    assignment_expression as javascript_assignment_expression,
    await_expression as javascript_await_expression,
    binary_expression as javascript_binary_expression,
    catch_clause as javascript_catch_clause,
    for_each_statement as javascript_for_each_statement,
    for_statement as javascript_for_statement,
    import_statement as javascript_import_statement,
    member_expression as javascript_member_expression,
    object as javascript_object,
    subscript_expression as javascript_subscript_expression,
    try_statement as javascript_try_statement,
    variable_declaration as javascript_variable_declaration,
    while_statement as javascript_while_statement,
)
from syntax_graph.types import (
    Dispatcher,
    Dispatchers,
)

JAVASCRIPT_DISPATCHERS: Dispatchers = (
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
        syntax_reader=javascript_array.reader,
    ),
    Dispatcher(
        applicable_types={
            "arrow_function",
        },
        syntax_reader=javascript_arrow_function.reader,
    ),
    Dispatcher(
        applicable_types={
            "assignment_expression",
            "augmented_assignment_expression",
        },
        syntax_reader=javascript_assignment_expression.reader,
    ),
    Dispatcher(
        applicable_types={
            "await_expression",
        },
        syntax_reader=javascript_await_expression.reader,
    ),
    Dispatcher(
        applicable_types={
            "binary_expression",
        },
        syntax_reader=javascript_binary_expression.reader,
    ),
    Dispatcher(
        applicable_types={
            "false",
            "true",
        },
        syntax_reader=common_boolean_literal.reader,
    ),
    Dispatcher(
        applicable_types={
            "break_statement",
        },
        syntax_reader=common_break_statement.reader,
    ),
    Dispatcher(
        applicable_types={
            "call_expression",
        },
        syntax_reader=common_call_expression.reader,
    ),
    Dispatcher(
        applicable_types={
            "catch_clause",
        },
        syntax_reader=javascript_catch_clause.reader,
    ),
    Dispatcher(
        applicable_types={
            "class_body",
        },
        syntax_reader=common_class_body.reader,
    ),
    Dispatcher(
        applicable_types={
            "class_declaration",
        },
        syntax_reader=common_class_declaration.reader,
    ),
    Dispatcher(
        applicable_types={
            "comment",
        },
        syntax_reader=common_comment.reader,
    ),
    Dispatcher(
        applicable_types={
            "do_statement",
        },
        syntax_reader=common_do_statement.reader,
    ),
    Dispatcher(
        applicable_types={
            "else_clause",
        },
        syntax_reader=common_else_clause.reader,
    ),
    Dispatcher(
        applicable_types={
            "export_statement",
        },
        syntax_reader=common_export_statement.reader,
    ),
    Dispatcher(
        applicable_types={
            "expression_statement",
        },
        syntax_reader=common_expression_statement.reader,
    ),
    Dispatcher(
        applicable_types={
            "identifier",
            "property_identifier",
        },
        syntax_reader=common_identifier.reader,
    ),
    Dispatcher(
        applicable_types={
            "if_statement",
        },
        syntax_reader=common_if_statement.reader,
    ),
    Dispatcher(
        applicable_types={
            "import_statement",
        },
        syntax_reader=javascript_import_statement.reader,
    ),
    Dispatcher(
        applicable_types={
            "finally_clause",
        },
        syntax_reader=common_finally_clause.reader,
    ),
    Dispatcher(
        applicable_types={
            "for_in_statement",
        },
        syntax_reader=javascript_for_each_statement.reader,
    ),
    Dispatcher(
        applicable_types={
            "for_statement",
        },
        syntax_reader=javascript_for_statement.reader,
    ),
    Dispatcher(
        applicable_types={
            "member_expression",
        },
        syntax_reader=javascript_member_expression.reader,
    ),
    Dispatcher(
        applicable_types={
            "function",
            "function_declaration",
            "generator_function_declaration",
            "method_definition",
        },
        syntax_reader=common_method_declaration.reader,
    ),
    Dispatcher(
        applicable_types={
            "new_expression",
        },
        syntax_reader=common_new_expression.reader,
    ),
    Dispatcher(
        applicable_types={
            "number",
        },
        syntax_reader=common_number_literal.reader,
    ),
    Dispatcher(
        applicable_types={
            "null",
        },
        syntax_reader=common_null_literal.reader,
    ),
    Dispatcher(
        applicable_types={
            "object",
        },
        syntax_reader=javascript_object.reader,
    ),
    Dispatcher(
        applicable_types={
            "pair",
        },
        syntax_reader=common_pair.reader,
    ),
    Dispatcher(
        applicable_types={
            "formal_parameters",
        },
        syntax_reader=common_parameter_list.reader,
    ),
    Dispatcher(
        applicable_types={
            "parenthesized_expression",
        },
        syntax_reader=common_parenthesized_expression.reader,
    ),
    Dispatcher(
        applicable_types={
            "program",
        },
        syntax_reader=common_program.reader,
    ),
    Dispatcher(
        applicable_types={
            "return_statement",
        },
        syntax_reader=common_return_statement.reader,
    ),
    Dispatcher(
        applicable_types={
            "statement_block",
        },
        syntax_reader=common_statement_block.reader,
    ),
    Dispatcher(
        applicable_types={
            "string",
            "template_string",
        },
        syntax_reader=common_string_literal.reader,
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
        syntax_reader=common_switch_body.reader,
    ),
    Dispatcher(
        applicable_types={
            "switch_case",
        },
        syntax_reader=common_switch_case.reader,
    ),
    Dispatcher(
        applicable_types={
            "switch_default",
        },
        syntax_reader=common_switch_default.reader,
    ),
    Dispatcher(
        applicable_types={
            "switch_statement",
        },
        syntax_reader=common_switch_statement.reader,
    ),
    Dispatcher(
        applicable_types={
            "this",
        },
        syntax_reader=common_this.reader,
    ),
    Dispatcher(
        applicable_types={
            "throw_statement",
        },
        syntax_reader=common_throw_statement.reader,
    ),
    Dispatcher(
        applicable_types={
            "try_statement",
        },
        syntax_reader=javascript_try_statement.reader,
    ),
    Dispatcher(
        applicable_types={
            "unary_expression",
        },
        syntax_reader=common_unary_expression.reader,
    ),
    Dispatcher(
        applicable_types={
            "update_expression",
        },
        syntax_reader=common_update_expression.reader,
    ),
    Dispatcher(
        applicable_types={
            "variable_declaration",
            "lexical_declaration",
        },
        syntax_reader=javascript_variable_declaration.reader,
    ),
    Dispatcher(
        applicable_types={
            "while_statement",
        },
        syntax_reader=javascript_while_statement.reader,
    ),
    Dispatcher(
        applicable_types={
            "yield_expression",
        },
        syntax_reader=common_yield_expression.reader,
    ),
)
