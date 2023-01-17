from syntax_graph.syntax_readers.hcl import (
    source_file as hcl_source_file,
)
from syntax_graph.types import (
    Dispatcher,
    Dispatchers,
)

HCL_DISPATCHERS: Dispatchers = (
    Dispatcher(
        applicable_types={
            "source_file",
        },
        syntax_reader=hcl_source_file.reader,
    ),
)
