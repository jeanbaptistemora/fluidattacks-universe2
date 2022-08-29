from syntax_graph.syntax_readers.common import (
    array as common_array,
    binary_expression as common_binary_expression,
    boolean_literal as common_boolean_literal,
    break_statement as common_break_statement,
    catch_clause as common_catch_clause,
    catch_declaration as common_catch_declaration,
    class_declaration as common_class_declaration,
    comment as common_comment,
    conditional_expression as common_conditional_expression,
    declaration_block as common_declaration_block,
    do_statement as common_do_statement,
    execution_block as common_execution_block,
    expression_statement as common_expression_statement,
    finally_clause as common_finally_clause,
    identifier as common_identifier,
    if_statement as common_if_statement,
    interpolation as common_interpolation,
    method_declaration as common_method_declaration,
    null_literal as common_null_literal,
    number_literal as common_number_literal,
    object_creation_expression as common_object_creation_expression,
    parameter as common_parameter,
    parenthesized_expression as common_parenthesized_expression,
    program as common_program,
    return_statement as common_return_statement,
    string_literal as common_string_literal,
    throw_statement as common_throw_statement,
    try_statement as common_try_statement,
    variable_declaration as common_variable_declaration,
    variable_declarator as common_variable_declarator,
)
from syntax_graph.syntax_readers.java import (
    annotation as java_annotation,
    annotation_argument_list as java_annotation_argument_list,
    argument_list as java_argument_list,
    array_access as java_array_access,
    array_creation_expression as java_array_creation_expression,
    assignment_expression as java_assignment_expression,
    class_body as java_class_body,
    dimensions_expr as java_dimensions_expr,
    element_value_pair as java_element_value_pair,
    enhanced_for_statement as java_enhanced_for_statement,
    field_access as java_field_access,
    field_declaration as java_field_declaration,
    for_statement as java_for_statement,
    import_declaration as java_import_declaration,
    interface_declaration as java_interface_declaration,
    method_invocation as java_method_invocation,
    modifiers as java_modifiers,
    package_declaration as java_package_declaration,
    parameter_list as java_parameter_list,
    switch_block as java_switch_block,
    switch_block_statement_group as java_switch_block_statement_group,
    switch_expression as java_switch_expression,
    switch_label as java_switch_label,
    unary_expression as java_unary_expression,
    update_expression as java_update_expression,
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
        syntax_reader=common_array.reader,
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
        syntax_reader=common_binary_expression.reader,
    ),
    Dispatcher(
        applicable_types={
            "boolean_literal",
            "true",
            "false",
        },
        syntax_reader=common_boolean_literal.reader,
    ),
    Dispatcher(
        applicable_types={
            "break_statement",
        },
        syntax_reader=common_break_statement.reader,
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
            "dimensions_expr",
        },
        syntax_reader=java_dimensions_expr.reader,
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
            "finally_clause",
        },
        syntax_reader=common_finally_clause.reader,
    ),
    Dispatcher(
        applicable_types={
            "identifier",
        },
        syntax_reader=common_identifier.reader,
    ),
    Dispatcher(
        applicable_types={
            "if_statement",
        },
        syntax_reader=common_if_statement.reader,
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
            "modifiers",
        },
        syntax_reader=java_modifiers.reader,
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
            "object_creation_expression",
        },
        syntax_reader=common_object_creation_expression.reader,
    ),
    Dispatcher(
        applicable_types={
            "program",
        },
        syntax_reader=common_program.reader,
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
            "return_statement",
        },
        syntax_reader=common_return_statement.reader,
    ),
    Dispatcher(
        applicable_types={
            "character_literal",
            "decimal_integer_literal",
            "integral_type",
            "string_literal",
        },
        syntax_reader=common_string_literal.reader,
    ),
    Dispatcher(
        applicable_types={
            "switch_block",
        },
        syntax_reader=java_switch_block.reader,
    ),
    Dispatcher(
        applicable_types={
            "switch_block_statement_group",
        },
        syntax_reader=java_switch_block_statement_group.reader,
    ),
    Dispatcher(
        applicable_types={
            "switch_expression",
        },
        syntax_reader=java_switch_expression.reader,
    ),
    Dispatcher(
        applicable_types={
            "switch_label",
        },
        syntax_reader=java_switch_label.reader,
    ),
    Dispatcher(
        applicable_types={
            "throw_statement",
        },
        syntax_reader=common_throw_statement.reader,
    ),
    Dispatcher(
        applicable_types={
            "try_statement",
        },
        syntax_reader=common_try_statement.reader,
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
            "while_statement",
        },
        syntax_reader=java_while_statement.reader,
    ),
)
