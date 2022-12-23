from syntax_graph.syntax_readers.kotlin import (
    class_body as kotlin_class_body,
    class_declaration as kotlin_class_declaration,
    import_declaration as kotlin_import_declaration,
    number_literal as kotlin_number_literal,
    program as kotlin_program,
    variable_declaration as kotlin_variable_declaration,
)
from syntax_graph.types import (
    Dispatcher,
    Dispatchers,
)

KOTLIN_DISPATCHERS: Dispatchers = (
    Dispatcher(
        applicable_types={
            "import_header",
            "package_header",
        },
        syntax_reader=kotlin_import_declaration.reader,
    ),
    Dispatcher(
        applicable_types={
            "source_file",
        },
        syntax_reader=kotlin_program.reader,
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
        applicable_types={
            "property_declaration",
        },
        syntax_reader=kotlin_variable_declaration.reader,
    ),
    Dispatcher(
        applicable_types={
            "class_body",
            "constructor_body",
            "interface_body",
        },
        syntax_reader=kotlin_class_body.reader,
    ),
    Dispatcher(
        applicable_types={
            "class_declaration",
        },
        syntax_reader=kotlin_class_declaration.reader,
    ),
)
