from .constants import (
    GSI_2_FACET,
)
from .types import (
    ToeInput,
    ToeInputMetadataToUpdate,
    ToeInputState,
)
from .utils import (
    format_toe_input_state_item,
)
from boto3.dynamodb.conditions import (
    Attr,
)
from custom_exceptions import (
    ToeInputAlreadyUpdated,
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
from dynamodb.types import (
    Item,
)
import simplejson as json


async def update_state(
    *,
    current_value: ToeInput,
    new_state: ToeInputState,
    metadata: ToeInputMetadataToUpdate,
) -> None:
    key_structure = TABLE.primary_key
    gsi_2_index = TABLE.indexes["gsi_2"]
    facet = TABLE.facets["toe_input_metadata"]
    toe_input_key = keys.build_key(
        facet=facet,
        values={
            "component": current_value.component,
            "entry_point": current_value.entry_point,
            "group_name": current_value.group_name,
            "root_id": current_value.state.unreliable_root_id,
        },
    )
    gsi_2_index = TABLE.indexes["gsi_2"]
    gsi_2_key = keys.build_key(
        facet=GSI_2_FACET,
        values={
            "be_present": str(new_state.be_present).lower(),
            "component": current_value.component,
            "entry_point": current_value.entry_point,
            "group_name": current_value.group_name,
            "root_id": current_value.state.unreliable_root_id,
        },
    )

    new_state_item: Item = format_toe_input_state_item(
        state_item=json.loads(json.dumps(new_state, default=serialize)),
        metadata=metadata,
    )
    new_item = {
        "state": new_state_item,
        gsi_2_index.primary_key.sort_key: gsi_2_key.sort_key,
    }
    condition_expression = Attr(key_structure.partition_key).exists() & Attr(
        "state.modified_date"
    ).eq(get_as_utc_iso_format(current_value.state.modified_date))
    try:
        await operations.update_item(
            condition_expression=condition_expression,
            item=new_item,
            key=toe_input_key,
            table=TABLE,
        )
    except ConditionalCheckFailedException as ex:
        raise ToeInputAlreadyUpdated() from ex

    historic_key = keys.build_key(
        facet=TABLE.facets["toe_input_historic_metadata"],
        values={
            "component": current_value.component,
            "entry_point": current_value.entry_point,
            "group_name": current_value.group_name,
            "root_id": current_value.state.unreliable_root_id,
            "iso8601utc": get_as_utc_iso_format(new_state.modified_date),
        },
    )
    base_historic_item: Item = json.loads(
        json.dumps(current_value, default=serialize)
    )
    await operations.put_item(
        facet=TABLE.facets["toe_input_historic_metadata"],
        condition_expression=Attr(key_structure.sort_key).not_exists(),
        item={
            **base_historic_item,
            "state": new_state_item,
            key_structure.partition_key: historic_key.partition_key,
            key_structure.sort_key: historic_key.sort_key,
        },
        table=TABLE,
    )
