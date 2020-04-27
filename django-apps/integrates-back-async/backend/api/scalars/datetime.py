from datetime import datetime
import dateutil

from ariadne import ScalarType

DATETIME_SCALAR = ScalarType('DateTime')

DYNAMO_DB_DATE_FORMAT = '%Y-%m-%dT%H:%M:%S.%f%z'


@DATETIME_SCALAR.serializer
def serialize_datetime(value):
    if isinstance(value, str):
        value = datetime.strptime(value, DYNAMO_DB_DATE_FORMAT)
    return value.isoformat()


@DATETIME_SCALAR.value_parser
def parse_datetime_value(value):
    return dateutil.parser.parse(value)


@DATETIME_SCALAR.literal_parser
def parse_datetime_literal(ast):
    value = str(ast.value)
    return parse_datetime_value(value)
