from .types import (
    EnrollmentMetadataToUpdate,
)
from .utils import (
    format_metadata_item,
)
from boto3.dynamodb.conditions import (
    Attr,
)
from custom_exceptions import (
    EnrollmentNotFound,
)
from db_model import (
    TABLE,
)
from dynamodb import (
    keys,
    operations,
)
from dynamodb.exceptions import (
    ConditionalCheckFailedException,
)


async def update_metadata(
    *,
    email: str,
    metadata: EnrollmentMetadataToUpdate,
) -> None:
    key_structure = TABLE.primary_key
    primary_key = keys.build_key(
        facet=TABLE.facets["enrollment_metadata"],
        values={
            "email": email,
        },
    )
    item = format_metadata_item(metadata=metadata)
    if item:
        try:
            await operations.update_item(
                condition_expression=Attr(
                    key_structure.partition_key
                ).exists(),
                item=item,
                key=primary_key,
                table=TABLE,
            )
        except ConditionalCheckFailedException as ex:
            raise EnrollmentNotFound() from ex
