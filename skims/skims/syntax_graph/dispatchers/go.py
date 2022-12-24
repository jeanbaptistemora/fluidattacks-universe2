from syntax_graph.syntax_readers.go import (
    import_declaration as go_import_declaration,
    package_clause as go_package_clause,
    source_file as go_source_file,
)
from syntax_graph.types import (
    Dispatcher,
    Dispatchers,
)

GO_DISPATCHERS: Dispatchers = (
    Dispatcher(
        applicable_types={
            "import_declaration",
        },
        syntax_reader=go_import_declaration.reader,
    ),
    Dispatcher(
        applicable_types={
            "package_clause",
        },
        syntax_reader=go_package_clause.reader,
    ),
    Dispatcher(
        applicable_types={
            "source_file",
        },
        syntax_reader=go_source_file.reader,
    ),
)
