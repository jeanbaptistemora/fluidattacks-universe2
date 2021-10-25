from sast_syntax_readers.common import (
    binary_expression as common_binary_expression,
    identifier as common_identifier,
    literal as common_literal,
    noop as common_noop,
    parenthesized_expression as common_parenthesized_expression,
    return_statement as common_return_statement,
    unary_expression as common_unary_expression,
    while_statement as common_while_statement,
)
from sast_syntax_readers.javascript import (
    array as javascript_array,
    arrow_function as javascript_arrrow_function,
    assignment_expression as javascript_assignment_expression,
    await_expression as javascript_await_expression,
    call_expression as javascript_call_expression,
    catch_clause as javascript_catch_clause,
    do_statement as javascript_do_statement,
    for_in_statement as javascript_for_in_statement,
    for_statement as javascript_for_statement,
    formal_parameters as javascript_formal_parameters,
    function_declaration as javascript_function_declaration,
    if_statement as javascript_if_statement,
    import_statement as javascript_import_statement,
    lexical_declaration as javascript_lexical_declaration,
    member_expression as javascript_member_expression,
    new_expression as javascript_new_expression,
    object_ as javascript_object,
    subscript_expression as javascript_subscript_expression,
    switch_case as javascript_switch_case,
    switch_default as javascript_switch_default,
    switch_statement as javascript_switch_statement,
    template_string as javascript_template_string,
    ternary_expression as javascript_ternary_expression,
    variable_declaration as javascript_variable_declaration,
    variable_declarator as javascript_variable_declarator,
)
from sast_syntax_readers.types import (
    Dispatcher,
    Dispatchers,
)

JAVASCRIPT_DISPATCHERS: Dispatchers = (
    Dispatcher(
        applicable_node_label_types={
            "array",
        },
        syntax_reader=javascript_array.reader,
    ),
    Dispatcher(
        applicable_node_label_types={
            "arrow_function",
        },
        syntax_reader=javascript_arrrow_function.reader,
    ),
    Dispatcher(
        applicable_node_label_types={
            "assignment_expression",
            "augmented_assignment_expression",
        },
        syntax_reader=javascript_assignment_expression.reader,
    ),
    Dispatcher(
        applicable_node_label_types={
            "await_expression",
        },
        syntax_reader=javascript_await_expression.reader,
    ),
    Dispatcher(
        applicable_node_label_types={
            "binary_expression",
        },
        syntax_reader=common_binary_expression.reader,
    ),
    Dispatcher(
        applicable_node_label_types={
            "call_expression",
        },
        syntax_reader=javascript_call_expression.reader,
    ),
    Dispatcher(
        applicable_node_label_types={
            "catch_clause",
        },
        syntax_reader=javascript_catch_clause.reader,
    ),
    Dispatcher(
        applicable_node_label_types={
            "do_statement",
        },
        syntax_reader=javascript_do_statement.reader,
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
        applicable_node_label_types={
            "for_statement",
        },
        syntax_reader=javascript_for_statement.reader,
    ),
    Dispatcher(
        applicable_node_label_types={
            "for_in_statement",
        },
        syntax_reader=javascript_for_in_statement.reader,
    ),
    Dispatcher(
        applicable_node_label_types={
            "formal_parameters",
        },
        syntax_reader=javascript_formal_parameters.reader,
    ),
    Dispatcher(
        applicable_node_label_types={
            "function",
            "function_declaration",
            "generator_function_declaration",
        },
        syntax_reader=javascript_function_declaration.reader,
    ),
    Dispatcher(
        applicable_node_label_types={
            "if_statement",
        },
        syntax_reader=javascript_if_statement.reader,
    ),
    Dispatcher(
        applicable_node_label_types={
            "import_statement",
        },
        syntax_reader=javascript_import_statement.reader,
    ),
    Dispatcher(
        applicable_node_label_types={
            "lexical_declaration",
        },
        syntax_reader=javascript_lexical_declaration.reader,
    ),
    Dispatcher(
        applicable_node_label_types={
            "member_expression",
        },
        syntax_reader=javascript_member_expression.reader,
    ),
    Dispatcher(
        applicable_node_label_types={
            "new_expression",
        },
        syntax_reader=javascript_new_expression.reader,
    ),
    Dispatcher(
        applicable_node_label_types={
            "object",
        },
        syntax_reader=javascript_object.reader,
    ),
    Dispatcher(
        applicable_node_label_types={
            "parenthesized_expression",
        },
        syntax_reader=common_parenthesized_expression.reader,
    ),
    Dispatcher(
        applicable_node_label_types={
            "return_statement",
        },
        syntax_reader=common_return_statement.reader,
    ),
    Dispatcher(
        applicable_node_label_types={
            "subscript_expression",
        },
        syntax_reader=javascript_subscript_expression.reader,
    ),
    Dispatcher(
        applicable_node_label_types={
            "switch_case",
        },
        syntax_reader=javascript_switch_case.reader,
    ),
    Dispatcher(
        applicable_node_label_types={
            "switch_default",
        },
        syntax_reader=javascript_switch_default.reader,
    ),
    Dispatcher(
        applicable_node_label_types={
            "switch_statement",
        },
        syntax_reader=javascript_switch_statement.reader,
    ),
    Dispatcher(
        applicable_node_label_types={
            "template_string",
        },
        syntax_reader=javascript_template_string.reader,
    ),
    Dispatcher(
        applicable_node_label_types={
            "ternary_expression",
        },
        syntax_reader=javascript_ternary_expression.reader,
    ),
    Dispatcher(
        applicable_node_label_types={
            "unary_expression",
        },
        syntax_reader=common_unary_expression.reader,
    ),
    Dispatcher(
        applicable_node_label_types={
            "variable_declaration",
        },
        syntax_reader=javascript_variable_declaration.reader,
    ),
    Dispatcher(
        applicable_node_label_types={
            "variable_declarator",
        },
        syntax_reader=javascript_variable_declarator.reader,
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
