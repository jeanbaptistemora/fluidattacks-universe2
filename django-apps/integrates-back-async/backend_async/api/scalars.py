# pylint: disable=import-error

import json
import dateutil

from ariadne import ScalarType

DATETIME_SCALAR = ScalarType("DateTime")
JSON_STRING_SCALAR = ScalarType("JSONString")


@DATETIME_SCALAR.serializer
def serialize_datetime(value):
    return value.isoformat()


@DATETIME_SCALAR.value_parser
def parse_datetime_value(value):
    return dateutil.parser.parse(value)


@DATETIME_SCALAR.literal_parser
def parse_datetime_literal(ast):
    value = str(ast.value)
    return parse_datetime_value(value)


@JSON_STRING_SCALAR.serializer
def serialize_jsonstring(value):
    return json.dumps(value)


@JSON_STRING_SCALAR.value_parser
def parse_jsonstring_value(value):
    return json.loads(value)


@JSON_STRING_SCALAR.literal_parser
def parse_jsonstring_literal(ast):
    value = str(ast.value)
    return json.loads(value)
