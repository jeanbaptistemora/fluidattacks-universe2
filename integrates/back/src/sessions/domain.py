# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

import collections
from context import (
    FI_JWT_ENCRYPTION_KEY,
    FI_JWT_SECRET,
    FI_JWT_SECRET_API,
)
import contextlib
from custom_exceptions import (
    ExpiredToken,
    InvalidAuthorization,
    SecureAccessException,
    StakeholderNotFound,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model import (
    stakeholders as stakeholders_model,
)
from db_model.stakeholders.types import (
    Stakeholder,
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
from sessions import (
    function,
    utils as sessions_utils,
)
from settings import (
    JWT_COOKIE_NAME,
    LOGGING,
)
from starlette.requests import (
    Request,
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
    try:
        loaders: Dataloaders = get_new_context()
        stakeholder: Stakeholder = await loaders.stakeholder.load(email)
    except StakeholderNotFound as ex:
        raise InvalidAuthorization() from ex

    if stakeholder.session_token:
        if stakeholder.session_token.state == StateSessionType.REVOKED:
            raise ExpiredToken()

        if stakeholder.session_token.jti != content["jti"]:
            raise ExpiredToken()
    else:
        raise InvalidAuthorization()


async def create_session_web_new(request: Request, email: str) -> None:
    session_key: str = request.session["session_key"]

    # Check if there is a session already
    request.session["is_concurrent"] = bool(await get_session_key_new(email))

    # Proccede overwritting the user session
    # This means that if a session did exist before, this one will
    # take place and the other will be removed
    return await stakeholders_model.update_metadata(
        metadata=StakeholderMetadataToUpdate(
            session_key=session_key,
        ),
        email=email,
    )


async def get_session_key_new(email: str) -> Optional[str]:
    session_key: Optional[str] = None
    with contextlib.suppress(StakeholderNotFound):
        loaders: Dataloaders = get_new_context()
        stakeholder: Stakeholder = await loaders.stakeholder.load(email)
        session_key = stakeholder.session_key
    return session_key


async def remove_session_key_new(email: str) -> None:
    await stakeholders_model.update_metadata(
        metadata=StakeholderMetadataToUpdate(
            session_key="",
        ),
        email=email,
    )


async def check_session_web_validity_new(request: Request, email: str) -> None:
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
        if await get_session_key_new(email) == session_key:
            # Session and cookie are ok and up to date
            pass
        else:
            # Session or the cookie are expired, let's logout the stakeholder
            await remove_session_key_new(email)
            request.session.clear()
            raise SecureAccessException()
    except (KeyError, StakeholderNotFound):
        # Stakeholder do not even has an active session
        raise SecureAccessException() from None
