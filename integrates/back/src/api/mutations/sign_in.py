# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

import aiohttp
from api.mutations import (
    SignInPayload,
)
from ariadne import (
    convert_kwargs_to_snake_case,
)
from authlib.integrations.starlette_client import (
    OAuthError,
)
from decorators import (
    retry_on_exceptions,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from httpx import (
    ConnectTimeout,
)
import json
import logging
import logging.config
from newutils import (
    analytics,
    datetime as datetime_utils,
    token as token_helper,
)
from settings import (
    MOBILE_SESSION_AGE,
)
from settings.auth import (
    BITBUCKET_ARGS,
    GOOGLE_ARGS,
    OAUTH,
)
from typing import (
    Any,
    Optional,
)

# Constants
LOGGER = logging.getLogger(__name__)


@retry_on_exceptions(
    exceptions=(
        ConnectTimeout,
        OAuthError,
    ),
    max_attempts=5,
    sleep_seconds=float("0.5"),
)
async def get_provider_user_info(
    provider: str, token: str
) -> Optional[dict[str, str]]:
    if provider == "bitbucket":
        userinfo_endpoint = BITBUCKET_ARGS["userinfo_endpoint"]
    elif provider == "google":
        userinfo_endpoint = (
            f'{GOOGLE_ARGS["userinfo_endpoint"]}?access_token={token}'
        )
    elif provider == "microsoft":
        client = OAUTH.azure
        user = (
            await client._parse_id_token(  # pylint: disable=protected-access
                {"access_token": None, "id_token": token},
                None,
                claims_options={},
            )
        )
        email = user.get("email", user.get("upn", "")).lower()
        return {**user, "email": email, "given_name": user["name"]}

    async with aiohttp.ClientSession() as session:
        async with session.get(
            userinfo_endpoint,  # type: ignore
            headers={"Authorization": f"Bearer {token}"},
        ) as user:
            if user.status != 200:
                return None
            user = await user.read()
            user = json.loads(user)
            if provider == "bitbucket":
                async with aiohttp.ClientSession() as session:
                    async with session.get(
                        f"{userinfo_endpoint}/emails",
                        headers={"Authorization": f"Bearer {token}"},
                    ) as emails:
                        emails = await emails.json()
                        email = next(
                            iter(
                                [
                                    email.get("email", "")
                                    for email in emails.get(  # type: ignore
                                        "values", ""
                                    )
                                    if email.get("is_primary")
                                ]
                            ),
                            "",
                        )

                user["email"] = email
                user_name = user.get("display_name", "")
                user["given_name"] = user_name.split(" ")[0]
                user["family_name"] = (
                    user_name.split(" ")[1] if len(user_name) == 2 else ""
                )

            return user


@convert_kwargs_to_snake_case
async def mutate(
    _: Any, _info: GraphQLResolveInfo, auth_token: str, provider: str
) -> SignInPayload:
    session_jwt = ""
    success = False
    user = await get_provider_user_info(provider, auth_token)
    if user:
        email = user["email"].lower()
        session_jwt = token_helper.new_encoded_jwt(
            {
                "user_email": email,
                "first_name": user["given_name"],
                "last_name": user.get("family_name", ""),
                "exp": datetime_utils.get_now_plus_delta(
                    seconds=MOBILE_SESSION_AGE
                ),
                "sub": "session_token",
            }
        )
        await analytics.mixpanel_track(email, "MobileAuth", provider=provider)
        success = True
    else:
        LOGGER.exception("Mobile login failed", extra={"extra": locals()})

    return SignInPayload(session_jwt=session_jwt, success=success)
