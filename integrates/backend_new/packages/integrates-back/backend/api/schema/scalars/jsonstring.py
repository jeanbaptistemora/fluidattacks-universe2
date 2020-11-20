import json

from ariadne import ScalarType

JSON_STRING_SCALAR = ScalarType('JSONString')


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
