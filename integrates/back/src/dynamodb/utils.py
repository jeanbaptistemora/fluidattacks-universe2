# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

import base64
from custom_exceptions import (
    InvalidFilterCursor,
)
from dynamodb.types import (
    Index,
    Item,
    Table,
)
import json
from typing import (
    Dict,
    Optional,
)


def get_cursor(
    index: Optional[Index],
    item: Optional[Item],
    table: Table,
) -> str:
    cursor_obj = None
    if item:
        cursor_obj = {
            table.primary_key.partition_key: item[
                table.primary_key.partition_key
            ],
            table.primary_key.sort_key: item[table.primary_key.sort_key],
        }
        if index:
            cursor_obj[index.primary_key.partition_key] = item[
                index.primary_key.partition_key
            ]
            cursor_obj[index.primary_key.sort_key] = item[
                index.primary_key.sort_key
            ]

    return base64.b64encode(json.dumps(cursor_obj).encode()).decode()


def get_key_from_cursor(
    cursor: str, index: Optional[Index], table: Table
) -> Dict[str, str]:
    cursor_obj = json.loads(base64.decodebytes(cursor.encode()))
    key = {
        table.primary_key.partition_key: cursor_obj[
            table.primary_key.partition_key
        ],
        table.primary_key.sort_key: cursor_obj[table.primary_key.sort_key],
    }
    if index:
        try:
            key[index.primary_key.partition_key] = cursor_obj[
                index.primary_key.partition_key
            ]
            key[index.primary_key.sort_key] = cursor_obj[
                index.primary_key.sort_key
            ]
        except KeyError as exc:
            raise InvalidFilterCursor() from exc
    return key
