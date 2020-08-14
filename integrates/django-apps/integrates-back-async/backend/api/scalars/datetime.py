import dateutil

from ariadne import ScalarType

DATETIME_SCALAR = ScalarType('DateTime')


@DATETIME_SCALAR.serializer
def serialize_datetime(value):
    if isinstance(value, str):
        value = dateutil.parser.parse(value)

    return value.isoformat()


@DATETIME_SCALAR.value_parser
def parse_datetime_value(value):
    if value:
        return dateutil.parser.parse(value)

    return value


@DATETIME_SCALAR.literal_parser
def parse_datetime_literal(ast):
    value = str(ast.value) if ast.value else ast.value

    return parse_datetime_value(value)
