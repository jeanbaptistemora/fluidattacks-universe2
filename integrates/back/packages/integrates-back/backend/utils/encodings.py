# Standard library
import json
from datetime import datetime
from typing import (
    Any, cast, Dict,
)

from newutils import datetime as datetime_utils


def safe_encode(string: str) -> str:
    """Turn a utf-8 string into a string of [a-z0-9] characters."""
    return string.encode('utf-8').hex().lower()


def safe_decode(hexstr: str) -> str:
    """Inverse of safe_encode."""
    return bytes.fromhex(hexstr).decode('utf-8')


def mapping_to_key(mapping: Dict[str, str]) -> str:
    """Turn a mapping of str to str into a str suitable for use in DynamoDB."""
    if not mapping:
        raise ValueError('Empty parameters')

    if not all(
        isinstance(obj, str)
        for arguments in mapping.items()
        for obj in arguments
    ):
        raise TypeError(f'Expected Dict[str, str], got: {type(mapping)}')

    return '/'.join([
        ':'.join([
            attribute_name,
            safe_encode(attribute_value),
        ])
        for attribute_name, attribute_value in mapping.items()
    ])


def key_to_mapping(key: str) -> Dict[str, str]:
    """Inverse of dict_to_key."""
    if not isinstance(key, str):
        raise TypeError(f'Expected str, got: {type(key)}')

    return {
        attribute_name: safe_decode(attribute_value)
        for attribute in key.split('/')
        for attribute_name, attribute_value in [attribute.split(':')]
    }


def jwt_payload_encode(payload: Dict[str, Any]) -> str:
    def hook(obj: object) -> str:
        # special cases where json encoder does not handle the object type
        # or a special format is needed
        if isinstance(obj, datetime):
            return cast(
                str,
                datetime_utils.get_as_str(
                    obj,
                    date_format='%Y-%m-%dT%H:%M:%S.%f'
                )
            )
        # let JSONEncoder handle unsupported object types
        return cast(str, json.JSONEncoder().default(obj))
    encoder = json.JSONEncoder(default=hook)
    return encoder.encode(payload)


def jwt_payload_decode(payload: str) -> Dict[str, Any]:
    def hook(jwt_payload: Dict[str, Any]) -> Dict[str, Any]:
        if 'exp' in jwt_payload:
            exp = jwt_payload['exp']
            if isinstance(exp, int):
                exp = datetime.fromtimestamp(exp)
            else:
                exp = datetime.strptime(
                    exp, '%Y-%m-%dT%H:%M:%S.%f'
                )
            jwt_payload['exp'] = exp
        return jwt_payload
    decoder = json.JSONDecoder(object_hook=hook)
    return cast(
        Dict[str, Any],
        decoder.decode(payload)
    )
