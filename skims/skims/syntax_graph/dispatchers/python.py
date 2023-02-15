from syntax_graph.syntax_readers.python import (
    argument as python_argument,
    argument_list as python_argument_list,
    array as python_array,
    as_pattern as python_as_pattern,
    assert_statement as python_assert_statement,
    assignment as python_assignment,
    attribute as python_attribute,
    await_expression as python_await_expression,
    binary_expression as python_binary_expression,
    boolean_literal as python_boolean_literal,
    break_statement as python_break_statement,
    call as python_call,
    class_definition as python_class_definition,
    comment as python_comment,
    comprehension as python_comprehension,
    continue_statement as python_continue_statement,
    decorated_definition as python_decorated_definition,
    decorator as python_decorator,
    dictionary as python_dictionary,
    else_clause as python_else_clause,
    except_clause as python_except_clause,
    execution_block as python_execution_block,
    expression_statement as python_expression_statement,
    finally_clause as python_finally_clause,
    for_in_clause as python_for_in_clause,
    for_statement as python_for_statement,
    function_definition as python_function_definition,
    identifier as python_identifier,
    if_clause as python_if_clause,
    if_statement as python_if_statement,
    import_statement as python_import_statement,
    list as python_list,
    module as python_module,
    named_expression as python_named_expression,
    not_operator as python_not_operator,
    number_literal as python_number_literal,
    pair as python_pair,
    parameter as python_parameter,
    parameters as python_parameters,
    parenthesized_expression as python_parenthesized_expression,
    raise_statement as python_raise_statement,
    reserved_word as python_reserved_word,
    return_statement as python_return_statement,
    splat_pattern as python_splat_pattern,
    string_literal as python_string_literal,
    subscript as python_subscript,
    try_statement as python_try_statement,
    using_statement as python_using_statement,
    while_statement as python_while_statement,
)
from syntax_graph.types import (
    Dispatcher,
    Dispatchers,
)

