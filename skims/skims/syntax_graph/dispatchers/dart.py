# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from syntax_graph.syntax_readers.dart import (
    argument as dart_argument,
    argument_part as dart_argument_part,
    arguments as dart_arguments,
    assignable_selector as dart_assignable_selector,
    assignment_expression as dart_assignment_expression,
    boolean_literal as dart_boolean_literal,
    comment as dart_comment,
    conditional_expression as dart_conditional_expression,
    declaration_block as dart_declaration_block,
    execution_block as dart_execution_block,
    expression_statement as dart_expression_statement,
    extension_declaration as dart_extension_declaration,
    function_body as dart_function_body,
    function_signature as dart_function_signature,
    getter_signature as dart_getter_signature,
    identifier as dart_identifier,
    import_or_export as dart_import_or_export,
    library_name as dart_library_name,
    method_declaration as dart_method_declaration,
    method_signature as dart_method_signature,
    new_expression as dart_new_expression,
    number_literal as dart_number_literal,
    operator as dart_operator,
    parameter as dart_parameter,
    parameter_list as dart_parameter_list,
    program as dart_program,
    reserved_word as dart_reserved_word,
    selector as dart_selector,
    string_literal as dart_string_literal,
    type_identifier as dart_type_identifier,
    variable_declaration as dart_variable_declaration,
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
        syntax_reader=dart_assignable_selector.reader,
    ),
    Dispatcher(
        applicable_types={
            "assignment_expression",
        },
        syntax_reader=dart_assignment_expression.reader,
    ),
    Dispatcher(
        applicable_types={
            "false",
            "true",
        },
        syntax_reader=dart_boolean_literal.reader,
    ),
    Dispatcher(
        applicable_types={
            "conditional_expression",
        },
        syntax_reader=dart_conditional_expression.reader,
    ),
    Dispatcher(
        applicable_types={
            "comment",
            "documentation_comment",
        },
        syntax_reader=dart_comment.reader,
    ),
    Dispatcher(
        applicable_types={
            "declaration",
        },
        syntax_reader=dart_declaration_block.reader,
    ),
    Dispatcher(
        applicable_types={
            "block",
            "extension_body",
        },
        syntax_reader=dart_execution_block.reader,
    ),
    Dispatcher(
        applicable_types={
            "decimal_integer_literal",
        },
        syntax_reader=dart_number_literal.reader,
    ),
    Dispatcher(
        applicable_types={
            "additive_expression",
            "equality_expression",
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
            "getter_signature",
        },
        syntax_reader=dart_getter_signature.reader,
    ),
    Dispatcher(
        applicable_types={
            "identifier",
        },
        syntax_reader=dart_identifier.reader,
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
        syntax_reader=dart_library_name.reader,
    ),
    Dispatcher(
        applicable_types={
            "constructor_signature",
        },
        syntax_reader=dart_method_declaration.reader,
    ),
    Dispatcher(
        applicable_types={
            "method_signature",
        },
        syntax_reader=dart_method_signature.reader,
    ),
    Dispatcher(
        applicable_types={
            "new_expression",
        },
        syntax_reader=dart_new_expression.reader,
    ),
    Dispatcher(
        applicable_types={
            "additive_operator",
            "equality_operator",
        },
        syntax_reader=dart_operator.reader,
    ),
    Dispatcher(
        applicable_types={
            "formal_parameter",
        },
        syntax_reader=dart_parameter.reader,
    ),
    Dispatcher(
        applicable_types={
            "formal_parameter_list",
        },
        syntax_reader=dart_parameter_list.reader,
    ),
    Dispatcher(
        applicable_types={
            "program",
        },
        syntax_reader=dart_program.reader,
    ),
    Dispatcher(
        applicable_types={
            "get",
            "this",
        },
        syntax_reader=dart_reserved_word.reader,
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
        syntax_reader=dart_string_literal.reader,
    ),
    Dispatcher(
        applicable_types={
            "local_variable_declaration",
        },
        syntax_reader=dart_variable_declaration.reader,
    ),
)
