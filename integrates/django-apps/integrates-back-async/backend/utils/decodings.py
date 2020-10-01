import json

from backend.utils import (
    datetime as datetime_utils,
)


def jwt_payload_decode(payload: str) -> dict:
    def hook(jwt_payload: dict) -> dict:
        if 'exp' in jwt_payload:
            jwt_payload['exp'] = datetime_utils.get_from_str(
                jwt_payload['exp'],
                date_format='%Y-%m-%dT%H:%M:%S.%f'
            )
        return jwt_payload
    decoder = json.JSONDecoder(object_hook=hook)
    return decoder.decode(payload)
