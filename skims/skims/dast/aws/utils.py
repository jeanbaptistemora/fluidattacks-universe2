import aioboto3
from model.core_model import (
    AwsCredentials,
)
from typing import (
    Dict,
    Optional,
)


async def run_boto3_fun(
    credentials: AwsCredentials,
    service: str,
    function: str,
    parameters: Optional[Dict[str, str]] = None,
) -> Dict[str, str]:
    session = aioboto3.Session(
        aws_access_key_id=credentials.access_key_id,
        aws_secret_access_key=credentials.secret_access_key,
    )
    async with session.client(
        service,
    ) as client:
        return await (getattr(client, function))(**(parameters or {}))
