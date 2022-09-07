# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from .constants import (
    ALL_SUBSCRIPTIONS_INDEX_METADATA,
    SUBSCRIPTIONS_PREFIX,
)
from .enums import (
    SubscriptionFrequency,
)
from .types import (
    Subscription,
)
from .utils import (
    format_subscriptions,
)
from aiodataloader import (
    DataLoader,
)
from aioextensions import (
    collect,
)
from boto3.dynamodb.conditions import (
    Key,
)
from custom_exceptions import (
    ErrorLoadingStakeholderSubscriptions,
)
from db_model import (
    TABLE,
)
from dynamodb import (
    keys,
    operations,
)
from typing import (
    Iterable,
)


async def _get_stakeholder_subscriptions(
    *, email: str
) -> tuple[Subscription, ...]:
    primary_key = keys.build_key(
        facet=TABLE.facets["stakeholder_subscription"],
        values={"email": email},
    )
    key_structure = TABLE.primary_key
    condition_expression = Key(key_structure.partition_key).eq(
        primary_key.partition_key
    ) & Key(key_structure.sort_key).begins_with(SUBSCRIPTIONS_PREFIX)
    response = await operations.query(
        condition_expression=condition_expression,
        facets=(TABLE.facets["stakeholder_subscription"],),
        table=TABLE,
    )
    return tuple(format_subscriptions(item) for item in response.items)


async def get_all_subscriptions(
    *, frequency: SubscriptionFrequency
) -> tuple[Subscription, ...]:
    primary_key = keys.build_key(
        facet=ALL_SUBSCRIPTIONS_INDEX_METADATA,
        values={
            "all": "all",
            "frequency": frequency.lower(),
        },
    )
    index = TABLE.indexes["gsi_2"]
    key_structure = index.primary_key
    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key)
            & Key(key_structure.sort_key).eq(primary_key.sort_key)
        ),
        facets=(ALL_SUBSCRIPTIONS_INDEX_METADATA,),
        table=TABLE,
        index=index,
    )

    if not response.items:
        raise ErrorLoadingStakeholderSubscriptions()

    return tuple(format_subscriptions(item) for item in response.items)


class StakeholderSubscriptionsLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, emails: Iterable[str]
    ) -> tuple[tuple[Subscription, ...], ...]:
        return await collect(
            _get_stakeholder_subscriptions(email=email) for email in emails
        )
