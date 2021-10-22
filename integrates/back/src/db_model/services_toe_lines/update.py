from .types import (
    ServicesToeLines,
    ServicesToeLinesMetadataToUpdate,
)
from boto3.dynamodb.conditions import (
    Attr,
)
from custom_exceptions import (
    ToeLinesNotFound,
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


async def update(*, services_toe_lines: ServicesToeLines) -> None:
    key_structure = TABLE.primary_key
    facet = TABLE.facets["root_services_toe_lines"]
    toe_lines_key = keys.build_key(
        facet=facet,
        values={
            "filename": services_toe_lines.filename,
            "group_name": services_toe_lines.group_name,
            "root_id": services_toe_lines.root_id,
        },
    )
    toe_lines_item = {
        key_structure.partition_key: toe_lines_key.partition_key,
        key_structure.sort_key: toe_lines_key.sort_key,
        **dict(services_toe_lines._asdict()),
    }
    condition_expression = Attr(key_structure.partition_key).exists()
    try:
        await operations.put_item(
            condition_expression=condition_expression,
            facet=facet,
            item=toe_lines_item,
            table=TABLE,
        )
    except ConditionalCheckFailedException as ex:
        raise ToeLinesNotFound() from ex


async def update_metadata(
    *,
    group_name: str,
    filename: str,
    root_id: str,
    metadata: ServicesToeLinesMetadataToUpdate,
) -> None:
    key_structure = TABLE.primary_key
    metadata_key = keys.build_key(
        facet=TABLE.facets["root_services_toe_lines"],
        values={
            "filename": filename,
            "group_name": group_name,
            "root_id": root_id,
        },
    )
    metadata_item = {
        key: value
        for key, value in metadata._asdict().items()
        if value is not None
    }
    condition_expression = Attr(key_structure.partition_key).exists()
    await operations.update_item(
        condition_expression=condition_expression,
        item=metadata_item,
        key=metadata_key,
        table=TABLE,
    )
