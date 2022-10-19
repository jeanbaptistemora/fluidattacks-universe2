# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from boto3.dynamodb.conditions import (
    Key,
)
from dynamodb.context import (
    FI_ENVIRONMENT,
    FI_WEBHOOK_POC_ORG,
)
from dynamodb.processors import (
    opensearch,
    redshift,
    webhooks,
)
from dynamodb.resource import (
    TABLE_RESOURCE,
)
from dynamodb.types import (
    EventName,
    Trigger,
)
from typing import (
    Any,
)


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


POC_GROUPS = _get_poc_groups(FI_WEBHOOK_POC_ORG) if FI_WEBHOOK_POC_ORG else []

TRIGGERS: tuple[Trigger, ...] = (
    Trigger(
        records_filter=(
            lambda record: FI_ENVIRONMENT == "prod"
            and record.pk.startswith("VULN#")
            and record.sk.startswith("FIN#")
            and record.event_name == EventName.INSERT
        ),
        records_processor=webhooks.process_google_chat,
    ),
    Trigger(
        records_filter=(
            lambda record: FI_ENVIRONMENT == "prod"
            and record.pk.startswith("VULN#")
            and record.sk.startswith("FIN#")
            and record.new_image is not None
            and record.new_image["group_name"] in POC_GROUPS
            and (
                (  # After approving the draft
                    record.event_name == EventName.MODIFY
                    and record.old_image is not None
                    and record.new_image.get("created_date")
                    != record.old_image.get("created_date")
                )
                or (
                    # After uploading vulns to an existing finding
                    record.event_name == EventName.INSERT
                    and _is_released(
                        record.new_image["group_name"],
                        record.new_image["finding_id"],
                    )
                )
            )
        ),
        records_processor=webhooks.process_poc,
    ),
    Trigger(
        records_filter=(
            lambda record: record.pk.startswith("VULN#")
            and record.sk.startswith("FIN#")
        ),
        records_processor=opensearch.process_vulns,
    ),
    Trigger(
        records_filter=(
            lambda record: record.pk.startswith("FIN#")
            and record.sk.startswith("GROUP#")
        ),
        records_processor=opensearch.process_findings,
    ),
    Trigger(
        records_filter=(
            lambda record: record.pk.startswith("EXEC#")
            and record.sk.startswith("GROUP#")
        ),
        records_processor=opensearch.process_executions,
    ),
    Trigger(
        records_filter=(
            lambda record: FI_ENVIRONMENT == "prod"
            and record.event_name == EventName.REMOVE
            and record.pk.startswith("FIN#")
        ),
        records_processor=redshift.process_findings,
    ),
    Trigger(
        records_filter=(
            lambda record: FI_ENVIRONMENT == "prod"
            and record.event_name == EventName.REMOVE
            and record.pk.startswith("VULN#")
        ),
        records_processor=redshift.process_vulnerabilities,
    ),
    Trigger(
        records_filter=(
            lambda record: FI_ENVIRONMENT == "prod"
            and record.event_name == EventName.REMOVE
            and record.pk.startswith("GROUP#")
            and record.sk.startswith("INPUTS#")
        ),
        records_processor=redshift.process_toe_inputs,
    ),
    Trigger(
        records_filter=(
            lambda record: record.pk.startswith("EVENT#")
            and record.sk.startswith("GROUP#")
        ),
        records_processor=opensearch.process_events,
    ),
)
