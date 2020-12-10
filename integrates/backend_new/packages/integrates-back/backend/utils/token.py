# Standard libraries
# Third party libraries
from jwcrypto.jwe import JWE
from jwcrypto.jwk import JWK
# Local libraries
from backend.utils import (
    encodings,
    decodings
)
from __init__ import (
    FI_JWT_ENCRYPTION_KEY,
)


def encrypt_jwt_payload(payload: dict) -> dict:
    serialized_payload = encodings.jwt_payload_encode(payload)
    key = JWK.from_json(FI_JWT_ENCRYPTION_KEY)
    claims = JWE(
        algs=[
            'A256GCM',
            'A256GCMKW',
        ],
        plaintext=serialized_payload.encode('utf-8'),
        protected={
            'alg': 'A256GCMKW',
            'enc': 'A256GCM',
        },
        recipient=key,
    ).serialize()
    return decodings.jwt_payload_decode(claims)


def decrypt_jwt_payload(payload: dict) -> dict:
    if 'ciphertext' not in payload:
        return payload
    serialized_payload = encodings.jwt_payload_encode(payload)
    key = JWK.from_json(FI_JWT_ENCRYPTION_KEY)
    result = JWE()
    result.deserialize(serialized_payload.encode('utf-8'))
    result.decrypt(key)
    return decodings.jwt_payload_decode(result.payload.decode('utf-8'))
