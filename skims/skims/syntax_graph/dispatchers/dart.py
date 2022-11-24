from syntax_graph.syntax_readers.dart import (
    annotation as dart_annotation,
    argument as dart_argument,
    argument_part as dart_argument_part,
    arguments as dart_arguments,
    assignable_expression as dart_assignable_expression,
    assignable_selector as dart_assignable_selector,
    assignment_expression as dart_assignment_expression,
    await_expression as dart_await_expression,
    binary_expression as dart_binary_expression,
    boolean_literal as dart_boolean_literal,
    break_statement as dart_break_statement,
    class_body as dart_class_body,
    class_definition as dart_class_definition,
    comment as dart_comment,
    conditional_expression as dart_conditional_expression,
    constant_constructor_signature as dart_constant_constructor_signature,
    continue_statement as dart_continue_statement,
    declaration_block as dart_declaration_block,
    enum_declaration as dart_enum_declaration,
    execution_block as dart_execution_block,
    expression_statement as dart_expression_statement,
    extension_declaration as dart_extension_declaration,
    finally_clause as dart_finally_clause,
    for_statement as dart_for_statement,
    function_body as dart_function_body,
    function_declaration as dart_function_declaration,
    function_expression as dart_function_expression,
    function_signature as dart_function_signature,
    getter_signature as dart_getter_signature,
    identifier as dart_identifier,
    identifier_list as dart_identifier_list,
    if_statement as dart_if_statement,
    import_or_export as dart_import_or_export,
    initialized_identifier as dart_initialized_identifier,
    lambda_expression as dart_lambda_expression,
    library_name as dart_library_name,
    method_declaration as dart_method_declaration,
    method_signature as dart_method_signature,
    new_expression as dart_new_expression,
    number_literal as dart_number_literal,
    operator as dart_operator,
    operator_signature as dart_operator_signature,
    parameter as dart_parameter,
    parameter_list as dart_parameter_list,
    program as dart_program,
    reserved_word as dart_reserved_word,
    return_statement as dart_return_statement,
    selector as dart_selector,
    string_literal as dart_string_literal,
    switch_body as dart_switch_body,
    switch_statement as dart_switch_statement,
    throw_statement as dart_throw_statement,
    try_statement as dart_try_statement,
    unary_expression as dart_unary_expression,
    update_expression as dart_update_expression,
    variable_declaration as dart_variable_declaration,
    while_statement as dart_while_statement,
)
from syntax_graph.types import (
    Dispatcher,
    Dispatchers,
)

