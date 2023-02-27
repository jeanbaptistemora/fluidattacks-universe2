from syntax_graph.syntax_readers.swift import (
    assignment as swift_assignment,
    call_expression as swift_call_expresion,
    class_body as swift_class_body,
    class_declaration as swift_class_declaration,
    comment as swift_comment,
    expression_statement as swift_expression_statement,
    function_body as swift_function_body,
    function_declaration as swift_function_declaration,
    identifier as swift_identifier,
    if_statement as swift_if_statement,
    import_statement as swift_import_statement,
    navigation_expression as swift_navigation_expression,
    navigation_suffix as swift_navigation_suffix,
    parameter as swift_parameter,
    prefix_expression as swift_prefix_expression,
    property_declaration as swift_property_declaration,
    source_file as swift_source_file,
    string_literal as swift_string_literal,
    try_expression as swift_try_expression,
    value_argument as swift_value_argument,
    value_arguments as swift_argument_list,
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
            "value_arguments",
        },
        syntax_reader=swift_argument_list.reader,
    ),
    Dispatcher(
        applicable_types={
            "call_expression",
        },
        syntax_reader=swift_call_expresion.reader,
    ),
    Dispatcher(
        applicable_types={
            "class_body",
        },
        syntax_reader=swift_class_body.reader,
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
            "directly_assignable_expression",
        },
        syntax_reader=swift_expression_statement.reader,
    ),
    Dispatcher(
        applicable_types={
            "function_body",
        },
        syntax_reader=swift_function_body.reader,
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
            "import_declaration",
        },
        syntax_reader=swift_import_statement.reader,
    ),
    Dispatcher(
        applicable_types={
            "navigation_expression",
        },
        syntax_reader=swift_navigation_expression.reader,
    ),
    Dispatcher(
        applicable_types={
            "navigation_suffix",
        },
        syntax_reader=swift_navigation_suffix.reader,
    ),
    Dispatcher(
        applicable_types={
            "parameter",
        },
        syntax_reader=swift_parameter.reader,
    ),
    Dispatcher(
        applicable_types={
            "prefix_expression",
        },
        syntax_reader=swift_prefix_expression.reader,
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
            "line_string_literal",
        },
        syntax_reader=swift_string_literal.reader,
    ),
    Dispatcher(
        applicable_types={
            "try_expression",
        },
        syntax_reader=swift_try_expression.reader,
    ),
    Dispatcher(
        applicable_types={
            "value_argument",
        },
        syntax_reader=swift_value_argument.reader,
    ),
    Dispatcher(
        applicable_types={
            "while_statement",
        },
        syntax_reader=swift_while_statement.reader,
    ),
)
