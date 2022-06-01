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
    Mapping,
    Optional,
    Sequence,
    Set,
)

_ORGS_TABLE = "fi_organizations"
_LastObjKey = Mapping[str, bytes | bytearray | str | int | Decimal | bool | Set[int] | Set[Decimal] | Set[str] | Set[bytes] | Set[bytearray] | Sequence[Any] | Mapping[str, Any] | None]  # type: ignore[misc]


@dataclass(frozen=True)  # type: ignore[misc]
class _Page:
    response: QueryOutputTableTypeDef
    last_index: Optional[_LastObjKey]


def _to_group(pag: _Page) -> FrozenList[GroupId]:
    return tuple(to_primitive(i["sk"], str).unwrap().split("#")[1] for i in pag.response["Items"])  # type: ignore[misc]


@dataclass(frozen=True)
class _GroupsClient:
    _table: Table


class GroupsClient(_GroupsClient):
    def __init__(self, resource: DynamoDBServiceResource) -> None:
        super().__init__(resource.Table(_ORGS_TABLE))

    def _get_groups_page(
        self, org: OrganizationId, last_index: Optional[_LastObjKey]
    ) -> Cmd[_Page]:
        def _action() -> _Page:
            condition = Key("pk").eq(f"ORG#{org.uuid}") & Key(
                "sk"
            ).begins_with("GROUP#")
            filter_exp = Attr("deletion_date").not_exists()
            response_items = (
                self._table.query(  # type: ignore[misc]
                    KeyConditionExpression=condition,
                    FilterExpression=filter_exp,
                    ExclusiveStartKey=last_index,
                )
                if last_index
                else self._table.query(  # type: ignore[misc]
                    KeyConditionExpression=condition,
                    FilterExpression=filter_exp,
                )
            )
            return _Page(
                response_items,  # type: ignore[misc]
                response_items.get("LastEvaluatedKey"),  # type: ignore[misc]
            )

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
