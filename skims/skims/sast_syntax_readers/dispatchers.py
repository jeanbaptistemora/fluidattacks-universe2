from model import (
    graph_model,
)
from sast_syntax_readers.c_sharp import (
    argument as c_sharp_argument,
    array_creation_expression as c_sharp_array_creation_expression,
    assignment_expression as c_sharp_assignment_expression,
    case_switch_label as c_sharp_case_switch_label,
    default_switch_label as c_sharp_default_switch_label,
    element_access_expression as c_sharp_element_access_expression,
    for_statement as c_sharp_for_statement,
    invocation_expression as c_sharp_invocation_expression,
    lambda_expression as c_sharp_lambda_expression,
    local_declaration_statement as c_sharp_local_declaration_statement,
    member_access_expression as c_sharp_member_access_expression,
    method_declaration as c_sharp_method_declaration,
    parameter as c_sharp_parameter,
    switch_statement as c_sharp_switch_statement,
    using_statement as c_sharp_using_statement,
    variable_declaration as c_sharp_variable_declaration,
    while_statement as c_sharp_while_statement,
)
from sast_syntax_readers.common import (
    attribute_access as common_attribute_access,
    binary_expression as common_binary_expression,
    cast_expression as common_cast_expression,
    identifier as common_identifier,
    if_statement as common_if_statement,
    literal as common_literal,
    noop as common_noop,
    object_creation_expression as common_object_creation_expression,
    parenthesized_expression as common_parenthesized_expression,
    return_statement as common_return_statement,
    unary_expression as common_unary_expression,
    while_statement as common_while_statement,
)
from sast_syntax_readers.go import (
    assignment_statement as go_assignment_statement,
    call_expression as go_call_expression,
    function_declaration as go_function_declaration,
    return_statement as go_return_statement,
    variable_declaration as go_variable_declaration,
)
from sast_syntax_readers.java import (
    array_access as java_array_access,
    array_creation_expression as java_array_creation_expression,
    array_initializer as java_array_initializer,
    assignment_expression as java_assignment_expression,
    catch_clause as java_catch_clause,
    enhanced_for_statement as java_enhanced_for_statement,
    for_statement as java_for_statement,
    if_statement as java_if_statement,
    instanceof_expression as java_instanceof_expression,
    lambda_expression as java_lambda_expression,
    local_variable_declaration as java_local_variable_declaration,
    method_declaration as java_method_declaration,
    method_invocation as java_method_invocation,
    resource as java_resource,
    switch_expression as java_switch_expression,
    switch_label as java_switch_label,
    ternary_expression as java_ternary_expression,
    this as java_this,
)
from sast_syntax_readers.javascript import (
    array as javascript_array,
    arrow_function as javascript_arrrow_function,
    assignment_expression as javascript_assignment_expression,
    await_expression as javascript_await_expression,
    call_expression as javascript_call_expression,
    catch_clause as javascript_catch_clause,
    do_statement as javascript_do_statement,
    for_in_statement as javascript_for_in_statement,
    for_statement as javascript_for_statement,
    formal_parameters as javascript_formal_parameters,
    function_declaration as javascript_function_declaration,
    if_statement as javascript_if_statement,
    import_statement as javascript_import_statement,
    lexical_declaration as javascript_lexical_declaration,
    member_expression as javascript_member_expression,
    new_expression as javascript_new_expression,
    object_ as javascript_object,
    subscript_expression as javascript_subscript_expression,
    switch_case as javascript_switch_case,
    switch_default as javascript_switch_default,
    switch_statement as javascript_switch_statement,
    template_string as javascript_template_string,
    ternary_expression as javascript_ternary_expression,
    variable_declaration as javascript_variable_declaration,
    variable_declarator as javascript_variable_declarator,
)
from sast_syntax_readers.kotlin import (
    assignment as kotlin_assignment,
    call_expression as kotlin_call_expression,
    if_expression as kotlin_if_expression,
    navigation_expression as kotlin_navigation_expression,
    object_declaration as kotlin_object_declaration,
    property_declaration as kotlin_property_declaration,
)
from sast_syntax_readers.types import (
    Dispatcher,
    Dispatchers,
)
from typing import (
    Dict,
    Tuple,
)

