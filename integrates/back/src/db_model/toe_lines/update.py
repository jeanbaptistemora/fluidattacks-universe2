from .constants import (
    GSI_2_FACET,
)
from .types import (
    ToeLines,
    ToeLinesState,
)
from .utils import (
    format_toe_lines_item,
)
from boto3.dynamodb.conditions import (
    Attr,
)
from custom_exceptions import (
    ToeLinesAlreadyUpdated,
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
    current_value: ToeLines,
    new_state: ToeLinesState,
) -> None:
    key_structure = TABLE.primary_key
    gsi_2_index = TABLE.indexes["gsi_2"]
    metadata_key = keys.build_key(
        facet=TABLE.facets["toe_lines_metadata"],
        values={
            "filename": current_value.filename,
            "group_name": current_value.group_name,
            "root_id": current_value.root_id,
        },
    )
    new_state_item: Item = json.loads(json.dumps(new_state, default=serialize))

    condition_expression = Attr(key_structure.partition_key).exists() & Attr(
        "state.modified_date"
    ).eq(get_as_utc_iso_format(current_value.state.modified_date))

    gsi_2_key = keys.build_key(
        facet=GSI_2_FACET,
        values={
            "be_present": str(new_state.be_present).lower(),
            "filename": current_value.filename,
            "group_name": current_value.group_name,
            "root_id": current_value.root_id,
        },
    )
    gsi_2_index = TABLE.indexes["gsi_2"]
    metadata_item = {
        gsi_2_index.primary_key.sort_key: gsi_2_key.sort_key,
        "state": new_state_item,
    }
    try:
        await operations.update_item(
            condition_expression=condition_expression,
            item=metadata_item,
            key=metadata_key,
            table=TABLE,
        )
    except ConditionalCheckFailedException as ex:
        raise ToeLinesAlreadyUpdated() from ex

    historic_key = keys.build_key(
        facet=TABLE.facets["toe_lines_historic_metadata"],
        values={
            "filename": current_value.filename,
            "group_name": current_value.group_name,
            "root_id": current_value.root_id,
            "iso8601utc": get_as_utc_iso_format(new_state.modified_date),
        },
    )
    historic_item = format_toe_lines_item(
        primary_key=historic_key,
        key_structure=key_structure,
        toe_lines=current_value,
    ) | {"state": new_state_item}
    await operations.put_item(
        facet=TABLE.facets["toe_lines_historic_metadata"],
        condition_expression=Attr(key_structure.sort_key).not_exists(),
        item=historic_item,
        table=TABLE,
    )
