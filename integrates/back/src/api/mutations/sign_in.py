from aioextensions import (
    collect,
)
import aiohttp
from ariadne import (
    convert_kwargs_to_snake_case,
)
from authlib.integrations.starlette_client import (
    OAuthError,
)
import authz
from context import (
    FI_COMMUNITY_PROJECTS,
)
from custom_types import (
    SignInPayload as SignInPayloadType,
)
from decorators import (
    retry_on_exceptions,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from group_access import (
    domain as group_access_domain,
)
from groups import (
    domain as groups_domain,
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
from organizations import (
    domain as orgs_domain,
)
from settings import (
    LOGGING,
    MOBILE_SESSION_AGE,
)
from settings.auth import (
    BITBUCKET_ARGS,
    GOOGLE_ARGS,
    OAUTH,
)
from subscriptions import (
    domain as subscriptions_domain,
)
from typing import (
    Any,
    cast,
    Dict,
    Optional,
)
from users import (
    domain as users_domain,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


async def autoenroll_user(email: str) -> None:
    new_user_user_level_role: str = "customer"
    new_user_group_level_role: str = "customer"

    await groups_domain.add_without_group(
        email=email, role=new_user_user_level_role
    )
    for group in FI_COMMUNITY_PROJECTS.split(","):
        await collect(
            [
                group_access_domain.update_has_access(email, group, True),
                authz.grant_group_level_role(
                    email, group, new_user_group_level_role
                ),
            ]
        )

    # Enroll new users to Daily Digest by default
    if await subscriptions_domain.subscribe_user_to_entity_report(
        event_frequency="DAILY",
        report_entity="DIGEST",
        report_subject="ALL_GROUPS",
        user_email=email,
    ):
        LOGGER.info(
            "New user subscribed to Daily Digest", extra={"extra": email}
        )

    # Enroll new Fluid users to Comments by default
    if (
        "@fluidattacks.com" in email
        and await subscriptions_domain.subscribe_user_to_entity_report(
            event_frequency="DAILY",
            report_entity="COMMENTS",
            report_subject="ALL_GROUPS",
            user_email=email,
        )
    ):
        LOGGER.info(
            "New user subscribed to comments in all groups",
            extra={"extra": email},
        )


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
) -> Optional[Dict[str, str]]:
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
            userinfo_endpoint, headers={"Authorization": f"Bearer {token}"}
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
                                    for email in emails.get("values", "")
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

            return cast(Optional[Dict[str, str]], user)


@convert_kwargs_to_snake_case
async def mutate(
    _: Any, _info: GraphQLResolveInfo, auth_token: str, provider: str
) -> SignInPayloadType:
    session_jwt = ""
    success = False

    user = await get_provider_user_info(provider, auth_token)
    if user:
        await log_user_in(user)
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

    return SignInPayloadType(session_jwt=session_jwt, success=success)


async def log_user_in(user: Dict[str, str]) -> None:
    first_name = user.get("given_name", "")[:29]
    last_name = user.get("family_name", "")[:29]
    email = user["email"].lower()

    today = datetime_utils.get_now_as_str()
    data_dict = {
        "first_name": first_name,
        "last_login": today,
        "last_name": last_name,
        "date_joined": today,
    }

    if not await users_domain.is_registered(email):
        await analytics.mixpanel_track(email, "Register")
        if not await orgs_domain.get_user_organizations(email):
            await autoenroll_user(email)

        await users_domain.update_multiple_user_attributes(email, data_dict)
    else:
        if await users_domain.get_data(email, "first_name"):
            await users_domain.update_last_login(email)
        else:
            await users_domain.update_multiple_user_attributes(
                email, data_dict
            )
