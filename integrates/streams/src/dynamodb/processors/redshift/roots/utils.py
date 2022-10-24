# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from datetime import (
    datetime,
)
from dynamodb.types import (
    Item,
)


def format_row_code_languages(
    item: Item,
) -> list[Item]:
    if not item.get("unreliable_indicators"):
        return []
    unreliable_indicators = item["unreliable_indicators"]
    unreliable_code_languages = unreliable_indicators.get(
        "unreliable_code_languages", []
    )
    return [
        dict(
            id=item["pk"].split("#")[1],
            language=language_item["language"],
            loc=int(language_item["loc"]),
        )
        for language_item in unreliable_code_languages
    ]


def format_row_environment_url(
    item: Item,
) -> Item:
    return dict(
        id=item["sk"].split("URL#")[-1],
        cloud_name=item.get("cloud_name"),
        created_at=datetime.fromisoformat(item["created_at"])
        if "created_at" in item
        else None,
        root_id=item["pk"].split("#")[1],
        url_type=item.get("url_type"),
    )


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
