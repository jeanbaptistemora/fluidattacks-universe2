import aioboto3
from dast.aws.types import (
    Location,
)
from model import (
    core_model,
)
from model.core_model import (
    AwsCredentials,
    MethodsEnum,
)
from typing import (
    Any,
    Dict,
    List,
    Optional,
)
from vulnerabilities import (
    build_inputs_vuln,
    build_metadata,
)


def build_vulnerabilities(
    locations: List[Location],
    method: MethodsEnum,
) -> core_model.Vulnerabilities:
    return tuple(
        build_inputs_vuln(
            method=method,
            what=location.arn,
            where=location.access_pattern,
            stream="skims",
            metadata=build_metadata(
                method=method,
                description=location.description,
                snippet="",
            ),
        )
        for location in locations
    )


async def run_boto3_fun(
    credentials: AwsCredentials,
    service: str,
    function: str,
    parameters: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    session = aioboto3.Session(
        aws_access_key_id=credentials.access_key_id,
        aws_secret_access_key=credentials.secret_access_key,
    )
    async with session.client(
        service,
    ) as client:
        return await (getattr(client, function))(**(parameters or {}))
