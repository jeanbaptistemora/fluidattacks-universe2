from ._core import (
    OrganizationId,
)
from dataclasses import (
    dataclass,
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
    unsafe_from_cmd,
)
from fa_purity.stream.factory import (
    from_piter,
)
from fa_purity.stream.transform import (
    chain,
)
from mypy_boto3_dynamodb import (
    DynamoDBClient,
)
from mypy_boto3_dynamodb.type_defs import (
    ScanOutputTableTypeDef,
)
from typing import (
    Any,
    Dict,
    Iterable,
    TypeVar,
)

_T = TypeVar("_T")
_DB_TABLE = "fi_organizations"


def _mark_impure(item: _T) -> Cmd[_T]:
    return Cmd.from_cmd(lambda: item)


def _assert_dict(item: _T) -> Dict[Any, Any]:  # type: ignore[misc]
    if isinstance(item, dict):
        return item
    raise Exception(f"Expected `dict` instance; got `{type(item)}`")


def _to_items(page: ScanOutputTableTypeDef) -> FrozenList[OrganizationId]:
    return tuple(  # type: ignore[misc]
        OrganizationId(
            to_primitive(_assert_dict(item["pk"])["S"], str).unwrap(),  # type: ignore[misc]
            to_primitive(_assert_dict(item["sk"])["S"], str).unwrap().lstrip("INFO#"),  # type: ignore[misc]
        )
        for item in page["Items"]  # type: ignore[misc]
    )


@dataclass(frozen=True)
class OrgsClient:
    _client: DynamoDBClient

    def all_orgs(self) -> Stream[OrganizationId]:
        def _new_iter() -> Iterable[Cmd[ScanOutputTableTypeDef]]:
            exp_attrs_values: Dict[str, Dict[str, str]] = {
                ":pk": {"S": "ORG#"},
                ":sk": {"S": "INFO#"},
            }
            response = self._client.get_paginator("scan").paginate(
                ExpressionAttributeNames={
                    "#pk": "pk",
                    "#sk": "sk",
                },
                ExpressionAttributeValues=exp_attrs_values,
                FilterExpression=(
                    "begins_with(#pk, :pk) and begins_with(#sk, :sk)"
                ),
                TableName=_DB_TABLE,
            )  # type: ignore[misc]
            return map(_mark_impure, response)  # type: ignore[misc]

        data = from_piter(unsafe_from_cmd(Cmd.from_cmd(_new_iter)))  # type: ignore[misc]
        return data.map(lambda x: _to_items(x)).map(lambda x: from_flist(x)).transform(lambda s: chain(s))  # type: ignore[misc]
