import aioboto3
from context import (
    FI_AWS_BATCH_ACCESS_KEY,
    FI_AWS_BATCH_SECRET_KEY,
    PRODUCT_API_TOKEN,
)
from typing import (
    Any,
    Dict,
)


async def clone_roots_in_batch(group: str, *roots: str) -> Dict[str, Any]:
    queue_name = "skims_all_soon"
    job_name = f"integrates-clone-repos-{group}"
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
                    "/melts/clone-repos",
                    group,
                    *roots,
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
