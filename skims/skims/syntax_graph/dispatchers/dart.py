# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from syntax_graph.syntax_readers.common import (
    boolean_literal as common_boolean_literal,
    execution_block as common_execution_block,
    identifier as common_identifier,
    library_name as common_library_name,
    number_literal as common_number_literal,
    parameter_list as common_parameter_list,
    program as common_program,
    string_literal as common_string_literal,
)
from syntax_graph.syntax_readers.dart import (
    argument as dart_argument,
    argument_part as dart_argument_part,
    arguments as dart_arguments,
    expression_statement as dart_expression_statement,
    extension_declaration as dart_extension_declaration,
    function_body as dart_function_body,
    function_signature as dart_function_signature,
    import_or_export as dart_import_or_export,
    selector as dart_selector,
    type_identifier as dart_type_identifier,
)
from syntax_graph.types import (
    Dispatcher,
    Dispatchers,
)

DART_DISPATCHERS: Dispatchers = (
    Dispatcher(
        applicable_types={
            "argument",
        },
        syntax_reader=dart_argument.reader,
    ),
    Dispatcher(
        applicable_types={
            "argument_part",
        },
        syntax_reader=dart_argument_part.reader,
    ),
    Dispatcher(
        applicable_types={
            "arguments",
        },
        syntax_reader=dart_arguments.reader,
    ),
    Dispatcher(
        applicable_types={
            "unconditional_assignable_selector",
        },
        syntax_reader=dart_arguments.reader,
    ),
    Dispatcher(
        applicable_types={
            "block",
            "extension_body",
        },
        syntax_reader=common_execution_block.reader,
    ),
    Dispatcher(
        applicable_types={
            "false",
            "true",
        },
        syntax_reader=common_boolean_literal.reader,
    ),
    Dispatcher(
        applicable_types={
            "decimal_integer_literal",
        },
        syntax_reader=common_number_literal.reader,
    ),
    Dispatcher(
        applicable_types={
            "expression_statement",
        },
        syntax_reader=dart_expression_statement.reader,
    ),
    Dispatcher(
        applicable_types={
            "extension_declaration",
        },
        syntax_reader=dart_extension_declaration.reader,
    ),
    Dispatcher(
        applicable_types={
            "function_body",
        },
        syntax_reader=dart_function_body.reader,
    ),
    Dispatcher(
        applicable_types={
            "function_signature",
        },
        syntax_reader=dart_function_signature.reader,
    ),
    Dispatcher(
        applicable_types={
            "identifier",
        },
        syntax_reader=common_identifier.reader,
    ),
    Dispatcher(
        applicable_types={
            "import_or_export",
        },
        syntax_reader=dart_import_or_export.reader,
    ),
    Dispatcher(
        applicable_types={
            "library_name",
        },
        syntax_reader=common_library_name.reader,
    ),
    Dispatcher(
        applicable_types={
            "formal_parameter_list",
        },
        syntax_reader=common_parameter_list.reader,
    ),
    Dispatcher(
        applicable_types={
            "program",
        },
        syntax_reader=common_program.reader,
    ),
    Dispatcher(
        applicable_types={
            "selector",
        },
        syntax_reader=dart_selector.reader,
    ),
    Dispatcher(
        applicable_types={
            "type_identifier",
        },
        syntax_reader=dart_type_identifier.reader,
    ),
    Dispatcher(
        applicable_types={
            "string_literal",
        },
        syntax_reader=common_string_literal.reader,
    ),
)
