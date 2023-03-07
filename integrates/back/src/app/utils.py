from aioextensions import (
    collect,
)
from authlib.integrations.starlette_client import (
    OAuth,
    OAuthError,
)
from dataloaders import (
    Dataloaders,
)
from db_model.groups.enums import (
    GroupManaged,
)
from db_model.stakeholders.types import (
    Stakeholder,
)
from db_model.trials.types import (
    Trial,
)
from decorators import (
    retry_on_exceptions,
)
from decorators.utils import (
    is_personal_email,
)
from group_access.domain import (
    get_stakeholder_groups_names,
)
from httpx import (
    ConnectTimeout,
)
from newutils import (
    analytics,
)
from starlette.requests import (
    Request,
)
from typing import (
    Any,
    Iterable,
)

VALID_MANAGED = [
    GroupManaged.MANAGED,
    GroupManaged.NOT_MANAGED,
    GroupManaged.TRIAL,
]


async def get_bitbucket_oauth_userinfo(
    client: OAuth, token: dict[str, str]
) -> dict[str, str]:
    query_headers = {"Authorization": f'Bearer {token["access_token"]}'}
    user = await client.get("user", token=token, headers=query_headers)
    emails = await client.get(
        "user/emails", token=token, headers=query_headers
    )

    user_name = user.json().get("display_name", "")
    email = next(
        iter(
            [
                email.get("email", "")
                for email in emails.json().get("values", "")
                if email.get("is_primary")
            ]
        ),
        "",
    )
    return {
        "email": email,
        "given_name": user_name.split(" ")[0],
        "family_name": user_name.split(" ")[1] if len(user_name) == 2 else "",
    }


@retry_on_exceptions(
    exceptions=(ConnectTimeout, OAuthError),
    max_attempts=5,
    sleep_seconds=float("0.5"),
)
async def get_jwt_userinfo(
    client: OAuth, request: Request, token: str
) -> dict[str, str]:
    return dict(
        await client.parse_id_token(
            request,
            token,
            # Workaround to support microsoft multi-tenant
            claims_options={} if client.name == "azure" else None,
        )
    )


def get_redirect_url(request: Request, pattern: str) -> Any:
    return request.url_for(pattern).replace("http:", "https:")


async def get_group_valid_managed(
    loaders: Dataloaders, group_name: str
) -> bool:
    group = await loaders.group.load(group_name)
    return group.state.managed in VALID_MANAGED


async def get_is_autoenroll_user(
    loaders: Dataloaders,
    email: str,
    stakeholder: Stakeholder | None,
    trial: Trial | None,
) -> bool:
    active_group_names: Iterable[str] = await get_stakeholder_groups_names(
        loaders, email, True
    )
    groups_valid_managed = await collect(
        [
            get_group_valid_managed(loaders, group_name)
            for group_name in active_group_names
        ]
    )
    unauthorized_user = bool(
        (not stakeholder)
        or (stakeholder and not stakeholder.enrolled)
        or (trial and trial.completed)
    )
    return unauthorized_user and not any(groups_valid_managed)


async def send_autoenroll_mixpanel_event(
    loaders: Dataloaders, email: str, stakeholder: Stakeholder | None = None
) -> None:
    trial = await loaders.trial.load(email)
    if await get_is_autoenroll_user(loaders, email, stakeholder, trial):
        if await is_personal_email(email):
            await analytics.mixpanel_track(email, "AutoenrollCorporateOnly")
        elif trial and trial.completed:
            await analytics.mixpanel_track(email, "AutoenrollAlreadyInTrial")
        else:
            await analytics.mixpanel_track(email, "AutoenrollmentWelcome")
    else:
        await analytics.mixpanel_track(email, "CurrentStakeholder")
