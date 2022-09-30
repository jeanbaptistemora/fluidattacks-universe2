# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from boto3.dynamodb.conditions import (
    Key,
)
from dynamodb.context import (
    FI_GOOGLE_CHAT_WEBOOK_URL,
    FI_WEBHOOK_POC_KEY,
    FI_WEBHOOK_POC_ORG,
    FI_WEBHOOK_POC_URL,
)
from dynamodb.resource import (
    TABLE_RESOURCE,
)
from dynamodb.types import (
    Record,
)
import itertools
import logging
from operator import (
    itemgetter,
)
import requests  # type: ignore
from typing import (
    Any,
)

LOGGER = logging.getLogger(__name__)


def process_google_chat(records: tuple[Record, ...]) -> None:
    """Notifies external integrations"""
    items_to_notify = tuple(
        record.new_image for record in records if record.new_image
    )
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


def _get_poc_groups(org_id: str) -> list[str]:
    query_args = {
        "ExpressionAttributeNames": {"#name": "name"},
        "IndexName": "inverted_index",
        "KeyConditionExpression": (
            Key("sk").eq(org_id) & Key("pk").begins_with("GROUP#")
        ),
        "ProjectionExpression": "#name",
    }
    response = TABLE_RESOURCE.query(**query_args)
    items: list[dict[str, Any]] = response.get("Items", [])
    while response.get("LastEvaluatedKey"):
        response = TABLE_RESOURCE.query(
            **query_args,
            ExclusiveStartKey=response.get("LastEvaluatedKey"),
        )
        items += response.get("Items", [])
    return [item["name"] for item in items]


def process_poc(records: tuple[Record, ...]) -> None:
    poc_groups = _get_poc_groups(FI_WEBHOOK_POC_ORG)
    for record in records:
        if record.new_image and record.new_image["group_name"] in poc_groups:
            try:
                requests.post(
                    FI_WEBHOOK_POC_URL,
                    headers={"x-api-key": FI_WEBHOOK_POC_KEY},
                    json={"id_vulnerability": record.new_image["id"]},
                )
            except requests.exceptions.RequestException as ex:
                LOGGER.exception(ex)
