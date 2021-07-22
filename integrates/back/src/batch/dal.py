import aioboto3
from aioextensions import (
    collect,
    in_thread,
)
from batch.types import (
    BatchProcessing,
)
import boto3
from boto3.dynamodb.conditions import (
    Key,
)
from botocore.exceptions import (
    ClientError,
)
from context import (
    CI_COMMIT_REF_NAME,
    FI_AWS_DYNAMODB_ACCESS_KEY,
    FI_AWS_DYNAMODB_SECRET_KEY,
    FI_AWS_SESSION_TOKEN,
    FI_ENVIRONMENT,
    PRODUCT_API_TOKEN,
)
from custom_types import (
    DynamoDelete,
)
from dynamodb import (
    operations_legacy as dynamodb_ops,
)
from enum import (
    Enum,
)
from itertools import (
    chain,
    product,
)
import logging
import logging.config
from newutils.datetime import (
    get_as_epoch,
    get_now,
)
from newutils.encodings import (
    safe_encode,
)
from settings import (
    LOGGING,
)
from typing import (
    List,
    NamedTuple,
    Optional,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)
TABLE_NAME: str = "fi_async_processing"


def mapping_to_key(items: List[str]) -> str:
    return ".".join(
        [safe_encode(attribute_value) for attribute_value in sorted(items)]
    )


class JobStatus(Enum):
    SUBMITTED: str = "SUBMITTED"
    PENDING: str = "PENDING"
    RUNNABLE: str = "RUNNABLE"
    STARTING: str = "STARTING"
    RUNNING: str = "RUNNING"
    SUCCEEDED: str = "SUCCEEDED"
    FAILED: str = "FAILED"


class Job(NamedTuple):
    exit_code: int
    exit_reason: str
    id: str
    name: str
    queue: str
    started_at: int
    stopped_at: int
    status: str


async def list_queues_jobs(
    queues: List[str],
    statuses: List[JobStatus],
) -> List[Job]:
    return list(
        chain.from_iterable(
            await collect(
                [
                    list_queue_jobs(queue, status)
                    for queue, status in product(queues, statuses)
                ]
            )
        )
    )


async def list_queue_jobs(queue: str, status: JobStatus) -> List[Job]:
    client = boto3.client("batch")
    results: List[Job] = []

    async def _request(next_token: Optional[str] = None) -> Optional[str]:
        response = await in_thread(
            client.list_jobs,
            jobQueue=queue,
            jobStatus=status.name,
            **(dict(nextToken=next_token) if next_token else dict()),
        )
        results.extend(
            Job(
                id=job_summary["jobId"],
                exit_code=job_summary["container"]["exitCode"],
                exit_reason=job_summary["container"].get("reason", ""),
                name=job_summary["jobName"],
                queue=queue,
                started_at=job_summary["startedAt"],
                stopped_at=job_summary["stoppedAt"],
                status=status.name,
            )
            for job_summary in response.get("jobSummaryList", [])
        )
        return response.get("nextToken")

    next_token = await _request()
    while next_token:
        next_token = await _request(next_token)

    return results


async def delete_action(
    *,
    action_name: str,
    additional_info: str,
    entity: str,
    subject: str,
    time: str,
) -> bool:
    try:
        return await dynamodb_ops.delete_item(
            delete_attrs=DynamoDelete(
                Key=dict(
                    pk=mapping_to_key(
                        [action_name, additional_info, entity, subject, time]
                    ),
                )
            ),
            table=TABLE_NAME,
        )
    except ClientError as exc:
        LOGGER.exception(exc, extra=dict(extra=locals()))
    return False


async def is_action_by_key(*, key: str) -> bool:
    query_attrs = dict(KeyConditionExpression=Key("pk").eq(key))
    response_items = await dynamodb_ops.query(TABLE_NAME, query_attrs)

    if not response_items:
        return False

    return bool(response_items[0])


async def get_action(
    *,
    action_name: str,
    additional_info: str,
    entity: str,
    subject: str,
    time: str,
) -> Optional[BatchProcessing]:
    key: str = mapping_to_key(
        [action_name, additional_info, entity, subject, time]
    )
    query_attrs = dict(KeyConditionExpression=Key("pk").eq(key))
    response_items = await dynamodb_ops.query(TABLE_NAME, query_attrs)

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
    )


async def get_actions() -> List[BatchProcessing]:
    items = await dynamodb_ops.scan(table=TABLE_NAME, scan_attrs=dict())

    return [
        BatchProcessing(
            key=item["pk"],
            action_name=item["action_name"].lower(),
            entity=item["entity"].lower(),
            subject=item["subject"].lower(),
            time=item["time"],
            additional_info=item.get("additional_info", ""),
        )
        for item in items
    ]


async def put_action_to_dynamodb(
    *,
    action_name: str,
    entity: str,
    subject: str,
    time: str,
    additional_info: str,
) -> bool:
    try:
        return await dynamodb_ops.put_item(
            item=dict(
                pk=mapping_to_key(
                    [action_name, additional_info, entity, subject, time]
                ),
                action_name=action_name,
                additional_info=additional_info,
                entity=entity,
                subject=subject,
                time=time,
            ),
            table=TABLE_NAME,
        )
    except ClientError as exc:
        LOGGER.exception(exc, extra=dict(extra=locals()))
    return False


async def put_action_to_batch(
    *,
    action_name: str,
    entity: str,
    subject: str,
    time: str,
    additional_info: str,
) -> bool:
    if FI_ENVIRONMENT == "development":
        return True
    try:
        resource_options = dict(
            service_name="batch",
            aws_access_key_id=FI_AWS_DYNAMODB_ACCESS_KEY,
            aws_secret_access_key=FI_AWS_DYNAMODB_SECRET_KEY,
            aws_session_token=FI_AWS_SESSION_TOKEN,
        )
        async with aioboto3.client(**resource_options) as batch:
            await batch.submit_job(
                jobName=f"integrates-{action_name}",
                jobQueue="spot_soon",
                jobDefinition="default",
                containerOverrides={
                    "vcpus": 2,
                    "command": [
                        "./m",
                        "integrates.batch",
                        "prod",
                        action_name,
                        subject,
                        entity,
                        time,
                        additional_info,
                    ],
                    "environment": [
                        {"name": "CI", "value": "true"},
                        {
                            "name": "CI_COMMIT_REF_NAME",
                            "value": CI_COMMIT_REF_NAME,
                        },
                        {
                            "name": "PRODUCT_API_TOKEN",
                            "value": PRODUCT_API_TOKEN,
                        },
                    ],
                    "memory": 7200,
                },
                retryStrategy={
                    "attempts": 1,
                },
                timeout={"attemptDurationSeconds": 3600},
            )
    except ClientError as exc:
        LOGGER.exception(exc, extra=dict(extra=locals()))
        return False
    else:
        return True


async def put_action(
    *,
    action_name: str,
    entity: str,
    subject: str,
    additional_info: str,
) -> bool:
    time: str = str(get_as_epoch(get_now()))
    action = dict(
        action_name=action_name,
        entity=entity,
        subject=subject,
        time=time,
        additional_info=additional_info,
    )

    return all(
        await collect(
            (put_action_to_batch(**action), put_action_to_dynamodb(**action))
        )
    )
