from ariadne import (
    ScalarType,
)
import dateutil.parser  # type: ignore
from typing import (
    Any,
)

DATETIME_SCALAR = ScalarType("DateTime")


@DATETIME_SCALAR.serializer
def serialize_datetime(value: Any) -> Any:
    if isinstance(value, str):
        value = dateutil.parser.parse(value)
    return value.isoformat()


@DATETIME_SCALAR.value_parser
def parse_datetime_value(value: Any) -> Any:
    if value:
        return dateutil.parser.parse(value)
    return value


@DATETIME_SCALAR.literal_parser
def parse_datetime_literal(ast: Any) -> Any:
    value = str(ast.value) if ast.value else ast.value
    return parse_datetime_value(value)
