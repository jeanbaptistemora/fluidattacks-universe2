# Standard library
from collections.abc import Mapping
from datetime import datetime
from decimal import Decimal
from typing import (
    List,
    Optional,
)

# Local libraries
from backend.dal import (
    subscriptions as subscriptions_dal,
)
from backend.dal.subscriptions import (
    NumericType,
)


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


async def get_user_subscriptions(
    *,
    user_email: str,
) -> List[Mapping]:
    return await subscriptions_dal.get_user_subscriptions(
        user_email=user_email,
    )


async def get_subscriptions_to_entity_report(
    *,
    audience: str,
) -> List[Mapping]:
    return await subscriptions_dal.get_subscriptions_to_entity_report(
        audience=audience,
    )


async def subscribe_user_to_entity_report(
    *,
    period: NumericType,
    report_entity: str,
    report_subject: str,
    user_email: str,
) -> bool:
    return await subscriptions_dal.subscribe_user_to_entity_report(
        period=period,
        report_entity=report_entity,
        report_subject=report_subject,
        user_email=user_email,
    )
