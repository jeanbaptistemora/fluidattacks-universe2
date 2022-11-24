from sast_syntax_readers.common import (
    identifier as common_identifier,
    literal as common_literal,
)
from sast_syntax_readers.java import (
    this as java_this,
)
from sast_syntax_readers.kotlin import (
    assignment as kotlin_assignment,
    call_expression as kotlin_call_expression,
    if_expression as kotlin_if_expression,
    navigation_expression as kotlin_navigation_expression,
    object_declaration as kotlin_object_declaration,
    property_declaration as kotlin_property_declaration,
)
from sast_syntax_readers.types import (
    Dispatcher,
    Dispatchers,
)

KOTLIN_DISPATCHERS: Dispatchers = (
    Dispatcher(
        applicable_node_label_types={
            "assignment",
        },
        syntax_reader=kotlin_assignment.reader,
    ),
    Dispatcher(
        applicable_node_label_types={
            "call_expression",
        },
        syntax_reader=kotlin_call_expression.reader,
    ),
    Dispatcher(
        applicable_node_label_types={
            "class_declaration",
            "function_declaration",
        },
        syntax_reader=kotlin_object_declaration.reader,
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
            "if_expression",
        },
        syntax_reader=kotlin_if_expression.reader,
    ),
    Dispatcher(
        applicable_node_label_types={
            "navigation_expression",
        },
        syntax_reader=kotlin_navigation_expression.reader,
    ),
    Dispatcher(
        applicable_node_label_types={
            "property_declaration",
        },
        syntax_reader=kotlin_property_declaration.reader,
    ),
    Dispatcher(
        applicable_node_label_types={
            "this",
            "this_expression",
        },
        syntax_reader=java_this.reader,
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
)
