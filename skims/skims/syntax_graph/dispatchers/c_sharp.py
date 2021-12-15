from syntax_graph.syntax_readers.c_sharp import (
    argument as c_sharp_argument,
    argument_list as c_sharp_argument_list,
    assignment_expression as c_sharp_assignment_expression,
    binary_expression as c_sharp_binary_expression,
    bracketed_argument_list as c_sharp_bracketed_argument_list,
    class_declaration as c_sharp_class_declaration,
    comment as c_sharp_comment,
    compilation_unit as c_sharp_compilation_unit,
    element_access_expression as c_sharp_element_access_expression,
    expression_statement as c_sharp_expression_statement,
    if_statement as c_sharp_if_statement,
    invocation_expression as c_sharp_invocation_expression,
    local_declaration_statement as c_sharp_local_declaration_statement,
    member_access_expression as c_sharp_member_access_expression,
    method_declaration as c_sharp_method_declaration,
    namespace_declaration as c_sharp_namespace_declaration,
    object_creation_expression as c_sharp_object_creation_expression,
    parameter as c_sharp_parameter,
    parameter_list as c_sharp_parameter_list,
    prefix_expression as c_sharp_prefix_expression,
    return_statement as c_sharp_return_statement,
    throw_statement as c_sharp_throw_statement,
    type_of_expression as c_sharp_type_of_expression,
    using_directive as c_sharp_using_directive,
    variable_declaration as c_sharp_variable_declaration,
)
from syntax_graph.syntax_readers.common import (
    boolean_literal as common_boolean_literal,
    declaration_block as common_declaration_block,
    execution_block as common_execution_block,
    identifier as common_identifier,
    null_literal as common_null_literal,
    number_literal as common_number_literal,
    string_literal as common_string_literal,
)
from syntax_graph.types import (
    Dispatcher,
    Dispatchers,
)

CSHARP_DISPATCHERS: Dispatchers = (
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
            "assignment_expression",
        },
        syntax_reader=c_sharp_assignment_expression.reader,
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
            "declaration_list",
        },
        syntax_reader=common_declaration_block.reader,
    ),
    Dispatcher(
        applicable_types={
            "element_access_expression",
        },
        syntax_reader=c_sharp_element_access_expression.reader,
    ),
    Dispatcher(
        applicable_types={
            "expression_statement",
        },
        syntax_reader=c_sharp_expression_statement.reader,
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
            "invocation_expression",
        },
        syntax_reader=c_sharp_invocation_expression.reader,
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
            "method_declaration",
        },
        syntax_reader=c_sharp_method_declaration.reader,
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
            "prefix_unary_expression",
        },
        syntax_reader=c_sharp_prefix_expression.reader,
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
        },
        syntax_reader=common_string_literal.reader,
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
            "using_directive",
        },
        syntax_reader=c_sharp_using_directive.reader,
    ),
    Dispatcher(
        applicable_types={
            "variable_declaration",
        },
        syntax_reader=c_sharp_variable_declaration.reader,
    ),
)
