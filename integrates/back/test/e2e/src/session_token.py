import binascii
from cryptography.hazmat.backends import (
    default_backend,
)
from cryptography.hazmat.primitives.kdf.scrypt import (
    Scrypt,
)
import json
from jwcrypto.jwe import (
    JWE,
)
from jwcrypto.jwk import (
    JWK,
)
from jwcrypto.jwt import (
    JWT,
)
import secrets
from typing import (
    Any,
)

# Constants

TIME_ZONE = "America/Bogota"
DEFAULT_DATE_FORMAT: str = "%Y-%m-%d %H:%M:%S"
NUMBER_OF_BYTES = 32  # length of the key
SCRYPT_N = 2**14  # cpu/memory cost
SCRYPT_R = 8  # block size
SCRYPT_P = 1  # parallelization


def calculate_hash_token() -> dict[str, str]:
    jti_token = secrets.token_bytes(NUMBER_OF_BYTES)
    salt = secrets.token_bytes(NUMBER_OF_BYTES)
    backend = default_backend()
    jti_hashed = Scrypt(
        salt=salt,
        length=NUMBER_OF_BYTES,
        n=SCRYPT_N,
        r=SCRYPT_R,
        p=SCRYPT_P,
        backend=backend,
    ).derive(jti_token)

    return {
        "jti_hashed": binascii.hexlify(jti_hashed).decode(),
        "jti": binascii.hexlify(jti_token).decode(),
        "salt": binascii.hexlify(salt).decode(),
    }


def encode_token(
    expiration_time: int,
    jwt_encryption_key: str,
    jwt_secret: str,
    payload: dict[str, Any],
    subject: str,
) -> str:
    """Encrypts the payload into a jwe token and returns its encoded version"""
    jws_key = JWK.from_json(jwt_secret)
    jwe_key = JWK.from_json(jwt_encryption_key)
    default_claims = dict(exp=expiration_time, sub=subject)
    jwt_object = JWT(
        default_claims=default_claims,
        claims=JWE(
            algs=[
                "A256GCM",
                "A256GCMKW",
            ],
            plaintext=json.dumps(payload).encode("utf-8"),
            protected={
                "alg": "A256GCMKW",
                "enc": "A256GCM",
            },
            recipient=jwe_key,
        ).serialize(),
        header={"alg": "RS512"},
    )
    jwt_object.make_signed_token(jws_key)

    return jwt_object.serialize()
