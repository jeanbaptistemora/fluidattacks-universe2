from syntax_graph.syntax_readers.swift import (
    assignment as swift_assignment,
    class_declaration as swift_class_declaration,
    comment as swift_comment,
    function_declaration as swift_function_declaration,
    identifier as swift_identifier,
    if_statement as swift_if_statement,
    parameter as swift_parameter,
    property_declaration as swift_property_declaration,
    source_file as swift_source_file,
    while_statement as swift_while_statement,
)
from syntax_graph.types import (
    Dispatcher,
    Dispatchers,
)

SWIFT_DISPATCHERS: Dispatchers = (
    Dispatcher(
        applicable_types={
            "assignment",
        },
        syntax_reader=swift_assignment.reader,
    ),
    Dispatcher(
        applicable_types={
            "class_declaration",
        },
        syntax_reader=swift_class_declaration.reader,
    ),
    Dispatcher(
        applicable_types={"comment", "multiline_comment"},
        syntax_reader=swift_comment.reader,
    ),
    Dispatcher(
        applicable_types={
            "function_declaration",
        },
        syntax_reader=swift_function_declaration.reader,
    ),
    Dispatcher(
        applicable_types={
            "identifier",
            "postfix_expression",
            "simple_identifier",
        },
        syntax_reader=swift_identifier.reader,
    ),
    Dispatcher(
        applicable_types={
            "if_statement",
        },
        syntax_reader=swift_if_statement.reader,
    ),
    Dispatcher(
        applicable_types={
            "parameter",
        },
        syntax_reader=swift_parameter.reader,
    ),
    Dispatcher(
        applicable_types={
            "property_declaration",
        },
        syntax_reader=swift_property_declaration.reader,
    ),
    Dispatcher(
        applicable_types={
            "source_file",
        },
        syntax_reader=swift_source_file.reader,
    ),
    Dispatcher(
        applicable_types={
            "while_statement",
        },
        syntax_reader=swift_while_statement.reader,
    ),
)
