from datetime import (
    datetime,
)
from dynamodb.types import (
    Item,
)
import hashlib


def format_row_code_languages(
    item: Item,
) -> list[Item]:
    if not item.get("unreliable_indicators"):
        return []
    unreliable_indicators = item["unreliable_indicators"]
    unreliable_code_languages = unreliable_indicators.get(
        "unreliable_code_languages", []
    )
    root_id = item["pk"].split("#")[1]
    return [
        dict(
            id=hashlib.sha256(
                (root_id + language_item["language"]).encode("utf-8")
            ).hexdigest(),
            language=language_item["language"],
            loc=int(language_item["loc"]),
            root_id=root_id,
        )
        for language_item in unreliable_code_languages
    ]


def format_row_metadata(
    item: Item,
) -> Item:
    root_id = item["pk"].split("#")[1]
    group_name = item["sk"].split("#")[1]
    organization_name = item["pk_2"].split("#")[1] if "pk_2" in item else None
    return dict(
        id=root_id,
        created_date=datetime.fromisoformat(item["created_date"])
        if item.get("created_date")
        else None,
        group_name=group_name,
        organization_name=organization_name,
        type=str(item["type"]).upper(),
    )
