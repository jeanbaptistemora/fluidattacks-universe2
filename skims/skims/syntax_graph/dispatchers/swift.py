from syntax_graph.syntax_readers.swift import (
    class_declaration as swift_class_declaration,
    function_declaration as swift_function_declaration,
    identifier as swift_identifier,
    if_statement as swift_if_statement,
    source_file as swift_source_file,
)
from syntax_graph.types import (
    Dispatcher,
    Dispatchers,
)

SWIFT_DISPATCHERS: Dispatchers = (
    Dispatcher(
        applicable_types={
            "class_declaration",
        },
        syntax_reader=swift_class_declaration.reader,
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
            "source_file",
        },
        syntax_reader=swift_source_file.reader,
    ),
)
