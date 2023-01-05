from sast_syntax_readers.common import (
    identifier as common_identifier,
    literal as common_literal,
)
from sast_syntax_readers.java import (
    this as java_this,
)
from sast_syntax_readers.types import (
    Dispatcher,
    Dispatchers,
)

KOTLIN_DISPATCHERS: Dispatchers = (
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
