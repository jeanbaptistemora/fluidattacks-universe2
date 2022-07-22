from syntax_graph.syntax_readers.common import (
    array as common_array,
    binary_expression as common_binary_expression,
    call_expression as common_call_expression,
    comment as common_comment,
    expression_statement as common_expression_statement,
    identifier as common_identifier,
    if_statement as common_if_statement,
    method_declaration as common_method_declaration,
    number_literal as common_number_literal,
    pair as common_pair,
    parenthesized_expression as common_parenthesized_expression,
    program as common_program,
    statement_block as common_statement_block,
    string_literal as common_string_literal,
    throw_statement as common_throw_statement,
    variable_declaration as common_variable_declaration,
    variable_declarator as common_variable_declarator,
)
from syntax_graph.syntax_readers.javascript import (
    arguments as javascript_arguments,
    arrow_function as javascript_arrow_function,
    assignment_expression as javascript_assignment_expression,
    lexical_declaration as javascript_lexical_declaration,
    member_expression as javascript_member_expression,
    object as javascript_object,
    try_statement as javascript_try_statement,
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
        syntax_reader=common_array.reader,
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
        },
        syntax_reader=javascript_assignment_expression.reader,
    ),
    Dispatcher(
        applicable_types={
            "binary_expression",
        },
        syntax_reader=common_binary_expression.reader,
    ),
    Dispatcher(
        applicable_types={
            "call_expression",
        },
        syntax_reader=common_call_expression.reader,
    ),
    Dispatcher(
        applicable_types={
            "comment",
        },
        syntax_reader=common_comment.reader,
    ),
    Dispatcher(
        applicable_types={
            "expression_statement",
        },
        syntax_reader=common_expression_statement.reader,
    ),
    Dispatcher(
        applicable_types={
            "function_declaration",
        },
        syntax_reader=common_method_declaration.reader,
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
            "lexical_declaration",
        },
        syntax_reader=javascript_lexical_declaration.reader,
    ),
    Dispatcher(
        applicable_types={
            "member_expression",
        },
        syntax_reader=javascript_member_expression.reader,
    ),
    Dispatcher(
        applicable_types={
            "number",
        },
        syntax_reader=common_number_literal.reader,
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
            "statement_block",
        },
        syntax_reader=common_statement_block.reader,
    ),
    Dispatcher(
        applicable_types={
            "string",
        },
        syntax_reader=common_string_literal.reader,
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
            "variable_declaration",
        },
        syntax_reader=common_variable_declaration.reader,
    ),
    Dispatcher(
        applicable_types={
            "variable_declarator",
        },
        syntax_reader=common_variable_declarator.reader,
    ),
)
