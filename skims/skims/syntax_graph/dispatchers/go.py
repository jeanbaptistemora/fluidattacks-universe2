from syntax_graph.syntax_readers.go import (
    assignment_statement as go_assignment_statement,
    block as go_block,
    expression_list as go_expression_list,
    function_declaration as go_function_declaration,
    identifier as go_identifier,
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
            "expression_list",
        },
        syntax_reader=go_expression_list.reader,
    ),
    Dispatcher(
        applicable_types={
            "function_declaration",
        },
        syntax_reader=go_function_declaration.reader,
    ),
    Dispatcher(
        applicable_types={
            "identifier",
        },
        syntax_reader=go_identifier.reader,
    ),
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
