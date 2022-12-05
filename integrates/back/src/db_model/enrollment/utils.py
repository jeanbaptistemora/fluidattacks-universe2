from .types import (
    Enrollment,
    EnrollmentMetadataToUpdate,
    Trial,
)
from datetime import (
    datetime,
)
from db_model.utils import (
    serialize,
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
        extension_date=datetime.fromisoformat(item["extension_date"])
        if item.get("extension_date")
        else None,
        extension_days=item["extension_days"],
        start_date=datetime.fromisoformat(item["start_date"])
        if item.get("start_date")
        else None,
    )


def format_metadata_item(metadata: EnrollmentMetadataToUpdate) -> Item:
    item: Item = {
        "enrolled": metadata.enrolled,
        "trial": json.loads(json.dumps(metadata.trial, default=serialize)),
    }
    return {
        key: None if not value and value is not False else value
        for key, value in item.items()
        if value is not None
    }
