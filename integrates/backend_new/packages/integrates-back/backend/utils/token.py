# Standard libraries
# Third party libraries
from typing import Any, Dict
from jose import jwt
from jwcrypto.jwe import JWE
from jwcrypto.jwk import JWK
# Local libraries
from backend.utils import (
    encodings,
    decodings
)
from backend_new import settings

from __init__ import (
    FI_JWT_ENCRYPTION_KEY,
)


def encrypt_jwt_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Creates a JWE from a payload"""
    serialized_payload = encodings.jwt_payload_encode(payload)
    key = JWK.from_json(FI_JWT_ENCRYPTION_KEY)
    claims: str = JWE(
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


def decrypt_jwt_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Returns the decrypted payload of a JWE"""
    if 'ciphertext' not in payload:
        return payload
    serialized_payload = encodings.jwt_payload_encode(payload)
    key = JWK.from_json(FI_JWT_ENCRYPTION_KEY)
    result = JWE()
    result.deserialize(serialized_payload.encode('utf-8'))
    result.decrypt(key)
    return decodings.jwt_payload_decode(result.payload.decode('utf-8'))


def new_encoded_jwt(
    payload: Dict[str, Any],
    api: bool = False,
    encrypt: bool = False
) -> str:
    """Encrypts the payload into a jwt token and returns its encoded version"""
    processed_payload = encrypt_jwt_payload(payload) if encrypt else payload
    secret = settings.JWT_SECRET_API if api else settings.JWT_SECRET
    token: str = jwt.encode(
        processed_payload,
        algorithm='HS512',
        key=secret,
    )
    return token


def decode_jwt(
    jwt_token: str,
    api: bool = False
) -> Dict[str, Any]:
    """Decodes a jwt token and returns its decrypted payload"""
    secret = settings.JWT_SECRET_API if api else settings.JWT_SECRET
    content = jwt.decode(
        token=jwt_token,
        key=secret,
        algorithms=['HS512']
    )
    return decrypt_jwt_payload(content)
