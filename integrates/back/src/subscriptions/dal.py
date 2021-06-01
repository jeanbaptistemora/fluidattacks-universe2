from boto3.dynamodb.conditions import (
    Key,
)
from custom_types import (
    DynamoDelete,
)
from decimal import (
    Decimal,
)
from dynamodb import (
    operations_legacy as dynamodb_ops,
)
from newutils.encodings import (
    key_to_mapping,
    mapping_to_key,
)
from typing import (
    Any,
    Dict,
    List,
    Union,
)

# Constants
SUBSCRIPTIONS_TABLE = "fi_subscriptions"
NumericType = Union[Decimal, float, int]


def _unpack_items(items: List[Dict[Any, Any]]) -> List[Dict[Any, Any]]:
    return [
        {
            **item,
            "pk": key_to_mapping(item["pk"]),
            "sk": key_to_mapping(item["sk"]),
        }
        for item in items
    ]


async def get_subscriptions_to_entity_report(
    *,
    audience: str,
) -> List[Dict[Any, Any]]:
    results = await dynamodb_ops.query(
        query_attrs=dict(
            IndexName="pk_meta",
            KeyConditionExpression=(
                Key("pk_meta").eq(audience)
                & Key("sk_meta").eq("entity_report")
            ),
        ),
        table=SUBSCRIPTIONS_TABLE,
    )
    return _unpack_items(results)


async def get_user_subscriptions(
    *,
    user_email: str,
) -> List[Dict[Any, Any]]:
    results = await dynamodb_ops.query(
        query_attrs=dict(
            KeyConditionExpression=Key("pk").eq(
                mapping_to_key(
                    {
                        "meta": "user",
                        "email": user_email,
                    }
                )
            ),
        ),
        table=SUBSCRIPTIONS_TABLE,
    )
    return _unpack_items(results)


async def subscribe_user_to_entity_report(
    *,
    event_period: NumericType,
    report_entity: str,
    report_subject: str,
    user_email: str,
) -> bool:
    return await dynamodb_ops.put_item(
        item=dict(
            pk=mapping_to_key(
                {
                    "meta": "user",
                    "email": user_email,
                }
            ),
            sk=mapping_to_key(
                {
                    "meta": "entity_report",
                    "entity": report_entity,
                    "subject": report_subject,
                }
            ),
            period=Decimal(event_period),
            pk_meta="user",
            sk_meta="entity_report",
        ),
        table=SUBSCRIPTIONS_TABLE,
    )


async def unsubscribe_user_to_entity_report(
    *,
    report_entity: str,
    report_subject: str,
    user_email: str,
) -> bool:
    return await dynamodb_ops.delete_item(
        delete_attrs=DynamoDelete(
            Key=dict(
                pk=mapping_to_key(
                    {
                        "meta": "user",
                        "email": user_email,
                    }
                ),
                sk=mapping_to_key(
                    {
                        "meta": "entity_report",
                        "entity": report_entity,
                        "subject": report_subject,
                    }
                ),
            )
        ),
        table=SUBSCRIPTIONS_TABLE,
    )
