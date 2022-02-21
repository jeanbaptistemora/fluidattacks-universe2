from aioextensions import (
    collect,
    run,
)
import boto3
from core.expected_code_date import (
    main as get_expected_code_date,
)
from dateutil.parser import (  # type: ignore
    parse as date_parser,
)
from integrates.graphql import (
    API_TOKEN,
    create_session,
)
import json
import os
import sys
from typing import (
    List,
    NamedTuple,
    Optional,
    Tuple,
)


class BatchProcessing(NamedTuple):
    key: str
    action_name: str
    entity: str
    subject: str
    time: str
    additional_info: str
    queue: str


def get_action(
    *,
    action_dynamo_pk: str,
) -> Optional[BatchProcessing]:
    client = boto3.client("dynamodb", "us-east-1")
    query_payload = {
        "TableName": "fi_async_processing",
        "KeyConditionExpression": "#69240 = :69240",
        "ExpressionAttributeNames": {"#69240": "pk"},
        "ExpressionAttributeValues": {":69240": {"S": action_dynamo_pk}},
    }
    response_items = client.query(**query_payload)
    if not response_items:
        return None

    item = response_items[0]
    return BatchProcessing(
        key=item["pk"],
        action_name=item["action_name"].lower(),
        entity=item["entity"].lower(),
        subject=item["subject"].lower(),
        time=item["time"],
        additional_info=item.get("additional_info", ""),
        queue=item["queue"],
    )


async def should_run(
    group: str, namespace: str, check: str, token: str
) -> bool:
    expected_code_date = await get_expected_code_date(
        check, group, namespace, token
    )
    metadata_path = (
        f"groups/${group}/fusion/${namespace}/.git/fluidattacks_metadata"
    )
    try:
        with open(metadata_path, encoding="utf-8") as handler:
            metadata_date = date_parser(json.load(handler)["date"])
    except (FileNotFoundError, KeyError, ValueError) as exc:
        raise Exception(
            f"Either {metadata_path} does not exist or it is corrupt"
        ) from exc
    return metadata_date > expected_code_date


async def _should_run(
    group: str, namespace: str, check: str, token: str
) -> Tuple[str, str, str, bool]:
    return (
        group,
        namespace,
        check,
        await should_run(group, namespace, check, token),
    )


def main() -> None:
    action_dynamo_pk = sys.argv[1]
    create_session(os.environ["INTEGRATES_API_TOKEN"])
    item = get_action(
        action_dynamo_pk=action_dynamo_pk,
    )
    if not item:
        raise Exception(f"No jobs were found for the key {action_dynamo_pk}")

    group_name = item.entity
    job_details = json.loads(item.additional_info)
    roots: List[str] = job_details["roots"]
    checks: List[str] = job_details["checks"]
    should_run_dict = {
        root: {check: False for check in checks} for root in roots
    }
    for _, root, check, should in run(
        collect(
            (
                _should_run(group_name, root, check, API_TOKEN.get())
                for root in roots
                for check in checks
            )
        )
    ):
        should_run_dict[root][check] = should
