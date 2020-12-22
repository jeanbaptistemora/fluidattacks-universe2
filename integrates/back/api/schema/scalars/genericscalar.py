from graphql.language.ast import (
    StringValueNode,
    BooleanValueNode,
    IntValueNode,
    FloatValueNode,
    ListValueNode,
    ObjectValueNode
)

from ariadne import ScalarType

GENERIC_SCALAR = ScalarType('GenericScalar')


@GENERIC_SCALAR.serializer
def serialize_genericscalar(value):
    return value


@GENERIC_SCALAR.value_parser
def parse_genericscalar_value(value):
    return value


@GENERIC_SCALAR.literal_parser
def parse_genericscalar_literal(ast):
    if isinstance(ast, (StringValueNode, BooleanValueNode)):
        return ast.value
    if isinstance(ast, IntValueNode):
        return int(ast.value)
    if isinstance(ast, FloatValueNode):
        return float(ast.value)
    if isinstance(ast, ListValueNode):
        return [parse_genericscalar_literal(value) for value in ast.values]
    if isinstance(ast, ObjectValueNode):
        return {
            field.name.value: parse_genericscalar_literal(field.value)
            for field in ast.fields
        }
    return None
