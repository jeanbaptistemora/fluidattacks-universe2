from sast_syntax_readers.common import (
    attribute_access as common_attribute_access,
    binary_expression as common_binary_expression,
    identifier as common_identifier,
    if_statement as common_if_statement,
    literal as common_literal,
    noop as common_noop,
    parenthesized_expression as common_parenthesized_expression,
    unary_expression as common_unary_expression,
)
from sast_syntax_readers.types import (
    Dispatcher,
    Dispatchers,
)

GO_DISPATCHERS: Dispatchers = (
    Dispatcher(
        applicable_node_label_types={
            "binary_expression",
        },
        syntax_reader=common_binary_expression.reader,
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
            "if_statement",
        },
        syntax_reader=common_if_statement.reader,
    ),
    Dispatcher(
        applicable_node_label_types={
            "parenthesized_expression",
        },
        syntax_reader=common_parenthesized_expression.reader,
    ),
    Dispatcher(
        applicable_node_label_types={
            "selector_expression",
        },
        syntax_reader=common_attribute_access.reader,
    ),
    Dispatcher(
        applicable_node_label_types={
            "unary_expression",
        },
        syntax_reader=common_unary_expression.reader,
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
