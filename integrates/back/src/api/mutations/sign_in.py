import aiohttp
from ariadne import (
    convert_kwargs_to_snake_case,
)
from authlib.integrations.starlette_client import (
    OAuthError,
)
from custom_exceptions import (
    StakeholderNotFound,
)
from custom_types import (
    SignInPayload as SignInPayloadType,
)
from dataloaders import (
    Dataloaders,
)
from db_model import (
    stakeholders as stakeholders_model,
)
from db_model.stakeholders.types import (
    NotificationsPreferences,
    Stakeholder,
    StakeholderMetadataToUpdate,
)
from decorators import (
    retry_on_exceptions,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
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
from settings import (
    MOBILE_SESSION_AGE,
)
from settings.auth import (
    BITBUCKET_ARGS,
    GOOGLE_ARGS,
    OAUTH,
)
from stakeholders import (
    domain as stakeholders_domain,
)
from subscriptions import (
    domain as subscriptions_domain,
)
from typing import (
    Any,
    Optional,
)

# Constants
LOGGER = logging.getLogger(__name__)


async def autoenroll_stakeholder(email: str) -> None:
    await groups_domain.add_without_group(
        email=email,
        role="user",
        is_register_after_complete=True,
    )
    await stakeholders_model.update_metadata(
        email=email,
        metadata=StakeholderMetadataToUpdate(
            notifications_preferences=NotificationsPreferences(
                email=[
                    "ACCESS_GRANTED",
                    "AGENT_TOKEN",
                    "CHARTS_REPORT",
                    "EVENT_REPORT",
                    "FILE_UPDATE",
                    "GROUP_INFORMATION",
                    "GROUP_REPORT",
                    "NEW_COMMENT",
                    "NEW_DRAFT",
                    "PORTFOLIO_UPDATE",
                    "REMEDIATE_FINDING",
                    "REMINDER_NOTIFICATION",
                    "ROOT_UPDATE",
                    "SERVICE_UPDATE",
                    "UNSUBSCRIPTION_ALERT",
                    "UPDATED_TREATMENT",
                    "VULNERABILITY_ASSIGNED",
                    "VULNERABILITY_REPORT",
                ]
            )
        ),
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

            return user


@convert_kwargs_to_snake_case
async def mutate(
    _: Any, info: GraphQLResolveInfo, auth_token: str, provider: str
) -> SignInPayloadType:
    session_jwt = ""
    success = False
    loaders: Dataloaders = info.context.loaders
    user = await get_provider_user_info(provider, auth_token)
    if user:
        await log_stakeholder_in(loaders=loaders, stakeholder=user)
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


async def log_stakeholder_in(
    loaders: Dataloaders, stakeholder: dict[str, str]
) -> None:
    email = stakeholder["email"].lower()
    try:
        db_user: Stakeholder = await loaders.stakeholder.load(email)
        if not db_user.is_registered:
            await stakeholders_domain.register(email)
        await stakeholders_domain.update_last_login(email)
    except StakeholderNotFound:
        first_name = stakeholder.get("given_name", "")[:29]
        last_name = stakeholder.get("family_name", "")[:29]
        today = datetime_utils.get_iso_date()
        stakeholder_data = StakeholderMetadataToUpdate(
            first_name=first_name,
            last_login_date=today,
            last_name=last_name,
            registration_date=today,
        )
        await analytics.mixpanel_track(email, "Register")
        await autoenroll_stakeholder(email)
        await stakeholders_domain.update_attributes(email, stakeholder_data)
