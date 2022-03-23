from .config import (
    generate_config,
)
from aioextensions import (
    collect,
    run,
)
from batch.repositories import (
    delete_out_of_scope_files,
    get_namespace,
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
    get_group_roots,
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
from utils.logs import (
    log_blocking,
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
    if not response_items or not response_items["Items"]:
        return None

    item = response_items["Items"][0]
    return BatchProcessing(
        key=item["pk"]["S"],
        action_name=item["action_name"]["S"].lower(),
        entity=item["entity"]["S"].lower(),
        subject=item["subject"]["S"].lower(),
        time=item["time"]["S"],
        additional_info=item.get("additional_info", {}).get("S"),
        queue=item["queue"]["S"],
    )


def delete_action(
    *,
    action_dynamo_pk: str,
) -> None:
    client = boto3.client("dynamodb", "us-east-1")
    operation_payload = {
        "TableName": "fi_async_processing",
        "Key": {"pk": {"S": action_dynamo_pk}},
    }
    client.delete_item(**operation_payload)


def set_running(
    *,
    action_dynamo_pk: str,
) -> None:
    client = boto3.client("dynamodb", "us-east-1")
    operation_payload = {
        "TableName": "fi_async_processing",
        "Key": {"pk": {"S": action_dynamo_pk}},
        "UpdateExpression": "SET #25fb0 = :25fb0",
        "ExpressionAttributeNames": {"#25fb0": "running"},
        "ExpressionAttributeValues": {":25fb0": {"BOOL": True}},
    }
    client.update_item(**operation_payload)


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
    *,
    group_name: str,
    roots: List[str],
    checks: List[str],
    token: str,
    group_language: str,
) -> Tuple[SkimsConfig, ...]:
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


async def _get_namespace(
    group_name: str, root_nickname: str, signed_url: Optional[str] = None
) -> Tuple[str, Optional[str]]:
    return (
        root_nickname,
        await get_namespace(
            group_name, root_nickname, presigned_ulr=signed_url, delete=False
        ),
    )


async def main(action_dynamo_pk: Optional[str] = None) -> None:
    action_dynamo_pk = action_dynamo_pk or sys.argv[1]
    CTX.debug = False
    token = os.environ["INTEGRATES_API_TOKEN"]
    create_session(token)
    item = get_action(
        action_dynamo_pk=action_dynamo_pk,
    )

    if not item:
        raise Exception(f"No jobs were found for the key {action_dynamo_pk}")

    if item.action_name != "execute-machine":
        raise Exception("Invalid action name", item.action_name)

    set_running(action_dynamo_pk=action_dynamo_pk)
    group_name = item.entity

    job_details = json.loads(item.additional_info)
    roots_nicknames: List[str] = job_details["roots"]
    checks: List[str] = job_details["checks"]

    roots_dict = {
        item.nickname: item for item in await get_group_roots(group=group_name)
    }

    namespaces_path_dict = dict(
        await collect(
            [
                _get_namespace(
                    group_name,
                    root_nickname,
                    roots_dict[root_nickname].download_url
                    if root_nickname in roots_dict
                    else None,
                )
                for root_nickname in roots_nicknames
            ]
        )
    )
    await delete_out_of_scope_files(group_name, *roots_nicknames)
    group_language = await get_group_language(group_name)
    configs = await collect(
        generate_config(
            group_name=group_name,
            namespace=root_nickname,
            checks=tuple(checks),
            language=group_language,
            working_dir=namespaces_path_dict[root_nickname],
        )
        for root_nickname in roots_nicknames
        if namespaces_path_dict.get(root_nickname) is not None
    )

    for config in configs:
        with suppress(Exception):
            log_blocking("info", "Running skims for %s", config.namespace)
            await execute_skims(config, group_name, token)

    delete_action(action_dynamo_pk=action_dynamo_pk)


if __name__ == "__main__":
    run(main())
