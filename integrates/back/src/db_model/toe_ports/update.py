from .constants import (
    GSI_2_FACET,
)
from .types import (
    ToePort,
    ToePortState,
)
from boto3.dynamodb.conditions import (
    Attr,
)
from custom_exceptions import (
    InvalidParameter,
    ToePortAlreadyUpdated,
)
from db_model.utils import (
    get_as_utc_iso_format,
    serialize,
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
import simplejson as json


async def update_state(
    *,
    current_value: ToePort,
    state: ToePortState,
) -> None:
    key_structure = TABLE.primary_key
    state_item = json.loads(json.dumps(state, default=serialize))
    gsi_2_index = TABLE.indexes["gsi_2"]
    if state.modified_date is None:
        raise InvalidParameter("modified_date")
    if state.modified_by is None:
        raise InvalidParameter("modified_by")

    try:
        metadata_key = keys.build_key(
            facet=TABLE.facets["toe_port_metadata"],
            values={
                "group_name": current_value.group_name,
                "address": current_value.address,
                "port": current_value.port,
                "root_id": current_value.root_id,
            },
        )
        gsi_2_key = keys.build_key(
            facet=GSI_2_FACET,
            values={
                "be_present": str(state.be_present).lower(),
                "group_name": current_value.group_name,
                "address": current_value.address,
                "port": current_value.port,
                "root_id": current_value.root_id,
            },
        )
        gsi_2_index = TABLE.indexes["gsi_2"]
        item = {
            "state": state_item,
            gsi_2_index.primary_key.sort_key: gsi_2_key.sort_key,
            gsi_2_index.primary_key.partition_key: gsi_2_key.partition_key,
        }
        condition_expression = Attr(key_structure.partition_key).exists()
        if current_value.state.modified_date is None:
            condition_expression &= Attr("state.modified_date").not_exists()
        else:
            condition_expression &= Attr("state.modified_date").eq(
                get_as_utc_iso_format(current_value.state.modified_date)
            )
        await operations.update_item(
            condition_expression=condition_expression,
            item=item,
            key=metadata_key,
            table=TABLE,
        )
    except ConditionalCheckFailedException as ex:
        raise ToePortAlreadyUpdated() from ex

    historic_state_key = keys.build_key(
        facet=TABLE.facets["toe_port_historic_state"],
        values={
            "address": current_value.address,
            "port": current_value.port,
            "group_name": current_value.group_name,
            "root_id": current_value.root_id,
            "iso8601utc": get_as_utc_iso_format(state.modified_date),
        },
    )
    historic_item = {
        key_structure.partition_key: historic_state_key.partition_key,
        key_structure.sort_key: historic_state_key.sort_key,
        **state_item,
    }
    await operations.put_item(
        facet=TABLE.facets["toe_port_historic_state"],
        item=historic_item,
        table=TABLE,
    )
