from aioextensions import (
    collect,
    run,
)
from batch.get_config import (
    generate_config,
)
import boto3
from contextlib import (
    suppress,
)
from core.expected_code_date import (
    main as get_expected_code_date,
)
from core.scan import (
    main as execute_skims,
)
from ctx import (
    CTX,
)
from dateutil.parser import (  # type: ignore
    parse as date_parser,
)
from integrates.dal import (
    get_group_language,
)
from integrates.graphql import (
    create_session,
)
import json
from model.core_model import (
    SkimsConfig,
)
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
        f"groups/{group}/fusion/{namespace}/.git/fluidattacks_metadata"
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


async def _gererate_configs(
    *, group_name: str, roots: List[str], checks: List[str], token: str
) -> Tuple[SkimsConfig, ...]:
    group_language = await get_group_language(group_name)
    should_run_dict = {
        root: {check: False for check in checks} for root in roots
    }

    for _, root, check, should in await collect(
        _should_run(group_name, root, check, token)
        for root in roots
        for check in checks
    ):
        should_run_dict[root][check] = should

    return tuple(
        await collect(
            generate_config(
                group_name=group_name,
                namespace=root,
                checks=tuple(
                    check for check, should in checks_dict.items() if should
                ),
                language=group_language,
                working_dir=f"groups/{group_name}/fusion/{root}",
            )
            for root, checks_dict in should_run_dict.items()
        )
    )


def main() -> None:
    action_dynamo_pk = sys.argv[1]
    CTX.debug = False
    token = os.environ["INTEGRATES_API_TOKEN"]
    create_session(token)
    item = get_action(
        action_dynamo_pk=action_dynamo_pk,
    )

    if not item:
        raise Exception(f"No jobs were found for the key {action_dynamo_pk}")

    group_name = item.entity
    job_details = json.loads(item.additional_info)
    roots: List[str] = job_details["roots"]
    checks: List[str] = job_details["checks"]
    configs = run(
        _gererate_configs(
            group_name=group_name, roots=roots, checks=checks, token=token
        )
    )
    for config in configs:
        with suppress(Exception):
            execute_skims(config, group_name, token)


if __name__ == "__main__":
    main()
