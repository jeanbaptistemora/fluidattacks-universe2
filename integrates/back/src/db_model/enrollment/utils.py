from .types import (
    Enrollment,
    EnrollmentMetadataToUpdate,
)
from dynamodb.types import (
    Item,
)


def format_enrollment(item: Item) -> Enrollment:
    return Enrollment(
        email=str(item["email"]).lower().strip(),
        enrolled=item["enrolled"],
    )


def format_metadata_item(metadata: EnrollmentMetadataToUpdate) -> Item:
    item: Item = {
        "enrolled": metadata.enrolled,
    }
    return {
        key: None if not value and value is not False else value
        for key, value in item.items()
        if value is not None
    }
