# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

import binascii
from cryptography.hazmat.backends import (
    default_backend,
)
from cryptography.hazmat.primitives.kdf.scrypt import (
    Scrypt,
)
from datetime import (
    datetime,
)
from jose import (
    jwt,
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
import pytz
import secrets
from typing import (
    Any,
    cast,
    Dict,
)

# Constants

TIME_ZONE = "America/Bogota"
DEFAULT_DATE_FORMAT: str = "%Y-%m-%d %H:%M:%S"
NUMBER_OF_BYTES = 32  # length of the key
SCRYPT_N = 2**14  # cpu/memory cost
SCRYPT_R = 8  # block size
SCRYPT_P = 1  # parallelization


def _get_as_str(
    date: datetime,
    date_format: str = DEFAULT_DATE_FORMAT,
    zone: str = TIME_ZONE,
) -> str:
    return date.astimezone(tz=pytz.timezone(zone)).strftime(date_format)


def _jwt_payload_encode(payload: Dict[str, Any]) -> str:
    def hook(obj: object) -> str:
        # special cases where json encoder does not handle the object type
        # or a special format is needed
        if isinstance(obj, datetime):
            return _get_as_str(
                obj, date_format="%Y-%m-%dT%H:%M:%S.%f", zone="UTC"
            )
        # let JSONEncoder handle unsupported object types
        return cast(str, json.JSONEncoder().default(obj))

    encoder = json.JSONEncoder(default=hook)
    return encoder.encode(payload)


def _jwt_payload_decode(payload: str) -> Dict[str, Any]:
    def hook(jwt_payload: Dict[str, Any]) -> Dict[str, Any]:
        if "exp" in jwt_payload:
            exp = jwt_payload["exp"]
            if isinstance(exp, int):
                exp = datetime.fromtimestamp(exp)
            else:
                exp = datetime.strptime(exp, "%Y-%m-%dT%H:%M:%S.%f")
            jwt_payload["exp"] = exp
        return jwt_payload

    decoder = json.JSONDecoder(object_hook=hook)
    return cast(Dict[str, Any], decoder.decode(payload))


def _encrypt_jwt_payload(
    payload: Dict[str, Any], jwt_encryption_key: str
) -> Dict[str, Any]:
    """Creates a JWE from a payload"""
    serialized_payload = _jwt_payload_encode(payload)
    key = JWK.from_json(jwt_encryption_key)
    claims: str = JWE(
        algs=[
            "A256GCM",
            "A256GCMKW",
        ],
        plaintext=serialized_payload.encode("utf-8"),
        protected={
            "alg": "A256GCMKW",
            "enc": "A256GCM",
        },
        recipient=key,
    ).serialize()
    return _jwt_payload_decode(claims)


def new_encoded_jwt(
    payload: Dict[str, Any],
    jwt_encryption_key: str,
    jwt_secret: str,
) -> str:
    """Encrypts the payload into a jwt token and returns its encoded version"""
    processed_payload = _encrypt_jwt_payload(payload, jwt_encryption_key)
    token: str = jwt.encode(
        processed_payload,
        algorithm="HS512",
        key=jwt_secret,
    )
    return token


def calculate_hash_token() -> Dict[str, str]:
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
    payload: Dict[str, Any],
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
        header={"alg": "HS512"},
    )
    jwt_object.make_signed_token(jws_key)

    return jwt_object.serialize()
