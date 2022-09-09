# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from aioextensions import (
    collect,
)
from analytics import (
    domain as analytics_domain,
)
import authz
import base64
from custom_exceptions import (
    SnapshotNotFound,
    UnableToSendMail,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model import (
    subscriptions as subscriptions_model,
)
from db_model.enums import (
    Notification,
)
from db_model.groups.enums import (
    GroupStateStatus,
)
from db_model.groups.types import (
    Group,
)
from db_model.organizations.types import (
    Organization,
)
from db_model.stakeholders.types import (
    Stakeholder,
)
from db_model.subscriptions.enums import (
    SubscriptionEntity,
    SubscriptionFrequency,
)
from db_model.subscriptions.types import (
    Subscription,
)
from decorators import (
    retry_on_exceptions,
)
import logging
import logging.config
from mailer import (
    analytics as analytics_mail,
)
from newutils import (
    datetime as datetime_utils,
    reports as reports_utils,
    subscriptions as subscriptions_utils,
)
from organizations import (
    domain as orgs_domain,
)
from settings import (
    LOGGING,
)
import sys
from tags import (
    domain as tags_domain,
)
from urllib.parse import (
    quote_plus,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


async def can_subscribe(
    *,
    loaders: Dataloaders,
    entity: SubscriptionEntity,
    subject: str,
    email: str,
) -> bool:
    success: bool = False

    if entity == SubscriptionEntity.GROUP:
        success = await authz.has_access_to_group(
            loaders,
            email,
            subject.lower(),
        )
    elif entity == SubscriptionEntity.ORGANIZATION:
        success = await orgs_domain.has_access(
            loaders=loaders,
            email=email,
            organization_id=subject,
        )
    elif entity == SubscriptionEntity.PORTFOLIO:
        success = await tags_domain.has_access(
            loaders=loaders,
            email=email,
            subject=subject,
        )
    else:
        LOGGER.error(
            "Invalid entity or subject",
            extra={
                "extra": {
                    "entity": entity,
                    "subject": subject,
                    "email": email,
                }
            },
        )

    return success


async def get_all_subscriptions(
    *, frequency: SubscriptionFrequency
) -> tuple[Subscription, ...]:
    return await subscriptions_model.get_all_subscriptions(frequency=frequency)


@retry_on_exceptions(
    exceptions=(UnableToSendMail,),
    max_attempts=3,
    sleep_seconds=1.0,
)
async def _send_mail_analytics(
    *,
    frequency: SubscriptionFrequency,
    entity: SubscriptionEntity,
    subject: str,
    email: str,
) -> None:
    loaders: Dataloaders = get_new_context()
    if entity == SubscriptionEntity.GROUP:
        group_name = subject.lower()
        group: Group = await loaders.group.load(group_name)
        if group.state.status == GroupStateStatus.DELETED:
            await unsubscribe(
                entity=entity,
                subject=subject,
                email=email,
            )
            return

    stakeholder: Stakeholder = await loaders.stakeholder.load(email)
    if (
        Notification.CHARTS_REPORT
        not in stakeholder.notifications_preferences.email
    ):
        return

    try:
        image_url: str = await reports_utils.expose_bytes_as_url(
            content=base64.b64decode(
                await analytics_domain.get_graphics_report(
                    entity=entity.lower(),
                    subject=subject,
                )
            ),
            ext="png",
            ttl=604800,  # seven days
        )
    except SnapshotNotFound as ex:
        LOGGER.exception(ex)
        LOGGER.exception(
            ex,
            extra={
                "extra": dict(
                    entity=entity,
                    subject=subject,
                    email=email,
                )
            },
        )
        return

    if entity == SubscriptionEntity.ORGANIZATION:
        organization: Organization = await loaders.organization.load(subject)
        subject = organization.name
    elif entity == SubscriptionEntity.PORTFOLIO:
        subject = subject.split("PORTFOLIO#")[-1]

    await analytics_mail.send_mail_analytics(
        loaders,
        email,
        date=datetime_utils.get_as_str(datetime_utils.get_now(), "%Y/%m/%d"),
        frequency_title=frequency.title(),
        frequency_lower=frequency.lower(),
        image_src=image_url,
        report_entity=entity.value.lower(),
        report_subject=subject.lower(),
        report_subject_title=subject.title(),
        report_entity_percent=quote_plus(
            subscriptions_utils.translate_entity(entity)
        ),
        report_subject_percent=quote_plus(subject.lower()),
    )
    LOGGER.info(
        "Analytics email sent",
        extra={"extra": dict(email=email)},
    )


async def subscribe(
    *,
    frequency: SubscriptionFrequency,
    entity: SubscriptionEntity,
    subject: str,
    email: str,
) -> None:
    if frequency == SubscriptionFrequency.NEVER:
        await unsubscribe(
            entity=entity,
            subject=subject,
            email=email,
        )
        return

    await subscriptions_model.add(
        subscription=Subscription(
            email=email,
            entity=entity,
            frequency=frequency,
            subject=subject,
        )
    )
    await _send_mail_analytics(
        frequency=frequency,
        entity=entity,
        subject=subject,
        email=email,
    )


async def unsubscribe(
    *,
    entity: SubscriptionEntity,
    subject: str,
    email: str,
) -> None:
    await subscriptions_model.remove(
        entity=entity,
        subject=subject,
        email=email,
    )


async def _validate_subscription(subscription: Subscription) -> bool:
    # A stakeholder may be subscribed but now he does not have access to the
    #   group or organization, so let's handle this case
    loaders: Dataloaders = get_new_context()
    if await can_subscribe(
        loaders=loaders,
        entity=subscription.entity,
        subject=subscription.subject,
        email=subscription.email,
    ):
        return True
    # Unsubscribe this stakeholder, he won't even notice as he no longer
    #   has access to the requested resource
    await unsubscribe(
        entity=subscription.entity,
        subject=subscription.subject,
        email=subscription.email,
    )
    return False


async def _process_subscription(
    *,
    subscription: Subscription,
) -> None:
    if not await _validate_subscription(subscription):
        LOGGER.warning(
            "Stakeholder without access, unsubscribed",
            extra={"extra": {"subscription": subscription}},
        )
        return
    try:
        await _send_mail_analytics(
            frequency=subscription.frequency,
            entity=subscription.entity,
            subject=subscription.subject,
            email=subscription.email,
        )
    except UnableToSendMail as ex:
        LOGGER.exception(ex, extra={"extra": {"subscription": subscription}})


async def trigger_subscriptions_analytics() -> None:
    """Process subscriptions given a frequency from a related scheduler."""
    # Hourly:  Supported but not in use by any subscription
    # Daily:   Monday to Friday @ 10:00 UTC (5:00 GMT-5)
    # Weekly:  Mondays @ 10:00 UTC (5:00 GMT-5)
    # Monthly: First of month @ 10:00 UTC (5:00 GMT-5)
    frequency = SubscriptionFrequency[str(sys.argv[2]).upper()]
    subscriptions = await get_all_subscriptions(frequency=frequency)
    LOGGER.info(
        "Subscriptions loaded",
        extra={"extra": {"length": len(subscriptions), "period": frequency}},
    )
    await collect(
        _process_subscription(subscription=subscription)
        for subscription in subscriptions
    )
