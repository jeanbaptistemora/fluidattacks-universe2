# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

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
from jwcrypto.jwk import (
    JWK,
)
from jwcrypto.jwt import (
    JWT,
)
from sessions import (
    utils as sessions_utils,
)
from starlette.requests import (
    Request,
)
from typing import (
    Any,
    Dict,
    Optional,
)


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
