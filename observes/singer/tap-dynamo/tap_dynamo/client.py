import boto3
from dataclasses import (
    dataclass,
)
from fa_purity.cmd import (
    Cmd,
)
from fa_purity.frozen import (
    FrozenDict,
)
import logging
from mypy_boto3_dynamodb.service_resource import (
    DynamoDBServiceResource,
    Table as DynamoTable,
)
from typing import (
    Any,
    cast,
    Dict,
    Optional,
)

LOG = logging.getLogger(__name__)


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
    _raw_client: DynamoTable


@dataclass(frozen=True)
class TableClient(_TableClient):
    def __init__(self, obj: _TableClient) -> None:
        super().__init__(obj._raw_client)

    def _scan_action(self, args: ScanArgs) -> FrozenDict[str, Any]:
        # pylint: disable=assignment-from-no-return
        LOG.info("SCAN: %s", args)
        response = self._raw_client.scan(**args.to_dict())
        # TODO: unsafe cast should be removed
        return FrozenDict(cast(Dict[str, Any], response))

    def scan(self, args: ScanArgs) -> Cmd[FrozenDict[str, Any]]:
        return Cmd.from_cmd(lambda: self._scan_action(args))


@dataclass(frozen=True)
class _Client:
    _raw_client: DynamoDBServiceResource


@dataclass(frozen=True)
class Client(_Client):
    def __init__(self, obj: _Client) -> None:
        super().__init__(obj._raw_client)

    def table(self, table_name: str) -> TableClient:
        _table = _TableClient(self._raw_client.Table(table_name))
        return TableClient(_table)


def new_client() -> Cmd[Client]:
    # This impure procedure gets inputs (credentials) through the environment
    # e.g. AWS_DEFAULT_REGION
    raw = Cmd.from_cmd(lambda: boto3.resource("dynamodb"))
    return raw.map(lambda d: Client(_Client(d)))
