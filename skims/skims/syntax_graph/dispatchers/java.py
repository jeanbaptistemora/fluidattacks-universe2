from syntax_graph.syntax_readers.common import (
    boolean_literal as common_boolean_literal,
    catch_clause as common_catch_clause,
    catch_declaration as common_catch_declaration,
    conditional_expression as common_conditional_expression,
    declaration_block as common_declaration_block,
    do_statement as common_do_statement,
    execution_block as common_execution_block,
    identifier as common_identifier,
    interpolation as common_interpolation,
    null_literal as common_null_literal,
    number_literal as common_number_literal,
    string_literal as common_string_literal,
    while_statement as common_while_statement,
)
from syntax_graph.syntax_readers.java import (
    program as java_program,
)
from syntax_graph.types import (
    Dispatcher,
    Dispatchers,
)

JAVA_DISPATCHERS: Dispatchers = (
    Dispatcher(
        applicable_types={
            "program",
        },
        syntax_reader=java_program.reader,
    ),
    Dispatcher(
        applicable_types={
            "boolean_literal",
        },
        syntax_reader=common_boolean_literal.reader,
    ),
    Dispatcher(
        applicable_types={
            "block",
        },
        syntax_reader=common_execution_block.reader,
    ),
    Dispatcher(
        applicable_types={
            "catch_clause",
        },
        syntax_reader=common_catch_clause.reader,
    ),
    Dispatcher(
        applicable_types={
            "catch_declaration",
        },
        syntax_reader=common_catch_declaration.reader,
    ),
    Dispatcher(
        applicable_types={
            "conditional_expression",
        },
        syntax_reader=common_conditional_expression.reader,
    ),
    Dispatcher(
        applicable_types={
            "declaration_list",
        },
        syntax_reader=common_declaration_block.reader,
    ),
    Dispatcher(
        applicable_types={
            "do_statement",
        },
        syntax_reader=common_do_statement.reader,
    ),
    Dispatcher(
        applicable_types={
            "identifier",
        },
        syntax_reader=common_identifier.reader,
    ),
    Dispatcher(
        applicable_types={
            "interpolation",
        },
        syntax_reader=common_interpolation.reader,
    ),
    Dispatcher(
        applicable_types={
            "null_literal",
        },
        syntax_reader=common_null_literal.reader,
    ),
    Dispatcher(
        applicable_types={
            "integer_literal",
        },
        syntax_reader=common_number_literal.reader,
    ),
    Dispatcher(
        applicable_types={
            "real_literal",
        },
        syntax_reader=common_number_literal.reader,
    ),
    Dispatcher(
        applicable_types={
            "character_literal",
            "string_literal",
            "verbatim_string_literal",
        },
        syntax_reader=common_string_literal.reader,
    ),
    Dispatcher(
        applicable_types={
            "while_statement",
        },
        syntax_reader=common_while_statement.reader,
    ),
)
