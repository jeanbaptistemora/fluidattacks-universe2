import aioboto3
from aioextensions import (
    collect,
    in_thread,
)
import aiohttp
import asyncio
from batch.enums import (
    Action,
    JobStatus,
    Product,
)
from batch.types import (
    AttributesNoOverridden,
    BatchProcessing,
    Job,
    PutActionResult,
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
from more_itertools.recipes import (
    flatten,
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
    Tuple,
    Union,
)
from urllib.parse import (
    urlparse,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger("console")
OPTIONS = dict(
    service_name="batch",
    aws_access_key_id=FI_AWS_BATCH_ACCESS_KEY,
    aws_secret_access_key=FI_AWS_BATCH_SECRET_KEY,
    aws_session_token=FI_AWS_SESSION_TOKEN,
)
TABLE_NAME: str = "fi_async_processing"


def mapping_to_key(items: List[str]) -> str:
    key = ".".join(
        [safe_encode(attribute_value) for attribute_value in sorted(items)]
    )
    return hashlib.sha256(key.encode()).hexdigest()


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


async def list_jobs(  # pylint: disable=too-many-locals
    queue: str,
    next_token: Optional[str] = None,
    **kwargs: Any,
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
        **kwargs,
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


async def _get_all_jobs(**kwargs: Any) -> List[Dict[str, Any]]:
    _response = await list_jobs(**kwargs)
    for _job in _response["jobSummaryList"]:
        _job["jobQueue"] = kwargs.get("queue")

    result = _response["jobSummaryList"]

    if _next_token := _response.get("nextToken"):
        kwargs["nextToken"] = _next_token
        result.extend(await _get_all_jobs(**kwargs))
    return result


async def list_jobs_by_group(queue: str, group: str) -> List[Dict[str, Any]]:
    return await _get_all_jobs(
        queue=queue,
        filters=[
            {"name": "JOB_NAME", "values": [f"skims-execute-machine-{group}*"]}
        ],
    )


async def list_jobs_by_status(queue: str, status: str) -> List[Dict[str, Any]]:
    return await _get_all_jobs(queue=queue, jobStatus=status)


async def list_log_streams(
    group: str, *job_ids: str
) -> List[Dict[str, Union[str, int]]]:
    options = OPTIONS.copy()
    options.update({"service_name": "logs"})

    async with aioboto3.Session().client(**options) as cloudwatch:

        async def _request(
            _job_id: Optional[str] = None, next_token: Optional[str] = None
        ) -> List[Dict[str, Any]]:
            _response = await cloudwatch.describe_log_streams(
                logGroupName="skims",
                logStreamNamePrefix=f"{group}/{_job_id}/"
                if _job_id
                else f"{group}/",
                **({"nextToken": next_token} if next_token else {}),
            )
            result: List[Dict[str, Any]] = _response["logStreams"]

            if _next_token := _response.get("nextToken"):
                result.extend(await _request(_job_id, next_token=_next_token))
            return result

        if job_ids:
            return list(
                more_itertools.flatten(
                    await collect(_request(_job_id) for _job_id in job_ids)
                )
            )
        return await _request()


async def describe_jobs(*job_ids: str) -> Tuple[Dict[str, Any], ...]:
    if not job_ids:
        return ()

    async with aioboto3.Session().client(**OPTIONS) as batch:
        return tuple(
            flatten(
                response["jobs"]
                for response in await collect(
                    tuple(
                        batch.describe_jobs(jobs=list(_set_jobs))
                        for _set_jobs in more_itertools.divide(
                            math.ceil(len(job_ids) / 100), job_ids
                        )
                    )
                )
            )
        )


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


async def delete_action(
    *,
    action_name: Optional[str] = None,
    additional_info: Optional[str] = None,
    entity: Optional[str] = None,
    subject: Optional[str] = None,
    time: Optional[str] = None,
    dynamodb_pk: Optional[str] = None,
) -> bool:
    try:
        if not dynamodb_pk and any(
            [
                not action_name,
                not additional_info,
                not entity,
                not subject,
                not time,
            ]
        ):
            raise Exception(
                (
                    "you must supply the dynamodb pk argument"
                    " or any other arguments to build pk"
                )
            )
        key = dynamodb_pk or generate_key_to_dynamod(
            action_name=action_name,  # type: ignore
            additional_info=additional_info,  # type: ignore
            entity=entity,  # type: ignore
            subject=subject,  # type: ignore
        )
        return await dynamodb_ops.delete_item(
            delete_attrs=DynamoDelete(Key=dict(pk=key)), table=TABLE_NAME
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
    action_dynamo_pk: str,
) -> Optional[BatchProcessing]:
    query_attrs = dict(KeyConditionExpression=Key("pk").eq(action_dynamo_pk))
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
        batch_job_id=item.get("batch_job_id"),
        running=item.get("running", False),
    )


async def get_actions_by_name(
    action_name: str, entity: str
) -> Tuple[BatchProcessing, ...]:
    query_attrs = {
        "IndexName": "gsi-1",
        "KeyConditionExpression": (
            Key("action_name").eq(action_name) & Key("entity").eq(entity)
        ),
    }
    response_items = await dynamodb_ops.query(TABLE_NAME, query_attrs)

    return tuple(
        BatchProcessing(
            key=item["pk"],
            action_name=item["action_name"].lower(),
            entity=item["entity"].lower(),
            subject=item["subject"].lower(),
            time=item["time"],
            additional_info=item.get("additional_info", ""),
            queue=item["queue"],
            batch_job_id=item.get("batch_job_id"),
            running=item.get("running", False),
        )
        for item in response_items
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
            batch_job_id=item.get("batch_job_id"),
            running=item.get("running", False),
        )
        for item in items
    ]


def generate_key_to_dynamod(
    *,
    action_name: str,
    additional_info: str,
    entity: str,
    subject: str,
) -> str:
    return mapping_to_key(
        [
            action_name,
            additional_info,
            entity,
            subject,
        ]
    )


async def put_action_to_dynamodb(
    *,
    action_name: str,
    entity: str,
    subject: str,
    time: str,
    additional_info: str,
    batch_job_id: Optional[str] = None,
    queue: str = "spot_soon",
    key: Optional[str] = None,
) -> Optional[str]:
    try:
        key = key or generate_key_to_dynamod(
            action_name=action_name,
            additional_info=additional_info,
            entity=entity,
            subject=subject,
        )
        success = await dynamodb_ops.put_item(
            item=dict(
                pk=key,
                action_name=action_name,
                additional_info=additional_info,
                entity=entity,
                subject=subject,
                time=time,
                queue=queue,
                batch_job_id=batch_job_id,
            ),
            table=TABLE_NAME,
        )
        if success:
            return key
    except ClientError as exc:
        LOGGER.exception(exc, extra=dict(extra=locals()))

    return None


async def update_action_to_dynamodb(*, key: str, **kwargs: Any) -> bool:
    no_update_attributes = {
        "action_name",
        "entity",
        "subject",
        "time",
        "queue",
    }
    has_bad = no_update_attributes.intersection(set(kwargs.keys()))
    if has_bad:
        raise AttributesNoOverridden(*has_bad)

    success = False
    remove_expression = ""
    set_expression = ""
    expression_names = {}
    expression_values = {}

    for attr, value in kwargs.items():
        if value is None:
            remove_expression += f"#{attr}, "
            expression_names.update({f"#{attr}": attr})
        else:
            set_expression += f"#{attr} = :{attr}, "
            expression_names.update({f"#{attr}": attr})
            expression_values.update({f":{attr}": value})

    if set_expression:
        set_expression = f'SET {set_expression.strip(", ")}'
    if remove_expression:
        remove_expression = f'REMOVE {remove_expression.strip(", ")}'
    update_attrs = {
        "Key": {"pk": key},
        "UpdateExpression": f"{set_expression} {remove_expression}".strip(),
    }

    if expression_values:
        update_attrs.update({"ExpressionAttributeValues": expression_values})
    if expression_names:
        update_attrs.update({"ExpressionAttributeNames": expression_names})
    try:
        success = await dynamodb_ops.update_item(TABLE_NAME, update_attrs)
    except ClientError as ex:
        LOGGER.exception(ex, extra={"extra": locals()})
    return success


async def put_action_to_batch(
    *,
    action_name: str,
    action_dynamo_pk: str,
    entity: str,
    product_name: str,
    attempt_duration_seconds: int = 3600,
    memory: int = 7200,
    queue: str = "spot_soon",
    vcpus: int = 2,
    **kwargs: Any,
) -> Optional[str]:
    if FI_ENVIRONMENT == "development":
        return None
    try:
        async with aioboto3.Session().client(**OPTIONS) as batch:
            return (
                await batch.submit_job(
                    jobName=f"{product_name}-{action_name}-{entity}",
                    jobQueue=queue,
                    jobDefinition="makes",
                    containerOverrides={
                        "vcpus": vcpus,
                        "command": [
                            "m",
                            "f",
                            f"/{product_name}/batch",
                            "prod",
                            action_dynamo_pk,
                        ],
                        "environment": [
                            {"name": "CI", "value": "true"},
                            {
                                "name": "MAKES_AWS_BATCH_COMPAT",
                                "value": "true",
                            },
                            {
                                "name": "PRODUCT_API_TOKEN",
                                "value": PRODUCT_API_TOKEN,
                            },
                        ],
                        "memory": memory,
                    },
                    retryStrategy={
                        "attempts": 1,
                    },
                    timeout={
                        "attemptDurationSeconds": attempt_duration_seconds
                    },
                    **kwargs,
                )
            )["jobId"]
    except ClientError as exc:
        LOGGER.exception(
            exc,
            extra=dict(
                extra=dict(
                    action_name=action_name,
                    action_dynamo_pk=action_dynamo_pk,
                )
            ),
        )
        return None


async def put_action(  # pylint: disable=too-many-locals
    *,
    action: Action,
    additional_info: str,
    entity: str,
    product_name: Product,
    subject: str,
    attempt_duration_seconds: int = 3600,
    dynamodb_pk: Optional[str] = None,
    queue: str = "spot_soon",
    vcpus: int = 2,
    **kwargs: Any,
) -> PutActionResult:
    time: str = str(get_as_epoch(get_now()))
    action_dict = dict(
        action_name=action.value,
        entity=entity,
        subject=subject,
        time=time,
        additional_info=additional_info,
        queue=queue,
    )
    if (
        (dynamodb_pk is not None)
        and (current_action := await get_action(action_dynamo_pk=dynamodb_pk))
        and (not current_action.running)
    ):
        LOGGER.info(
            "There is a job that is still in queue, it will be updated",
            extra={"extra": None},
        )
        success = await update_action_to_dynamodb(
            key=dynamodb_pk,
            additional_info=additional_info,
            batch_job_id=current_action.batch_job_id,
        )
        return PutActionResult(
            success=success,
            batch_job_id=current_action.batch_job_id,
            dynamo_pk=dynamodb_pk,
        )

    possible_key = dynamodb_pk or generate_key_to_dynamod(
        action_name=action.value,
        additional_info=additional_info,
        entity=entity,
        subject=subject,
    )
    if (
        current_action := await get_action(action_dynamo_pk=possible_key)
    ) and (not current_action.running):
        return PutActionResult(
            success=True,
            batch_job_id=current_action.batch_job_id,
            dynamo_pk=dynamodb_pk,
        )

    job_id = await put_action_to_batch(
        action_name=action.value,
        vcpus=vcpus,
        queue=queue,
        entity=entity,
        attempt_duration_seconds=attempt_duration_seconds,
        action_dynamo_pk=possible_key,
        product_name=product_name.value,
        **kwargs,
    )
    dynamo_pk = await put_action_to_dynamodb(
        key=possible_key, **action_dict, batch_job_id=job_id
    )
    return PutActionResult(
        success=True,
        batch_job_id=job_id,
        dynamo_pk=dynamo_pk,
    )
