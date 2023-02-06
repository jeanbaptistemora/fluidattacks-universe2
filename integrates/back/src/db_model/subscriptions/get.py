from .constants import (
    ALL_SUBSCRIPTIONS_INDEX_METADATA,
    SUBSCRIPTIONS_PREFIX,
)
from .enums import (
    SubscriptionEntity,
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


async def _get_stakeholder_subscriptions(*, email: str) -> list[Subscription]:
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

    return [format_subscriptions(item) for item in response.items]


async def get_all_subscriptions(
    *, frequency: SubscriptionFrequency
) -> list[Subscription]:
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

    return [format_subscriptions(item) for item in response.items]


async def _get_historic_subscription(
    *,
    email: str,
    entity: SubscriptionEntity,
    subject: str,
) -> list[Subscription]:
    primary_key = keys.build_key(
        facet=TABLE.facets["stakeholder_historic_subscription"],
        values={
            "email": email,
            "entity": entity.lower(),
            "subject": subject,
        },
    )
    key_structure = TABLE.primary_key
    condition_expression = Key(key_structure.partition_key).eq(
        primary_key.partition_key
    ) & Key(key_structure.sort_key).begins_with(SUBSCRIPTIONS_PREFIX)
    response = await operations.query(
        condition_expression=condition_expression,
        facets=(TABLE.facets["stakeholder_historic_subscription"],),
        table=TABLE,
    )

    return [format_subscriptions(item) for item in response.items]


class StakeholderSubscriptionsLoader(DataLoader[str, list[Subscription]]):
    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, emails: Iterable[str]
    ) -> list[list[Subscription]]:
        return list(
            await collect(
                _get_stakeholder_subscriptions(email=email) for email in emails
            )
        )


class StakeholderHistoricSubscriptionLoader(
    DataLoader[tuple[str, SubscriptionEntity, str], list[Subscription]]
):
    # pylint: disable=method-hidden
    async def batch_load_fn(
        self,
        requests: Iterable[tuple[str, SubscriptionEntity, str]],
    ) -> list[list[Subscription]]:
        return list(
            await collect(
                _get_historic_subscription(
                    email=email,
                    entity=entity,
                    subject=subject,
                )
                for email, entity, subject in requests
            )
        )
