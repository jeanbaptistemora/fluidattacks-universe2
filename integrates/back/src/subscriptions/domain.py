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
    reports,
)
from organizations import (
    domain as orgs_domain,
)
from settings import (
    LOGGING,
)
from subscriptions import (
    dal as subscriptions_dal,
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


def _translate_entity(entity: str) -> str:
    translation = {
        "organization": "org",
    }
    if entity in translation:
        return translation[entity]
    return entity


async def can_subscribe_user_to_entity_report(
    *,
    loaders: Dataloaders,
    report_entity: str,
    report_subject: str,
    user_email: str,
) -> bool:
    success: bool = False

    if report_entity.lower() == "group":
        success = await authz.has_access_to_group(
            loaders,
            user_email,
            report_subject.lower(),
        )
    elif report_entity.lower() == "organization":
        success = await orgs_domain.has_access(
            loaders=loaders,
            email=user_email,
            organization_id=report_subject,
        )
    elif report_entity.lower() == "portfolio":
        success = await tags_domain.has_user_access(
            loaders=loaders,
            email=user_email,
            subject=report_subject,
        )
    else:
        LOGGER.error(
            "- Invalid report_entity or report_subject",
            extra={
                "extra": {
                    "report_entity": report_entity,
                    "report_subject": report_subject,
                    "user_email": user_email,
                }
            },
        )

    return success


async def get_all_subscriptions(
    *, frequency: SubscriptionFrequency
) -> tuple[Subscription, ...]:
    return await subscriptions_dal.get_all_subscriptions(frequency=frequency)


@retry_on_exceptions(
    exceptions=(UnableToSendMail,),
    max_attempts=3,
    sleep_seconds=1.0,
)
async def _send_analytics_report(
    *,
    event_frequency: str,
    report_entity: str,
    report_subject: str,
    user_email: str,
) -> None:
    loaders: Dataloaders = get_new_context()
    try:
        if await _should_not_send_report(
            loaders=loaders,
            report_entity=report_entity,
            report_subject=report_subject,
            user_email=user_email,
        ):
            return

        image_url: str = await reports.expose_bytes_as_url(
            content=base64.b64decode(
                await analytics_domain.get_graphics_report(
                    entity=report_entity.lower(),
                    subject=report_subject,
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
                    report_entity=report_entity,
                    report_subject=report_subject,
                    user_email=user_email,
                )
            },
        )
        return

    report_entity = report_entity.lower()
    if report_entity == "organization":
        organization: Organization = await loaders.organization.load(
            report_subject
        )
        report_subject = organization.name
    elif report_entity == "portfolio":
        report_subject = report_subject.split("PORTFOLIO#")[-1]

    report_subject = report_subject.lower()

    stakeholder: Stakeholder = await loaders.stakeholder.load(user_email)
    if (
        Notification.CHARTS_REPORT
        in stakeholder.notifications_preferences.email
    ):
        await analytics_mail.send_mail_analytics(
            get_new_context(),
            user_email,
            date=datetime_utils.get_as_str(
                datetime_utils.get_now(), "%Y/%m/%d"
            ),
            frequency_title=event_frequency.title(),
            frequency_lower=event_frequency.lower(),
            image_src=image_url,
            report_entity=report_entity,
            report_subject=report_subject,
            report_subject_title=report_subject.title(),
            report_entity_percent=quote_plus(_translate_entity(report_entity)),
            report_subject_percent=quote_plus(report_subject),
        )

    LOGGER.info(
        "- analytics email sent to user",
        extra={"extra": dict(user_email=user_email)},
    )


async def _should_not_send_report(
    *,
    loaders: Dataloaders,
    report_entity: str,
    report_subject: str,
    user_email: str,
) -> bool:
    if report_entity.lower() == "group":
        group_name = report_subject.lower()
        group: Group = await loaders.group.load(group_name)
        if group.state.status == GroupStateStatus.DELETED:
            await unsubscribe_user_to_entity_report(
                report_entity=report_entity,
                report_subject=report_subject,
                user_email=user_email,
            )
            return True
    return False


async def subscribe_user_to_entity_report(
    *,
    event_frequency: str,
    report_entity: str,
    report_subject: str,
    user_email: str,
) -> None:
    if event_frequency.lower() == "never":
        await unsubscribe_user_to_entity_report(
            report_entity=report_entity,
            report_subject=report_subject,
            user_email=user_email,
        )
    else:
        subscription = Subscription(
            email=user_email,
            entity=SubscriptionEntity[report_entity],
            frequency=SubscriptionFrequency[event_frequency],
            subject=report_subject,
        )
        await subscriptions_dal.add(subscription=subscription)
        await _send_analytics_report(
            event_frequency=event_frequency,
            report_entity=report_entity,
            report_subject=report_subject,
            user_email=user_email,
        )
        LOGGER.info(
            "User subscribed correctly",
            extra={
                "extra": {
                    "frequency": event_frequency,
                    "entity": report_entity,
                    "subject": report_subject,
                    "user": user_email,
                }
            },
        )


async def unsubscribe_user_to_entity_report(
    *,
    report_entity: str,
    report_subject: str,
    user_email: str,
) -> None:
    await subscriptions_dal.remove(
        report_entity=report_entity,
        report_subject=report_subject,
        user_email=user_email,
    )


async def _validate_subscription_typed(
    subscription: Subscription,
) -> bool:
    # A user may be subscribed but now he does not have access to the
    #   group or organization, so let's handle this case
    loaders: Dataloaders = get_new_context()
    if await can_subscribe_user_to_entity_report(
        loaders=loaders,
        report_entity=subscription.entity,
        report_subject=subscription.subject,
        user_email=subscription.email,
    ):
        return True
    # Unsubscribe this user, he won't even notice as he no longer
    #   has access to the requested resource
    await unsubscribe_user_to_entity_report(
        report_entity=subscription.entity,
        report_subject=subscription.subject,
        user_email=subscription.email,
    )
    return False


async def _process_subscription_typed(
    *,
    subscription: Subscription,
) -> None:
    if not await _validate_subscription_typed(subscription):
        LOGGER.warning(
            "- user without access, unsubscribed",
            extra={"extra": {"subscription": subscription}},
        )
        return
    try:
        await _send_analytics_report(
            event_frequency=subscription.frequency,
            report_entity=subscription.entity,
            report_subject=subscription.subject,
            user_email=subscription.email,
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
        "- subscriptions loaded",
        extra={"extra": {"length": len(subscriptions), "period": frequency}},
    )
    await collect(
        _process_subscription_typed(subscription=subscription)
        for subscription in subscriptions
    )
