from ._raw_client import (
    ApiError,
    GraphQlAsmClient,
)
from fa_purity import (
    Cmd,
    JsonObj,
    ResultE,
)
from fa_purity.frozen import (
    freeze,
)
from fa_purity.json.value.transform import (
    Unfolder,
)
from fa_purity.result.factory import (
    try_get,
)


def _decode_error(data: JsonObj) -> ResultE[None]:
    return (
        try_get(data, "errors")
        .alt(lambda _: None)
        .swap()
        .alt(lambda m: ApiError(m).to_exception())
    )


def _decode_org(raw: JsonObj) -> ResultE[str]:
    group = try_get(raw, "data").bind(lambda x: Unfolder(x).get("group"))
    return group.bind(
        lambda g: Unfolder(g)
        .uget("organization")
        .bind(lambda u: u.to_primitive(str).alt(Exception))
    )


def get_org(client: GraphQlAsmClient, group: str) -> Cmd[ResultE[str]]:
    query = """
    query ObservesGetGroupOrganization($groupName: String!){
        group(groupName: $groupName){
            organization
        }
    }
    """
    values = {"groupName": group}
    return client.get(query, freeze(values)).map(
        lambda j: _decode_error(j).bind(lambda _: _decode_org(j))
    )
