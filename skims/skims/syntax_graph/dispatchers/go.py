from syntax_graph.syntax_readers.go import (
    source_file as go_source_file,
)
from syntax_graph.types import (
    Dispatcher,
    Dispatchers,
)

GO_DISPATCHERS: Dispatchers = (
    Dispatcher(
        applicable_types={
            "source_file",
        },
        syntax_reader=go_source_file.reader,
    ),
)
