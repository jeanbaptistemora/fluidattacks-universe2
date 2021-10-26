from syntax_graph.syntax_readers.c_sharp import (
    compilation_unit as c_sharp_compilation_unit,
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
)
