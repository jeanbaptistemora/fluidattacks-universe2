from syntax_graph.syntax_readers.json import (
    array as json_array,
    boolean as json_boolean,
    comment as json_comment,
    document as json_document,
    number as json_number,
    object as json_object,
    pair as json_pair,
    string as json_string,
)
from syntax_graph.types import (
    Dispatcher,
    Dispatchers,
)

JSON_DISPATCHERS: Dispatchers = (
    Dispatcher(
        applicable_types={
            "array",
        },
        syntax_reader=json_array.reader,
    ),
    Dispatcher(
        applicable_types={
            "false",
            "true",
        },
        syntax_reader=json_boolean.reader,
    ),
    Dispatcher(
        applicable_types={
            "comment",
        },
        syntax_reader=json_comment.reader,
    ),
    Dispatcher(
        applicable_types={
            "document",
        },
        syntax_reader=json_document.reader,
    ),
    Dispatcher(
        applicable_types={
            "number",
        },
        syntax_reader=json_number.reader,
    ),
    Dispatcher(
        applicable_types={
            "object",
        },
        syntax_reader=json_object.reader,
    ),
    Dispatcher(
        applicable_types={
            "pair",
        },
        syntax_reader=json_pair.reader,
    ),
    Dispatcher(
        applicable_types={
            "string",
        },
        syntax_reader=json_string.reader,
    ),
)
