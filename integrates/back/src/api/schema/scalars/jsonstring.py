from ariadne import (
    ScalarType,
)
import json
from typing import (
    Any,
)

JSON_STRING_SCALAR = ScalarType("JSONString")


@JSON_STRING_SCALAR.serializer
def serialize_jsonstring(value: Any) -> str:
    return json.dumps(value)


@JSON_STRING_SCALAR.value_parser
def parse_jsonstring_value(value: str) -> Any:
    return json.loads(value)


@JSON_STRING_SCALAR.literal_parser  # type: ignore
def parse_jsonstring_literal(ast: Any) -> Any:
    value = str(ast.value)
    return json.loads(value)
