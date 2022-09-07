# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from aioextensions import (
    collect,
    schedule,
)
from context import (
    BASE_URL,
)
from custom_exceptions import (
    InvalidAuthorization,
    UnableToSendMail,
)
from dataloaders import (
    Dataloaders,
)
from db_model import (
    group_access as group_access_model,
)
from db_model.group_access.types import (
    GroupAccess,
    GroupAccessMetadataToUpdate,
    GroupConfirmDeletion,
)
from db_model.organization_access.types import (
    OrganizationAccess,
)
from db_model.subscriptions.types import (
    Subscription,
)
from decorators import (
    retry_on_exceptions,
)
from group_access import (
    domain as group_access_domain,
)
from groups.domain import (
    get_groups_by_stakeholder,
)
from jose import (
    JWTError,
)
from jwcrypto.jwe import (
    JWException,
)
from mailchimp_transactional.api_client import (
    ApiClientError,
)
from mailer.common import (
    send_mail_confirm_deletion,
)
from newutils.datetime import (
    get_as_epoch,
    get_now_plus_delta,
)
from newutils.token import (
    decode_jwt,
    new_encoded_jwt,
)
from newutils.validations import (
    validate_email_address,
)
from organizations import (
    domain as orgs_domain,
)
from redis_cluster.operations import (
    redis_del_by_deps,
)
from sessions.dal import (
    remove_session_key,
)
from stakeholders import (
    domain as stakeholders_domain,
)
from subscriptions.domain import (
    unsubscribe,
)
from typing import (
    Any,
    Optional,
)

mail_confirm_deletion = retry_on_exceptions(
    exceptions=(UnableToSendMail, ApiClientError),
    max_attempts=4,
    sleep_seconds=2,
)(send_mail_confirm_deletion)


async def remove_stakeholder_all_organizations(
    *, loaders: Dataloaders, email: str, modified_by: str
) -> None:
    organizations: tuple[
        OrganizationAccess, ...
    ] = await loaders.stakeholder_organizations_access.load(email)

    organizations_ids: list[str] = [
        org.organization_id for org in organizations
    ]
    await collect(
        tuple(
            orgs_domain.remove_access(
                loaders, organization_id, email, modified_by
            )
            for organization_id in organizations_ids
        )
    )

    subscriptions: tuple[
        Subscription
    ] = await loaders.stakeholder_subscriptions.load(email)
    await collect(
        tuple(
            unsubscribe(
                entity=subscription.entity,
                subject=subscription.subject,
                email=email,
            )
            for subscription in subscriptions
        )
    )

    await collect(
        tuple(
            redis_del_by_deps(
                "remove_stakeholder_organization_access",
                organization_id=organization_id,
            )
            for organization_id in organizations_ids
        )
    )

    active, inactive = await collect(
        [
            group_access_domain.get_stakeholder_groups_names(
                loaders, email, active=True
            ),
            group_access_domain.get_stakeholder_groups_names(
                loaders, email, active=False
            ),
        ]
    )
    stakeholder_groups = set(active + inactive)
    await collect(
        tuple(
            group_access_domain.remove_access(loaders, email, group)
            for group in stakeholder_groups
        )
    )

    await stakeholders_domain.remove(loaders=loaders, email=email)


async def complete_deletion(*, loaders: Dataloaders, email: str) -> None:
    await group_access_model.remove(email=email, group_name="confirm_deletion")
    await remove_stakeholder_all_organizations(
        loaders=loaders,
        email=email,
        modified_by=email,
    )
    await collect(
        [
            remove_session_key(email, "jti"),
            remove_session_key(email, "web"),
            remove_session_key(email, "jwt"),
        ]
    )
    stakeholder_groups = await get_groups_by_stakeholder(loaders, email)
    await collect(
        tuple(
            redis_del_by_deps(
                "remove_stakeholder_access",
                group_name=group_name,
            )
            for group_name in stakeholder_groups
        )
    )


async def get_email_from_url_token(
    *,
    loaders: Dataloaders,
    url_token: str,
) -> str:
    try:
        token_content = decode_jwt(url_token)
    except (JWTError, JWException) as ex:
        raise InvalidAuthorization() from ex

    email: str = token_content["user_email"]
    if not await group_access_domain.exists(
        loaders=loaders, group_name="confirm_deletion", email=email
    ):
        return ""

    access_with_deletion: GroupAccess = await loaders.group_access.load(
        ("confirm_deletion", email)
    )
    if (
        access_with_deletion.confirm_deletion
        and access_with_deletion.confirm_deletion.url_token == url_token
    ):
        return email

    return ""


async def get_confirm_deletion(
    *,
    loaders: Dataloaders,
    email: str,
) -> Optional[GroupAccess]:
    if await group_access_domain.exists(loaders, "confirm_deletion", email):
        confirm_deletion = await loaders.group_access.load(
            ("confirm_deletion", email)
        )

        return confirm_deletion
    return None


async def confirm_deletion_mail(
    *,
    loaders: Dataloaders,
    email: str,
) -> bool:
    expiration_time = get_as_epoch(get_now_plus_delta(weeks=1))
    url_token = new_encoded_jwt(
        {
            "user_email": email,
        },
    )
    if validate_email_address(email):
        await group_access_model.update_metadata(
            email=email,
            group_name="confirm_deletion",
            metadata=GroupAccessMetadataToUpdate(
                expiration_time=expiration_time,
                confirm_deletion=GroupConfirmDeletion(
                    is_used=False,
                    url_token=url_token,
                ),
            ),
        )
        confirm_access_url = f"{BASE_URL}/confirm_deletion/{url_token}"
        mail_to = [email]
        email_context: dict[str, Any] = {
            "email": email,
            "confirm_deletion_url": confirm_access_url,
            "empty_notification_notice": True,
        }
        schedule(mail_confirm_deletion(loaders, mail_to, email_context))

        return True

    return False
