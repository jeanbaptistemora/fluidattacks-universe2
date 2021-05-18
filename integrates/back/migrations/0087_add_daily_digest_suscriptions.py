# /usr/bin/env python3
# -.- coding: utf-8 -.-
# pylint: disable=invalid-name
"""
This migration subscribes all active users to Daily Digest,
excluding "executive" users and those already subscribed

Execution Time:    2021-05-18 at 10:53:37 UTC-05
Finalization Time: 2021-05-18 at 11:53:39 UTC-05
"""

# Standard
from itertools import chain
import time

# Third party
from aioextensions import collect, run

# Local
from groups.dal import get_active_groups
from group_access import domain as group_access_domain
from subscriptions.domain import (
    get_subscriptions_to_entity_report,
    subscribe_user_to_entity_report,
)


async def main() -> None:
    groups = await get_active_groups()
    active_users = set(chain.from_iterable(
        await collect(
            group_access_domain.get_users_to_notify(group)
            for group in groups
        )
    ))

    subscriptions = await get_subscriptions_to_entity_report(
        audience='user',
    )
    digest_suscribers = [
        subscription['pk']['email']
        for subscription in subscriptions
        if subscription['sk']['entity'].lower() == 'digest'
    ]

    to_subscribe = [
        user
        for user in active_users
        if user not in digest_suscribers
    ]

    await collect(
        subscribe_user_to_entity_report(
            event_frequency='DAILY',
            report_entity='DIGEST',
            report_subject='ALL_GROUPS',
            user_email=user,
        )
        for user in to_subscribe
    )


if __name__ == '__main__':
    execution_time = time.strftime(
        'Execution Time:    %Y-%m-%d at %H:%M:%S UTC%Z'
    )
    run(main())
    finalization_time = time.strftime(
        'Finalization Time: %Y-%m-%d at %H:%M:%S UTC%Z'
    )
    print(f'{execution_time}\n{finalization_time}')
