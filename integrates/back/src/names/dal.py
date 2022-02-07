from boto3.dynamodb.conditions import (
    Key,
)
from custom_exceptions import (
    EmptyPoolName,
)
from custom_types import (
    DynamoDelete,
)
from dynamodb import (
    operations_legacy as dynamodb_ops,
)
import logging
import logging.config
from settings import (
    LOGGING,
)
from typing import (
    List,
)
import uuid

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)
TABLE_NAME: str = "integrates"


async def create(name: str, entity: str) -> bool:
    """
    Create an available entity name
    """
    new_item = {
        "pk": f"AVAILABLE_{entity.upper()}",
        "sk": name.upper(),
        "gsi-2-pk": f"RANDOM_AVAILABLE_{entity.upper()}_SORT",
        "gsi-2-sk": str(uuid.uuid4()),
    }
    await dynamodb_ops.put_item(TABLE_NAME, new_item)
    return True


async def exists(name: str, entity: str) -> bool:
    """
    Returns True if the given entity name exists
    """
    item = await dynamodb_ops.get_item(
        TABLE_NAME,
        {"Key": {"pk": f"AVAILABLE_{entity.upper()}", "sk": name.upper()}},
    )
    return bool(item)


async def get_all(entity: str) -> List[str]:
    """
    Returns all availale entity names
    """
    key_exp = Key("pk").eq(f"AVAILABLE_{entity.upper()}")
    all_available = await dynamodb_ops.query(
        TABLE_NAME,
        {"KeyConditionExpression": key_exp, "ProjectionExpression": "sk"},
    )
    all_names = [available["sk"] for available in all_available]
    return all_names


async def get_one(entity: str) -> str:
    """
    Returns a random available entity name
    """
    name = ""
    random_uuid = str(uuid.uuid4())
    key_exp_gt = Key("gsi-2-pk").eq(
        f"RANDOM_AVAILABLE_{entity.upper()}_SORT"
    ) & Key("gsi-2-sk").gt(random_uuid)
    key_exp_lt = Key("gsi-2-pk").eq(
        f"RANDOM_AVAILABLE_{entity.upper()}_SORT"
    ) & Key("gsi-2-sk").lte(random_uuid)
    query_attrs = {
        "KeyConditionExpression": key_exp_gt,
        "IndexName": "gsi-2",
        "ProjectionExpression": "sk",
        "Limit": 1,
    }
    # Make two attempts to return a name using the random uuid
    # First attempt with greater than operator
    response_items = await dynamodb_ops.query(TABLE_NAME, query_attrs)
    if response_items:
        name = response_items[0].get("sk", "").lower()
    else:
        # Second attempt with less than or equal operator
        query_attrs["KeyConditionExpression"] = key_exp_lt
        response_items = await dynamodb_ops.query(TABLE_NAME, query_attrs)
        if response_items:
            name = response_items[0].get("sk", "").lower()
        else:
            raise EmptyPoolName(entity)
    return name


async def remove(name: str, entity: str) -> bool:
    """
    Removes an available entity given its name
    """
    primary_keys = {"pk": f"AVAILABLE_{entity.upper()}", "sk": name.upper()}
    await dynamodb_ops.delete_item(TABLE_NAME, DynamoDelete(Key=primary_keys))
    return True
