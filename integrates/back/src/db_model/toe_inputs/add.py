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
    InvalidParameter,
    RepeatedToeInput,
)
from db_model.utils import (
    get_as_utc_iso_format,
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
    if toe_input.state.modified_date is None:
        raise InvalidParameter("modified_date")

    key_structure = TABLE.primary_key
    gsi_2_index = TABLE.indexes["gsi_2"]
    facet = TABLE.facets["toe_input_metadata"]
    toe_input_key = keys.build_key(
        facet=facet,
        values={
            "component": toe_input.component,
            "entry_point": toe_input.entry_point,
            "group_name": toe_input.group_name,
            "root_id": toe_input.state.unreliable_root_id,
        },
    )
    gsi_2_key = keys.build_key(
        facet=GSI_2_FACET,
        values={
            "be_present": str(toe_input.state.be_present).lower(),
            "component": toe_input.component,
            "entry_point": toe_input.entry_point,
            "group_name": toe_input.group_name,
            "root_id": toe_input.state.unreliable_root_id,
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

    historic_key = keys.build_key(
        facet=TABLE.facets["toe_input_historic_metadata"],
        values={
            "component": toe_input.component,
            "entry_point": toe_input.entry_point,
            "group_name": toe_input.group_name,
            "root_id": toe_input.state.unreliable_root_id,
            "iso8601utc": get_as_utc_iso_format(toe_input.state.modified_date),
        },
    )
    await operations.put_item(
        facet=TABLE.facets["toe_input_historic_metadata"],
        item={
            **toe_input_item,
            key_structure.partition_key: historic_key.partition_key,
            key_structure.sort_key: historic_key.sort_key,
        },
        table=TABLE,
    )
