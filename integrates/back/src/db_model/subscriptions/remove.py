from boto3.dynamodb.conditions import (
    Key,
)
from db_model import (
    TABLE,
)
from db_model.subscriptions.enums import (
    SubscriptionEntity,
)
from dynamodb import (
    keys,
    operations,
)
from dynamodb.types import (
    PrimaryKey,
)


async def remove(
    *,
    entity: SubscriptionEntity,
    subject: str,
    email: str,
) -> None:
    historic_key = keys.build_key(
        facet=TABLE.facets["stakeholder_historic_subscription"],
        values={
            "email": email,
            "entity": entity.lower(),
            "subject": subject,
        },
    )
    key_structure = TABLE.primary_key
    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(historic_key.partition_key)
        ),
        facets=(TABLE.facets["stakeholder_historic_subscription"],),
        table=TABLE,
    )
    await operations.batch_delete_item(
        keys=tuple(
            PrimaryKey(
                partition_key=item[key_structure.partition_key],
                sort_key=item[key_structure.sort_key],
            )
            for item in response.items
        ),
        table=TABLE,
    )

    primary_key = keys.build_key(
        facet=TABLE.facets["stakeholder_subscription"],
        values={
            "email": email,
            "entity": entity.lower(),
            "subject": subject,
        },
    )
    await operations.delete_item(key=primary_key, table=TABLE)
