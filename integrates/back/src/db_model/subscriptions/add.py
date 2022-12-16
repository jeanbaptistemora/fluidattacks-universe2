from .constants import (
    ALL_SUBSCRIPTIONS_INDEX_METADATA,
)
from .types import (
    Subscription,
)
from .utils import (
    format_subscription_item,
)
from db_model import (
    TABLE,
)
from db_model.utils import (
    get_as_utc_iso_format,
)
from dynamodb import (
    keys,
    operations,
)


async def add(*, subscription: Subscription) -> None:
    key_structure = TABLE.primary_key
    gsi_2_index = TABLE.indexes["gsi_2"]
    subscription_key = keys.build_key(
        facet=TABLE.facets["stakeholder_subscription"],
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
            "frequency": subscription.frequency.lower(),
        },
    )
    subscription_item = {
        key_structure.partition_key: subscription_key.partition_key,
        key_structure.sort_key: subscription_key.sort_key,
        gsi_2_index.primary_key.sort_key: gsi_2_key.sort_key,
        gsi_2_index.primary_key.partition_key: gsi_2_key.partition_key,
        **format_subscription_item(subscription),
    }

    historic_subscription_key = keys.build_key(
        facet=TABLE.facets["stakeholder_historic_subscription"],
        values={
            "email": subscription.email,
            "entity": subscription.entity.lower(),
            "subject": subscription.subject,
            # The modified date will always exist here
            "iso8601utc": get_as_utc_iso_format(
                subscription.state.modified_date
            )
            if subscription.state.modified_date
            else "",
        },
    )

    historic_subscription_item = {
        key_structure.partition_key: historic_subscription_key.partition_key,
        key_structure.sort_key: historic_subscription_key.sort_key,
        **format_subscription_item(subscription),
    }

    await operations.batch_put_item(
        items=(subscription_item, historic_subscription_item), table=TABLE
    )
