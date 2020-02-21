# Standard library
from decimal import Decimal


def transform_to_json(obj):
    """ Turn any input into valid JSON types """
    if isinstance(obj, (str, int, float, bool, type(None))):
        return obj
    if isinstance(obj, Decimal):
        return float(obj)
    if isinstance(obj, (list, tuple)):
        return list(map(transform_to_json, obj))
    if isinstance(obj, dict):
        return {key: transform_to_json(value) for key, value in obj.items()}
    if hasattr(obj, '__str__'):
        return str(obj)

    return None
