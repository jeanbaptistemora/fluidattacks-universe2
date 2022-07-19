from syntax_graph.syntax_readers.common import (
    array as common_array,
    call_expression as common_call_expression,
    comment as common_comment,
    expression_statement as common_expression_statement,
    identifier as common_identifier,
    pair as common_pair,
    program as common_program,
    string_literal as common_string_literal,
    variable_declarator as common_variable_declarator,
)
from syntax_graph.syntax_readers.javascript import (
    arguments as javascript_arguments,
    arrow_function as javascript_arrow_function,
    lexical_declaration as javascript_lexical_declaration,
    object as javascript_object,
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
            "identifier",
            "property_identifier",
        },
        syntax_reader=common_identifier.reader,
    ),
    Dispatcher(
        applicable_types={
            "lexical_declaration",
        },
        syntax_reader=javascript_lexical_declaration.reader,
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
            "program",
        },
        syntax_reader=common_program.reader,
    ),
    Dispatcher(
        applicable_types={
            "string",
        },
        syntax_reader=common_string_literal.reader,
    ),
    Dispatcher(
        applicable_types={
            "variable_declarator",
        },
        syntax_reader=common_variable_declarator.reader,
    ),
)
