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
from custom_types import (
    User as UserType,
)
from datetime import (
    datetime,
    timedelta,
)
from jose import (
    jwt,
    JWTError,
)
from jwcrypto.jwe import (
    InvalidJWEData,
    JWE,
)
from jwcrypto.jwk import (
    JWK,
)
import logging
import logging.config
from newutils import (
    encodings,
)
from redis_cluster.model import (
    KeyNotFound as RedisKeyNotFound,
)
from redis_cluster.operations import (
    redis_get_entity_attr,
)
import secrets
from sessions import (
    dal as sessions_dal,
)
from settings import (
    JWT_COOKIE_NAME,
    JWT_SECRET,
    JWT_SECRET_API,
    LOGGING,
)
from typing import (
    Any,
    cast,
    Dict,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)
MAX_API_AGE_WEEKS = 26  # max exp time of access token 6 months
NUMBER_OF_BYTES = 32  # length of the key
SCRYPT_N = 2 ** 14  # cpu/memory cost
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
    if "ciphertext" not in payload:
        return payload
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


def decode_jwt(jwt_token: str, api: bool = False) -> Dict[str, Any]:
    """Decodes a jwt token and returns its decrypted payload"""
    secret = JWT_SECRET_API if api else JWT_SECRET
    content = jwt.decode(token=jwt_token, key=secret, algorithms=["HS512"])
    return _decrypt_jwt_payload(content)


async def get_jwt_content(context: Any) -> Dict[str, str]:  # noqa: MC0001
    context_store_key = function.get_id(get_jwt_content)
    if isinstance(context, dict):
        context = context.get("request", {})
    store = get_request_store(context)

    # Within the context of one request we only need to process it once
    if context_store_key in store:
        return store[context_store_key]

    try:
        cookies = context.cookies
        cookie_token = cookies.get(JWT_COOKIE_NAME)
        header_token = context.headers.get("Authorization")
        token = header_token.split()[1] if header_token else cookie_token

        if context.session.get("username"):
            await sessions_dal.check_jwt_token_validity(context)

        if not token:
            raise InvalidAuthorization()

        if jwt_has_api_token(token):
            content = decode_jwt(token, api=True)
        else:
            content = decode_jwt(token)
            if content.get("sub") == "starlette_session":
                try:
                    session_jti: str = await redis_get_entity_attr(
                        entity="session",
                        attr="jti",
                        email=content["user_email"],
                    )
                    if session_jti != content["jti"]:
                        raise ExpiredToken()
                except RedisKeyNotFound:
                    # Session expired (user logged out)
                    raise ExpiredToken() from None
    except jwt.ExpiredSignatureError:
        # Session expired
        raise InvalidAuthorization() from None
    except (AttributeError, IndexError) as ex:
        LOGGER.exception(ex, extra={"extra": context})
        raise InvalidAuthorization() from None
    except jwt.JWTClaimsError as ex:
        LOGGER.exception(ex, extra={"extra": context})
        raise InvalidAuthorization() from None
    except JWTError as ex:
        LOGGER.exception(ex, extra={"extra": context})
        raise InvalidAuthorization() from None
    except InvalidJWEData:
        raise InvalidAuthorization() from None
    else:
        store[context_store_key] = content
        return content


def get_request_store(context: Any) -> collections.defaultdict:
    """Returns customized store attribute of a Django/Starlette request"""
    return context.store if hasattr(context, "store") else context.state.store


def is_api_token(user_data: UserType) -> bool:
    return user_data.get("sub") == (
        "api_token" if "sub" in user_data else "jti" in user_data
    )


def is_valid_expiration_time(expiration_time: float) -> bool:
    """Verify that expiration time is minor than six months"""
    exp = datetime.utcfromtimestamp(expiration_time)
    now = datetime.utcnow()
    return now < exp < (now + timedelta(weeks=MAX_API_AGE_WEEKS))


def jwt_has_api_token(token: str) -> bool:
    payload = jwt.get_unverified_claims(token)
    payload = _decrypt_jwt_payload(payload)
    return cast(
        bool,
        payload.get("sub")
        == ("api_token" if "sub" in payload else "jti" in payload),
    )


def new_encoded_jwt(
    payload: Dict[str, Any], api: bool = False, encrypt: bool = True
) -> str:
    """Encrypts the payload into a jwt token and returns its encoded version"""
    processed_payload = _encrypt_jwt_payload(payload) if encrypt else payload
    secret = JWT_SECRET_API if api else JWT_SECRET
    token: str = jwt.encode(
        processed_payload,
        algorithm="HS512",
        key=secret,
    )
    return token


def verificate_hash_token(
    access_token: Dict[str, str], jti_token: str
) -> bool:
    resp = False
    backend = default_backend()
    token_hashed = Scrypt(
        salt=binascii.unhexlify(access_token["salt"]),
        length=NUMBER_OF_BYTES,
        n=SCRYPT_N,
        r=SCRYPT_R,
        p=SCRYPT_P,
        backend=backend,
    )
    try:
        token_hashed.verify(
            binascii.unhexlify(jti_token),
            binascii.unhexlify(access_token["jti"]),
        )
        resp = True
    except InvalidKey as ex:
        LOGGER.exception(ex, extra=dict(extra=locals()))
    return resp
