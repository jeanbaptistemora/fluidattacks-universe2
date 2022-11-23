from .types import (
    Enrollment,
    EnrollmentMetadataToUpdate,
    Trial,
)
from dynamodb.types import (
    Item,
)
import simplejson as json


def format_enrollment(item: Item) -> Enrollment:
    return Enrollment(
        email=str(item["email"]).lower().strip(),
        enrolled=item["enrolled"],
        trial=format_trial(item["trial"]),
    )


def format_trial(item: Item) -> Trial:
    return Trial(
        completed=item["completed"],
        extension_date=item["extension_date"],
        extension_days=item["extension_days"],
        start_date=item["start_date"],
    )


def format_metadata_item(metadata: EnrollmentMetadataToUpdate) -> Item:
    item: Item = {
        "enrolled": metadata.enrolled,
        "trial": json.loads(json.dumps(metadata.trial)),
    }
    return {
        key: None if not value and value is not False else value
        for key, value in item.items()
        if value is not None
    }
