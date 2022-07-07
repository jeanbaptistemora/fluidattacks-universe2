from syntax_graph.syntax_readers.c_sharp import (
    accessor_declaration as c_sharp_accessor_declaration,
    argument as c_sharp_argument,
    argument_list as c_sharp_argument_list,
    arrow_expression_clause as c_sharp_arrow_expression_clause,
    assignment_expression as c_sharp_assignment_expression,
    bracketed_argument_list as c_sharp_bracketed_argument_list,
    compilation_unit as c_sharp_compilation_unit,
    conditional_access_expression as c_sharp_conditional_access_expression,
    constructor_declaration as c_sharp_constructor_declaration,
    element_access_expression as c_sharp_element_access_expression,
    element_binding_expression as c_sharp_element_binding_expression,
    field_declaration as c_sharp_field_declaration,
    for_each_statement as c_sharp_for_each_statement,
    for_statemente as c_sharp_for_statement,
    if_statement as c_sharp_if_statement,
    initializer_expression as c_sharp_initializer_expression,
    interface_declaration as c_sharp_interface_declaration,
    interpolated_string_expression as c_sharp_interpolated_string_expression,
    invocation_expression as c_sharp_invocation_expression,
    lambda_expression as c_sharp_lambda_expression,
    local_declaration_statement as c_sharp_local_declaration_statement,
    member_access_expression as c_sharp_member_access_expression,
    member_binding_expression as c_sharp_member_binding_expression,
    namespace_declaration as c_sharp_namespace_declaration,
    object_creation_expression as c_sharp_object_creation_expression,
    parameter_list as c_sharp_parameter_list,
    postfix_unary_expression as c_sharp_postfix_unary_expression,
    prefix_expression as c_sharp_prefix_expression,
    property_declaration as c_sharp_property_declaration,
    return_statement as c_sharp_return_statement,
    this_expression as c_sharp_this_expression,
    throw_statement as c_sharp_throw_statement,
    type_of_expression as c_sharp_type_of_expression,
    type_parameter_list as c_sharp_type_parameter_list,
    using_directive as c_sharp_using_directive,
    using_statement as c_sharp_using_statement,
    variable_declaration as c_sharp_variable_declaration,
    while_statement as c_sharp_while_statement,
)
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
            "argument",
        },
        syntax_reader=c_sharp_argument.reader,
    ),
    Dispatcher(
        applicable_types={
            "argument_list",
        },
        syntax_reader=c_sharp_argument_list.reader,
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
            "bracketed_argument_list",
        },
        syntax_reader=c_sharp_bracketed_argument_list.reader,
    ),
    Dispatcher(
        applicable_types={
            "block",
        },
        syntax_reader=common_execution_block.reader,
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
            "compilation_unit",
        },
        syntax_reader=c_sharp_compilation_unit.reader,
    ),
    Dispatcher(
        applicable_types={
            "conditional_expression",
        },
        syntax_reader=common_conditional_expression.reader,
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
        syntax_reader=common_expression_statement.reader,
    ),
    Dispatcher(
        applicable_types={
            "field_declaration",
        },
        syntax_reader=c_sharp_field_declaration.reader,
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
            "identifier",
        },
        syntax_reader=common_identifier.reader,
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
        syntax_reader=common_interpolation.reader,
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
            "method_declaration",
        },
        syntax_reader=common_method_declaration.reader,
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
        syntax_reader=common_null_literal.reader,
    ),
    Dispatcher(
        applicable_types={
            "integer_literal",
        },
        syntax_reader=common_number_literal.reader,
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
        syntax_reader=common_parameter.reader,
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
        syntax_reader=common_parenthesized_expression.reader,
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
            "real_literal",
        },
        syntax_reader=common_number_literal.reader,
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
        },
        syntax_reader=common_string_literal.reader,
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
        syntax_reader=common_try_statement.reader,
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
