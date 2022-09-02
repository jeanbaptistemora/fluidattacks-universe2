from dynamodb.context import (
    FI_GOOGLE_CHAT_WEBOOK_URL,
)
from dynamodb.types import (
    Record,
)
import itertools
from operator import (
    itemgetter,
)
import requests  # type: ignore


def process(records: tuple[Record, ...]) -> None:
    """Notifies external integrations"""
    items_to_notify = tuple(record.item for record in records if record.item)
    items_by_group = itertools.groupby(
        sorted(items_to_notify, key=itemgetter("group_name")),
        key=itemgetter("group_name"),
    )

    for group_name, items in items_by_group:
        items_by_finding = itertools.groupby(
            sorted(items, key=lambda item: item["sk"].split("#")[1]),
            key=lambda item: item["sk"].split("#")[1],
        )
        base_url = "https://app.fluidattacks.com/groups"
        text = "\n".join(
            [
                f"🏹 New vulnerabilities reported on group {group_name}:",
                *[
                    f"- {base_url}/{group_name}/vulns/{finding_id}/locations"
                    for finding_id, _ in items_by_finding
                ],
            ]
        )

        requests.post(FI_GOOGLE_CHAT_WEBOOK_URL, json={"text": text})
