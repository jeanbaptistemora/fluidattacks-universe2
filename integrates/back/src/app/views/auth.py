# Starlette authz-related views/functions

from aioextensions import (
    collect,
)
from app import (
    utils,
)
from authlib.integrations.base_client.errors import (
    MismatchingStateError,
)
from authlib.integrations.starlette_client import (
    OAuthError,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model import (
    stakeholders as stakeholders_model,
)
from db_model.stakeholders.types import (
    NotificationsPreferences,
    StakeholderMetadataToUpdate,
    StakeholderState,
)
from decorators import (
    retry_on_exceptions,
)
from httpx import (
    ConnectTimeout,
)
import logging
import logging.config
from newutils import (
    analytics,
    datetime as datetime_utils,
    templates as templates_utils,
)
from organizations import (
    domain as orgs_domain,
)
from sessions import (
    domain as sessions_domain,
    utils as sessions_utils,
)
from sessions.types import (
    UserAccessInfo,
)
from settings.auth import (
    OAUTH,
)
from stakeholders import (
    domain as stakeholders_domain,
)
from starlette.requests import (
    Request,
)
from starlette.responses import (
    HTMLResponse,
    RedirectResponse,
    Response,
)
import uuid

LOGGER = logging.getLogger(__name__)
SUBSCRIPTIONS = dict(
    default=[
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
    ],
    user=[
        "UPDATED_TREATMENT",
        "VULNERABILITY_ASSIGNED",
        "VULNERABILITY_REPORT",
    ],
    user_manager=[
        "AGENT_TOKEN",
        "EVENT_REPORT",
        "FILE_UPDATE",
        "GROUP_INFORMATION",
        "GROUP_REPORT",
        "REMINDER_NOTIFICATION",
        "ROOT_UPDATE",
        "SERVICE_UPDATE",
        "UNSUBSCRIPTION_ALERT",
        "UPDATED_TREATMENT",
        "VULNERABILITY_REPORT",
    ],
    vulnerability_manager=[
        "EVENT_REPORT",
        "UPDATED_TREATMENT",
        "VULNERABILITY_REPORT",
    ],
)


@retry_on_exceptions(
    exceptions=(OAuthError,),
    max_attempts=5,
    sleep_seconds=float("0.3"),
)
async def authz_azure(request: Request) -> HTMLResponse:
    client = OAUTH.azure
    try:
        token = await client.authorize_access_token(request)
    except (MismatchingStateError) as ex:
        LOGGER.exception(ex, extra=dict(extra=locals()))
        return templates_utils.unauthorized(request)
    user = await utils.get_jwt_userinfo(client, request, token)
    email = user.get("email", user.get("upn", "")).lower()
    response = RedirectResponse(url="/home")
    await handle_user(
        request,
        response,  # type: ignore
        {**user, "email": email, "given_name": user["name"]},
    )
    return response  # type: ignore


@retry_on_exceptions(
    exceptions=(OAuthError,),
    max_attempts=5,
    sleep_seconds=float("0.3"),
)
async def authz_bitbucket(request: Request) -> HTMLResponse:
    client = OAUTH.bitbucket
    try:
        token = await client.authorize_access_token(request)
    except (MismatchingStateError) as ex:
        LOGGER.exception(ex, extra=dict(extra=locals()))
        return templates_utils.unauthorized(request)
    user = await utils.get_bitbucket_oauth_userinfo(client, token)
    response = RedirectResponse(url="/home")
    await handle_user(request, response, user)  # type: ignore
    return response  # type: ignore


@retry_on_exceptions(
    exceptions=(OAuthError,),
    max_attempts=5,
    sleep_seconds=float("0.3"),
)
async def authz_google(request: Request) -> HTMLResponse:
    client = OAUTH.google
    try:
        token = await client.authorize_access_token(request)
    except (MismatchingStateError) as ex:
        LOGGER.exception(ex, extra=dict(extra=locals()))
        return templates_utils.unauthorized(request)
    user = await utils.get_jwt_userinfo(client, request, token)
    response = RedirectResponse(url="/home")
    await handle_user(request, response, user)  # type: ignore
    return response  # type: ignore


async def do_azure_login(request: Request) -> Response:
    redirect_uri = utils.get_redirect_url(request, "authz_azure")
    azure = OAUTH.create_client("azure")
    return await azure.authorize_redirect(request, redirect_uri)


async def do_bitbucket_login(request: Request) -> Response:
    redirect_uri = utils.get_redirect_url(request, "authz_bitbucket")
    bitbucket = OAUTH.create_client("bitbucket")
    return await bitbucket.authorize_redirect(request, redirect_uri)


@retry_on_exceptions(
    exceptions=(ConnectTimeout,),
    max_attempts=5,
    sleep_seconds=float("0.3"),
)
async def do_google_login(request: Request) -> Response:
    redirect_uri = utils.get_redirect_url(request, "authz_google")
    google = OAUTH.create_client("google")
    return await google.authorize_redirect(request, redirect_uri)


def get_subscriptions(roles: list[str]) -> list[str]:
    if all(rol in SUBSCRIPTIONS for rol in roles):
        all_subscriptions = [
            SUBSCRIPTIONS.get(item, []) for item in set(roles)
        ]
        return list({item for list in all_subscriptions for item in list})

    return SUBSCRIPTIONS.get("default", [])


async def complete_register(
    *,
    email: str,
    first_name: str,
    last_name: str,
    roles: list[str],
) -> None:
    today = datetime_utils.get_utc_now()
    await collect(
        (
            stakeholders_model.update_metadata(
                email=email,
                metadata=StakeholderMetadataToUpdate(
                    first_name=first_name,
                    last_login_date=today,
                    last_name=last_name,
                    registration_date=today,
                ),
            ),
            stakeholders_model.update_state(
                user_email=email,
                state=StakeholderState(
                    notifications_preferences=NotificationsPreferences(
                        email=get_subscriptions(roles)
                    ),
                    modified_date=today,
                    modified_by=email.strip().lower(),
                ),
            ),
        )
    )
    await analytics.mixpanel_track(email, "Register")


async def handle_user(
    request: Request, response: HTMLResponse, user: dict[str, str]
) -> None:
    user_info: UserAccessInfo = sessions_utils.format_user_access_info(user)
    session_key = str(uuid.uuid4())
    request.session["session_key"] = session_key

    await log_stakeholder_in(get_new_context(), user_info)
    jwt_token = await sessions_domain.create_session_token(user_info)
    sessions_domain.set_token_in_response(response, jwt_token)
    await sessions_domain.create_session_web(request, user_info.user_email)


async def autoenroll_stakeholder(
    email: str,
    first_name: str,
    last_name: str,
) -> None:
    await orgs_domain.add_without_group(
        email=email,
        role="user",
        is_register_after_complete=True,
    )

    await complete_register(
        email=email,
        first_name=first_name,
        last_name=last_name,
        roles=["user_manager"],
    )


async def invited_stakeholder(
    loaders: Dataloaders,
    email: str,
    first_name: str,
    last_name: str,
) -> None:
    orgs_access = await loaders.stakeholder_organizations_access.load(email)
    groups_access = await loaders.stakeholder_groups_access.load(email)
    roles = []
    if len(orgs_access) > 0:
        roles.extend(
            [org.invitation.role for org in orgs_access if org.invitation]
        )
    if len(groups_access) > 0:
        roles.extend(
            [
                group.invitation.role
                for group in groups_access
                if group.invitation
            ]
        )

    await complete_register(
        email=email, first_name=first_name, last_name=last_name, roles=roles
    )


async def log_stakeholder_in(
    loaders: Dataloaders,
    user_info: UserAccessInfo,
) -> None:
    email = user_info.user_email.lower()
    first_name = user_info.first_name[:29]
    last_name = user_info.last_name[:29]
    stakeholder = await loaders.stakeholder.load(email)

    if stakeholder:
        if not stakeholder.enrolled:
            await analytics.mixpanel_track(email, "AutoenrollmentWelcome")
        if not stakeholder.registration_date:
            await invited_stakeholder(loaders, email, first_name, last_name)
        if not stakeholder.is_registered:
            await stakeholders_domain.register(email)

        await stakeholders_domain.update_last_login(email)
    else:
        await autoenroll_stakeholder(email, first_name, last_name)
        await analytics.mixpanel_track(email, "AutoenrollmentWelcome")
