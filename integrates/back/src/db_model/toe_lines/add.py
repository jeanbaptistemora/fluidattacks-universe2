from .constants import (
    GSI_2_FACET,
)
from .types import (
    ToeLines,
)
from boto3.dynamodb.conditions import (
    Attr,
)
from custom_exceptions import (
    RepeatedToeLines,
)
from db_model.toe_lines.utils import (
    format_toe_lines_item,
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


async def add(*, toe_lines: ToeLines) -> None:
    key_structure = TABLE.primary_key
    gsi_2_index = TABLE.indexes["gsi_2"]
    facet = TABLE.facets["toe_lines_metadata"]
    toe_lines_key = keys.build_key(
        facet=facet,
        values={
            "filename": toe_lines.filename,
            "group_name": toe_lines.group_name,
            "root_id": toe_lines.root_id,
        },
    )
    gsi_2_key = keys.build_key(
        facet=GSI_2_FACET,
        values={
            "be_present": str(toe_lines.state.be_present).lower(),
            "filename": toe_lines.filename,
            "group_name": toe_lines.group_name,
            "root_id": toe_lines.root_id,
        },
    )
    toe_lines_item = format_toe_lines_item(
        toe_lines_key,
        key_structure,
        toe_lines,
        gsi_2_index,
        gsi_2_key,
    )
    condition_expression = Attr(key_structure.partition_key).not_exists()
    try:
        await operations.put_item(
            condition_expression=condition_expression,
            facet=facet,
            item=toe_lines_item,
            table=TABLE,
        )
    except ConditionalCheckFailedException as ex:
        raise RepeatedToeLines() from ex

    historic_key = keys.build_key(
        facet=TABLE.facets["toe_lines_historic_metadata"],
        values={
            "filename": toe_lines.filename,
            "group_name": toe_lines.group_name,
            "root_id": toe_lines.root_id,
            # The modified date will always exist here
            "iso8601utc": get_as_utc_iso_format(toe_lines.state.modified_date)
            if toe_lines.state.modified_date
            else "",
        },
    )
    historic_item = format_toe_lines_item(
        historic_key, key_structure, toe_lines
    )
    try:
        await operations.put_item(
            condition_expression=condition_expression,
            facet=TABLE.facets["toe_lines_historic_metadata"],
            item=historic_item,
            table=TABLE,
        )
    except ConditionalCheckFailedException as ex:
        raise RepeatedToeLines() from ex
