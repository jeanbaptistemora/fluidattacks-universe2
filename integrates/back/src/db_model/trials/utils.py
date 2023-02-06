from .types import (
    Trial,
)
from datetime import (
    datetime,
)
from dynamodb.types import (
    Item,
)


def format_trial(item: Item) -> Trial:
    return Trial(
        completed=item["completed"],
        email=item["email"],
        extension_date=(
            datetime.fromisoformat(item["extension_date"])
            if item.get("extension_date")
            else None
        ),
        extension_days=item["extension_days"],
        start_date=(
            datetime.fromisoformat(item["start_date"])
            if item.get("start_date")
            else None
        ),
    )
