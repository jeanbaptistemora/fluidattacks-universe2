from syntax_graph.syntax_readers.python import (
    function_definition as python_function_definition,
    identifier as python_identifier,
    import_statement as python_import_statement,
    module as python_module,
)
from syntax_graph.types import (
    Dispatcher,
    Dispatchers,
)

PYTHON_DISPATCHERS: Dispatchers = (
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
)
