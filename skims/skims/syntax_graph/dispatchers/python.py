from syntax_graph.syntax_readers.python import (
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
            "module",
        },
        syntax_reader=python_module.reader,
    ),
    Dispatcher(
        applicable_types={
            "import_statement",
        },
        syntax_reader=python_import_statement.reader,
    ),
)
