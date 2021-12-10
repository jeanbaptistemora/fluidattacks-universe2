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
    FI_MAIL_CUSTOMER_SUCCESS,
    FI_MAIL_REVIEWERS,
    FI_MAIL_SUBSCRIPTIONS_TEST,
    FI_TEST_PROJECTS,
)
from custom_exceptions import (
    SnapshotNotFound,
    UnableToSendMail,
)
from custom_types import (
    MailContent,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from datetime import (
    datetime,
)
from decimal import (
    Decimal,
)
from group_access.domain import (
    get_users_to_notify,
)
from groups import (
    domain as groups_domain,
)
import itertools
import logging
import logging.config
from mailer import (
    analytics as analytics_mail,
    groups as groups_mail,
)
from newutils import (
    datetime as datetime_utils,
    reports,
)
from newutils.utils import (
    get_key_or_fallback,
)
from organizations import (
    domain as orgs_domain,
)
from settings import (
    LOGGING,
    NOEXTRA,
)
from subscriptions import (
    dal as subscriptions_dal,
)
from subscriptions.dal import (
    NumericType,
)
from tags import (
    domain as tags_domain,
)
from typing import (
    Any,
    Dict,
    List,
    Tuple,
    Union,
)
from urllib.parse import (
    quote_plus,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER_ERRORS = logging.getLogger(__name__)
LOGGER_CONSOLE = logging.getLogger("console")


def _frequency_to_period(*, frequency: str) -> int:
    mapping: Dict[str, int] = {
        "HOURLY": 3600,
        "DAILY": 86400,
        "WEEKLY": 604800,
        "MONTHLY": 2419200,
    }
    return mapping[frequency]


def _period_to_frequency(*, period: NumericType) -> str:
    mapping: Dict[int, str] = {
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
                    user_email, with_cache=False
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
) -> List[Dict[Any, Any]]:
    return await subscriptions_dal.get_subscriptions_to_entity_report(
        audience=audience,
    )


async def get_user_subscriptions(
    *,
    user_email: str,
) -> List[Dict[Any, Any]]:
    return await subscriptions_dal.get_user_subscriptions(
        user_email=user_email,
    )


async def get_user_subscriptions_to_entity_report(
    *,
    user_email: str,
) -> List[Dict[str, str]]:
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
    try:
        if await _should_not_send_report(
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
        LOGGER_CONSOLE.exception(ex, **NOEXTRA)
        LOGGER_ERRORS.exception(
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
        report_subject = await orgs_domain.get_name_by_id(report_subject)
    elif report_entity == "portfolio":
        report_subject = report_subject.split("PORTFOLIO#")[-1]

    report_subject = report_subject.lower()

    await analytics_mail.send_mail_analytics(
        user_email,
        date=datetime_utils.get_as_str(datetime_utils.get_now(), "%Y/%m/%d"),
        frequency_title=event_frequency.title(),
        frequency_lower=event_frequency.lower(),
        image_src=image_url,
        report_entity=report_entity,
        report_subject=report_subject,
        report_subject_title=report_subject.title(),
        report_entity_percent=quote_plus(_translate_entity(report_entity)),
        report_subject_percent=quote_plus(report_subject),
    )

    LOGGER_CONSOLE.info(
        "- analytics email sent to user",
        extra={"extra": dict(user_email=user_email)},
    )


async def _send_digest_report(
    *,
    user_email: str,
    digest_stats: Union[Tuple[MailContent], Tuple],
    loaders: Dataloaders = None,
) -> None:
    groups = await groups_domain.get_groups_by_user(
        user_email, with_cache=False
    )

    if FI_ENVIRONMENT == "production":
        groups = [
            group
            for group in groups
            if group not in FI_TEST_PROJECTS.split(",")
        ]

    mail_contents: Union[Tuple[MailContent], Tuple]
    if digest_stats:
        mail_contents = tuple(
            group_stats
            for group_stats in digest_stats
            if group_stats["group"] in groups
        )
    elif loaders:
        mail_contents = await collect(
            tuple(
                groups_domain.get_group_digest_stats(loaders, group)
                for group in groups
            ),
            workers=2,
        )
    else:
        LOGGER_CONSOLE.info(
            "- digest email NOT sent to user",
            extra={"extra": dict(user_email=user_email)},
        )

        return

    user_stats = groups_domain.process_user_digest_stats(mail_contents)

    if user_stats["groups_len"] == 0:
        LOGGER_CONSOLE.warning(
            "- NO available info to user",
            extra={"extra": dict(user_email=user_email)},
        )
        return

    await groups_mail.send_mail_daily_digest([user_email], user_stats)


async def _send_user_to_entity_report(
    *,
    event_frequency: str,
    report_entity: str,
    report_subject: str,
    user_email: str,
    digest_stats: Union[Tuple[MailContent], Tuple],
    loaders: Dataloaders = None,
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
    report_entity: str,
    report_subject: str,
    user_email: str,
) -> bool:
    if report_entity.lower() == "group":
        group_data = await groups_domain.get_attributes(
            report_subject.lower(),
            [
                "deletion_date",
                "historic_deletion",
                "project_name",
                "project_status",
            ],
        )
        if not await groups_domain.is_alive(
            report_subject.lower(), group_data
        ):
            if (
                get_key_or_fallback(
                    group_data, "group_status", "project_status"
                )
                == "FINISHED"
            ):
                await unsubscribe_user_to_entity_report(
                    report_entity=report_entity,
                    report_subject=report_subject,
                    user_email=user_email,
                )

            return True

    return False


def _should_process_event(
    *,
    bot_time: datetime,
    event_frequency: str,
    report_entity: str,
) -> bool:
    """Given a job that runs every hour, should it process a periodic event?.

    Such a bot should not run less or more often than the minimum event
    frequency to trigger.
    """
    bot_time = bot_time.replace(minute=0)
    bot_time_hour: int = bot_time.hour
    bot_time_day: int = bot_time.day
    bot_time_weekday: int = bot_time.weekday()

    event_frequency = event_frequency.lower()

    success: bool = (
        (
            # Tuesday to Saturday @ 9 GMT
            report_entity.lower() == "digest"
            and bot_time_hour == 9
            and 1 <= bot_time_weekday <= 5
        )
        or (
            # First of month @ 10 GMT
            event_frequency == "monthly"
            and bot_time_hour == 10
            and bot_time_day == 1
        )
        or (
            # Mondays @ 10 GMT
            event_frequency == "weekly"
            and bot_time_hour == 10
            and bot_time_weekday == 0
        )
        or (
            # Monday to Friday @ 10 GMT
            event_frequency == "daily"
            and bot_time_hour == 10
            and bot_time_weekday <= 4
            and report_entity.lower() != "digest"
            and report_entity.lower() != "comments"
        )
        or (
            # @ any hour
            event_frequency
            == "hourly"
        )
    )

    return success


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
                digest_stats=tuple(),
            )
            LOGGER_CONSOLE.info(
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
    subscriptions: List[Dict[Any, Any]],
) -> Union[Tuple[MailContent], Tuple]:
    """Process the digest stats for each group with a subscriber"""
    digest_suscribers = [
        subscription["pk"]["email"]
        for subscription in subscriptions
        if subscription["sk"]["entity"].lower() == "digest"
    ]

    digest_groups = await collect(
        [
            groups_domain.get_groups_by_user(user_email, with_cache=False)
            for user_email in digest_suscribers
        ],
        workers=1024,
    )
    digest_groups = set(itertools.chain.from_iterable(digest_groups))

    if FI_ENVIRONMENT == "production":
        digest_groups = {
            group
            for group in digest_groups
            if group not in FI_TEST_PROJECTS.split(",")
        }

    LOGGER_CONSOLE.info(
        "Digest: get stats for groups",
        extra={"extra": dict(digest_groups=str(digest_groups))},
    )
    return await collect(
        [
            groups_domain.get_group_digest_stats(loaders, group)
            for group in digest_groups
        ],
        workers=2,
    )


async def _process_subscription(
    *,
    bot_time: datetime,
    digest_stats: Union[Tuple[MailContent], Tuple],
    loaders: Dataloaders,
    subscription: Dict[Any, Any],
) -> None:
    event_period: Decimal = subscription["period"]
    event_frequency: str = _period_to_frequency(period=event_period)
    user_email: str = subscription["pk"]["email"]
    report_entity: str = subscription["sk"]["entity"]
    report_subject: str = subscription["sk"]["subject"]

    # A user may be subscribed but now he does not have access to the
    #   group or organization, so let's handle this case
    if await can_subscribe_user_to_entity_report(
        report_entity=report_entity,
        report_subject=report_subject,
        user_email=user_email,
    ):
        # The processor is expected to run every hour
        if _should_process_event(
            bot_time=bot_time,
            event_frequency=event_frequency,
            report_entity=report_entity,
        ):
            LOGGER_CONSOLE.info(
                "- subscription to be processed",
                extra={"extra": {"subscription": subscription}},
            )
            try:
                await _send_user_to_entity_report(
                    event_frequency=event_frequency,
                    report_entity=report_entity,
                    report_subject=report_subject,
                    user_email=user_email,
                    digest_stats=digest_stats,
                    loaders=loaders,
                )
            except UnableToSendMail as ex:
                LOGGER_ERRORS.exception(
                    ex, extra={"extra": {"subscription": subscription}}
                )
    else:
        LOGGER_CONSOLE.warning(
            "- can not be subscribed, unsubscribing",
            extra={"extra": {"subscription": subscription}},
        )
        # Unsubscribe this user, he won't even notice as he no longer
        #   has access to the requested resource
        await unsubscribe_user_to_entity_report(
            report_entity=report_entity,
            report_subject=report_subject,
            user_email=user_email,
        )


async def trigger_user_to_entity_report() -> None:
    bot_time: datetime = datetime.utcnow()

    LOGGER_CONSOLE.info(
        f"UTC datetime: {datetime_utils.get_as_str(bot_time)}", **NOEXTRA
    )

    subscriptions = [
        subscription
        for subscription in await get_subscriptions_to_entity_report(
            audience="user",
        )
        if subscription["sk"]["entity"] != "comments"
    ]

    LOGGER_CONSOLE.info(
        "- subscriptions loaded",
        extra={
            "extra": {
                "length": len(subscriptions),
                "sample": subscriptions[:1],
            }
        },
    )

    # Prepare digest stats for any group with a subscriber
    digest_stats: Union[Tuple[MailContent], Tuple] = tuple()
    loaders: Dataloaders = get_new_context()
    if _should_process_event(
        bot_time=bot_time,
        event_frequency="DAILY",
        report_entity="DIGEST",
    ):
        digest_stats = await _get_digest_stats(loaders, subscriptions)

    await collect(
        [
            _process_subscription(
                bot_time=bot_time,
                digest_stats=digest_stats,
                loaders=loaders,
                subscription=subscription,
            )
            for subscription in subscriptions
        ],
        workers=16,
    )


async def _validate_subscription(
    subscription: Dict[Any, Any],
) -> bool:
    # A user may be subscribed but now he does not have access to the
    #   group or organization, so let's handle this case
    if await can_subscribe_user_to_entity_report(
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


async def _process_subscription_analytics(
    subscription: Dict[Any, Any],
) -> None:
    if not await _validate_subscription(subscription):
        LOGGER_CONSOLE.warning(
            "- user without access, unsubscribed",
            extra={"extra": {"subscription": subscription}},
        )
        return
    try:
        await _send_analytics_report(
            event_frequency=_period_to_frequency(
                period=subscription["period"]
            ),
            report_entity=subscription["sk"]["entity"],
            report_subject=subscription["sk"]["subject"],
            user_email=subscription["pk"]["email"],
        )
    except UnableToSendMail as ex:
        LOGGER_ERRORS.exception(
            ex, extra={"extra": {"subscription": subscription}}
        )


async def trigger_subscriptions_analytics_daily() -> None:
    """Schedule cron: Monday to Friday @ 10:00 UTC (5:00 GMT-5)."""
    subscriptions = [
        subscription
        for subscription in await get_subscriptions_to_entity_report(
            audience="user",
        )
        if str(subscription["sk"]["entity"]).lower() != "comments"
        and str(subscription["sk"]["entity"]).lower() != "digest"
        and _period_to_frequency(period=subscription["period"]) == "DAILY"
        and FI_MAIL_SUBSCRIPTIONS_TEST == subscription["pk"]["email"]
    ]
    LOGGER_CONSOLE.info(
        "- subscriptions loaded",
        extra={"extra": {"length": len(subscriptions), "period": "DAILY"}},
    )
    await collect(
        _process_subscription_analytics(subscription)
        for subscription in subscriptions
    )


async def is_user_subscribed_to_comments(
    *,
    user_email: str,
) -> bool:
    subscriptions = await get_user_subscriptions(user_email=user_email)
    sub_to_comments = [
        subscription
        for subscription in subscriptions
        if str(subscription["sk"]["entity"]).lower() == "comments"
    ]
    return len(sub_to_comments) > 0


async def _get_consult_users(
    *,
    group_name: str,
    comment_type: str,
    is_finding_released: bool = True,
) -> List[str]:
    recipients = FI_MAIL_REVIEWERS.split(",")
    users = await get_users_to_notify(group_name)
    if comment_type.lower() == "observation" or not is_finding_released:
        roles: List[str] = await collect(
            [get_group_level_role(email, group_name) for email in users]
        )
        hackers = [
            email
            for email, role in zip(users, roles)
            if role in {"hacker", "analyst"}
        ]

        return [*recipients, *hackers]

    return [*recipients, *users]


async def get_users_subscribed_to_consult(
    *,
    group_name: str,
    comment_type: str,
    is_finding_released: bool = True,
) -> List[str]:
    recipients: List[str] = await _get_consult_users(
        group_name=group_name,
        comment_type=comment_type,
        is_finding_released=is_finding_released,
    )
    are_users_subscribed: List[bool] = await collect(
        [
            is_user_subscribed_to_comments(user_email=recipient)
            for recipient in recipients
        ]
    )
    suscribed_recipients = [
        recipient
        for recipient, is_user_subscribed in zip(
            recipients, are_users_subscribed
        )
        if is_user_subscribed
    ]
    customer_success_recipients = FI_MAIL_CUSTOMER_SUCCESS.split(",")

    return [*suscribed_recipients, *customer_success_recipients]
