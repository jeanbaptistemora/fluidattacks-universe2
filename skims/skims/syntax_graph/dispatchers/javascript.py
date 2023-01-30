from syntax_graph.syntax_readers.javascript import (
    arguments as javascript_arguments,
    array as javascript_array,
    arrow_function as javascript_arrow_function,
    assignment_expression as javascript_assignment_expression,
    await_expression as javascript_await_expression,
    binary_expression as javascript_binary_expression,
    boolean_literal as javascript_boolean_literal,
    break_statement as javascript_break_statement,
    call_expression as javascript_call_expression,
    catch_clause as javascript_catch_clause,
    class_body as javascript_class_body,
    class_declaration as javascript_class_declaration,
    comment as javascript_comment,
    do_statement as javascript_do_statement,
    else_clause as javascript_else_clause,
    execution_block as javascript_execution_block,
    export_statement as javascript_export_statement,
    expression_statement as javascript_expression_statement,
    finally_clause as javascript_finally_clause,
    for_each_statement as javascript_for_each_statement,
    for_statement as javascript_for_statement,
    identifier as javascript_identifier,
    if_statement as javascript_if_statement,
    import_node as javascript_import,
    import_statement as javascript_import_statement,
    jsx_attribute as javascript_jsx_attribute,
    jsx_element as javascript_jsx_element,
    member_expression as javascript_member_expression,
    method_declaration as javascript_method_declaration,
    new_expression as javascript_new_expression,
    null_literal as javascript_null_literal,
    number_literal as javascript_number_literal,
    object as javascript_object,
    pair as javascript_pair,
    parameter_list as javascript_parameter_list,
    parenthesized_expression as javascript_parenthesized_expression,
    program as javascript_program,
    return_statement as javascript_return_statement,
    string_literal as javascript_string_literal,
    subscript_expression as javascript_subscript_expression,
    switch_body as javascript_switch_body,
    switch_section as javascript_switch_section,
    switch_statement as javascript_switch_statement,
    ternary_expression as javascript_ternary_expression,
    this as javascript_this,
    throw_statement as javascript_throw_statement,
    try_statement as javascript_try_statement,
    unary_expression as javascript_unary_expression,
    update_expression as javascript_update_expression,
    variable_declaration as javascript_variable_declaration,
    while_statement as javascript_while_statement,
    yield_expression as javascript_yield_expression,
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
            "jsx_element",
            "jsx_fragment",
            "jsx_self_closing_element",
            "jsx_opening_element",
        },
        syntax_reader=javascript_jsx_element.reader,
    ),
    Dispatcher(
        applicable_types={
            "jsx_attribute",
        },
        syntax_reader=javascript_jsx_attribute.reader,
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
        syntax_reader=javascript_boolean_literal.reader,
    ),
    Dispatcher(
        applicable_types={
            "break_statement",
        },
        syntax_reader=javascript_break_statement.reader,
    ),
    Dispatcher(
        applicable_types={
            "call_expression",
        },
        syntax_reader=javascript_call_expression.reader,
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
        syntax_reader=javascript_class_body.reader,
    ),
    Dispatcher(
        applicable_types={
            "class_declaration",
        },
        syntax_reader=javascript_class_declaration.reader,
    ),
    Dispatcher(
        applicable_types={
            "comment",
        },
        syntax_reader=javascript_comment.reader,
    ),
    Dispatcher(
        applicable_types={
            "do_statement",
        },
        syntax_reader=javascript_do_statement.reader,
    ),
    Dispatcher(
        applicable_types={
            "else_clause",
        },
        syntax_reader=javascript_else_clause.reader,
    ),
    Dispatcher(
        applicable_types={
            "export_statement",
        },
        syntax_reader=javascript_export_statement.reader,
    ),
    Dispatcher(
        applicable_types={
            "expression_statement",
        },
        syntax_reader=javascript_expression_statement.reader,
    ),
    Dispatcher(
        applicable_types={
            "identifier",
            "property_identifier",
            "shorthand_property_identifier",
            "shorthand_property_identifier_pattern",
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
            "import",
        },
        syntax_reader=javascript_import.reader,
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
        syntax_reader=javascript_finally_clause.reader,
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
        syntax_reader=javascript_method_declaration.reader,
    ),
    Dispatcher(
        applicable_types={
            "new_expression",
        },
        syntax_reader=javascript_new_expression.reader,
    ),
    Dispatcher(
        applicable_types={
            "number",
        },
        syntax_reader=javascript_number_literal.reader,
    ),
    Dispatcher(
        applicable_types={
            "null",
        },
        syntax_reader=javascript_null_literal.reader,
    ),
    Dispatcher(
        applicable_types={
            "object",
            "object_pattern",
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
            "formal_parameters",
        },
        syntax_reader=javascript_parameter_list.reader,
    ),
    Dispatcher(
        applicable_types={
            "parenthesized_expression",
            "rest_pattern",
            "spread_element",
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
            "return_statement",
        },
        syntax_reader=javascript_return_statement.reader,
    ),
    Dispatcher(
        applicable_types={
            "statement_block",
        },
        syntax_reader=javascript_execution_block.reader,
    ),
    Dispatcher(
        applicable_types={
            "regex",
            "string",
            "template_string",
            "undefined",
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
            "switch_default",
        },
        syntax_reader=javascript_switch_section.reader,
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
        syntax_reader=javascript_ternary_expression.reader,
    ),
    Dispatcher(
        applicable_types={
            "this",
        },
        syntax_reader=javascript_this.reader,
    ),
    Dispatcher(
        applicable_types={
            "throw_statement",
        },
        syntax_reader=javascript_throw_statement.reader,
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
        syntax_reader=javascript_unary_expression.reader,
    ),
    Dispatcher(
        applicable_types={
            "update_expression",
        },
        syntax_reader=javascript_update_expression.reader,
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
        syntax_reader=javascript_yield_expression.reader,
    ),
)
