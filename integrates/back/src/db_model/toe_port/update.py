# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from .constants import (
    GSI_2_FACET,
)
from .types import (
    ToePort,
    ToePortMetadataToUpdate,
)
from .utils import (
    format_toe_port_item,
)
from boto3.dynamodb.conditions import (
    Attr,
)
from custom_exceptions import (
    ToePortAlreadyUpdated,
)
from datetime import (
    datetime,
)
from db_model import (
    utils as db_model_utils,
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
from typing import (
    Union,
)


async def update_metadata(
    *, current_value: ToePort, metadata: ToePortMetadataToUpdate
) -> None:
    key_structure = TABLE.primary_key
    gsi_2_index = TABLE.indexes["gsi_2"]
    facet = TABLE.facets["toe_port_metadata"]
    metadata_key = keys.build_key(
        facet=facet,
        values={
            "group_name": current_value.group_name,
            "ip": current_value.ip,
            "port": current_value.port,
            "root_id": current_value.root_id,
        },
    )
    current_gsi_2_key = keys.build_key(
        facet=GSI_2_FACET,
        values={
            "be_present": str(current_value.be_present).lower(),
            "group_name": current_value.group_name,
            "ip": current_value.ip,
            "port": current_value.port,
            "root_id": current_value.root_id,
        },
    )
    current_value_item = format_toe_port_item(
        metadata_key,
        key_structure,
        current_gsi_2_key,
        gsi_2_index,
        current_value,
    )
    metadata_item: dict[str, Union[str, datetime, None]] = {
        key: db_model_utils.get_date_as_utc_iso_format(value)
        if isinstance(value, datetime)
        else value
        for key, value in metadata._asdict().items()
        if value is not None
        and key
        not in {
            "clean_attacked_at",
            "clean_be_present_until",
            "clean_first_attack_at",
            "clean_seen_at",
        }
    }
    if metadata.clean_attacked_at:
        metadata_item["attacked_at"] = None
    if metadata.clean_be_present_until:
        metadata_item["be_present_until"] = None
    if metadata.clean_first_attack_at:
        metadata_item["first_attack_at"] = None
    if metadata.clean_seen_at:
        metadata_item["seen_at"] = None

    conditions = tuple(
        Attr(attr_name).not_exists()
        if current_value_item[attr_name] is None
        else Attr(attr_name).eq(current_value_item[attr_name])
        for attr_name in metadata_item
    )
    condition_expression = Attr(key_structure.partition_key).exists()
    for condition in conditions:
        condition_expression &= condition
    if "be_present" in metadata_item:
        gsi_2_key = keys.build_key(
            facet=GSI_2_FACET,
            values={
                "be_present": str(metadata_item["be_present"]).lower(),
                "group_name": current_value.group_name,
                "ip": current_value.ip,
                "port": current_value.port,
                "root_id": current_value.root_id,
            },
        )
        gsi_2_index = TABLE.indexes["gsi_2"]
        metadata_item[gsi_2_index.primary_key.sort_key] = gsi_2_key.sort_key
    try:
        if metadata_item:
            await operations.update_item(
                condition_expression=condition_expression,
                item=metadata_item,
                key=metadata_key,
                table=TABLE,
            )
    except ConditionalCheckFailedException as ex:
        raise ToePortAlreadyUpdated() from ex
