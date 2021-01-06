# Standard library
import base64
import logging
from datetime import datetime
from decimal import Decimal
from typing import (
    Any,
    Dict,
    List,
    Optional,
)
from urllib.parse import quote_plus

# Third party libraries
import botocore.exceptions

# Local libraries
from backend import (
    mailer,
)
from backend.dal import (
    project as group_dal,
    subscriptions as subscriptions_dal,
)
from backend.dal.subscriptions import (
    NumericType,
)
from backend.domain import (
    analytics as analytics_domain,
    organization as org_domain,
    tag as portfolio_domain,
)
from backend.utils import (
    datetime as datetime_utils,
    reports,
)
from backend.services import (
    has_access_to_project as has_access_to_group,
)

from back.settings import (
    LOGGING,
    NOEXTRA
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER_ERRORS = logging.getLogger(__name__)
LOGGER_CONSOLE = logging.getLogger('console')


def frequency_to_period(*, frequency: str) -> int:
    mapping: Dict[str, int] = {
        'HOURLY': 3600,
        'DAILY': 86400,
        'WEEKLY': 604800,
        'MONTHLY': 2419200,
    }

    return mapping[frequency]


def period_to_frequency(*, period: NumericType) -> str:
    mapping: Dict[int, str] = {
        3600: 'HOURLY',
        86400: 'DAILY',
        604800: 'WEEKLY',
        2419200: 'MONTHLY',
    }

    return mapping[int(period)]


def is_subscription_active_right_now(
    *,
    bot_period: NumericType,
    bot_time: Optional[NumericType] = None,
    event_period: NumericType,
) -> bool:
    """Given a job that runs periodically, should it process a periodic event?.

    Example: if a bot runs every 3600 seconds, and the event is active
    every 86400 seconds, then once every 24 cycles the bot should process
    the event.

    This has a sensitivity of 1 second, such a bot should not run
    less often than this threshold for accurate results.
    """
    bot_time = Decimal(bot_time or datetime.utcnow().timestamp())
    bot_period = Decimal(bot_period)
    event_period = Decimal(event_period)

    return bot_period * (bot_time // bot_period) % event_period < 1


def should_process_event(
    *,
    bot_time: datetime,
    event_frequency: str,
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
        # Firth of month @ 10 GMT
        event_frequency == 'monthly'
        and bot_time_hour == 10
        and bot_time_day == 1
    ) or (
        # Mondays @ 10 GMT
        event_frequency == 'weekly'
        and bot_time_hour == 10
        and bot_time_weekday == 0
    ) or (
        # Any day @ 10 GMT
        event_frequency == 'daily'
        and bot_time_hour == 10
    ) or (
        # @ any hour
        event_frequency == 'hourly'
    )

    LOGGER_CONSOLE.info('- %s', locals(), **NOEXTRA)

    return success


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
            'entity': subscription['sk']['entity'],
            'frequency': period_to_frequency(period=subscription['period']),
            'subject': subscription['sk']['subject'],
        }
        for subscription in (
            await subscriptions_dal.get_user_subscriptions(
                user_email=user_email,
            )
        )
        if subscription['sk']['meta'] == 'entity_report'
    ]


async def get_subscriptions_to_entity_report(
    *,
    audience: str,
) -> List[Dict[Any, Any]]:
    return await subscriptions_dal.get_subscriptions_to_entity_report(
        audience=audience,
    )


async def can_subscribe_user_to_entity_report(
    *,
    report_entity: str,
    report_subject: str,
    user_email: str,
) -> bool:
    success: bool = False

    if report_entity.lower() == 'group':
        success = await has_access_to_group(
            user_email,
            report_subject.lower(),
        )
    elif report_entity.lower() == 'organization':
        success = await org_domain.has_user_access(
            email=user_email,
            organization_id=report_subject,
        )
    elif report_entity.lower() == 'portfolio':
        success = await portfolio_domain.has_user_access(
            email=user_email,
            subject=report_subject,
        )
    else:
        raise ValueError('Invalid report_entity')

    return success


