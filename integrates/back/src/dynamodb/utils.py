import base64
from dynamodb.types import (
    Item,
    Table,
)
import json
from typing import (
    Dict,
    Optional,
)


def get_cursor(table: Table, item: Optional[Item]) -> str:
    cursor_obj = None
    if item:
        cursor_obj = {
            table.primary_key.partition_key: item[
                table.primary_key.partition_key
            ],
            table.primary_key.sort_key: item[table.primary_key.sort_key],
        }

    return base64.b64encode(json.dumps(cursor_obj).encode()).decode()


def get_key_from_cursor(cursor: str) -> Dict[str, str]:
    return json.loads(base64.decodebytes(cursor.encode()))
