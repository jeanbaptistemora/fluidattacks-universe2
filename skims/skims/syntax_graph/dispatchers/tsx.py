# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from syntax_graph.syntax_readers.common import (
    array as common_array,
    assignment_expression as common_assignment_expression,
    comment as common_comment,
    expression_statement as common_expression_statement,
    identifier as common_identifier,
    program as common_program,
    string_literal as common_string_literal,
    variable_declaration as common_variable_declaration,
    variable_declarator as common_variable_declarator,
)
from syntax_graph.syntax_readers.tsx import (  # type: ignore
    array_type as tsx_array_type,
    type_annotation as tsx_type_annotation,
)
from syntax_graph.types import (
    Dispatcher,
    Dispatchers,
)

TSX_DISPATCHERS: Dispatchers = (
    Dispatcher(
        applicable_types={
            "array",
        },
        syntax_reader=common_array.reader,
    ),
    Dispatcher(
        applicable_types={
            "array_type",
        },
        syntax_reader=tsx_array_type.reader,
    ),
    Dispatcher(
        applicable_types={
            "comment",
        },
        syntax_reader=common_comment.reader,
    ),
    Dispatcher(
        applicable_types={
            "expression_statement",
        },
        syntax_reader=common_expression_statement.reader,
    ),
    Dispatcher(
        applicable_types={
            "identifier",
        },
        syntax_reader=common_identifier.reader,
    ),
    Dispatcher(
        applicable_types={
            "program",
        },
        syntax_reader=common_program.reader,
    ),
    Dispatcher(
        applicable_types={
            "variable_declaration",
        },
        syntax_reader=common_variable_declaration.reader,
    ),
    Dispatcher(
        applicable_types={
            "variable_declarator",
        },
        syntax_reader=common_variable_declarator.reader,
    ),
    Dispatcher(
        applicable_types={
            "assignment_expression",
        },
        syntax_reader=common_assignment_expression.reader,
    ),
    Dispatcher(
        applicable_types={
            "string",
        },
        syntax_reader=common_string_literal.reader,
    ),
    Dispatcher(
        applicable_types={
            "type_annotation",
        },
        syntax_reader=tsx_type_annotation.reader,
    ),
)
