# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

import binascii
from context import (
    FI_JWT_ENCRYPTION_KEY,
    FI_JWT_SECRET,
    FI_JWT_SECRET_API,
)
from cryptography.exceptions import (
    InvalidKey,
)
from cryptography.hazmat.backends import (
    default_backend,
)
from cryptography.hazmat.primitives.kdf.scrypt import (
    Scrypt,
)
from custom_exceptions import (
    ExpiredToken,
)
from datetime import (
    datetime,
    timedelta,
)
from db_model.stakeholders.types import (
    StakeholderAccessToken,
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
import logging
import logging.config
import secrets
from settings import (
    LOGGING,
)
from typing import (
    Any,
    Dict,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)
MAX_API_AGE_WEEKS = 26  # max exp time of access token 6 months
NUMBER_OF_BYTES = 32  # length of the key
SCRYPT_N = 2**14  # cpu/memory cost
SCRYPT_R = 8  # block size
SCRYPT_P = 1  # parallelization


def decode_jwe(payload: str) -> Dict[str, Any]:
    """Decodes a jwe token and returns its decrypted payload"""
    jwe_key = JWK.from_json(FI_JWT_ENCRYPTION_KEY)
    jwe_token = JWE()
    jwe_token.deserialize(payload)
    jwe_token.decrypt(jwe_key)
    decoded_payload = json.loads(jwe_token.payload.decode("utf-8"))

    return decoded_payload


def get_secret(jwt_token: JWT) -> str:
    """Returns the secret needed to decrypt JWE"""
    # pylint: disable=protected-access
    payload = jwt_token._token.objects["payload"]
    deserialized_payload = json.loads(payload.decode("utf-8"))
    sub = deserialized_payload.get("sub")

    if sub is None:
        sub = decode_jwe(payload).get("sub")

    if sub == "api_token":
        return FI_JWT_SECRET_API
    return FI_JWT_SECRET


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


def validate_hash_token(
    access_token: StakeholderAccessToken, jti_token: str
) -> bool:
    resp = False
    backend = default_backend()
    token_hashed = Scrypt(
        salt=binascii.unhexlify(access_token.salt),
        length=NUMBER_OF_BYTES,
        n=SCRYPT_N,
        r=SCRYPT_R,
        p=SCRYPT_P,
        backend=backend,
    )
    try:
        token_hashed.verify(
            binascii.unhexlify(jti_token),
            binascii.unhexlify(access_token.jti),
        )
        resp = True
    except InvalidKey as ex:
        LOGGER.exception(ex, extra=dict(extra=locals()))
    return resp


def is_api_token(user_data: Dict[str, Any]) -> bool:
    return user_data.get("sub") == (
        "api_token" if "sub" in user_data else "jti" in user_data
    )


def is_valid_expiration_time(expiration_time: float) -> bool:
    """Verify that expiration time is minor than six months"""
    exp = datetime.utcfromtimestamp(expiration_time)
    now = datetime.utcnow()
    return now < exp < (now + timedelta(weeks=MAX_API_AGE_WEEKS))


def validate_expiration_time(payload: Dict[str, Any]) -> Dict[str, Any]:
    if "exp" not in payload:
        return payload

    exp = payload["exp"]
    utc_now = int(datetime.now().timestamp())
    if isinstance(exp, str):
        exp_as_datetime = datetime.strptime(exp, "%Y-%m-%dT%H:%M:%S.%f")
        exp = int(exp_as_datetime.timestamp())
        payload["exp"] = exp

    if exp < utc_now:
        raise ExpiredToken()

    return payload