from .enums import (
    FindingEvidenceName,
)
from boto3.dynamodb.conditions import (
    Attr,
)
from db_model import (
    TABLE,
)
from dynamodb import (
    keys,
    operations,
)


async def remove_evidence(
    *,
    group_name: str,
    finding_id: str,
    evidence_name: FindingEvidenceName,
) -> None:
    key_structure = TABLE.primary_key
    metadata_key = keys.build_key(
        facet=TABLE.facets["finding_metadata"],
        values={"group_name": group_name, "id": finding_id},
    )
    metadata_item = {f"evidences.{evidence_name.value}": None}
    condition_expression = Attr(key_structure.partition_key).exists()
    await operations.update_item(
        condition_expression=condition_expression,
        item=metadata_item,
        key=metadata_key,
        table=TABLE,
    )
