# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from .constants import (
    GSI_2_FACET,
)
from .types import (
    ToeInput,
)
from .utils import (
    format_toe_input_item,
)
from boto3.dynamodb.conditions import (
    Attr,
)
from custom_exceptions import (
    RepeatedToeInput,
)
from dynamodb import (
    keys,
    operations,
)
from dynamodb.exceptions import (
    ConditionalCheckFailedException,
)
from dynamodb.model import (
    TABLE,
)


async def add(*, toe_input: ToeInput) -> None:
    key_structure = TABLE.primary_key
    gsi_2_index = TABLE.indexes["gsi_2"]
    facet = TABLE.facets["toe_input_metadata"]
    toe_input_key = keys.build_key(
        facet=facet,
        values={
            "component": toe_input.component,
            "entry_point": toe_input.entry_point,
            "group_name": toe_input.group_name,
            "root_id": toe_input.unreliable_root_id,
        },
    )
    gsi_2_key = keys.build_key(
        facet=GSI_2_FACET,
        values={
            "be_present": str(toe_input.be_present).lower(),
            "component": toe_input.component,
            "entry_point": toe_input.entry_point,
            "group_name": toe_input.group_name,
            "root_id": toe_input.unreliable_root_id,
        },
    )
    toe_input_item = format_toe_input_item(
        toe_input_key, key_structure, gsi_2_key, gsi_2_index, toe_input
    )
    condition_expression = Attr(key_structure.partition_key).not_exists()
    try:
        await operations.put_item(
            condition_expression=condition_expression,
            facet=facet,
            item=toe_input_item,
            table=TABLE,
        )
    except ConditionalCheckFailedException as ex:
        raise RepeatedToeInput() from ex
