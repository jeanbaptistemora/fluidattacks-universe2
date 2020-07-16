# Standard library
from collections.abc import Mapping
from datetime import datetime
from decimal import Decimal
from typing import (
    Dict,
    List,
    Optional,
)

# Third party libraries
import botocore.exceptions

# Local libraries
from backend import (
    mailer,
)
from backend.dal import (
    subscriptions as subscriptions_dal,
)
from backend.dal.subscriptions import (
    NumericType,
)
from backend.domain import (
    analytics as analytics_domain,
    organization as org_domain,
)
from backend.utils import (
    aio,
    logging,
    reports,
)
from backend.services import (
    has_access_to_project as has_access_to_group,
)


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
    bot_time: Optional[datetime] = None,
    event_frequency: str,
) -> bool:
    """Given a job that runs every hour, should it process a periodic event?.

    Such a bot should not run less or more often than the minimum event
    frequency to trigger.
    """
    bot_time = bot_time or datetime.utcnow()
    bot_time = bot_time.replace(minute=0)

    event_frequency = event_frequency.lower()

    return (
        # Firth of month @ 10 GMT
        event_frequency == 'monthly'
        and bot_time.hour == 10
        and bot_time.day == 1
    ) or (
        # Mondays @ 10 GMT
        event_frequency == 'weekly'
        and bot_time.hour == 10
        and bot_time.weekday() == 0
    ) or (
        # Any day @ 10 GMT
        event_frequency == 'daily'
        and bot_time.hour == 10
    ) or (
        # @ any hour
        event_frequency == 'hourly'
    )


async def get_user_subscriptions(
    *,
    user_email: str,
) -> List[Mapping]:
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
) -> List[Mapping]:
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
        success = await aio.ensure_io_bound(
            has_access_to_group,
            user_email,
            report_subject.lower(),
        )
    elif report_entity.lower() == 'organization':
        success = await org_domain.has_user_access(
            email=user_email,
            organization_id=report_subject,
        )
    else:
        raise ValueError('Invalid report_entity')

    return success


async def subscribe_user_to_entity_report(
    *,
    frequency: str,
    report_entity: str,
    report_subject: str,
    user_email: str,
) -> bool:
    success: bool

    if frequency.lower() == 'never':
        success = await unsubscribe_user_to_entity_report(
            report_entity=report_entity,
            report_subject=report_subject,
            user_email=user_email,
        )
    else:
        success = await subscriptions_dal.subscribe_user_to_entity_report(
            period=frequency_to_period(
                frequency=frequency,
            ),
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


async def trigger_user_to_entity_report():
    coroutines = []

    for subscription in await get_subscriptions_to_entity_report(
        audience='user',
    ):
        event_period: Decimal = subscription['period']
        event_frequency: str = period_to_frequency(period=event_period)
        user_email: str = subscription['pk']['email']
        report_entity: str = subscription['sk']['entity']
        report_subject: str = subscription['sk']['subject']

        if all((
            # This is expected to run every hour
            should_process_event(
                event_frequency=event_frequency,
            ),
            # A user may be subscribed but now he does not have access to the
            #   group or organization, so let's ignore them!
            await can_subscribe_user_to_entity_report(
                report_entity=report_entity,
                report_subject=report_subject,
                user_email=user_email,
            ),
        )):
            try:
                image_url: str = await reports.expose_bytes_as_url(
                    content=await analytics_domain.get_graphics_report(
                        entity=report_entity.lower(),
                        subject=report_subject,
                    ),
                    ext='png',
                    ttl=event_period,
                )
            except botocore.exceptions.ClientError:
                await logging.log(
                    level='error',
                    message='Report not available',
                    payload_data=dict(
                        report_entity=report_entity,
                        report_subject=report_subject,
                    ),
                )
            else:
                # We should trigger the event!!
                coroutines.append(
                    mailer.send_mail_charts(
                        user_email,
                        frequency_title=event_frequency.title(),
                        frequency_lower=event_frequency.lower(),
                        image_src=image_url,
                        report_entity=report_entity.lower(),
                        report_subject=(
                            await org_domain.get_name_by_id(report_subject)
                            if report_entity.lower() == 'organization'
                            else report_subject
                        )
                    ),
                )

    await aio.materialize(coroutines)
