# pylint: disable=import-error

import dateutil

from ariadne import ScalarType

DATETIME_SCALAR = ScalarType('DateTime')


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