PYTHON_DISPATCHERS: Dispatchers = (
    Dispatcher(
        applicable_types={
            "argument_list",
        },
        syntax_reader=python_argument_list.reader,
    ),
    Dispatcher(
        applicable_types={
            "keyword_argument",
        },
        syntax_reader=python_argument.reader,
    ),
    Dispatcher(
        applicable_types={
            "list",
            "tuple",
            "tuple_pattern",
            "pattern_list",
            "set",
        },
        syntax_reader=python_array.reader,
    ),
    Dispatcher(
        applicable_types={
            "as_pattern",
        },
        syntax_reader=python_as_pattern.reader,
    ),
    Dispatcher(
        applicable_types={
            "assert_statement",
        },
        syntax_reader=python_assert_statement.reader,
    ),
    Dispatcher(
        applicable_types={
            "assignment",
        },
        syntax_reader=python_assignment.reader,
    ),
    Dispatcher(
        applicable_types={
            "attribute",
        },
        syntax_reader=python_attribute.reader,
    ),
    Dispatcher(
        applicable_types={
            "await",
        },
        syntax_reader=python_await_expression.reader,
    ),
    Dispatcher(
        applicable_types={
            "augmented_assignment",
            "binary_operator",
            "boolean_operator",
            "comparison_operator",
        },
        syntax_reader=python_binary_expression.reader,
    ),
    Dispatcher(
        applicable_types={
            "false",
            "true",
        },
        syntax_reader=python_boolean_literal.reader,
    ),
    Dispatcher(
        applicable_types={
            "break_statement",
        },
        syntax_reader=python_break_statement.reader,
    ),
    Dispatcher(
        applicable_types={
            "call",
        },
        syntax_reader=python_call.reader,
    ),
    Dispatcher(
        applicable_types={
            "class_definition",
        },
        syntax_reader=python_class_definition.reader,
    ),
    Dispatcher(
        applicable_types={
            "comment",
        },
        syntax_reader=python_comment.reader,
    ),
    Dispatcher(
        applicable_types={
            "continue_statement",
            "pass_statement",
        },
        syntax_reader=python_continue_statement.reader,
    ),
    Dispatcher(
        applicable_types={
            "decorated_definition",
        },
        syntax_reader=python_decorated_definition.reader,
    ),
    Dispatcher(
        applicable_types={
            "decorator",
        },
        syntax_reader=python_decorator.reader,
    ),
    Dispatcher(
        applicable_types={
            "dictionary",
        },
        syntax_reader=python_dictionary.reader,
    ),
    Dispatcher(
        applicable_types={
            "else_clause",
        },
        syntax_reader=python_else_clause.reader,
    ),
    Dispatcher(
        applicable_types={
            "except_clause",
        },
        syntax_reader=python_except_clause.reader,
    ),
    Dispatcher(
        applicable_types={
            "block",
        },
        syntax_reader=python_execution_block.reader,
    ),
    Dispatcher(
        applicable_types={
            "expression_statement",
        },
        syntax_reader=python_expression_statement.reader,
    ),
    Dispatcher(
        applicable_types={
            "finally_clause",
        },
        syntax_reader=python_finally_clause.reader,
    ),
    Dispatcher(
        applicable_types={
            "for_in_clause",
        },
        syntax_reader=python_for_in_clause.reader,
    ),
    Dispatcher(
        applicable_types={
            "for_statement",
        },
        syntax_reader=python_for_statement.reader,
    ),
    Dispatcher(
        applicable_types={
            "function_definition",
        },
        syntax_reader=python_function_definition.reader,
    ),
    Dispatcher(
        applicable_types={
            "identifier",
        },
        syntax_reader=python_identifier.reader,
    ),
    Dispatcher(
        applicable_types={
            "if_clause",
        },
        syntax_reader=python_if_clause.reader,
    ),
    Dispatcher(
        applicable_types={
            "elif_clause",
            "if_statement",
        },
        syntax_reader=python_if_statement.reader,
    ),
    Dispatcher(
        applicable_types={
            "import_from_statement",
            "import_statement",
        },
        syntax_reader=python_import_statement.reader,
    ),
    Dispatcher(
        applicable_types={
            "dictionary_comprehension",
            "list_comprehension",
            "set_comprehension",
        },
        syntax_reader=python_comprehension.reader,
    ),
    Dispatcher(
        applicable_types={
            "list",
        },
        syntax_reader=python_list.reader,
    ),
    Dispatcher(
        applicable_types={
            "module",
        },
        syntax_reader=python_module.reader,
    ),
    Dispatcher(
        applicable_types={
            "named_expression",
        },
        syntax_reader=python_named_expression.reader,
    ),
    Dispatcher(
        applicable_types={
            "not_operator",
        },
        syntax_reader=python_not_operator.reader,
    ),
    Dispatcher(
        applicable_types={
            "integer",
            "float",
        },
        syntax_reader=python_number_literal.reader,
    ),
    Dispatcher(
        applicable_types={
            "pair",
        },
        syntax_reader=python_pair.reader,
    ),
    Dispatcher(
        applicable_types={
            "default_parameter",
            "parameter",
            "typed_parameter",
            "typed_default_parameter",
            "keyword_argument",
        },
        syntax_reader=python_parameter.reader,
    ),
    Dispatcher(
        applicable_types={
            "parameters",
        },
        syntax_reader=python_parameters.reader,
    ),
    Dispatcher(
        applicable_types={
            "parenthesized_expression",
        },
        syntax_reader=python_parenthesized_expression.reader,
    ),
    Dispatcher(
        applicable_types={
            "raise_statement",
        },
        syntax_reader=python_raise_statement.reader,
    ),
    Dispatcher(
        applicable_types={
            "in",
            "none",
            "pass",
            "return",
        },
        syntax_reader=python_reserved_word.reader,
    ),
    Dispatcher(
        applicable_types={
            "return_statement",
            "yield",
        },
        syntax_reader=python_return_statement.reader,
    ),
    Dispatcher(
        applicable_types={
            "list_splat_pattern",
            "dictionary_splat_pattern",
        },
        syntax_reader=python_splat_pattern.reader,
    ),
    Dispatcher(
        applicable_types={
            "string",
        },
        syntax_reader=python_string_literal.reader,
    ),
    Dispatcher(
        applicable_types={
            "subscript",
        },
        syntax_reader=python_subscript.reader,
    ),
    Dispatcher(
        applicable_types={
            "try_statement",
        },
        syntax_reader=python_try_statement.reader,
    ),
    Dispatcher(
        applicable_types={
            "with_statement",
        },
        syntax_reader=python_using_statement.reader,
    ),
    Dispatcher(
        applicable_types={
            "while_statement",
        },
        syntax_reader=python_while_statement.reader,
    ),
)
