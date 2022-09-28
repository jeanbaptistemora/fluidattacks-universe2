# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from syntax_graph.syntax_readers.javascript import (
    array as javascript_array,
    assignment_expression as javascript_assignment_expression,
    comment as javascript_comment,
    expression_statement as javascript_expression_statement,
    identifier as javascript_identifier,
    program as javascript_program,
    string_literal as javascript_string_literal,
)
from syntax_graph.syntax_readers.typescript import (
    array_type as typescript_array_type,
    type_annotation as typescript_type_annotation,
    variable_declaration as typescript_variable_declaration,
    variable_declarator as typescript_variable_declarator,
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
            "array_type",
        },
        syntax_reader=typescript_array_type.reader,
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
            "identifier",
        },
        syntax_reader=javascript_identifier.reader,
    ),
    Dispatcher(
        applicable_types={
            "program",
        },
        syntax_reader=javascript_program.reader,
    ),
    Dispatcher(
        applicable_types={
            "string",
        },
        syntax_reader=javascript_string_literal.reader,
    ),
    Dispatcher(
        applicable_types={
            "type_annotation",
        },
        syntax_reader=typescript_type_annotation.reader,
    ),
    Dispatcher(
        applicable_types={
            "variable_declaration",
        },
        syntax_reader=typescript_variable_declaration.reader,
    ),
    Dispatcher(
        applicable_types={
            "variable_declarator",
        },
        syntax_reader=typescript_variable_declarator.reader,
    ),
)
