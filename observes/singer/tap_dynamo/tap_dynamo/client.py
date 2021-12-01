import boto3
from dataclasses import (
    dataclass,
)
from purity.v1 import (
    FrozenDict,
)
from tap_dynamo.auth import (
    Creds,
)
from typing import (
    Any,
    Dict,
    Optional,
)


@dataclass(frozen=True)
class ScanArgs:
    limit: int
    consistent_read: bool
    segment: int
    total_segments: int
    start_key: Optional[FrozenDict[str, str]]

    def to_dict(self) -> FrozenDict[str, Any]:
        data: Dict[str, Any] = {
            "Limit": self.limit,
            "ConsistentRead": self.consistent_read,
            "Segment": self.segment,
            "TotalSegments": self.total_segments,
        }
        if self.start_key:
            data["ExclusiveStartKey"] = dict(self.start_key)
        return FrozenDict(data)


@dataclass(frozen=True)
class _TableClient:
    _raw_client: Any


@dataclass(frozen=True)
class TableClient(_TableClient):
    def __init__(self, obj: _TableClient) -> None:
        super().__init__(obj._raw_client)

    def scan(self, args: ScanArgs) -> FrozenDict[str, Any]:
        response = self._raw_client.scan(**args.to_dict())
        return FrozenDict(response)


@dataclass(frozen=True)
class _Client:
    _raw_client: Any


@dataclass(frozen=True)
class Client(_Client):
    def __init__(self, obj: _Client) -> None:
        super().__init__(obj._raw_client)

    def table(self, table_name: str) -> TableClient:
        _table = self._raw_client.Table(table_name)
        return TableClient(_TableClient(_table))


def new_client(creds: Creds) -> Client:
    raw = boto3.resource(
        "dynamodb",
        aws_access_key_id=creds.key_id,
        aws_secret_access_key=creds.key,
        region_name=creds.region,
    )
    return Client(_Client(raw))
