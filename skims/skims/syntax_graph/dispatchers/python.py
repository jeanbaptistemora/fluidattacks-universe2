from syntax_graph.syntax_readers.python import (
    argument_list as python_argument_list,
    assignment as python_assignment,
    attribute as python_attribute,
    call as python_call,
    class_definition as python_class_definition,
    except_clause as python_except_clause,
    execution_block as python_execution_block,
    expression_statement as python_expression_statement,
    finally_clause as python_finally_clause,
    for_statement as python_for_statement,
    function_definition as python_function_definition,
    identifier as python_identifier,
    if_statement as python_if_statement,
    import_statement as python_import_statement,
    list as python_list,
    module as python_module,
    parameters as python_parameters,
    reserved_word as python_reserved_word,
    try_statement as python_try_statement,
    tuple as python_tuple,
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
            "parameters",
        },
        syntax_reader=python_parameters.reader,
    ),
    Dispatcher(
        applicable_types={
            "return",
            "in",
        },
        syntax_reader=python_reserved_word.reader,
    ),
    Dispatcher(
        applicable_types={
            "try_statement",
        },
        syntax_reader=python_try_statement.reader,
    ),
    Dispatcher(
        applicable_types={
            "tuple",
        },
        syntax_reader=python_tuple.reader,
    ),
    Dispatcher(
        applicable_types={
            "while_statement",
        },
        syntax_reader=python_while_statement.reader,
    ),
)
