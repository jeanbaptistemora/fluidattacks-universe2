from syntax_graph.syntax_readers.go import (
    argument_list as go_argument_list,
    assignment_statement as go_assignment_statement,
    binary_expression as go_binary_expression,
    block as go_block,
    call_expression as go_call_expression,
    comment as go_comment,
    composite_literal as go_composite_literal,
    expression_list as go_expression_list,
    function_declaration as go_function_declaration,
    identifier as go_identifier,
    if_statement as go_if_statement,
    import_declaration as go_import_declaration,
    int_literal as go_int_literal,
    literal_value as go_literal_value,
    nil as go_nil,
    package_clause as go_package_clause,
    parameter_declaration as go_parameter_declaration,
    parameter_list as go_parameter_list,
    qualified_type as go_qualified_type,
    return_statement as go_return_statement,
    selector_expression as go_selector_expression,
    source_file as go_source_file,
    string_literal as go_string_literal,
    type_declaration as go_type_declaration,
    unary_expression as go_unary_expression,
    var_declaration as go_var_declaration,
)
from syntax_graph.types import (
    Dispatcher,
    Dispatchers,
)

GO_DISPATCHERS: Dispatchers = (
    Dispatcher(
        applicable_types={
            "argument_list",
        },
        syntax_reader=go_argument_list.reader,
    ),
    Dispatcher(
        applicable_types={
            "assignment_statement",
            "short_var_declaration",
        },
        syntax_reader=go_assignment_statement.reader,
    ),
    Dispatcher(
        applicable_types={
            "block",
        },
        syntax_reader=go_block.reader,
    ),
    Dispatcher(
        applicable_types={
            "binary_expression",
        },
        syntax_reader=go_binary_expression.reader,
    ),
    Dispatcher(
        applicable_types={
            "call_expression",
        },
        syntax_reader=go_call_expression.reader,
    ),
    Dispatcher(
        applicable_types={
            "comment",
        },
        syntax_reader=go_comment.reader,
    ),
    Dispatcher(
        applicable_types={
            "composite_literal",
        },
        syntax_reader=go_composite_literal.reader,
    ),
    Dispatcher(
        applicable_types={
            "expression_list",
        },
        syntax_reader=go_expression_list.reader,
    ),
    Dispatcher(
        applicable_types={
            "func_literal",
            "function_declaration",
            "method_declaration",
        },
        syntax_reader=go_function_declaration.reader,
    ),
    Dispatcher(
        applicable_types={
            "blank_identifier",
            "identifier",
            "field_identifier",
            "package_identifier",
            "type_identifier",
        },
        syntax_reader=go_identifier.reader,
    ),
    Dispatcher(
        applicable_types={
            "literal_value",
        },
        syntax_reader=go_literal_value.reader,
    ),
    Dispatcher(
        applicable_types={
            "if_statement",
        },
        syntax_reader=go_if_statement.reader,
    ),
    Dispatcher(
        applicable_types={
            "import_declaration",
        },
        syntax_reader=go_import_declaration.reader,
    ),
    Dispatcher(
        applicable_types={
            "int_literal",
        },
        syntax_reader=go_int_literal.reader,
    ),
    Dispatcher(
        applicable_types={
            "nil",
        },
        syntax_reader=go_nil.reader,
    ),
    Dispatcher(
        applicable_types={
            "package_clause",
        },
        syntax_reader=go_package_clause.reader,
    ),
    Dispatcher(
        applicable_types={
            "parameter_declaration",
        },
        syntax_reader=go_parameter_declaration.reader,
    ),
    Dispatcher(
        applicable_types={
            "parameter_list",
        },
        syntax_reader=go_parameter_list.reader,
    ),
    Dispatcher(
        applicable_types={
            "qualified_type",
        },
        syntax_reader=go_qualified_type.reader,
    ),
    Dispatcher(
        applicable_types={
            "return_statement",
        },
        syntax_reader=go_return_statement.reader,
    ),
    Dispatcher(
        applicable_types={
            "selector_expression",
        },
        syntax_reader=go_selector_expression.reader,
    ),
    Dispatcher(
        applicable_types={
            "source_file",
        },
        syntax_reader=go_source_file.reader,
    ),
    Dispatcher(
        applicable_types={
            "interpreted_string_literal",
            "raw_string_literal",
        },
        syntax_reader=go_string_literal.reader,
    ),
    Dispatcher(
        applicable_types={
            "type_declaration",
        },
        syntax_reader=go_type_declaration.reader,
    ),
    Dispatcher(
        applicable_types={
            "unary_expression",
        },
        syntax_reader=go_unary_expression.reader,
    ),
    Dispatcher(
        applicable_types={
            "var_declaration",
        },
        syntax_reader=go_var_declaration.reader,
    ),
)
