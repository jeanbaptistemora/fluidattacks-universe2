import boto3
from dataclasses import (
    dataclass,
)
from tap_dynamo.auth import (
    Creds,
)
from typing import (
    Any,
)


@dataclass(frozen=True)
class _Client:
    _raw_client: Any


@dataclass(frozen=True)
class Client(_Client):
    def __init__(self, obj: _Client) -> None:
        super().__init__(obj._raw_client)


def new_client(creds: Creds) -> Client:
    raw = boto3.resource(
        "dynamodb",
        aws_access_key_id=creds.key_id,
        aws_secret_access_key=creds.key,
        region_name=creds.region,
    )
    return Client(_Client(raw))
