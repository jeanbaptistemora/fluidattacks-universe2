import aioboto3
import aiohttp
import asyncio
from back.src.context import (
    FI_AWS_BATCH_ACCESS_KEY,
    FI_AWS_BATCH_SECRET_KEY,
    PRODUCT_API_TOKEN,
)
from back.src.schedulers.common import (
    error,
)
from batch.dal import (
    Job,
    JobStatus,
    list_queues_jobs,
)
import boto3
import datetime
import hashlib
import hmac
import json
import os
from typing import (
    Any,
    Dict,
    List,
    NamedTuple,
)
from urllib.parse import (
    urlparse,
)


def _json_load(path: str) -> Any:
    with open(path, encoding="utf-8") as file:
        return json.load(file)


QUEUES: Dict[str, Dict[str, str]] = _json_load(os.environ["MACHINE_QUEUES"])
FINDINGS: Dict[str, Dict[str, Dict[str, str]]] = _json_load(
    os.environ["SKIMS_FINDINGS"]
)


class JobArguments(NamedTuple):
    group_name: str
    finding_code: str
    root_nickname: str


def parse_name(name: str) -> JobArguments:
    tokens = name.split("-", maxsplit=3)
    return JobArguments(
        finding_code=tokens[2],
        group_name=tokens[1],
        root_nickname=tokens[3],
    )


def _get_priority_suffix(urgent: bool) -> str:
    return "soon" if urgent else "later"


def get_queue_for_finding(finding_code: str, urgent: bool = False) -> str:
    for queue_ in QUEUES:
        if finding_code in QUEUES[queue_]["findings"]:
            return f"{queue_}_{_get_priority_suffix(urgent)}"

    raise NotImplementedError(f"{finding_code} does not belong to a queue")


async def list_(
    *,
    finding_code: str,
    group_name: str,
    include_non_urgent: bool = False,
    include_urgent: bool = False,
    statuses: List[JobStatus],
) -> List[Job]:
    queues: List[str] = []
    if include_non_urgent:
        queues.append(get_queue_for_finding(finding_code, urgent=False))
    if include_urgent:
        queues.append(get_queue_for_finding(finding_code, urgent=True))

    jobs = await list_queues_jobs(
        filters=(
            lambda job: parse_name(job.name).finding_code == finding_code,
            lambda job: parse_name(job.name).group_name == group_name,
        ),
        queues=queues,
        statuses=statuses,
    )

    return sorted(
        jobs,
        key=lambda job: job.created_at or 0,
        reverse=True,
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


async def get_job(  # pylint: disable=too-many-locals
    group: str,
    check: str,
    namespace: str,
) -> Dict[str, Any]:
    service = "batch"
    session = boto3.Session()
    credentials = session.get_credentials()
    client = session.client(service)

    queue_name = get_queue_for_finding(check, False)
    jobs = [f"process-{group}-{check}-{namespace}"]
    endpoint = f"{client.meta.endpoint_url}/v1/listjobs"
    method = "POST"
    host = urlparse(endpoint).hostname or ""
    region = client.meta.region_name
    content_type = "application/x-amz-json-1.0"
    amz_target = "Batch_20120810.ListJobs"
    request_parameters = {
        "jobQueue": queue_name,
        "filters": [{"name": "JOB_NAME", "values": list(jobs)}],
    }

    request_parameters_str = json.dumps(request_parameters)
    access_key = credentials.access_key
    secret_key = credentials.secret_key
    time = datetime.datetime.utcnow()
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
                except json.decoder.JSONDecodeError as exc:
                    error(exc)
                    error(response.text())
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


async def queue_boto3(
    group: str,
    finding_code: str,
    namespace: str,
    urgent: bool,
) -> Dict[str, Any]:
    try:
        queue_name = get_queue_for_finding(finding_code, urgent=urgent)
    except NotImplementedError:
        print(f"[ERROR] {finding_code} does not belong to a queue")
        return {}
    job_name = f"process-{group}-{finding_code}-{namespace}"
    resource_options = dict(
        service_name="batch",
        aws_access_key_id=FI_AWS_BATCH_ACCESS_KEY,
        aws_secret_access_key=FI_AWS_BATCH_SECRET_KEY,
    )
    async with aioboto3.client(**resource_options) as batch:
        return await batch.submit_job(
            jobName=job_name,
            jobQueue=queue_name,
            jobDefinition="makes",
            containerOverrides={
                "vcpus": 1,
                "command": [
                    "m",
                    "f",
                    "/skims/process-group",
                    group,
                    finding_code,
                    namespace,
                ],
                "environment": [
                    {"name": "CI", "value": "true"},
                    {"name": "MAKES_AWS_BATCH_COMPAT", "value": "true"},
                    {
                        "name": "PRODUCT_API_TOKEN",
                        "value": PRODUCT_API_TOKEN,
                    },
                ],
                "memory": 1 * 1800,
            },
            retryStrategy={
                "attempts": 1,
            },
            timeout={"attemptDurationSeconds": 86400},
        )
