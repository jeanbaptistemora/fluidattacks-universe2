import aioboto3
from dast.aws.types import (
    Location,
)
import json
from json_source_map import (
    calculate,
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
from utils.string import (
    make_snippet,
    SnippetViewport,
)
from vulnerabilities import (
    build_inputs_vuln,
    build_metadata,
)


def _build_where(location: Location) -> str:
    if len(location.access_patterns) == 1:
        return f"{location.access_patterns[0]}: {location.values[0]}"
    return "; ".join(
        [
            f'{path.split("/")[-1]}: {location.values[index_path]}'
            for index_path, path in enumerate(location.access_patterns)
        ]
    )


def build_vulnerabilities(
    locations: List[Location],
    method: MethodsEnum,
    aws_response: Dict[str, Any],
) -> core_model.Vulnerabilities:
    str_content = json.dumps(aws_response, indent=4, default=str)
    json_paths = calculate(str_content)

    return tuple(
        build_inputs_vuln(
            method=method,
            what=location.arn,
            where=_build_where(location) if location.access_patterns else "0",
            stream="skims",
            metadata=build_metadata(
                method=method,
                description=location.description,
                snippet=make_snippet(
                    content=str_content,
                    viewport=SnippetViewport(
                        column=json_paths[
                            location.access_patterns[-1]
                        ].key_start.column
                        if location.access_patterns
                        else 0,
                        line=json_paths[
                            location.access_patterns[-1]
                        ].key_start.line
                        + 1
                        if location.access_patterns
                        else 0,
                        wrap=True,
                    ),
                ),
            ),
        )
        for location in locations
    )


async def run_boto3_fun(
    credentials: AwsCredentials,
    service: str,
    function: str,
    parameters: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    session = aioboto3.Session(
        aws_access_key_id=credentials.access_key_id,
        aws_secret_access_key=credentials.secret_access_key,
    )
    async with session.client(
        service,
    ) as client:
        return await (getattr(client, function))(**(parameters or {}))
