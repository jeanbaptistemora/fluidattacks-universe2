from syntax_graph.syntax_readers.json import (
    document as json_document,
)
from syntax_graph.types import (
    Dispatcher,
    Dispatchers,
)

JSON_DISPATCHERS: Dispatchers = (
    Dispatcher(
        applicable_types={
            "document",
        },
        syntax_reader=json_document.reader,
    ),
)
