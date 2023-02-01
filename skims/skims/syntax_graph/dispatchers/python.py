from syntax_graph.syntax_readers.python import (
    argument_list as python_argument_list,
    assignment as python_assignment,
    attribute as python_attribute,
    function_definition as python_function_definition,
    identifier as python_identifier,
    import_statement as python_import_statement,
    module as python_module,
    parameters as python_parameters,
    reserved_word as python_reserved_word,
    tuple as python_tuple,
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
            "import_statement",
        },
        syntax_reader=python_import_statement.reader,
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
            "tuple",
        },
        syntax_reader=python_tuple.reader,
    ),
)