DART_DISPATCHERS: Dispatchers = (
    Dispatcher(
        applicable_types={
            "marker_annotation",
        },
        syntax_reader=dart_annotation.reader,
    ),
    Dispatcher(
        applicable_types={
            "argument",
            "named_argument",
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
            "assignable_expression",
        },
        syntax_reader=dart_assignable_expression.reader,
    ),
    Dispatcher(
        applicable_types={
            "conditional_assignable_selector",
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
            "await_expression",
        },
        syntax_reader=dart_await_expression.reader,
    ),
    Dispatcher(
        applicable_types={
            "additive_expression",
            "equality_expression",
            "logical_and_expression",
            "logical_or_expression",
            "multiplicative_expression",
            "relational_expression",
            "type_test_expression",
        },
        syntax_reader=dart_binary_expression.reader,
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
            "break_statement",
        },
        syntax_reader=dart_break_statement.reader,
    ),
    Dispatcher(
        applicable_types={
            "class_body",
        },
        syntax_reader=dart_class_body.reader,
    ),
    Dispatcher(
        applicable_types={
            "class_definition",
        },
        syntax_reader=dart_class_definition.reader,
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
            "conditional_expression",
        },
        syntax_reader=dart_conditional_expression.reader,
    ),
    Dispatcher(
        applicable_types={
            "constant_constructor_signature",
        },
        syntax_reader=dart_constant_constructor_signature.reader,
    ),
    Dispatcher(
        applicable_types={
            "continue_statement",
        },
        syntax_reader=dart_continue_statement.reader,
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
            "enum_declaration",
        },
        syntax_reader=dart_enum_declaration.reader,
    ),
    Dispatcher(
        applicable_types={
            "assertion",
            "assert_statement",
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
            "finally_clause",
        },
        syntax_reader=dart_finally_clause.reader,
    ),
    Dispatcher(
        applicable_types={
            "for_statement",
        },
        syntax_reader=dart_for_statement.reader,
    ),
    Dispatcher(
        applicable_types={
            "function_body",
            "function_expression_body",
        },
        syntax_reader=dart_function_body.reader,
    ),
    Dispatcher(
        applicable_types={
            "function_expression",
        },
        syntax_reader=dart_function_expression.reader,
    ),
    Dispatcher(
        applicable_types={
            "local_function_declaration",
        },
        syntax_reader=dart_function_declaration.reader,
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
            "initialized_identifier_list",
            "static_final_declaration_list",
        },
        syntax_reader=dart_identifier_list.reader,
    ),
    Dispatcher(
        applicable_types={
            "if_statement",
        },
        syntax_reader=dart_if_statement.reader,
    ),
    Dispatcher(
        applicable_types={
            "initialized_identifier",
            "static_final_declaration",
        },
        syntax_reader=dart_initialized_identifier.reader,
    ),
    Dispatcher(
        applicable_types={
            "import_or_export",
        },
        syntax_reader=dart_import_or_export.reader,
    ),
    Dispatcher(
        applicable_types={
            "lambda_expression",
        },
        syntax_reader=dart_lambda_expression.reader,
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
            "decimal_floating_point_literal",
            "decimal_integer_literal",
        },
        syntax_reader=dart_number_literal.reader,
    ),
    Dispatcher(
        applicable_types={
            "||",
            "&&",
            "additive_operator",
            "equality_operator",
            "increment_operator",
            "is_operator",
            "multiplicative_operator",
            "operator",
            "prefix_operator",
            "postfix_operator",
            "relational_operator",
        },
        syntax_reader=dart_operator.reader,
    ),
    Dispatcher(
        applicable_types={
            "operator_signature",
        },
        syntax_reader=dart_operator_signature.reader,
    ),
    Dispatcher(
        applicable_types={
            "constructor_param",
            "formal_parameter",
        },
        syntax_reader=dart_parameter.reader,
    ),
    Dispatcher(
        applicable_types={
            "formal_parameter_list",
            "optional_formal_parameters",
        },
        syntax_reader=dart_parameter_list.reader,
    ),
    Dispatcher(
        applicable_types={
            "return_statement",
            "yield_statement",
        },
        syntax_reader=dart_return_statement.reader,
    ),
    Dispatcher(
        applicable_types={
            "program",
        },
        syntax_reader=dart_program.reader,
    ),
    Dispatcher(
        applicable_types={
            "const_builtin",
            "get",
            "inferred_type",
            "final_builtin",
            "late",
            "null_literal",
            "static",
            "sync*",
            "this",
            "type_identifier",
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
            "list_literal",
            "set_or_map_literal",
            "string_literal",
        },
        syntax_reader=dart_string_literal.reader,
    ),
    Dispatcher(
        applicable_types={
            "switch_block",
        },
        syntax_reader=dart_switch_body.reader,
    ),
    Dispatcher(
        applicable_types={
            "switch_statement",
        },
        syntax_reader=dart_switch_statement.reader,
    ),
    Dispatcher(
        applicable_types={
            "throw_expression",
        },
        syntax_reader=dart_throw_statement.reader,
    ),
    Dispatcher(
        applicable_types={
            "try_statement",
        },
        syntax_reader=dart_try_statement.reader,
    ),
    Dispatcher(
        applicable_types={
            "unary_expression",
        },
        syntax_reader=dart_unary_expression.reader,
    ),
    Dispatcher(
        applicable_types={
            "postfix_expression",
        },
        syntax_reader=dart_update_expression.reader,
    ),
    Dispatcher(
        applicable_types={
            "local_variable_declaration",
        },
        syntax_reader=dart_variable_declaration.reader,
    ),
    Dispatcher(
        applicable_types={
            "do_statement",
            "while_statement",
        },
        syntax_reader=dart_while_statement.reader,
    ),
)
