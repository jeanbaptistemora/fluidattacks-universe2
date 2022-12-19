from syntax_graph.syntax_readers.c_sharp import (
    accessor_declaration as c_sharp_accessor_declaration,
    anonymous_object_creation as c_sharp_anonymous_object_creation,
    argument as c_sharp_argument,
    argument_list as c_sharp_argument_list,
    array_creation_expression as c_sharp_array_creation_expression,
    array_type as c_sharp_array_type,
    arrow_expression_clause as c_sharp_arrow_expression_clause,
    assignment_expression as c_sharp_assignment_expression,
    attribute as c_sharp_attribute,
    attribute_list as c_sharp_attribute_list,
    binary_expression as c_sharp_binary_expression,
    boolean_literal as c_sharp_boolean_literal,
    bracketed_argument_list as c_sharp_bracketed_argument_list,
    break_statement as c_sharp_break_statement,
    cast_expression as c_sharp_cast_expression,
    catch_clause as c_sharp_catch_clause,
    catch_declaration as c_sharp_catch_declaration,
    class_declaration as c_sharp_class_declaration,
    comment as c_sharp_comment,
    compilation_unit as c_sharp_compilation_unit,
    conditional_access_expression as c_sharp_conditional_access_expression,
    conditional_expression as c_sharp_conditional_expression,
    constructor_declaration as c_sharp_constructor_declaration,
    declaration_block as c_sharp_declaration_block,
    do_statement as c_sharp_do_statement,
    element_access_expression as c_sharp_element_access_expression,
    element_binding_expression as c_sharp_element_binding_expression,
    execution_block as c_sharp_execution_block,
    expression_statement as c_sharp_expression_statement,
    field_declaration as c_sharp_field_declaration,
    file_scoped_namespace_declaration as c_sharp_file_scoped_namespace_decla,
    finally_clause as c_sharp_finally_clause,
    for_each_statement as c_sharp_for_each_statement,
    for_statement as c_sharp_for_statement,
    global_statement as c_sharp_global_statement,
    identifier as c_sharp_identifier,
    if_statement as c_sharp_if_statement,
    initializer_expression as c_sharp_initializer_expression,
    interface_declaration as c_sharp_interface_declaration,
    interpolated_string_expression as c_sharp_interpolated_string_expression,
    interpolation as c_sharp_interpolation,
    invocation_expression as c_sharp_invocation_expression,
    lambda_expression as c_sharp_lambda_expression,
    local_declaration_statement as c_sharp_local_declaration_statement,
    member_access_expression as c_sharp_member_access_expression,
    member_binding_expression as c_sharp_member_binding_expression,
    method_declaration as c_sharp_method_declaration,
    name_equals as c_sharp_name_equals,
    namespace_declaration as c_sharp_namespace_declaration,
    null_literal as c_sharp_null_literal,
    number_literal as c_sharp_number_literal,
    object_creation_expression as c_sharp_object_creation_expression,
    parameter as c_sharp_parameter,
    parameter_list as c_sharp_parameter_list,
    parenthesized_expression as c_sharp_parenthesized_expression,
    postfix_unary_expression as c_sharp_postfix_unary_expression,
    prefix_expression as c_sharp_prefix_expression,
    property_declaration as c_sharp_property_declaration,
    return_statement as c_sharp_return_statement,
    string_literal as c_sharp_string_literal,
    switch_body as c_sharp_switch_body,
    switch_section as c_sharp_switch_section,
    switch_statement as c_sharp_switch_statement,
    this_expression as c_sharp_this_expression,
    throw_statement as c_sharp_throw_statement,
    try_statement as c_sharp_try_statement,
    type_of_expression as c_sharp_type_of_expression,
    type_parameter_list as c_sharp_type_parameter_list,
    using_directive as c_sharp_using_directive,
    using_statement as c_sharp_using_statement,
    variable_declaration as c_sharp_variable_declaration,
    while_statement as c_sharp_while_statement,
)
from syntax_graph.types import (
    Dispatcher,
    Dispatchers,
)

