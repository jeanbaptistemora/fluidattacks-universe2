import aioboto3
from aioextensions import (
    collect,
    in_thread,
)
import aiohttp
import asyncio
from batch.enums import (
    JobStatus,
)
from batch.types import (
    BatchProcessing,
    Job,
    JobContainer,
    JobDescription,
)
import boto3
from boto3.dynamodb.conditions import (
    Key,
)
from botocore.exceptions import (
    ClientError,
)
from context import (
    FI_AWS_BATCH_ACCESS_KEY,
    FI_AWS_BATCH_SECRET_KEY,
    FI_AWS_DYNAMODB_ACCESS_KEY,
    FI_AWS_DYNAMODB_SECRET_KEY,
    FI_AWS_SESSION_TOKEN,
    FI_ENVIRONMENT,
    PRODUCT_API_TOKEN,
)
from custom_types import (
    DynamoDelete,
)
from datetime import (
    datetime,
)
from dynamodb import (
    operations_legacy as dynamodb_ops,
)
import hashlib
import hmac
from itertools import (
    chain,
    product,
)
import json
import logging
import logging.config
import math
import more_itertools
from more_itertools import (
    chunked,
)
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
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Set,
    Tuple,
    Union,
)
from urllib.parse import (
    urlparse,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)
TABLE_NAME: str = "fi_async_processing"


def mapping_to_key(items: List[str]) -> str:
    return ".".join(
        [safe_encode(attribute_value) for attribute_value in sorted(items)]
    )


async def list_queues_jobs(
    queues: List[str],
    statuses: List[JobStatus],
    *,
    filters: Tuple[Callable[[Job], bool], ...] = (),
) -> List[Job]:
    if FI_ENVIRONMENT == "development":
        return []
    return list(
        chain.from_iterable(
            await collect(
                [
                    _list_queue_jobs(queue, status, filters=filters)
                    for queue, status in product(queues, statuses)
                ]
            )
        )
    )


def _sign(key: bytes, msg: str) -> bytes:
    return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()


def _get_signature_key(
    key: str, date_stamp: str, region_name: str, service_name: str
) -> bytes:
    k_date = _sign(("AWS4" + key).encode("utf-8"), date_stamp)
    k_region = _sign(k_date, region_name)
    k_service = _sign(k_region, service_name)
    k_signing = _sign(k_service, "aws4_request")
    return k_signing


async def list_jobs_filter(  # pylint: disable=too-many-locals
    queue: str,
    filters: Tuple[str, ...],
    next_token: Optional[str] = None,
) -> Dict[str, Any]:
    service = "batch"
    session = boto3.Session()
    credentials = session.get_credentials()
    client = session.client(service)
    endpoint = f"{client.meta.endpoint_url}/v1/listjobs"
    method = "POST"
    host = urlparse(endpoint).hostname or ""
    region = client.meta.region_name
    content_type = "application/x-amz-json-1.0"
    amz_target = "Batch_20120810.ListJobs"
    request_parameters = {
        "jobQueue": queue,
        "filters": [{"name": "JOB_NAME", "values": list(filters)}],
    }
    if next_token:
        request_parameters["nextToken"] = next_token

    request_parameters_str = json.dumps(request_parameters)
    access_key = credentials.access_key
    secret_key = credentials.secret_key
    time = datetime.utcnow()
    amz_date = time.strftime("%Y%m%dT%H%M%SZ")
    date_stamp = time.strftime("%Y%m%d")

    canonical_uri = "/v1/listjobs"
    canonical_querystring = ""
    canonical_headers = (
        "content-type:"
        + content_type
        + "\n"
        + "host:"
        + host
        + "\n"
        + "x-amz-date:"
        + amz_date
        + "\n"
        + "x-amz-target:"
        + amz_target
        + "\n"
    )
    signed_headers = "content-type;host;x-amz-date;x-amz-target"
    payload_hash = hashlib.sha256(
        request_parameters_str.encode("utf-8")
    ).hexdigest()

    canonical_request = (
        method
        + "\n"
        + canonical_uri
        + "\n"
        + canonical_querystring
        + "\n"
        + canonical_headers
        + "\n"
        + signed_headers
        + "\n"
        + payload_hash
    )
    algorithm = "AWS4-HMAC-SHA256"
    credential_scope = (
        date_stamp + "/" + region + "/" + service + "/" + "aws4_request"
    )
    string_to_sign = (
        algorithm
        + "\n"
        + amz_date
        + "\n"
        + credential_scope
        + "\n"
        + hashlib.sha256(canonical_request.encode("utf-8")).hexdigest()
    )
    signing_key = _get_signature_key(secret_key, date_stamp, region, service)
    signature = hmac.new(
        signing_key, (string_to_sign).encode("utf-8"), hashlib.sha256
    ).hexdigest()
    authorization_header = (
        algorithm
        + " "
        + "Credential="
        + access_key
        + "/"
        + credential_scope
        + ", "
        + "SignedHeaders="
        + signed_headers
        + ", "
        + "Signature="
        + signature
    )
    headers = {
        "Content-Type": content_type,
        "X-Amz-Date": amz_date,
        "X-Amz-Target": amz_target,
        "Authorization": authorization_header,
    }
    retries = 0
    async with aiohttp.ClientSession(headers=headers) as session:
        retry = True
        while retry and retries < 100:
            retry = False
            async with session.post(
                endpoint, data=request_parameters_str
            ) as response:
                try:
                    result = await response.json()
                except json.decoder.JSONDecodeError:
                    break
                if (
                    not response.ok
                    and result.get("message", "") == "Too Many Requests"
                ):
                    retry = True
                    retries += 1
                    await asyncio.sleep(0.1)
                    continue
                return result
    return {}


