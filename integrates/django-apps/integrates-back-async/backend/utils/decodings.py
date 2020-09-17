import json
from datetime import datetime


def jwt_payload_decode(payload: str) -> dict:
    def hook(jwt_payload: dict) -> dict:
        if 'exp' in jwt_payload:
            jwt_payload['exp'] = datetime.strptime(
                jwt_payload['exp'], '%Y-%m-%dT%H:%M:%S.%f')
        return jwt_payload
    decoder = json.JSONDecoder(object_hook=hook)
    return decoder.decode(payload)