DISPATCHERS: Tuple[Dispatcher, ...] = (
    Dispatcher(
        applicable_languages={
            graph_model.GraphShardMetadataLanguage.CSHARP,
        },
        applicable_node_label_types={
            "assignment_expression",
        },
        syntax_reader=c_sharp_assignment_expression.reader,
    ),
    Dispatcher(
        applicable_languages={
            graph_model.GraphShardMetadataLanguage.JAVA,
        },
        applicable_node_label_types={
            "assignment_expression",
        },
        syntax_reader=java_assignment_expression.reader,
    ),
    Dispatcher(
        applicable_languages={
            graph_model.GraphShardMetadataLanguage.JAVASCRIPT,
            graph_model.GraphShardMetadataLanguage.TSX,
        },
        applicable_node_label_types={
            "assignment_expression",
            "augmented_assignment_expression",
        },
        syntax_reader=javascript_assignment_expression.reader,
    ),
    Dispatcher(
        applicable_languages={
            graph_model.GraphShardMetadataLanguage.GO,
        },
        applicable_node_label_types={
            "assignment_statement",
        },
        syntax_reader=go_assignment_statement.reader,
    ),
    Dispatcher(
        applicable_languages={
            graph_model.GraphShardMetadataLanguage.KOTLIN,
        },
        applicable_node_label_types={
            "assignment",
        },
        syntax_reader=kotlin_assignment.reader,
    ),
    Dispatcher(
        applicable_languages={
            graph_model.GraphShardMetadataLanguage.JAVA,
        },
        applicable_node_label_types={
            "ternary_expression",
        },
        syntax_reader=java_ternary_expression.reader,
    ),
    Dispatcher(
        applicable_languages={
            graph_model.GraphShardMetadataLanguage.GO,
            graph_model.GraphShardMetadataLanguage.JAVA,
            graph_model.GraphShardMetadataLanguage.JAVASCRIPT,
            graph_model.GraphShardMetadataLanguage.TSX,
            graph_model.GraphShardMetadataLanguage.CSHARP,
        },
        applicable_node_label_types={
            "binary_expression",
        },
        syntax_reader=common_binary_expression.reader,
    ),
    Dispatcher(
        applicable_languages={
            graph_model.GraphShardMetadataLanguage.GO,
            graph_model.GraphShardMetadataLanguage.JAVA,
            graph_model.GraphShardMetadataLanguage.JAVASCRIPT,
            graph_model.GraphShardMetadataLanguage.TSX,
        },
        applicable_node_label_types={
            "unary_expression",
        },
        syntax_reader=common_unary_expression.reader,
    ),
    Dispatcher(
        applicable_languages={
            graph_model.GraphShardMetadataLanguage.JAVA,
        },
        applicable_node_label_types={
            "enhanced_for_statement",
        },
        syntax_reader=java_enhanced_for_statement.reader,
    ),
    Dispatcher(
        applicable_languages={
            graph_model.GraphShardMetadataLanguage.JAVA,
            graph_model.GraphShardMetadataLanguage.JAVASCRIPT,
            graph_model.GraphShardMetadataLanguage.TSX,
        },
        applicable_node_label_types={
            "while_statement",
        },
        syntax_reader=common_while_statement.reader,
    ),
    Dispatcher(
        applicable_languages={
            graph_model.GraphShardMetadataLanguage.CSHARP,
        },
        applicable_node_label_types={
            "while_statement",
        },
        syntax_reader=c_sharp_while_statement.reader,
    ),
    Dispatcher(
        applicable_languages={
            graph_model.GraphShardMetadataLanguage.JAVA,
        },
        applicable_node_label_types={"for_statement"},
        syntax_reader=java_for_statement.reader,
    ),
    Dispatcher(
        applicable_languages={
            graph_model.GraphShardMetadataLanguage.CSHARP,
        },
        applicable_node_label_types={"for_statement"},
        syntax_reader=c_sharp_for_statement.reader,
    ),
    Dispatcher(
        applicable_languages={
            graph_model.GraphShardMetadataLanguage.GO,
            graph_model.GraphShardMetadataLanguage.JAVA,
            graph_model.GraphShardMetadataLanguage.JAVASCRIPT,
            graph_model.GraphShardMetadataLanguage.TSX,
            graph_model.GraphShardMetadataLanguage.CSHARP,
            graph_model.GraphShardMetadataLanguage.KOTLIN,
        },
        applicable_node_label_types={
            "field_access",
            "identifier",
            "simple_identifier",
        },
        syntax_reader=common_identifier.reader,
    ),
    Dispatcher(
        applicable_languages={
            graph_model.GraphShardMetadataLanguage.CSHARP,
            graph_model.GraphShardMetadataLanguage.GO,
        },
        applicable_node_label_types={
            "if_statement",
        },
        syntax_reader=common_if_statement.reader,
    ),
    Dispatcher(
        applicable_languages={
            graph_model.GraphShardMetadataLanguage.JAVASCRIPT,
            graph_model.GraphShardMetadataLanguage.TSX,
        },
        applicable_node_label_types={
            "if_statement",
        },
        syntax_reader=javascript_if_statement.reader,
    ),
    Dispatcher(
        applicable_languages={
            graph_model.GraphShardMetadataLanguage.JAVA,
        },
        applicable_node_label_types={
            "if_statement",
        },
        syntax_reader=java_if_statement.reader,
    ),
    Dispatcher(
        applicable_languages={
            graph_model.GraphShardMetadataLanguage.KOTLIN,
        },
        applicable_node_label_types={
            "if_expression",
        },
        syntax_reader=kotlin_if_expression.reader,
    ),
    Dispatcher(
        applicable_languages={
            graph_model.GraphShardMetadataLanguage.GO,
            graph_model.GraphShardMetadataLanguage.JAVA,
            graph_model.GraphShardMetadataLanguage.JAVASCRIPT,
            graph_model.GraphShardMetadataLanguage.TSX,
        },
        applicable_node_label_types={
            "parenthesized_expression",
        },
        syntax_reader=common_parenthesized_expression.reader,
    ),
    Dispatcher(
        applicable_languages={
            graph_model.GraphShardMetadataLanguage.JAVA,
            graph_model.GraphShardMetadataLanguage.CSHARP,
        },
        applicable_node_label_types={
            "cast_expression",
        },
        syntax_reader=common_cast_expression.reader,
    ),
    Dispatcher(
        applicable_languages={
            graph_model.GraphShardMetadataLanguage.JAVA,
        },
        applicable_node_label_types={
            "instanceof_expression",
        },
        syntax_reader=java_instanceof_expression.reader,
    ),
    Dispatcher(
        applicable_languages={
            graph_model.GraphShardMetadataLanguage.JAVA,
        },
        applicable_node_label_types={
            "catch_clause",
        },
        syntax_reader=java_catch_clause.reader,
    ),
    Dispatcher(
        applicable_languages={
            graph_model.GraphShardMetadataLanguage.JAVASCRIPT,
            graph_model.GraphShardMetadataLanguage.TSX,
        },
        applicable_node_label_types={
            "catch_clause",
        },
        syntax_reader=javascript_catch_clause.reader,
    ),
    Dispatcher(
        applicable_languages={
            graph_model.GraphShardMetadataLanguage.GO,
        },
        applicable_node_label_types={
            "selector_expression",
        },
        syntax_reader=common_attribute_access.reader,
    ),
    Dispatcher(
        applicable_languages={
            graph_model.GraphShardMetadataLanguage.KOTLIN,
        },
        applicable_node_label_types={
            "navigation_expression",
        },
        syntax_reader=kotlin_navigation_expression.reader,
    ),
    Dispatcher(
        applicable_languages={
            graph_model.GraphShardMetadataLanguage.JAVA,
        },
        applicable_node_label_types={
            "switch_expression",
        },
        syntax_reader=java_switch_expression.reader,
    ),
    Dispatcher(
        applicable_languages={
            graph_model.GraphShardMetadataLanguage.CSHARP,
        },
        applicable_node_label_types={
            "switch_statement",
        },
        syntax_reader=c_sharp_switch_statement.reader,
    ),
    Dispatcher(
        applicable_languages={
            graph_model.GraphShardMetadataLanguage.CSHARP,
        },
        applicable_node_label_types={
            "case_switch_label",
        },
        syntax_reader=c_sharp_case_switch_label.reader,
    ),
    Dispatcher(
        applicable_languages={
            graph_model.GraphShardMetadataLanguage.CSHARP,
        },
        applicable_node_label_types={
            "default_switch_label",
        },
        syntax_reader=c_sharp_default_switch_label.reader,
    ),
    Dispatcher(
        applicable_languages={
            graph_model.GraphShardMetadataLanguage.JAVA,
        },
        applicable_node_label_types={
            "switch_label",
        },
        syntax_reader=java_switch_label.reader,
    ),
    Dispatcher(
        applicable_languages={
            graph_model.GraphShardMetadataLanguage.JAVA,
        },
        applicable_node_label_types={
            "local_variable_declaration",
        },
        syntax_reader=java_local_variable_declaration.reader,
    ),
    Dispatcher(
        applicable_languages={
            graph_model.GraphShardMetadataLanguage.CSHARP,
        },
        applicable_node_label_types={
            "local_declaration_statement",
        },
        syntax_reader=c_sharp_local_declaration_statement.reader,
    ),
    Dispatcher(
        applicable_languages={
            graph_model.GraphShardMetadataLanguage.CSHARP,
        },
        applicable_node_label_types={
            "variable_declaration",
        },
        syntax_reader=c_sharp_variable_declaration.reader,
    ),
    Dispatcher(
        applicable_languages={
            graph_model.GraphShardMetadataLanguage.JAVASCRIPT,
            graph_model.GraphShardMetadataLanguage.TSX,
        },
        applicable_node_label_types={
            "variable_declaration",
        },
        syntax_reader=javascript_variable_declaration.reader,
    ),
    Dispatcher(
        applicable_languages={
            graph_model.GraphShardMetadataLanguage.JAVASCRIPT,
            graph_model.GraphShardMetadataLanguage.TSX,
        },
        applicable_node_label_types={
            "variable_declarator",
        },
        syntax_reader=javascript_variable_declarator.reader,
    ),
    Dispatcher(
        applicable_languages={
            graph_model.GraphShardMetadataLanguage.JAVASCRIPT,
            graph_model.GraphShardMetadataLanguage.TSX,
        },
        applicable_node_label_types={
            "lexical_declaration",
        },
        syntax_reader=javascript_lexical_declaration.reader,
    ),
    Dispatcher(
        applicable_languages={
            graph_model.GraphShardMetadataLanguage.GO,
        },
        applicable_node_label_types={
            "const_declaration",
            "short_var_declaration",
            "var_declaration",
        },
        syntax_reader=go_variable_declaration.reader,
    ),
    Dispatcher(
        applicable_languages={
            graph_model.GraphShardMetadataLanguage.KOTLIN,
        },
        applicable_node_label_types={
            "property_declaration",
        },
        syntax_reader=kotlin_property_declaration.reader,
    ),
    Dispatcher(
        applicable_languages={
            graph_model.GraphShardMetadataLanguage.JAVA,
        },
        applicable_node_label_types={
            "method_declaration",
            "constructor_declaration",
        },
        syntax_reader=java_method_declaration.reader,
    ),
    Dispatcher(
        applicable_languages={
            graph_model.GraphShardMetadataLanguage.CSHARP,
        },
        applicable_node_label_types={
            "method_declaration",
            "constructor_declaration",
        },
        syntax_reader=c_sharp_method_declaration.reader,
    ),
    Dispatcher(
        applicable_languages={
            graph_model.GraphShardMetadataLanguage.GO,
        },
        applicable_node_label_types={
            "function_declaration",
            "method_declaration",
        },
        syntax_reader=go_function_declaration.reader,
    ),
    Dispatcher(
        applicable_languages={
            graph_model.GraphShardMetadataLanguage.JAVASCRIPT,
            graph_model.GraphShardMetadataLanguage.TSX,
        },
        applicable_node_label_types={
            "function_declaration",
            "generator_function_declaration",
            "function",
        },
        syntax_reader=javascript_function_declaration.reader,
    ),
    Dispatcher(
        applicable_languages={
            graph_model.GraphShardMetadataLanguage.KOTLIN,
        },
        applicable_node_label_types={
            "class_declaration",
            "function_declaration",
        },
        syntax_reader=kotlin_object_declaration.reader,
    ),
    Dispatcher(
        applicable_languages={
            graph_model.GraphShardMetadataLanguage.GO,
        },
        applicable_node_label_types={
            "call_expression",
        },
        syntax_reader=go_call_expression.reader,
    ),
    Dispatcher(
        applicable_languages={
            graph_model.GraphShardMetadataLanguage.KOTLIN,
        },
        applicable_node_label_types={
            "call_expression",
        },
        syntax_reader=kotlin_call_expression.reader,
    ),
    Dispatcher(
        applicable_languages={
            graph_model.GraphShardMetadataLanguage.JAVA,
        },
        applicable_node_label_types={
            "method_invocation",
        },
        syntax_reader=java_method_invocation.reader,
    ),
    Dispatcher(
        applicable_languages={
            graph_model.GraphShardMetadataLanguage.JAVASCRIPT,
            graph_model.GraphShardMetadataLanguage.TSX,
        },
        applicable_node_label_types={
            "call_expression",
        },
        syntax_reader=javascript_call_expression.reader,
    ),
    Dispatcher(
        applicable_languages={
            graph_model.GraphShardMetadataLanguage.CSHARP,
        },
        applicable_node_label_types={
            "invocation_expression",
        },
        syntax_reader=c_sharp_invocation_expression.reader,
    ),
    Dispatcher(
        applicable_languages={
            graph_model.GraphShardMetadataLanguage.CSHARP,
        },
        applicable_node_label_types={
            "argument",
        },
        syntax_reader=c_sharp_argument.reader,
    ),
    Dispatcher(
        applicable_languages={
            graph_model.GraphShardMetadataLanguage.JAVA,
        },
        applicable_node_label_types={
            "lambda_expression",
        },
        syntax_reader=java_lambda_expression.reader,
    ),
    Dispatcher(
        applicable_languages={
            graph_model.GraphShardMetadataLanguage.CSHARP,
        },
        applicable_node_label_types={
            "lambda_expression",
        },
        syntax_reader=c_sharp_lambda_expression.reader,
    ),
    Dispatcher(
        applicable_languages={
            graph_model.GraphShardMetadataLanguage.JAVASCRIPT,
            graph_model.GraphShardMetadataLanguage.TSX,
        },
        applicable_node_label_types={
            "arrow_function",
        },
        syntax_reader=javascript_arrrow_function.reader,
    ),
    Dispatcher(
        applicable_languages={
            graph_model.GraphShardMetadataLanguage.JAVA,
        },
        applicable_node_label_types={
            "array_access",
        },
        syntax_reader=java_array_access.reader,
    ),
    Dispatcher(
        applicable_languages={
            graph_model.GraphShardMetadataLanguage.CSHARP,
        },
        applicable_node_label_types={
            "element_access_expression",
        },
        syntax_reader=c_sharp_element_access_expression.reader,
    ),
    Dispatcher(
        applicable_languages={
            graph_model.GraphShardMetadataLanguage.JAVA,
            graph_model.GraphShardMetadataLanguage.CSHARP,
        },
        applicable_node_label_types={
            "object_creation_expression",
        },
        syntax_reader=common_object_creation_expression.reader,
    ),
    Dispatcher(
        applicable_languages={
            graph_model.GraphShardMetadataLanguage.JAVASCRIPT,
            graph_model.GraphShardMetadataLanguage.TSX,
        },
        applicable_node_label_types={
            "new_expression",
        },
        syntax_reader=javascript_new_expression.reader,
    ),
    Dispatcher(
        applicable_languages={
            graph_model.GraphShardMetadataLanguage.JAVA,
        },
        applicable_node_label_types={
            "array_creation_expression",
        },
        syntax_reader=java_array_creation_expression.reader,
    ),
    Dispatcher(
        applicable_languages={
            graph_model.GraphShardMetadataLanguage.CSHARP,
        },
        applicable_node_label_types={
            "array_creation_expression",
        },
        syntax_reader=c_sharp_array_creation_expression.reader,
    ),
    Dispatcher(
        applicable_languages={
            graph_model.GraphShardMetadataLanguage.JAVA,
        },
        applicable_node_label_types={
            "array_initializer",
        },
        syntax_reader=java_array_initializer.reader,
    ),
    Dispatcher(
        applicable_languages={
            graph_model.GraphShardMetadataLanguage.CSHARP,
        },
        applicable_node_label_types={
            "using_statement",
        },
        syntax_reader=c_sharp_using_statement.reader,
    ),
    Dispatcher(
        applicable_languages={
            graph_model.GraphShardMetadataLanguage.JAVASCRIPT,
            graph_model.GraphShardMetadataLanguage.TSX,
        },
        applicable_node_label_types={
            "ternary_expression",
        },
        syntax_reader=javascript_ternary_expression.reader,
    ),
    Dispatcher(
        applicable_languages={
            graph_model.GraphShardMetadataLanguage.GO,
            graph_model.GraphShardMetadataLanguage.JAVA,
            graph_model.GraphShardMetadataLanguage.CSHARP,
            graph_model.GraphShardMetadataLanguage.JAVASCRIPT,
            graph_model.GraphShardMetadataLanguage.TSX,
            graph_model.GraphShardMetadataLanguage.KOTLIN,
        },
        applicable_node_label_types={
            "boolean_literal",
            "character_literal",
            "composite_literal",
            "decimal_integer_literal",
            "false",
            "int_literal",
            "integer_literal",
            "number",
            "interpreted_string_literal",
            "floating_point_type",
            "line_string_literal",
            "nil",
            "null_literal",
            "null",
            "raw_string_literal",
            "real_literal",
            "string_literal",
            "string",
            "verbatim_string_literal",
            "true",
            "undefined",
        },
        syntax_reader=common_literal.reader,
    ),
    Dispatcher(
        applicable_languages={
            graph_model.GraphShardMetadataLanguage.JAVA,
        },
        applicable_node_label_types={
            "resource",
        },
        syntax_reader=java_resource.reader,
    ),
    Dispatcher(
        applicable_languages={
            graph_model.GraphShardMetadataLanguage.GO,
        },
        applicable_node_label_types={
            "return_statement",
        },
        syntax_reader=go_return_statement.reader,
    ),
    Dispatcher(
        applicable_languages={
            graph_model.GraphShardMetadataLanguage.JAVA,
            graph_model.GraphShardMetadataLanguage.JAVASCRIPT,
            graph_model.GraphShardMetadataLanguage.TSX,
            graph_model.GraphShardMetadataLanguage.CSHARP,
        },
        applicable_node_label_types={
            "return_statement",
        },
        syntax_reader=common_return_statement.reader,
    ),
    Dispatcher(
        applicable_languages={
            graph_model.GraphShardMetadataLanguage.JAVA,
            graph_model.GraphShardMetadataLanguage.KOTLIN,
        },
        applicable_node_label_types={
            "this",
            "this_expression",
        },
        syntax_reader=java_this.reader,
    ),
    Dispatcher(
        applicable_languages={
            graph_model.GraphShardMetadataLanguage.CSHARP,
        },
        applicable_node_label_types={
            "member_access_expression",
        },
        syntax_reader=c_sharp_member_access_expression.reader,
    ),
    Dispatcher(
        applicable_languages={
            graph_model.GraphShardMetadataLanguage.CSHARP,
        },
        applicable_node_label_types={
            "parameter",
        },
        syntax_reader=c_sharp_parameter.reader,
    ),
    Dispatcher(
        applicable_languages={
            graph_model.GraphShardMetadataLanguage.JAVASCRIPT,
            graph_model.GraphShardMetadataLanguage.TSX,
        },
        applicable_node_label_types={
            "await_expression",
        },
        syntax_reader=javascript_await_expression.reader,
    ),
    Dispatcher(
        applicable_languages={
            graph_model.GraphShardMetadataLanguage.JAVASCRIPT,
            graph_model.GraphShardMetadataLanguage.TSX,
        },
        applicable_node_label_types={
            "member_expression",
        },
        syntax_reader=javascript_member_expression.reader,
    ),
    Dispatcher(
        applicable_languages={
            graph_model.GraphShardMetadataLanguage.JAVASCRIPT,
            graph_model.GraphShardMetadataLanguage.TSX,
        },
        applicable_node_label_types={
            "formal_parameters",
        },
        syntax_reader=javascript_formal_parameters.reader,
    ),
    Dispatcher(
        applicable_languages={
            graph_model.GraphShardMetadataLanguage.JAVASCRIPT,
            graph_model.GraphShardMetadataLanguage.TSX,
        },
        applicable_node_label_types={
            "do_statement",
        },
        syntax_reader=javascript_do_statement.reader,
    ),
    Dispatcher(
        applicable_languages={
            graph_model.GraphShardMetadataLanguage.JAVASCRIPT,
            graph_model.GraphShardMetadataLanguage.TSX,
        },
        applicable_node_label_types={
            "template_string",
        },
        syntax_reader=javascript_template_string.reader,
    ),
    Dispatcher(
        applicable_languages={
            graph_model.GraphShardMetadataLanguage.JAVASCRIPT,
            graph_model.GraphShardMetadataLanguage.TSX,
        },
        applicable_node_label_types={
            "object",
        },
        syntax_reader=javascript_object.reader,
    ),
    Dispatcher(
        applicable_languages={
            graph_model.GraphShardMetadataLanguage.JAVASCRIPT,
            graph_model.GraphShardMetadataLanguage.TSX,
        },
        applicable_node_label_types={
            "for_in_statement",
        },
        syntax_reader=javascript_for_in_statement.reader,
    ),
    Dispatcher(
        applicable_languages={
            graph_model.GraphShardMetadataLanguage.JAVASCRIPT,
            graph_model.GraphShardMetadataLanguage.TSX,
        },
        applicable_node_label_types={
            "array",
        },
        syntax_reader=javascript_array.reader,
    ),
    Dispatcher(
        applicable_languages={
            graph_model.GraphShardMetadataLanguage.JAVASCRIPT,
            graph_model.GraphShardMetadataLanguage.TSX,
        },
        applicable_node_label_types={
            "for_statement",
        },
        syntax_reader=javascript_for_statement.reader,
    ),
    Dispatcher(
        applicable_languages={
            graph_model.GraphShardMetadataLanguage.JAVASCRIPT,
            graph_model.GraphShardMetadataLanguage.TSX,
        },
        applicable_node_label_types={
            "switch_statement",
        },
        syntax_reader=javascript_switch_statement.reader,
    ),
    Dispatcher(
        applicable_languages={
            graph_model.GraphShardMetadataLanguage.JAVASCRIPT,
            graph_model.GraphShardMetadataLanguage.TSX,
        },
        applicable_node_label_types={
            "switch_case",
        },
        syntax_reader=javascript_switch_case.reader,
    ),
    Dispatcher(
        applicable_languages={
            graph_model.GraphShardMetadataLanguage.JAVASCRIPT,
            graph_model.GraphShardMetadataLanguage.TSX,
        },
        applicable_node_label_types={
            "switch_default",
        },
        syntax_reader=javascript_switch_default.reader,
    ),
    Dispatcher(
        applicable_languages={
            graph_model.GraphShardMetadataLanguage.JAVASCRIPT,
            graph_model.GraphShardMetadataLanguage.TSX,
        },
        applicable_node_label_types={
            "subscript_expression",
        },
        syntax_reader=javascript_subscript_expression.reader,
    ),
    Dispatcher(
        applicable_languages={
            graph_model.GraphShardMetadataLanguage.JAVASCRIPT,
            graph_model.GraphShardMetadataLanguage.TSX,
        },
        applicable_node_label_types={
            "import_statement",
        },
        syntax_reader=javascript_import_statement.reader,
    ),
    *[
        Dispatcher(
            applicable_languages={
                graph_model.GraphShardMetadataLanguage.CSHARP,
                graph_model.GraphShardMetadataLanguage.GO,
                graph_model.GraphShardMetadataLanguage.JAVA,
                graph_model.GraphShardMetadataLanguage.JAVASCRIPT,
                graph_model.GraphShardMetadataLanguage.TSX,
            },
            applicable_node_label_types={applicable_node_label_type},
            syntax_reader=common_noop.reader,
        )
        for applicable_node_label_type in (
            "block",
            "statement_block",
            "break_statement",
            "class_body",
            "class_declaration",
            "constructor_body",
            "continue_statement",
            "comment",
            "expression_statement",
            "finally_clause",
            "resource_specification",
            "try_statement",
            "try_with_resources_statement",
            "throw_statement",
            "update_expression",
            "argument_list",
            ";",
            "-",
            "+",
            "*",
            "/",
            "%",
            "(",
            ")",
            ".",
            "{",
            "}",
            "program",
        )
    ],
)
DISPATCHERS_BY_LANG: Dict[
    graph_model.GraphShardMetadataLanguage,
    Dispatchers,
] = {
    language: tuple(
        dispatcher
        for dispatcher in DISPATCHERS
        if language in dispatcher.applicable_languages
    )
    for language in graph_model.GraphShardMetadataLanguage
}