async def list_jobs_by_group(queue: str, group: str) -> List[Dict[str, Any]]:
    async def _request(
        next_token: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        _response = await list_jobs_filter(
            queue=queue,
            next_token=next_token,
            filters=(f"skims-process-{group}*",),
        )
        for _job in _response["jobSummaryList"]:
            _job["jobQueue"] = queue

        result = _response["jobSummaryList"]

        if _next_token := _response.get("nextToken"):
            result.extend(await _request(next_token=_next_token))
        return result

    return await _request(queue)


async def list_log_streams(
    group: str, *job_ids: str
) -> List[Dict[str, Union[str, int]]]:
    resource_options = dict(
        service_name="logs",
        aws_access_key_id=FI_AWS_BATCH_ACCESS_KEY,
        aws_secret_access_key=FI_AWS_BATCH_SECRET_KEY,
    )

    async with aioboto3.client(**resource_options) as cloudwatch:

        async def _request(
            _job_id: str, next_token: Optional[str] = None
        ) -> List[Dict[str, Any]]:
            _response = await cloudwatch.describe_log_streams(
                logGroupName="skims",
                logStreamNamePrefix=f"{group}/{_job_id}/",
                **({"nextToken": next_token} if next_token else {}),
            )
            result: List[Dict[str, Any]] = _response["logStreams"]

            if _next_token := _response.get("nextToken"):
                result.extend(await _request(_job_id, next_token=_next_token))
            return result

        return list(
            more_itertools.flatten(
                await collect(_request(_job_id) for _job_id in job_ids)
            )
        )


async def describe_jobs(*job_ids: str) -> List[Dict[str, Any]]:
    resource_options = dict(
        service_name="batch",
        aws_access_key_id=FI_AWS_BATCH_ACCESS_KEY,
        aws_secret_access_key=FI_AWS_BATCH_SECRET_KEY,
    )
    result = []
    async with aioboto3.client(**resource_options) as batch:
        for _set_jobs in more_itertools.divide(
            math.ceil(len(job_ids) / 100), job_ids
        ):
            response = await batch.describe_jobs(jobs=list(_set_jobs))
            result.extend(response["jobs"])
    return result


async def _list_queue_jobs(
    queue: str,
    status: JobStatus,
    *,
    filters: Tuple[Callable[[Job], bool], ...],
) -> List[Job]:
    client = boto3.client("batch")
    results: List[Job] = []

    async def _request(next_token: Optional[str] = None) -> Optional[str]:
        response = await in_thread(
            client.list_jobs,
            jobQueue=queue,
            jobStatus=status.name,
            **(dict(nextToken=next_token) if next_token else {}),
        )

        for job_summary in response.get("jobSummaryList", []):
            job = Job(
                created_at=job_summary.get("createdAt"),
                exit_code=job_summary.get("container", {}).get("exitCode"),
                exit_reason=job_summary.get("container", {}).get("reason"),
                id=job_summary["jobId"],
                name=job_summary["jobName"],
                queue=queue,
                started_at=job_summary.get("startedAt"),
                stopped_at=job_summary.get("stoppedAt"),
                status=status.name,
            )
            if all(filter_(job) for filter_ in filters):
                results.append(job)

        return response.get("nextToken")

    next_token = await _request()
    while next_token:
        next_token = await _request(next_token)

    return results


async def decribe_jobs(
    jobs_ids: Set[str],
) -> Tuple[JobDescription, ...]:
    if FI_ENVIRONMENT == "development":
        return tuple()
    resource_options = dict(
        service_name="batch",
        aws_access_key_id=FI_AWS_DYNAMODB_ACCESS_KEY,
        aws_secret_access_key=FI_AWS_DYNAMODB_SECRET_KEY,
        aws_session_token=FI_AWS_SESSION_TOKEN,
    )
    async with aioboto3.client(**resource_options) as batch:
        responses = await collect(
            tuple(
                batch.describe_jobs(jobs=jobs_ids_chunk)
                for jobs_ids_chunk in chunked(jobs_ids, 100)
            ),
        )
        response_jobs = chain.from_iterable(
            tuple(response.get("jobs", []) for response in responses)
        )
        job_descriptions = tuple(
            JobDescription(
                id=job["jobId"],
                name=job["jobName"],
                status=JobStatus[job["status"]],
                container=JobContainer(command=job["container"]["command"]),
            )
            for job in response_jobs
        )

    return job_descriptions


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
        queue=item["queue"],
    )


