from syntax_graph.syntax_readers.common import (
    identifier as common_identifier,
    program as common_program,
    variable_declarator as common_variable_declarator,
)
from syntax_graph.syntax_readers.javascript import (
    lexical_declaration as javascript_lexical_declaration,
)
from syntax_graph.types import (
    Dispatcher,
    Dispatchers,
)

JAVASCRIPT_DISPATCHERS: Dispatchers = (
    Dispatcher(
        applicable_types={
            "identifier",
        },
        syntax_reader=common_identifier.reader,
    ),
    Dispatcher(
        applicable_types={
            "lexical_declaration",
        },
        syntax_reader=javascript_lexical_declaration.reader,
    ),
    Dispatcher(
        applicable_types={
            "program",
        },
        syntax_reader=common_program.reader,
    ),
    Dispatcher(
        applicable_types={
            "variable_declarator",
        },
        syntax_reader=common_variable_declarator.reader,
    ),
)
