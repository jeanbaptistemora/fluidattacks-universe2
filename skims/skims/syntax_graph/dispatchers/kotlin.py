from syntax_graph.syntax_readers.kotlin import (
    assignment_expression as kotlin_assignment_expression,
    catch_clause as kotlin_catch_clause,
    class_body as kotlin_class_body,
    class_declaration as kotlin_class_declaration,
    declaration_block as kotlin_declaration_block,
    finally_clause as kotlin_finally_clause,
    for_statement as kotlin_for_statement,
    identifier as kotlin_identifier,
    if_statement as kotlin_if_statement,
    import_declaration as kotlin_import_declaration,
    jump_statement as kotlin_jump_statement,
    member_access_expression as kotlin_member_access_expression,
    method_declaration as kotlin_method_declaration,
    method_invocation as kotlin_method_invocation,
    number_literal as kotlin_number_literal,
    parenthesized_expression as kotlin_parenthesized_expression,
    program as kotlin_program,
    try_statement as kotlin_try_statement,
    variable_declaration as kotlin_variable_declaration,
    while_statement as kotlin_while_statement,
)
from syntax_graph.types import (
    Dispatcher,
    Dispatchers,
)

KOTLIN_DISPATCHERS: Dispatchers = (
    Dispatcher(
        applicable_types={
            "assignment",
        },
        syntax_reader=kotlin_assignment_expression.reader,
    ),
    Dispatcher(
        applicable_types={
            "catch_block",
        },
        syntax_reader=kotlin_catch_clause.reader,
    ),
    Dispatcher(
        applicable_types={
            "class_body",
            "statements",
        },
        syntax_reader=kotlin_class_body.reader,
    ),
    Dispatcher(
        applicable_types={
            "class_declaration",
        },
        syntax_reader=kotlin_class_declaration.reader,
    ),
    Dispatcher(
        applicable_types={
            "function_body",
            "control_structure_body",
        },
        syntax_reader=kotlin_declaration_block.reader,
    ),
    Dispatcher(
        applicable_types={
            "finally_block",
        },
        syntax_reader=kotlin_finally_clause.reader,
    ),
    Dispatcher(
        applicable_types={
            "for_statement",
        },
        syntax_reader=kotlin_for_statement.reader,
    ),
    Dispatcher(
        applicable_types={
            "identifier",
            "simple_identifier",
            "type_identifier",
        },
        syntax_reader=kotlin_identifier.reader,
    ),
    Dispatcher(
        applicable_types={
            "if_expression",
        },
        syntax_reader=kotlin_if_statement.reader,
    ),
    Dispatcher(
        applicable_types={
            "import_header",
            "package_header",
        },
        syntax_reader=kotlin_import_declaration.reader,
    ),
    Dispatcher(
        applicable_types={
            "jump_expression",
        },
        syntax_reader=kotlin_jump_statement.reader,
    ),
    Dispatcher(
        applicable_types={
            "navigation_expression",
        },
        syntax_reader=kotlin_member_access_expression.reader,
    ),
    Dispatcher(
        applicable_types={
            "constructor_declaration",
            "function_declaration",
        },
        syntax_reader=kotlin_method_declaration.reader,
    ),
    Dispatcher(
        applicable_types={
            "call_expression",
        },
        syntax_reader=kotlin_method_invocation.reader,
    ),
    Dispatcher(
        applicable_types={
            "decimal_integer_literal",
            "integer_literal",
            "real_literal",
        },
        syntax_reader=kotlin_number_literal.reader,
    ),
    Dispatcher(
        applicable_types={"parenthesized_expression"},
        syntax_reader=kotlin_parenthesized_expression.reader,
    ),
    Dispatcher(
        applicable_types={
            "source_file",
        },
        syntax_reader=kotlin_program.reader,
    ),
    Dispatcher(
        applicable_types={
            "try_catch_expression",
        },
        syntax_reader=kotlin_try_statement.reader,
    ),
    Dispatcher(
        applicable_types={
            "property_declaration",
        },
        syntax_reader=kotlin_variable_declaration.reader,
    ),
    Dispatcher(
        applicable_types={
            "while_statement",
        },
        syntax_reader=kotlin_while_statement.reader,
    ),
)
