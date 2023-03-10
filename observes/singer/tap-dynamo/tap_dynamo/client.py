from __future__ import (
    annotations,
)

import boto3
from dataclasses import (
    dataclass,
    field,
)
from fa_purity import (
    Maybe,
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
class _Private:
    pass


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
class TableClient:
    _private: _Private = field(repr=False, hash=False, compare=False)
    _raw_client: DynamoTable

    def _scan_action(self, args: ScanArgs) -> FrozenDict[str, Any]:
        # pylint: disable=assignment-from-no-return
        LOG.info("SCAN: %s", args)
        response = self._raw_client.scan(**args.to_dict())
        # TODO: unsafe cast should be removed
        return FrozenDict(cast(Dict[str, Any], response))

    def scan(self, args: ScanArgs) -> Cmd[FrozenDict[str, Any]]:
        return Cmd.from_cmd(lambda: self._scan_action(args))


@dataclass(frozen=True)
class DynamoConf:
    endpoint_url: str | None
    region_name: str | None
    use_ssl: bool | None
    verify: bool | None


@dataclass(frozen=True)
class Client:
    _private: _Private = field(repr=False, hash=False, compare=False)
    _raw_client: DynamoDBServiceResource

    def table(self, table_name: str) -> TableClient:
        return TableClient(_Private(), self._raw_client.Table(table_name))

    @staticmethod
    def new_client(conf: Maybe[DynamoConf]) -> Cmd[Client]:
        # This impure procedure gets inputs through the
        # environment when settings are `None` or not set
        # e.g. AWS_ACCESS_KEY_ID, AWS_DEFAULT_REGION
        raw = conf.map(
            lambda c: Cmd.from_cmd(
                lambda: boto3.resource(
                    "dynamodb",
                    c.region_name,
                    endpoint_url=c.endpoint_url,
                    use_ssl=c.use_ssl,
                    verify=c.verify,
                )
            )
        ).value_or(Cmd.from_cmd(lambda: boto3.resource("dynamodb")))
        return raw.map(lambda r: Client(_Private(), r))
