# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from syntax_graph.syntax_readers.javascript import (
    array as javascript_array,
    assignment_expression as javascript_assignment_expression,
    boolean_literal as javascript_boolean_literal,
    comment as javascript_comment,
    expression_statement as javascript_expression_statement,
    identifier as javascript_identifier,
    number_literal as javascript_number_literal,
    object as javascript_object,
    pair as javascript_pair,
    program as javascript_program,
    string_literal as javascript_string_literal,
    variable_declaration as javascript_variable_declaration,
)
from syntax_graph.syntax_readers.typescript import (
    as_expression as typescript_as_expression,
    interface_declaration as typescript_interface_declaration,
    intersection_type as typescript_intersection_type,
    property_signature as typescript_property_signature,
    type_alias_declaration as typescript_type_alias_declaration,
)
from syntax_graph.types import (
    Dispatcher,
    Dispatchers,
)

TYPESCRIPT_DISPATCHERS: Dispatchers = (
    Dispatcher(
        applicable_types={
            "array",
        },
        syntax_reader=javascript_array.reader,
    ),
    Dispatcher(
        applicable_types={
            "as_expression",
        },
        syntax_reader=typescript_as_expression.reader,
    ),
    Dispatcher(
        applicable_types={
            "assignment_expression",
        },
        syntax_reader=javascript_assignment_expression.reader,
    ),
    Dispatcher(
        applicable_types={
            "comment",
        },
        syntax_reader=javascript_comment.reader,
    ),
    Dispatcher(
        applicable_types={
            "expression_statement",
        },
        syntax_reader=javascript_expression_statement.reader,
    ),
    Dispatcher(
        applicable_types={
            "false",
            "true",
        },
        syntax_reader=javascript_boolean_literal.reader,
    ),
    Dispatcher(
        applicable_types={
            "identifier",
            "property_identifier",
            "type_identifier",
        },
        syntax_reader=javascript_identifier.reader,
    ),
    Dispatcher(
        applicable_types={
            "interface_declaration",
        },
        syntax_reader=typescript_interface_declaration.reader,
    ),
    Dispatcher(
        applicable_types={
            "intersection_type",
        },
        syntax_reader=typescript_intersection_type.reader,
    ),
    Dispatcher(
        applicable_types={
            "number",
        },
        syntax_reader=javascript_number_literal.reader,
    ),
    Dispatcher(
        applicable_types={
            "object",
            "object_type",
        },
        syntax_reader=javascript_object.reader,
    ),
    Dispatcher(
        applicable_types={
            "pair",
        },
        syntax_reader=javascript_pair.reader,
    ),
    Dispatcher(
        applicable_types={
            "program",
        },
        syntax_reader=javascript_program.reader,
    ),
    Dispatcher(
        applicable_types={
            "property_signature",
        },
        syntax_reader=typescript_property_signature.reader,
    ),
    Dispatcher(
        applicable_types={
            "string",
        },
        syntax_reader=javascript_string_literal.reader,
    ),
    Dispatcher(
        applicable_types={
            "type_alias_declaration",
        },
        syntax_reader=typescript_type_alias_declaration.reader,
    ),
    Dispatcher(
        applicable_types={
            "lexical_declaration",
            "variable_declaration",
        },
        syntax_reader=javascript_variable_declaration.reader,
    ),
)