async def subscribe_user_to_entity_report(
    *,
    event_frequency: str,
    report_entity: str,
    report_subject: str,
    user_email: str,
) -> bool:
    success: bool

    if event_frequency.lower() == 'never':
        success = await unsubscribe_user_to_entity_report(
            report_entity=report_entity,
            report_subject=report_subject,
            user_email=user_email,
        )
    else:
        event_period: int = frequency_to_period(frequency=event_frequency)

        success = await subscriptions_dal.subscribe_user_to_entity_report(
            event_period=event_period,
            report_entity=report_entity,
            report_subject=report_subject,
            user_email=user_email,
        )

        if success:
            await send_user_to_entity_report(
                event_frequency=event_frequency,
                report_entity=report_entity,
                report_subject=report_subject,
                user_email=user_email,
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


async def trigger_user_to_entity_report() -> None:
    bot_time: datetime = datetime.utcnow()

    LOGGER_CONSOLE.info('UTC datetime: %s', bot_time, **NOEXTRA)

    for subscription in await get_subscriptions_to_entity_report(
        audience='user',
    ):
        event_period: Decimal = subscription['period']
        event_frequency: str = period_to_frequency(period=event_period)
        user_email: str = subscription['pk']['email']
        report_entity: str = subscription['sk']['entity']
        report_subject: str = subscription['sk']['subject']

        LOGGER_CONSOLE.warning('Subscription: %s', locals(), **NOEXTRA)

        # A user may be subscribed but now he does not have access to the
        #   group or organization, so let's handle this case
        if await can_subscribe_user_to_entity_report(
            report_entity=report_entity,
            report_subject=report_subject,
            user_email=user_email,
        ):
            LOGGER_CONSOLE.info('- can be subscribed', **NOEXTRA)

            # The processor is expected to run every hour
            if should_process_event(
                bot_time=bot_time,
                event_frequency=event_frequency,
            ):
                LOGGER_CONSOLE.info('- processing event', **NOEXTRA)
                await send_user_to_entity_report(
                    event_frequency=event_frequency,
                    report_entity=report_entity,
                    report_subject=report_subject,
                    user_email=user_email,
                )
            else:
                LOGGER_CONSOLE.info('- not processing event', **NOEXTRA)
        else:
            LOGGER_CONSOLE.warning(
                '- can not be subscribed, unsubscribing', **NOEXTRA,
            )
            # Unsubscribe this user, he won't even notice as he no longer
            #   has access to the requested resource
            await unsubscribe_user_to_entity_report(
                report_entity=report_entity,
                report_subject=report_subject,
                user_email=user_email,
            )


async def should_not_send_report(
    *,
    report_entity: str,
    report_subject: str,
    user_email: str,
) -> bool:
    if report_entity.lower() == 'group':
        group_data = await group_dal.get_attributes(
            report_subject.lower(),
            [
                'deletion_date',
                'historic_deletion',
                'project_name',
                'project_status',
            ]
        )
        if not await group_dal.is_alive(report_subject.lower(), group_data):
            if group_data.get('project_status') == 'FINISHED':
                await unsubscribe_user_to_entity_report(
                    report_entity=report_entity,
                    report_subject=report_subject,
                    user_email=user_email,
                )

            return True

    return False


async def send_user_to_entity_report(
    *,
    event_frequency: str,
    report_entity: str,
    report_subject: str,
    user_email: str,
) -> None:
    try:
        if await should_not_send_report(
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
            ext='png',
            ttl=604800,  # seven days
        )
    except botocore.exceptions.ClientError as ex:
        LOGGER_CONSOLE.exception('%s', ex, **NOEXTRA)
        LOGGER_ERRORS.exception(
            ex,
            extra={
                'extra': dict(
                    report_entity=report_entity,
                    report_subject=report_subject,
                )
            })
    else:
        report_entity = report_entity.lower()
        if report_entity == 'organization':
            report_subject = await org_domain.get_name_by_id(report_subject)
        elif report_entity == 'portfolio':
            report_subject = report_subject.split('PORTFOLIO#')[-1]

        report_subject = report_subject.lower()

        LOGGER_CONSOLE.info('- sending email', **NOEXTRA)

        await mailer.send_mail_analytics(
            user_email,
            date=datetime_utils.get_as_str(
                datetime_utils.get_now(), '%Y/%m/%d'
            ),
            frequency_title=event_frequency.title(),
            frequency_lower=event_frequency.lower(),
            image_src=image_url,
            report_entity=report_entity,
            report_subject=report_subject,
            report_subject_title=report_subject.title(),
            report_entity_percent=quote_plus(translate_entity(report_entity)),
            report_subject_percent=quote_plus(report_subject),
        )

        LOGGER_CONSOLE.info('- email sent', **NOEXTRA)


def translate_entity(entity: str) -> str:
    translation = {
        'organization': 'org',
    }
    if entity in translation:
        return translation[entity]

    return entity
