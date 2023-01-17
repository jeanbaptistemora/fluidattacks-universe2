from syntax_graph.syntax_readers.yaml import (
    stream as yaml_stream,
)
from syntax_graph.types import (
    Dispatcher,
    Dispatchers,
)

YAML_DISPATCHERS: Dispatchers = (
    Dispatcher(
        applicable_types={
            "stream",
        },
        syntax_reader=yaml_stream.reader,
    ),
)
