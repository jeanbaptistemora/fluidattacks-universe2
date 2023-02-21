from ._core import (
    GroupId,
)
from asm_dal.organization import (
    OrganizationId,
)
from boto3.dynamodb.conditions import (
    Attr,
    Key,
)
from collections.abc import (
    Mapping,
    Sequence,
)
from dataclasses import (
    dataclass,
)
from decimal import (
    Decimal,
)
from fa_purity import (
    Cmd,
    FrozenList,
    Stream,
)
from fa_purity.json.primitive.factory import (
    to_primitive,
)
from fa_purity.pure_iter.factory import (
    from_flist,
    infinite_gen,
)
from fa_purity.stream.factory import (
    from_piter,
)
from fa_purity.stream.transform import (
    chain,
    until_none,
)
from fa_purity.union import (
    UnionFactory,
)
from fa_purity.utils import (
    raise_exception,
)
import logging
from mypy_boto3_dynamodb import (
    DynamoDBServiceResource,
)
from mypy_boto3_dynamodb.service_resource import (
    Table,
)
from mypy_boto3_dynamodb.type_defs import (
    QueryOutputTableTypeDef,
)
from typing import (
    Any,
)

LOG = logging.getLogger(__name__)
_ORGS_TABLE = "integrates_vms"
_LastObjKey = Mapping[  # type: ignore[misc]
    str,
    (
        bytes
        | bytearray
        | str
        | int
        | Decimal
        | bool
        | set[int]
        | set[Decimal]
        | set[str]
        | set[bytes]
        | set[bytearray]
        | Sequence[Any]
        | Mapping[str, Any]
        | None
    ),
]


@dataclass(frozen=True)
class _Page:
    response: QueryOutputTableTypeDef
    last_index: _LastObjKey | None


def _to_group(pag: _Page) -> FrozenList[GroupId]:
    return tuple(
        GroupId.new(to_primitive(i["pk"], str).unwrap().split("#")[1])
        .alt(raise_exception)
        .unwrap()
        for i in pag.response["Items"]
    )


@dataclass(frozen=True)
class _GroupsClient:
    _table: Table


class GroupsClient(_GroupsClient):
    def __init__(self, resource: DynamoDBServiceResource) -> None:
        super().__init__(resource.Table(_ORGS_TABLE))

    def _get_groups_page(
        self, org: OrganizationId, last_index: _LastObjKey | None
    ) -> Cmd[_Page]:
        def _action() -> _Page:
            LOG.debug("Getting groups of %s", org)
            condition = Key("sk").eq(f"ORG#{org.uuid}") & Key(
                "pk"
            ).begins_with("GROUP#")
            filter_exp = Attr("deletion_date").not_exists()
            response_items = (
                self._table.query(
                    KeyConditionExpression=condition,
                    FilterExpression=filter_exp,
                    ExclusiveStartKey=last_index,
                    IndexName="inverted_index",
                )
                if last_index
                else self._table.query(
                    KeyConditionExpression=condition,
                    FilterExpression=filter_exp,
                    IndexName="inverted_index",
                )
            )
            LOG.debug("Groups of %s retrieved!", org)
            page = _Page(
                response_items,
                response_items.get("LastEvaluatedKey"),
            )
            LOG.debug(page)
            return page

        return Cmd.from_cmd(_action)

    def get_groups(self, org: OrganizationId) -> Stream[GroupId]:
        init = self._get_groups_page(org, None)
        _union: UnionFactory[_Page, None] = UnionFactory()
        return (
            infinite_gen(
                lambda wp: wp.bind(
                    lambda p: self._get_groups_page(org, p.last_index).map(
                        _union.inl
                    )
                    if p and p.last_index
                    else Cmd.from_cmd(lambda: None).map(_union.inr)
                ),
                init.map(_union.inl),
            )
            .transform(lambda s: from_piter(s))
            .transform(lambda s: until_none(s))
            .map(lambda x: _to_group(x))
            .map(lambda x: from_flist(x))
            .transform(lambda s: chain(s))
        )
