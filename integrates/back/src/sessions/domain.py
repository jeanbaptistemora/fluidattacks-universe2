from aioextensions import (
    schedule,
)
from botocore.exceptions import (
    ClientError,
)
import collections
from context import (
    FI_JWT_ENCRYPTION_KEY,
    FI_JWT_SECRET,
    FI_JWT_SECRET_API,
)
from contextlib import (
    suppress,
)
from custom_exceptions import (
    ExpiredToken,
    InvalidAuthorization,
    SecureAccessException,
    StakeholderNotFound,
    UnavailabilityError,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from datetime import (
    datetime,
    timedelta,
)
from db_model import (
    stakeholders as stakeholders_model,
)
from db_model.stakeholders.types import (
    StakeholderMetadataToUpdate,
    StakeholderSessionToken,
    StateSessionType,
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
import pytz
from sessions import (
    function,
    utils as sessions_utils,
)
from sessions.types import (
    UserAccessInfo,
)
from settings import (
    JWT_COOKIE_NAME,
    JWT_COOKIE_SAMESITE,
    LOGGING,
    SESSION_COOKIE_AGE,
)
from starlette.requests import (
    Request,
)
from starlette.responses import (
    HTMLResponse,
)
from typing import (
    Any,
    Dict,
    Optional,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


def encode_token(
    expiration_time: int,
    payload: Dict[str, Any],
    subject: str,
    api: bool = False,
) -> str:
    """Encrypts the payload into a jwe token and returns its encoded version"""
    secret = FI_JWT_SECRET_API if api else FI_JWT_SECRET
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


def decode_token(token: str) -> Dict[str, Any]:
    """Decodes a jwt token and returns its decrypted payload"""
    jwt_token = JWT(jwt=token)
    secret = sessions_utils.get_secret(jwt_token)
    jws_key = JWK.from_json(secret)
    jwt_token.validate(jws_key)
    claims = json.loads(jwt_token.claims)
    decoded_payload = sessions_utils.decode_jwe(jwt_token.token.payload)

    # Old token
    if not claims.get("exp"):
        payload = sessions_utils.validate_expiration_time(decoded_payload)
        return payload

    default_claims = dict(exp=claims["exp"], sub=claims["sub"])
    return dict(decoded_payload, **default_claims)


async def get_jwt_content(context: Any) -> Dict[str, str]:  # noqa: MC0001
    context_store_key = function.get_id(get_jwt_content)
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
            await verify_session_token(content, email)
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


async def create_session_token(user: UserAccessInfo) -> str:
    jti = sessions_utils.calculate_hash_token()["jti"]
    user_email = user.user_email
    expiration_time = int(
        (datetime.utcnow() + timedelta(seconds=SESSION_COOKIE_AGE)).timestamp()
    )
    jwt_token: str = encode_token(
        expiration_time=expiration_time,
        payload=dict(
            user_email=user_email,
            first_name=user.first_name,
            last_name=user.last_name,
            jti=jti,
        ),
        subject="starlette_session",
    )
    await stakeholders_model.update_metadata(
        email=user_email,
        metadata=StakeholderMetadataToUpdate(
            session_token=StakeholderSessionToken(
                jti=jti, state=StateSessionType.IS_VALID
            )
        ),
    )

    return jwt_token


def set_token_in_response(response: HTMLResponse, token: str) -> HTMLResponse:
    response.set_cookie(
        key=JWT_COOKIE_NAME,
        samesite=JWT_COOKIE_SAMESITE,
        value=token,
        secure=True,
        httponly=True,
        max_age=SESSION_COOKIE_AGE,
    )
    return response


async def remove_session_token(content: Dict[str, Any], email: str) -> None:
    """Revoke session token attribute"""
    await stakeholders_model.update_metadata(
        metadata=StakeholderMetadataToUpdate(
            session_token=StakeholderSessionToken(
                jti=content["jti"],
                state=StateSessionType.REVOKED,
            ),
        ),
        email=email,
    )


async def verify_session_token(content: Dict[str, Any], email: str) -> None:
    loaders: Dataloaders = get_new_context()
    stakeholder = await loaders.stakeholder.load(email)
    if not stakeholder:
        raise InvalidAuthorization()

    if stakeholder.session_token:
        if stakeholder.session_token.state == StateSessionType.REVOKED:
            raise ExpiredToken()

        if stakeholder.session_token.jti != content["jti"]:
            raise ExpiredToken()
    else:
        raise InvalidAuthorization()


async def _has_valid_access_token(
    loaders: Dataloaders, email: str, context: dict[str, str], jti: str
) -> bool:
    """Verify if has active access token and match."""
    stakeholder = await loaders.stakeholder.load(email)
    if not stakeholder:
        return False
    if context and stakeholder.access_token:
        if sessions_utils.validate_hash_token(stakeholder.access_token, jti):
            if email.endswith(
                "@fluidattacks.com"
            ) and email.lower().startswith("forces."):
                return True
            with suppress(UnavailabilityError, ClientError):
                schedule(
                    stakeholders_model.update_metadata(
                        metadata=StakeholderMetadataToUpdate(
                            last_api_token_use_date=(
                                datetime.now(tz=pytz.timezone("UTC"))
                            ),
                        ),
                        email=email,
                    )
                )
            return True
    return False


async def verify_jti(
    loaders: Dataloaders, email: str, context: Dict[str, str], jti: str
) -> None:
    if not await _has_valid_access_token(loaders, email, context, jti):
        raise InvalidAuthorization()


async def create_session_web(request: Request, email: str) -> None:
    session_key: str = request.session["session_key"]

    # Check if there is a session already
    request.session["is_concurrent"] = bool(await get_session_key(email))

    # Proccede overwritting the user session
    # This means that if a session did exist before, this one will
    # take place and the other will be removed
    return await stakeholders_model.update_metadata(
        metadata=StakeholderMetadataToUpdate(
            session_key=session_key,
        ),
        email=email,
    )


async def get_session_key(email: str) -> Optional[str]:
    loaders: Dataloaders = get_new_context()
    stakeholder = await loaders.stakeholder.load(email)
    session_key = stakeholder.session_key if stakeholder else None
    return session_key


async def remove_session_key(email: str) -> None:
    await stakeholders_model.update_metadata(
        metadata=StakeholderMetadataToUpdate(
            session_key="",
        ),
        email=email,
    )


async def check_session_web_validity(request: Request, email: str) -> None:
    try:
        session_key: str = request.session["session_key"]

        # Check if the stakeholder has a concurrent session and in case they do
        # raise the concurrent session modal flag
        if request.session.get("is_concurrent"):
            request.session.pop("is_concurrent")
            await stakeholders_model.update_metadata(
                metadata=StakeholderMetadataToUpdate(
                    is_concurrent_session=True,
                ),
                email=email,
            )
        # Check if the stakeholder has an active session but it's different
        # than the one in the cookie
        if await get_session_key(email) == session_key:
            # Session and cookie are ok and up to date
            pass
        else:
            # Session or the cookie are expired, let's logout the stakeholder
            await remove_session_key(email)
            request.session.clear()
            raise SecureAccessException()
    except (KeyError, StakeholderNotFound):
        # Stakeholder do not even has an active session
        raise SecureAccessException() from None
