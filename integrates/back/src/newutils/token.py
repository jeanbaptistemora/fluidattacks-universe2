# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from . import (
    function,
)
import binascii
import collections
from context import (
    FI_JWT_ENCRYPTION_KEY,
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
    InvalidAuthorization,
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
    InvalidJWEData,
    JWE,
)
from jwcrypto.jwk import (
    JWK,
)
from jwcrypto.jwt import (
    JWT,
    JWTExpired,
)
import logging
import logging.config
import secrets
from sessions import (
    domain as sessions_domain,
)
from settings import (
    JWT_COOKIE_NAME,
    JWT_SECRET,
    JWT_SECRET_API,
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


async def get_jwt_content(context: Any) -> Dict[str, str]:  # noqa: MC0001
    context_store_key = function.get_id(get_jwt_content)
    if isinstance(context, dict):
        context = context.get("request", {})
    store = get_request_store(context)

    # Within the context of one request we only need to process it once
    if context_store_key in store:
        store[context_store_key]["user_email"] = store[context_store_key][
            "user_email"
        ].lower()
        return store[context_store_key]

    try:
        cookies = context.cookies
        cookie_token = cookies.get(JWT_COOKIE_NAME)
        header_token = context.headers.get("Authorization")
        token = header_token.split()[1] if header_token else cookie_token

        if not token:
            raise InvalidAuthorization()

        content = sessions_domain.decode_token(token)
        email = content["user_email"]
        if content.get("sub") == "starlette_session":
            await sessions_domain.verify_session_token(content, email)
    except JWTExpired:
        # Session expired
        raise InvalidAuthorization() from None
    except (AttributeError, IndexError) as ex:
        LOGGER.exception(ex, extra={"extra": context})
        raise InvalidAuthorization() from None
    except InvalidJWEData:
        raise InvalidAuthorization() from None
    else:
        content["user_email"] = content["user_email"].lower()
        store[context_store_key] = content
        return content


def get_request_store(context: Any) -> collections.defaultdict:
    """Returns customized store attribute of a Django/Starlette request"""
    return context.store if hasattr(context, "store") else context.state.store


def is_api_token(user_data: Dict[str, Any]) -> bool:
    return user_data.get("sub") == (
        "api_token" if "sub" in user_data else "jti" in user_data
    )


def is_valid_expiration_time(expiration_time: float) -> bool:
    """Verify that expiration time is minor than six months"""
    exp = datetime.utcfromtimestamp(expiration_time)
    now = datetime.utcnow()
    return now < exp < (now + timedelta(weeks=MAX_API_AGE_WEEKS))


def encode_token(
    expiration_time: int,
    payload: Dict[str, Any],
    subject: str,
    api: bool = False,
) -> str:
    """Encrypts the payload into a jwe token and returns its encoded version"""
    secret = JWT_SECRET_API if api else JWT_SECRET
    jws_key = JWK.from_json(secret)
    jwe_key = JWK.from_json(FI_JWT_ENCRYPTION_KEY)
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


def verificate_hash_token(
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