CSHARP_DISPATCHERS: Dispatchers = (
    Dispatcher(
        applicable_types={
            "accessor_declaration",
        },
        syntax_reader=c_sharp_accessor_declaration.reader,
    ),
    Dispatcher(
        applicable_types={
            "anonymous_object_creation_expression",
        },
        syntax_reader=c_sharp_anonymous_object_creation.reader,
    ),
    Dispatcher(
        applicable_types={
            "argument",
            "attribute_argument",
        },
        syntax_reader=c_sharp_argument.reader,
    ),
    Dispatcher(
        applicable_types={
            "argument_list",
            "attribute_argument_list",
        },
        syntax_reader=c_sharp_argument_list.reader,
    ),
    Dispatcher(
        applicable_types={
            "array_creation_expression",
            "implicit_array_creation_expression",
        },
        syntax_reader=c_sharp_array_creation_expression.reader,
    ),
    Dispatcher(
        applicable_types={
            "array_type",
        },
        syntax_reader=c_sharp_array_type.reader,
    ),
    Dispatcher(
        applicable_types={
            "arrow_expression_clause",
        },
        syntax_reader=c_sharp_arrow_expression_clause.reader,
    ),
    Dispatcher(
        applicable_types={
            "assignment_expression",
        },
        syntax_reader=c_sharp_assignment_expression.reader,
    ),
    Dispatcher(
        applicable_types={
            "attribute",
        },
        syntax_reader=c_sharp_attribute.reader,
    ),
    Dispatcher(
        applicable_types={
            "attribute_list",
        },
        syntax_reader=c_sharp_attribute_list.reader,
    ),
    Dispatcher(
        applicable_types={
            "binary_expression",
        },
        syntax_reader=c_sharp_binary_expression.reader,
    ),
    Dispatcher(
        applicable_types={
            "boolean_literal",
        },
        syntax_reader=c_sharp_boolean_literal.reader,
    ),
    Dispatcher(
        applicable_types={
            "bracketed_argument_list",
        },
        syntax_reader=c_sharp_bracketed_argument_list.reader,
    ),
    Dispatcher(
        applicable_types={
            "break_statement",
        },
        syntax_reader=c_sharp_break_statement.reader,
    ),
    Dispatcher(
        applicable_types={
            "block",
        },
        syntax_reader=c_sharp_execution_block.reader,
    ),
    Dispatcher(
        applicable_types={
            "cast_expression",
        },
        syntax_reader=c_sharp_cast_expression.reader,
    ),
    Dispatcher(
        applicable_types={
            "catch_clause",
        },
        syntax_reader=c_sharp_catch_clause.reader,
    ),
    Dispatcher(
        applicable_types={
            "catch_declaration",
        },
        syntax_reader=c_sharp_catch_declaration.reader,
    ),
    Dispatcher(
        applicable_types={
            "class_declaration",
        },
        syntax_reader=c_sharp_class_declaration.reader,
    ),
    Dispatcher(
        applicable_types={
            "comment",
        },
        syntax_reader=c_sharp_comment.reader,
    ),
    Dispatcher(
        applicable_types={
            "compilation_unit",
        },
        syntax_reader=c_sharp_compilation_unit.reader,
    ),
    Dispatcher(
        applicable_types={
            "conditional_expression",
        },
        syntax_reader=c_sharp_conditional_expression.reader,
    ),
    Dispatcher(
        applicable_types={
            "conditional_access_expression",
        },
        syntax_reader=c_sharp_conditional_access_expression.reader,
    ),
    Dispatcher(
        applicable_types={
            "constructor_declaration",
        },
        syntax_reader=c_sharp_constructor_declaration.reader,
    ),
    Dispatcher(
        applicable_types={
            "declaration_list",
        },
        syntax_reader=c_sharp_declaration_block.reader,
    ),
    Dispatcher(
        applicable_types={
            "do_statement",
        },
        syntax_reader=c_sharp_do_statement.reader,
    ),
    Dispatcher(
        applicable_types={
            "element_access_expression",
        },
        syntax_reader=c_sharp_element_access_expression.reader,
    ),
    Dispatcher(
        applicable_types={
            "element_binding_expression",
        },
        syntax_reader=c_sharp_element_binding_expression.reader,
    ),
    Dispatcher(
        applicable_types={
            "expression_statement",
        },
        syntax_reader=c_sharp_expression_statement.reader,
    ),
    Dispatcher(
        applicable_types={
            "field_declaration",
        },
        syntax_reader=c_sharp_field_declaration.reader,
    ),
    Dispatcher(
        applicable_types={
            "file_scoped_namespace_declaration",
        },
        syntax_reader=c_sharp_file_scoped_namespace_decla.reader,
    ),
    Dispatcher(
        applicable_types={
            "finally_clause",
        },
        syntax_reader=c_sharp_finally_clause.reader,
    ),
    Dispatcher(
        applicable_types={
            "for_each_statement",
        },
        syntax_reader=c_sharp_for_each_statement.reader,
    ),
    Dispatcher(
        applicable_types={
            "for_statement",
        },
        syntax_reader=c_sharp_for_statement.reader,
    ),
    Dispatcher(
        applicable_types={
            "global_statement",
        },
        syntax_reader=c_sharp_global_statement.reader,
    ),
    Dispatcher(
        applicable_types={
            "identifier",
        },
        syntax_reader=c_sharp_identifier.reader,
    ),
    Dispatcher(
        applicable_types={
            "if_statement",
        },
        syntax_reader=c_sharp_if_statement.reader,
    ),
    Dispatcher(
        applicable_types={
            "initializer_expression",
        },
        syntax_reader=c_sharp_initializer_expression.reader,
    ),
    Dispatcher(
        applicable_types={
            "interface_declaration",
        },
        syntax_reader=c_sharp_interface_declaration.reader,
    ),
    Dispatcher(
        applicable_types={
            "interpolated_string_expression",
        },
        syntax_reader=c_sharp_interpolated_string_expression.reader,
    ),
    Dispatcher(
        applicable_types={
            "invocation_expression",
        },
        syntax_reader=c_sharp_invocation_expression.reader,
    ),
    Dispatcher(
        applicable_types={
            "interpolation",
        },
        syntax_reader=c_sharp_interpolation.reader,
    ),
    Dispatcher(
        applicable_types={
            "lambda_expression",
        },
        syntax_reader=c_sharp_lambda_expression.reader,
    ),
    Dispatcher(
        applicable_types={
            "local_declaration_statement",
        },
        syntax_reader=c_sharp_local_declaration_statement.reader,
    ),
    Dispatcher(
        applicable_types={
            "member_access_expression",
        },
        syntax_reader=c_sharp_member_access_expression.reader,
    ),
    Dispatcher(
        applicable_types={
            "member_binding_expression",
        },
        syntax_reader=c_sharp_member_binding_expression.reader,
    ),
    Dispatcher(
        applicable_types={
            "local_function_statement",
            "method_declaration",
        },
        syntax_reader=c_sharp_method_declaration.reader,
    ),
    Dispatcher(
        applicable_types={
            "name_equals",
        },
        syntax_reader=c_sharp_name_equals.reader,
    ),
    Dispatcher(
        applicable_types={
            "namespace_declaration",
        },
        syntax_reader=c_sharp_namespace_declaration.reader,
    ),
    Dispatcher(
        applicable_types={
            "null_literal",
        },
        syntax_reader=c_sharp_null_literal.reader,
    ),
    Dispatcher(
        applicable_types={
            "integer_literal",
            "real_literal",
        },
        syntax_reader=c_sharp_number_literal.reader,
    ),
    Dispatcher(
        applicable_types={
            "object_creation_expression",
        },
        syntax_reader=c_sharp_object_creation_expression.reader,
    ),
    Dispatcher(
        applicable_types={
            "parameter",
        },
        syntax_reader=c_sharp_parameter.reader,
    ),
    Dispatcher(
        applicable_types={
            "parameter_list",
        },
        syntax_reader=c_sharp_parameter_list.reader,
    ),
    Dispatcher(
        applicable_types={
            "parenthesized_expression",
        },
        syntax_reader=c_sharp_parenthesized_expression.reader,
    ),
    Dispatcher(
        applicable_types={
            "postfix_unary_expression",
        },
        syntax_reader=c_sharp_postfix_unary_expression.reader,
    ),
    Dispatcher(
        applicable_types={
            "prefix_unary_expression",
        },
        syntax_reader=c_sharp_prefix_expression.reader,
    ),
    Dispatcher(
        applicable_types={
            "property_declaration",
        },
        syntax_reader=c_sharp_property_declaration.reader,
    ),
    Dispatcher(
        applicable_types={
            "return_statement",
        },
        syntax_reader=c_sharp_return_statement.reader,
    ),
    Dispatcher(
        applicable_types={
            "character_literal",
            "string_literal",
            "verbatim_string_literal",
            "predefined_type",
        },
        syntax_reader=c_sharp_string_literal.reader,
    ),
    Dispatcher(
        applicable_types={
            "switch_body",
        },
        syntax_reader=c_sharp_switch_body.reader,
    ),
    Dispatcher(
        applicable_types={
            "switch_statement",
        },
        syntax_reader=c_sharp_switch_statement.reader,
    ),
    Dispatcher(
        applicable_types={
            "switch_section",
        },
        syntax_reader=c_sharp_switch_section.reader,
    ),
    Dispatcher(
        applicable_types={
            "this_expression",
        },
        syntax_reader=c_sharp_this_expression.reader,
    ),
    Dispatcher(
        applicable_types={
            "throw_statement",
        },
        syntax_reader=c_sharp_throw_statement.reader,
    ),
    Dispatcher(
        applicable_types={
            "type_of_expression",
        },
        syntax_reader=c_sharp_type_of_expression.reader,
    ),
    Dispatcher(
        applicable_types={
            "type_parameter_list",
        },
        syntax_reader=c_sharp_type_parameter_list.reader,
    ),
    Dispatcher(
        applicable_types={
            "try_statement",
        },
        syntax_reader=c_sharp_try_statement.reader,
    ),
    Dispatcher(
        applicable_types={
            "using_directive",
        },
        syntax_reader=c_sharp_using_directive.reader,
    ),
    Dispatcher(
        applicable_types={
            "using_statement",
        },
        syntax_reader=c_sharp_using_statement.reader,
    ),
    Dispatcher(
        applicable_types={
            "variable_declaration",
        },
        syntax_reader=c_sharp_variable_declaration.reader,
    ),
    Dispatcher(
        applicable_types={
            "while_statement",
        },
        syntax_reader=c_sharp_while_statement.reader,
    ),
)
