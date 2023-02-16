from syntax_graph.syntax_readers.java import (
    annotation as java_annotation,
    annotation_argument_list as java_annotation_argument_list,
    argument_list as java_argument_list,
    array as java_array,
    array_access as java_array_access,
    array_creation_expression as java_array_creation_expression,
    assignment_expression as java_assignment_expression,
    binary_expression as java_binary_expression,
    boolean_literal as java_boolean_literal,
    break_statement as java_break_statement,
    cast_expression as java_cast_expression,
    catch_clause as java_catch_clause,
    catch_declaration as java_catch_declaration,
    catch_parameter as java_catch_parameter,
    catch_type as java_catch_type,
    class_body as java_class_body,
    class_declaration as java_class_declaration,
    comment as java_comment,
    continue_statement as java_continue_statement,
    declaration_block as java_declaration_block,
    dimensions_expr as java_dimensions_expr,
    do_statement as java_do_statement,
    element_value_pair as java_element_value_pair,
    enhanced_for_statement as java_enhanced_for_statement,
    execution_block as java_execution_block,
    expression_statement as java_expression_statement,
    field_access as java_field_access,
    field_declaration as java_field_declaration,
    finally_clause as java_finally_clause,
    for_statement as java_for_statement,
    identifier as java_identifier,
    if_statement as java_if_statement,
    import_declaration as java_import_declaration,
    instanceof_expression as java_instanceof_expression,
    interface_declaration as java_interface_declaration,
    lambda_expression as java_lambda_expression,
    method_declaration as java_method_declaration,
    method_invocation as java_method_invocation,
    modifiers as java_modifiers,
    null_literal as java_null_literal,
    number_literal as java_number_literal,
    object_creation_expression as java_object_creation_expression,
    package_declaration as java_package_declaration,
    parameter as java_parameter,
    parameter_list as java_parameter_list,
    parenthesized_expression as java_parenthesized_expression,
    program as java_program,
    resource as java_resource,
    resource_specification as java_resource_specification,
    return_statement as java_return_statement,
    string_literal as java_string_literal,
    switch_body as java_switch_body,
    switch_section as java_switch_section,
    switch_statement as java_switch_statement,
    ternary_expression as java_ternary_expression,
    this as java_this,
    throw_statement as java_throw_statement,
    try_statement as java_try_statement,
    unary_expression as java_unary_expression,
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
            "annotation",
            "marker_annotation",
        },
        syntax_reader=java_annotation.reader,
    ),
    Dispatcher(
        applicable_types={
            "annotation_argument_list",
        },
        syntax_reader=java_annotation_argument_list.reader,
    ),
    Dispatcher(
        applicable_types={
            "argument_list",
        },
        syntax_reader=java_argument_list.reader,
    ),
    Dispatcher(
        applicable_types={
            "array_initializer",
        },
        syntax_reader=java_array.reader,
    ),
    Dispatcher(
        applicable_types={
            "array_access",
        },
        syntax_reader=java_array_access.reader,
    ),
    Dispatcher(
        applicable_types={
            "array_creation_expression",
        },
        syntax_reader=java_array_creation_expression.reader,
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
        syntax_reader=java_binary_expression.reader,
    ),
    Dispatcher(
        applicable_types={
            "true",
            "false",
        },
        syntax_reader=java_boolean_literal.reader,
    ),
    Dispatcher(
        applicable_types={
            "break_statement",
        },
        syntax_reader=java_break_statement.reader,
    ),
    Dispatcher(
        applicable_types={
            "cast_expression",
        },
        syntax_reader=java_cast_expression.reader,
    ),
    Dispatcher(
        applicable_types={
            "catch_clause",
        },
        syntax_reader=java_catch_clause.reader,
    ),
    Dispatcher(
        applicable_types={
            "catch_declaration",
        },
        syntax_reader=java_catch_declaration.reader,
    ),
    Dispatcher(
        applicable_types={
            "catch_formal_parameter",
        },
        syntax_reader=java_catch_parameter.reader,
    ),
    Dispatcher(
        applicable_types={
            "catch_type",
        },
        syntax_reader=java_catch_type.reader,
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
        syntax_reader=java_class_declaration.reader,
    ),
    Dispatcher(
        applicable_types={
            "comment",
        },
        syntax_reader=java_comment.reader,
    ),
    Dispatcher(
        applicable_types={
            "continue_statement",
        },
        syntax_reader=java_continue_statement.reader,
    ),
    Dispatcher(
        applicable_types={
            "declaration_list",
        },
        syntax_reader=java_declaration_block.reader,
    ),
    Dispatcher(
        applicable_types={
            "dimensions_expr",
        },
        syntax_reader=java_dimensions_expr.reader,
    ),
    Dispatcher(
        applicable_types={
            "do_statement",
        },
        syntax_reader=java_do_statement.reader,
    ),
    Dispatcher(
        applicable_types={
            "block",
        },
        syntax_reader=java_execution_block.reader,
    ),
    Dispatcher(
        applicable_types={
            "element_value_pair",
        },
        syntax_reader=java_element_value_pair.reader,
    ),
    Dispatcher(
        applicable_types={
            "enhanced_for_statement",
        },
        syntax_reader=java_enhanced_for_statement.reader,
    ),
    Dispatcher(
        applicable_types={
            "expression_statement",
        },
        syntax_reader=java_expression_statement.reader,
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
            "finally_clause",
        },
        syntax_reader=java_finally_clause.reader,
    ),
    Dispatcher(
        applicable_types={
            "identifier",
            "type_identifier",
            "scoped_type_identifier",
        },
        syntax_reader=java_identifier.reader,
    ),
    Dispatcher(
        applicable_types={
            "if_statement",
        },
        syntax_reader=java_if_statement.reader,
    ),
    Dispatcher(
        applicable_types={
            "import_declaration",
        },
        syntax_reader=java_import_declaration.reader,
    ),
    Dispatcher(
        applicable_types={
            "instanceof_expression",
        },
        syntax_reader=java_instanceof_expression.reader,
    ),
    Dispatcher(
        applicable_types={
            "interface_declaration",
        },
        syntax_reader=java_interface_declaration.reader,
    ),
    Dispatcher(
        applicable_types={
            "constructor_declaration",
            "method_declaration",
        },
        syntax_reader=java_method_declaration.reader,
    ),
    Dispatcher(
        applicable_types={
            "lambda_expression",
        },
        syntax_reader=java_lambda_expression.reader,
    ),
    Dispatcher(
        applicable_types={
            "method_invocation",
        },
        syntax_reader=java_method_invocation.reader,
    ),
    Dispatcher(
        applicable_types={
            "modifiers",
        },
        syntax_reader=java_modifiers.reader,
    ),
    Dispatcher(
        applicable_types={
            "null_literal",
        },
        syntax_reader=java_null_literal.reader,
    ),
    Dispatcher(
        applicable_types={
            "decimal_integer_literal",
            "integer_literal",
            "real_literal",
        },
        syntax_reader=java_number_literal.reader,
    ),
    Dispatcher(
        applicable_types={
            "object_creation_expression",
        },
        syntax_reader=java_object_creation_expression.reader,
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
            "for_statement",
        },
        syntax_reader=java_for_statement.reader,
    ),
    Dispatcher(
        applicable_types={
            "formal_parameter",
        },
        syntax_reader=java_parameter.reader,
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
        syntax_reader=java_parenthesized_expression.reader,
    ),
    Dispatcher(
        applicable_types={
            "resource_specification",
        },
        syntax_reader=java_resource_specification.reader,
    ),
    Dispatcher(
        applicable_types={
            "resource",
        },
        syntax_reader=java_resource.reader,
    ),
    Dispatcher(
        applicable_types={
            "return_statement",
        },
        syntax_reader=java_return_statement.reader,
    ),
    Dispatcher(
        applicable_types={
            "character_literal",
            "integral_type",
            "string_literal",
        },
        syntax_reader=java_string_literal.reader,
    ),
    Dispatcher(
        applicable_types={
            "switch_block",
        },
        syntax_reader=java_switch_body.reader,
    ),
    Dispatcher(
        applicable_types={
            "switch_block_statement_group",
        },
        syntax_reader=java_switch_section.reader,
    ),
    Dispatcher(
        applicable_types={
            "switch_expression",
        },
        syntax_reader=java_switch_statement.reader,
    ),
    Dispatcher(
        applicable_types={
            "ternary_expression",
        },
        syntax_reader=java_ternary_expression.reader,
    ),
    Dispatcher(
        applicable_types={
            "this",
        },
        syntax_reader=java_this.reader,
    ),
    Dispatcher(
        applicable_types={
            "throw_statement",
        },
        syntax_reader=java_throw_statement.reader,
    ),
    Dispatcher(
        applicable_types={
            "try_statement",
            "try_with_resources_statement",
        },
        syntax_reader=java_try_statement.reader,
    ),
    Dispatcher(
        applicable_types={
            "unary_expression",
        },
        syntax_reader=java_unary_expression.reader,
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
