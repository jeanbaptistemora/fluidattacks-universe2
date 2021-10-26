from syntax_graph.syntax_readers.c_sharp import (
    compilation_unit as c_sharp_compilation_unit,
    namespace_declaration as c_sharp_namespace_declaration,
)
from syntax_graph.syntax_readers.common import (
    block as common_block,
)
from syntax_graph.types import (
    Dispatcher,
    Dispatchers,
)

CSHARP_DISPATCHERS: Dispatchers = (
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
        syntax_reader=common_block.reader,
    ),
    Dispatcher(
        applicable_types={
            "namespace_declaration",
        },
        syntax_reader=c_sharp_namespace_declaration.reader,
    ),
)
