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
    ExpiredToken,
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
from newutils import (
    datetime as datetime_utils,
    encodings,
)
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


def _encrypt_jwt_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Creates a JWE from a payload"""
    serialized_payload = encodings.jwt_payload_encode(payload)
    key = JWK.from_json(FI_JWT_ENCRYPTION_KEY)
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
    return encodings.jwt_payload_decode(claims)


def _decrypt_jwt_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Returns the decrypted payload of a JWE"""
    serialized_payload = encodings.jwt_payload_encode(payload)
    key = JWK.from_json(FI_JWT_ENCRYPTION_KEY)
    result = JWE()
    result.deserialize(serialized_payload.encode("utf-8"))
    result.decrypt(key)

    return encodings.jwt_payload_decode(result.payload.decode("utf-8"))


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

        content = decode_token(token)
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


def _decode_jwe(payload: str) -> Dict[str, Any]:
    """Decodes a jwe token and returns its decrypted payload"""
    jwe_key = JWK.from_json(FI_JWT_ENCRYPTION_KEY)
    jwe_token = JWE()
    jwe_token.deserialize(payload)
    jwe_token.decrypt(jwe_key)
    decoded_payload = json.loads(jwe_token.payload.decode("utf-8"))

    return decoded_payload


def decode_token(token: str) -> Dict[str, Any]:
    """Decodes a jwt token and returns its decrypted payload"""
    jwt_token = JWT(jwt=token)
    secret = _get_secret(jwt_token)
    jws_key = JWK.from_json(secret)
    jwt_token.validate(jws_key)
    claims = json.loads(jwt_token.claims)
    decoded_payload = _decode_jwe(jwt_token.token.payload)

    # Old token
    if not claims.get("exp"):
        payload = _validate_expiration_time(decoded_payload)
        return payload

    default_claims = dict(exp=claims["exp"], sub=claims["sub"])
    return dict(decoded_payload, **default_claims)


def _get_secret(jwt_token: JWT) -> str:
    """Returns the secret needed to decrypt JWE"""
    # pylint: disable=protected-access
    payload = jwt_token._token.objects["payload"]
    deserialized_payload = json.loads(payload.decode("utf-8"))
    sub = deserialized_payload.get("sub")

    if sub is None:
        sub = _decode_jwe(payload).get("sub")

    if sub == "api_token":
        return JWT_SECRET_API
    return JWT_SECRET


def _validate_expiration_time(payload: Dict[str, Any]) -> Dict[str, Any]:
    if "exp" not in payload:
        return payload

    exp = payload["exp"]
    utc_now = int(datetime_utils.get_utc_timestamp())
    if isinstance(exp, str):
        exp_as_datetime = datetime.strptime(exp, "%Y-%m-%dT%H:%M:%S.%f")
        exp = datetime_utils.get_as_epoch(exp_as_datetime)
        payload["exp"] = exp

    if exp < utc_now:
        raise ExpiredToken()

    return payload


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