async def get_actions() -> List[BatchProcessing]:
    items = await dynamodb_ops.scan(table=TABLE_NAME, scan_attrs={})

    return [
        BatchProcessing(
            key=item["pk"],
            action_name=item["action_name"].lower(),
            entity=item["entity"].lower(),
            subject=item["subject"].lower(),
            time=item["time"],
            additional_info=item.get("additional_info", ""),
            queue=item["queue"],
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
    queue: str = "spot_soon",
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
                queue=queue,
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
    queue: str = "spot_soon",
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
                jobQueue=queue,
                jobDefinition="makes",
                containerOverrides={
                    "vcpus": 2,
                    "command": format_command(
                        action_name=action_name,
                        subject=subject,
                        entity=entity,
                        time=time,
                        additional_info=additional_info,
                    ),
                    "environment": [
                        {"name": "CI", "value": "true"},
                        {"name": "MAKES_AWS_BATCH_COMPAT", "value": "true"},
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
        LOGGER.exception(
            exc,
            extra=dict(
                extra=dict(
                    action_name=action_name,
                    subject=subject,
                    entity=entity,
                    time=time,
                    additional_info=additional_info,
                )
            ),
        )
        return False
    else:
        return True


async def put_action(
    *,
    action_name: str,
    entity: str,
    subject: str,
    additional_info: str,
    queue: str = "spot_soon",
) -> bool:
    time: str = str(get_as_epoch(get_now()))
    action = dict(
        action_name=action_name,
        entity=entity,
        subject=subject,
        time=time,
        additional_info=additional_info,
        queue=queue,
    )

    return all(
        await collect(
            (
                put_action_to_batch(**action),
                put_action_to_dynamodb(**action),
            )
        )
    )


def format_command(
    *,
    action_name: str,
    subject: str,
    entity: str,
    time: str,
    additional_info: str,
) -> List[str]:
    return [
        "m",
        "f",
        "/integrates/batch",
        "prod",
        action_name,
        subject,
        entity,
        time,
        additional_info,
    ]
