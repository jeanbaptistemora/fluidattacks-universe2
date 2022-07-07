from syntax_graph.syntax_readers.common import (
    binary_expression as common_binary_expression,
    boolean_literal as common_boolean_literal,
    catch_clause as common_catch_clause,
    catch_declaration as common_catch_declaration,
    class_declaration as common_class_declaration,
    comment as common_comment,
    conditional_expression as common_conditional_expression,
    declaration_block as common_declaration_block,
    do_statement as common_do_statement,
    execution_block as common_execution_block,
    expression_statement as common_expression_statement,
    identifier as common_identifier,
    interpolation as common_interpolation,
    method_declaration as common_method_declaration,
    null_literal as common_null_literal,
    number_literal as common_number_literal,
    parameter as common_parameter,
    parenthesized_expression as common_parenthesized_expression,
    string_literal as common_string_literal,
    try_statement as common_try_statement,
)
from syntax_graph.syntax_readers.java import (
    argument_list as java_argument_list,
    assignment_expression as java_assignment_expression,
    class_body as java_class_body,
    field_access as java_field_access,
    field_declaration as java_field_declaration,
    import_declaration as java_import_declaration,
    interface_declaration as java_interface_declaration,
    method_invocation as java_method_invocation,
    package_declaration as java_package_declaration,
    parameter_list as java_parameter_list,
    program as java_program,
    update_expression as java_update_expression,
    variable_declaration as java_variable_declaration,
    variable_declarator as java_variable_declarator,
    while_statement as java_while_statement,
)
from syntax_graph.types import (
    Dispatcher,
    Dispatchers,
)

JAVA_DISPATCHERS: Dispatchers = (
    Dispatcher(
        applicable_types={
            "argument_list",
        },
        syntax_reader=java_argument_list.reader,
    ),
    Dispatcher(
        applicable_types={
            "assignment_expression",
        },
        syntax_reader=java_assignment_expression.reader,
    ),
    Dispatcher(
        applicable_types={
            "binary_expression",
        },
        syntax_reader=common_binary_expression.reader,
    ),
    Dispatcher(
        applicable_types={
            "boolean_literal",
        },
        syntax_reader=common_boolean_literal.reader,
    ),
    Dispatcher(
        applicable_types={
            "catch_clause",
        },
        syntax_reader=common_catch_clause.reader,
    ),
    Dispatcher(
        applicable_types={
            "catch_declaration",
        },
        syntax_reader=common_catch_declaration.reader,
    ),
    Dispatcher(
        applicable_types={
            "class_body",
            "constructor_body",
            "interface_body",
        },
        syntax_reader=java_class_body.reader,
    ),
    Dispatcher(
        applicable_types={
            "class_declaration",
        },
        syntax_reader=common_class_declaration.reader,
    ),
    Dispatcher(
        applicable_types={
            "comment",
        },
        syntax_reader=common_comment.reader,
    ),
    Dispatcher(
        applicable_types={
            "conditional_expression",
        },
        syntax_reader=common_conditional_expression.reader,
    ),
    Dispatcher(
        applicable_types={
            "declaration_list",
        },
        syntax_reader=common_declaration_block.reader,
    ),
    Dispatcher(
        applicable_types={
            "do_statement",
        },
        syntax_reader=common_do_statement.reader,
    ),
    Dispatcher(
        applicable_types={
            "block",
        },
        syntax_reader=common_execution_block.reader,
    ),
    Dispatcher(
        applicable_types={
            "expression_statement",
        },
        syntax_reader=common_expression_statement.reader,
    ),
    Dispatcher(
        applicable_types={
            "field_access",
        },
        syntax_reader=java_field_access.reader,
    ),
    Dispatcher(
        applicable_types={
            "field_declaration",
        },
        syntax_reader=java_field_declaration.reader,
    ),
    Dispatcher(
        applicable_types={
            "identifier",
        },
        syntax_reader=common_identifier.reader,
    ),
    Dispatcher(
        applicable_types={
            "import_declaration",
        },
        syntax_reader=java_import_declaration.reader,
    ),
    Dispatcher(
        applicable_types={
            "interface_declaration",
        },
        syntax_reader=java_interface_declaration.reader,
    ),
    Dispatcher(
        applicable_types={
            "interpolation",
        },
        syntax_reader=common_interpolation.reader,
    ),
    Dispatcher(
        applicable_types={
            "constructor_declaration",
            "method_declaration",
        },
        syntax_reader=common_method_declaration.reader,
    ),
    Dispatcher(
        applicable_types={
            "method_invocation",
        },
        syntax_reader=java_method_invocation.reader,
    ),
    Dispatcher(
        applicable_types={
            "null_literal",
        },
        syntax_reader=common_null_literal.reader,
    ),
    Dispatcher(
        applicable_types={
            "integer_literal",
            "real_literal",
        },
        syntax_reader=common_number_literal.reader,
    ),
    Dispatcher(
        applicable_types={
            "program",
        },
        syntax_reader=java_program.reader,
    ),
    Dispatcher(
        applicable_types={
            "package_declaration",
        },
        syntax_reader=java_package_declaration.reader,
    ),
    Dispatcher(
        applicable_types={
            "formal_parameter",
        },
        syntax_reader=common_parameter.reader,
    ),
    Dispatcher(
        applicable_types={
            "formal_parameters",
            "inferred_parameters",
        },
        syntax_reader=java_parameter_list.reader,
    ),
    Dispatcher(
        applicable_types={
            "parenthesized_expression",
        },
        syntax_reader=common_parenthesized_expression.reader,
    ),
    Dispatcher(
        applicable_types={
            "character_literal",
            "decimal_integer_literal",
            "string_literal",
        },
        syntax_reader=common_string_literal.reader,
    ),
    Dispatcher(
        applicable_types={
            "try_statement",
        },
        syntax_reader=common_try_statement.reader,
    ),
    Dispatcher(
        applicable_types={
            "update_expression",
        },
        syntax_reader=java_update_expression.reader,
    ),
    Dispatcher(
        applicable_types={
            "local_variable_declaration",
        },
        syntax_reader=java_variable_declaration.reader,
    ),
    Dispatcher(
        applicable_types={
            "variable_declarator",
        },
        syntax_reader=java_variable_declarator.reader,
    ),
    Dispatcher(
        applicable_types={
            "while_statement",
        },
        syntax_reader=java_while_statement.reader,
    ),
)
