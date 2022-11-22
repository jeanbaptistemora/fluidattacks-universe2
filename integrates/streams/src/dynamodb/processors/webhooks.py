# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
from boto3.dynamodb.conditions import (
    Key,
)
from dynamodb.context import (
    FI_GOOGLE_CHAT_WEBHOOK_URL,
    FI_WEBHOOK_POC_KEY,
    FI_WEBHOOK_POC_ORG,
    FI_WEBHOOK_POC_URL,
)
from dynamodb.resource import (
    TABLE_RESOURCE,
)
from dynamodb.types import (
    HookEvent,
    Item,
    Record,
    StreamEvent,
)
import itertools
import logging
from operator import (
    itemgetter,
)
import requests  # type: ignore
from typing import (
    Any,
    Optional,
)

LOGGER = logging.getLogger(__name__)


def _determine_vuln_event(
    stream_event: StreamEvent,
    new_vuln: Optional[Item],
    old_vuln: Optional[Item],
    is_finding_released: bool,
) -> Optional[HookEvent]:
    event: Optional[HookEvent] = None
    if new_vuln is not None:
        if (
            # A vulnerability was reported to a finding
            stream_event == StreamEvent.INSERT
            and is_finding_released
        ) or (
            # An existing report was promoted from draft to finding
            stream_event == StreamEvent.MODIFY
            and old_vuln is not None
            and new_vuln["created_date"] != old_vuln["created_date"]
        ):
            event = HookEvent.REPORTED_VULNERABILITY
        elif stream_event == StreamEvent.MODIFY and is_finding_released:
            event = HookEvent.EDITED_VULNERABILITY
    elif stream_event == StreamEvent.REMOVE and is_finding_released:
        event = HookEvent.DELETED_VULNERABILITY

    return event


def _get_attribute(
    attr: str, new_record: Optional[Item], old_record: Optional[Item]
) -> Any:
    value: Optional[Any] = None
    if new_record is not None and attr in new_record:
        value = new_record[attr]
    if value is None and old_record is not None and attr in old_record:
        value = old_record[attr]

    if value is None:
        raise KeyError()

    return value


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


def _is_released(group_name: str, finding_id: str) -> bool:
    response = TABLE_RESOURCE.get_item(
        Key={"pk": f"FIN#{finding_id}", "sk": f"GROUP#{group_name}"}
    )
    item = response["Item"]
    return item["state"]["status"] == "APPROVED"


def _notify_client(vuln_id: str, event: HookEvent) -> None:
    try:
        requests.post(
            FI_WEBHOOK_POC_URL,
            headers={"x-api-key": FI_WEBHOOK_POC_KEY},
            json={
                "event": event.value,
                "id_vulnerability": vuln_id,
            },
        )
        LOGGER.info(
            "[POC] Notified event `%s` for vulnerability %s",
            event.value,
            vuln_id,
        )
    except requests.exceptions.RequestException as ex:
        LOGGER.exception(ex)


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

        requests.post(FI_GOOGLE_CHAT_WEBHOOK_URL, json={"text": text})


def process_poc(records: tuple[Record, ...]) -> None:
    findings: set[str] = set()
    released_findings: set[str] = set()
    poc_groups = (
        _get_poc_groups(FI_WEBHOOK_POC_ORG) if FI_WEBHOOK_POC_ORG else []
    )
    for record in records:
        try:
            new_vuln, old_vuln = record.new_image, record.old_image
            group = str(_get_attribute("group_name", new_vuln, old_vuln))
            vuln_id = str(_get_attribute("pk", new_vuln, old_vuln)).split("#")[
                1
            ]
            finding_id = str(_get_attribute("sk", new_vuln, old_vuln)).split(
                "#"
            )[1]
            if group not in poc_groups:
                continue

            # We may avoid a few redundant requests
            # if vulns from the same finding are in the same stream
            if finding_id not in findings:
                findings.add(finding_id)
                if _is_released(group, finding_id):
                    released_findings.add(finding_id)

            event = _determine_vuln_event(
                record.event_name,
                new_vuln,
                old_vuln,
                finding_id in released_findings,
            )
            if event is not None:
                _notify_client(vuln_id, event)
        except KeyError as ex:
            LOGGER.exception(ex)
