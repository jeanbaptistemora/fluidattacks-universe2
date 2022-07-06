from aioextensions import (
    collect,
)
from analytics import (
    domain as analytics_domain,
)
import authz
from authz import (
    get_group_level_role,
)
import base64
from context import (
    FI_ENVIRONMENT,
    FI_TEST_PROJECTS,
)
from custom_exceptions import (
    SnapshotNotFound,
    UnableToProcessSubscription,
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
from decorators import (
    retry_on_exceptions,
)
from group_access.domain import (
    get_users_to_notify,
)
from groups import (
    domain as groups_domain,
)
from itertools import (
    chain,
)
import logging
import logging.config
from mailer import (
    analytics as analytics_mail,
    groups as groups_mail,
)
from newutils import (
    datetime as datetime_utils,
    groups as groups_utils,
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
from subscriptions.dal import (
    NumericType,
)
import sys
from tags import (
    domain as tags_domain,
)
from typing import (
    Any,
    Optional,
)
from urllib.parse import (
    quote_plus,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


def _frequency_to_period(*, frequency: str) -> int:
    mapping: dict[str, int] = {
        "HOURLY": 3600,
        "DAILY": 86400,
        "WEEKLY": 604800,
        "MONTHLY": 2419200,
    }
    return mapping[frequency]


def _period_to_frequency(*, period: NumericType) -> str:
    mapping: dict[int, str] = {
        3600: "HOURLY",
        86400: "DAILY",
        604800: "WEEKLY",
        2419200: "MONTHLY",
    }
    return mapping[int(period)]


def _translate_entity(entity: str) -> str:
    translation = {
        "organization": "org",
    }
    if entity in translation:
        return translation[entity]
    return entity


async def can_subscribe_user_to_entity_report(
    *,
    loaders: Any,
    report_entity: str,
    report_subject: str,
    user_email: str,
) -> bool:
    success: bool = False

    if report_entity.lower() == "group":
        success = await authz.has_access_to_group(
            user_email,
            report_subject.lower(),
        )
    elif report_entity.lower() == "organization":
        success = await orgs_domain.has_user_access(
            email=user_email,
            organization_id=report_subject,
        )
    elif report_entity.lower() == "portfolio":
        success = await tags_domain.has_user_access(
            loaders=loaders,
            email=user_email,
            subject=report_subject,
        )
    elif (
        report_entity.lower() == "digest"
        and report_subject.lower() == "all_groups"
    ):
        success = (
            len(
                await groups_domain.get_groups_by_user(
                    loaders, user_email, with_cache=False
                )
            )
            > 0
        )
    elif report_entity.lower() == "comments":
        success = True
    else:
        raise ValueError("Invalid report_entity or report_subject")

    return success


async def get_subscriptions_to_entity_report(
    *,
    audience: str,
) -> list[dict[str, Any]]:
    return await subscriptions_dal.get_subscriptions_to_entity_report(
        audience=audience,
    )


async def get_user_subscriptions(
    *,
    user_email: str,
) -> list[dict[str, Any]]:
    return await subscriptions_dal.get_user_subscriptions(
        user_email=user_email,
    )


async def get_user_subscriptions_to_entity_report(
    *,
    user_email: str,
) -> list[dict[str, str]]:
    return [
        {
            "entity": subscription["sk"]["entity"],
            "frequency": _period_to_frequency(period=subscription["period"]),
            "subject": subscription["sk"]["subject"],
        }
        for subscription in (
            await subscriptions_dal.get_user_subscriptions(
                user_email=user_email,
            )
        )
        if subscription["sk"]["meta"] == "entity_report"
    ]


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


async def _send_digest_report(
    *,
    user_email: str,
    digest_stats: Optional[tuple[dict[str, Any], ...]] = None,
    loaders: Optional[Dataloaders] = None,
) -> None:
    group_names: list[str] = await groups_domain.get_groups_by_user(
        loaders if loaders else get_new_context(), user_email, with_cache=False
    )

    if FI_ENVIRONMENT == "production":
        loaders = loaders if loaders else get_new_context()
        user_groups: tuple[Group, ...] = await loaders.group.load_many(
            group_names
        )
        groups_filtered = groups_utils.filter_active_groups(user_groups)
        group_names = [
            group.name
            for group in groups_filtered
            if group.name not in FI_TEST_PROJECTS.split(",")
        ]

    if digest_stats:
        mail_contents = tuple(
            group_stats
            for group_stats in digest_stats
            if group_stats["group"] in group_names
        )
    elif loaders:
        mail_contents = await collect(
            tuple(
                groups_domain.get_group_digest_stats(loaders, group)
                for group in group_names
            ),
            workers=2,
        )
    else:
        LOGGER.info(
            "- digest email NOT sent to user",
            extra={"extra": dict(user_email=user_email)},
        )
        return

    user_stats = groups_domain.process_user_digest_stats(mail_contents)
    if user_stats["groups_len"] == 0:
        LOGGER.warning(
            "- NO available info to user",
            extra={"extra": dict(user_email=user_email)},
        )
        return

    user_loaders = loaders if loaders else get_new_context()
    await groups_mail.send_mail_daily_digest(
        user_loaders,
        [user_email],
        user_stats,
    )


@retry_on_exceptions(
    exceptions=(UnableToSendMail,),
    max_attempts=3,
    sleep_seconds=1.0,
)
async def _send_user_to_entity_report(
    *,
    event_frequency: str,
    report_entity: str,
    report_subject: str,
    user_email: str,
    digest_stats: Optional[tuple[dict[str, Any], ...]] = None,
    loaders: Optional[Dataloaders] = None,
) -> None:
    if report_entity.lower() == "digest":
        await _send_digest_report(
            user_email=user_email,
            digest_stats=digest_stats,
            loaders=loaders,
        )
    elif report_entity.lower() != "comments":
        await _send_analytics_report(
            event_frequency=event_frequency,
            report_entity=report_entity,
            report_subject=report_subject,
            user_email=user_email,
        )


async def _should_not_send_report(
    *,
    loaders: Any,
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
) -> bool:
    if event_frequency.lower() == "never":
        success = await unsubscribe_user_to_entity_report(
            report_entity=report_entity,
            report_subject=report_subject,
            user_email=user_email,
        )
    else:
        event_period: int = _frequency_to_period(frequency=event_frequency)
        success = await subscriptions_dal.subscribe_user_to_entity_report(
            event_period=event_period,
            report_entity=report_entity,
            report_subject=report_subject,
            user_email=user_email,
        )
        if success:
            await _send_user_to_entity_report(
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
    return success


async def unsubscribe_user_to_entity_report(
    *,
    report_entity: str,
    report_subject: str,
    user_email: str,
) -> bool:
    return await subscriptions_dal.unsubscribe_user_to_entity_report(
        report_entity=report_entity,
        report_subject=report_subject,
        user_email=user_email,
    )


async def _get_digest_stats(
    loaders: Dataloaders,
    subscriptions: list[dict[str, Any]],
) -> tuple[dict[str, Any], ...]:
    """Process the digest stats for each group with a subscriber."""
    digest_suscribers: list[str] = [
        subscription["pk"]["email"]
        for subscription in subscriptions
        if str(subscription["sk"]["entity"]).lower() == "digest"
    ]

    digest_group_names = await collect(
        [
            groups_domain.get_groups_by_user(
                loaders, user_email, with_cache=False
            )
            for user_email in digest_suscribers
        ],
        workers=1024,
    )
    digest_group_names = tuple(set(chain.from_iterable(digest_group_names)))

    if FI_ENVIRONMENT == "production":
        all_groups: tuple[Group, ...] = await loaders.group.load_many(
            digest_group_names
        )
        groups_filtered = groups_utils.filter_active_groups(all_groups)
        digest_group_names = tuple(
            group.name
            for group in groups_filtered
            if group.name not in FI_TEST_PROJECTS.split(",")
        )

    LOGGER.info(
        "Digest: get stats for groups",
        extra={"extra": dict(digest_groups=str(digest_group_names))},
    )
    return await collect(
        [
            groups_domain.get_group_digest_stats(loaders, group)
            for group in digest_group_names
        ],
        workers=2,
    )


async def _validate_subscription(
    subscription: dict[str, Any],
) -> bool:
    # A user may be subscribed but now he does not have access to the
    #   group or organization, so let's handle this case
    loaders: Dataloaders = get_new_context()
    if await can_subscribe_user_to_entity_report(
        loaders=loaders,
        report_entity=subscription["sk"]["entity"],
        report_subject=subscription["sk"]["subject"],
        user_email=subscription["pk"]["email"],
    ):
        return True
    # Unsubscribe this user, he won't even notice as he no longer
    #   has access to the requested resource
    await unsubscribe_user_to_entity_report(
        report_entity=subscription["sk"]["entity"],
        report_subject=subscription["sk"]["subject"],
        user_email=subscription["pk"]["email"],
    )
    return False


async def _process_subscription(
    *,
    subscription: dict[str, Any],
    digest_stats: Optional[tuple[dict[str, Any], ...]] = None,
) -> None:
    if not await _validate_subscription(subscription):
        LOGGER.warning(
            "- user without access, unsubscribed",
            extra={"extra": {"subscription": subscription}},
        )
        return
    try:
        await _send_user_to_entity_report(
            event_frequency=_period_to_frequency(
                period=subscription["period"]
            ),
            report_entity=subscription["sk"]["entity"],
            report_subject=subscription["sk"]["subject"],
            user_email=subscription["pk"]["email"],
            digest_stats=digest_stats,
        )
    except UnableToSendMail as ex:
        LOGGER.exception(ex, extra={"extra": {"subscription": subscription}})


async def trigger_subscriptions_daily_digest() -> None:
    """Process daily digest. Fixed period by scheduler."""
    # Daily:   Tuesday to Saturday @ 9:00 UTC (4:00 GMT-5)
    subscriptions = [
        subscription
        for subscription in await get_subscriptions_to_entity_report(
            audience="user",
        )
        if str(subscription["sk"]["entity"]).lower() == "digest"
    ]
    LOGGER.info(
        "- daily digest subscriptions loaded",
        extra={"extra": {"length": len(subscriptions), "period": "DAILY"}},
    )
    digest_stats = await _get_digest_stats(get_new_context(), subscriptions)
    await collect(
        [
            _process_subscription(
                subscription=subscription,
                digest_stats=digest_stats,
            )
            for subscription in subscriptions
        ],
        workers=16,
    )


async def trigger_subscriptions_analytics() -> None:
    """Process subscriptions given a frequency from a related scheduler."""
    # Hourly:  Supported but not in use by any subscription
    # Daily:   Monday to Friday @ 10:00 UTC (5:00 GMT-5)
    # Weekly:  Mondays @ 10:00 UTC (5:00 GMT-5)
    # Monthly: First of month @ 10:00 UTC (5:00 GMT-5)
    frequency: str = str(sys.argv[2]).upper()
    if frequency not in {"DAILY", "HOURLY", "MONTHLY", "WEEKLY"}:
        LOGGER.error(
            "Wrong parameters for trigger", extra={"extra": {"args": sys.argv}}
        )
        raise UnableToProcessSubscription()

    subscriptions = [
        subscription
        for subscription in await get_subscriptions_to_entity_report(
            audience="user",
        )
        if str(subscription["sk"]["entity"]).lower() != "comments"
        and str(subscription["sk"]["entity"]).lower() != "digest"
        and _period_to_frequency(period=subscription["period"]) == frequency
    ]
    LOGGER.info(
        "- subscriptions loaded",
        extra={"extra": {"length": len(subscriptions), "period": frequency}},
    )
    await collect(
        _process_subscription(subscription=subscription)
        for subscription in subscriptions
    )


async def get_users_subscribed_to_consult(
    *,
    group_name: str,
    comment_type: str,
    is_finding_released: bool = True,
) -> list[str]:
    users = await get_users_to_notify(group_name)
    if comment_type.lower() == "observation" or not is_finding_released:
        roles: list[str] = await collect(
            tuple(get_group_level_role(email, group_name) for email in users),
            workers=16,
        )
        hackers = [
            email for email, role in zip(users, roles) if role == "hacker"
        ]

        return hackers

    return users
