from .constants import (
    ALL_SUBSCRIPTIONS_INDEX_METADATA,
)
from .types import (
    Subscription,
)
from .utils import (
    format_subscription_item,
)
from dynamodb import (
    keys,
    operations,
)
from dynamodb.model import (
    TABLE,
)


async def add(*, subscription: Subscription) -> None:
    key_structure = TABLE.primary_key
    gsi_2_index = TABLE.indexes["gsi_2"]
    facet = TABLE.facets["stakeholder_subscription"]
    subscription_key = keys.build_key(
        facet=facet,
        values={
            "email": subscription.email,
            "entity": subscription.entity.lower(),
            "subject": subscription.subject,
        },
    )
    gsi_2_key = keys.build_key(
        facet=ALL_SUBSCRIPTIONS_INDEX_METADATA,
        values={
            "all": "all",
            "frequency": subscription.frequency,
        },
    )
    item = {
        key_structure.partition_key: subscription_key.partition_key,
        key_structure.sort_key: subscription_key.sort_key,
        gsi_2_index.primary_key.sort_key: gsi_2_key.sort_key,
        gsi_2_index.primary_key.partition_key: gsi_2_key.partition_key,
        **format_subscription_item(subscription),
    }
    await operations.put_item(
        facet=facet,
        item=item,
        table=TABLE,
    )
