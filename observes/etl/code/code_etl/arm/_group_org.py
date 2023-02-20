from ._error import (
    ApiError,
)
from ._raw_client import (
    GraphQlAsmClient,
)
from fa_purity import (
    Cmd,
    JsonObj,
    Result,
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


def _decode_org(raw: JsonObj) -> ResultE[str]:
    group = try_get(raw, "group")
    return group.bind(
        lambda g: Unfolder(g)
        .uget("organization")
        .bind(lambda u: u.to_primitive(str).alt(Exception))
    )


def get_org(
    client: GraphQlAsmClient, group: str
) -> Cmd[Result[str, ApiError]]:
    query = """
    query ObservesGetGroupOrganization($groupName: String!){
        group(groupName: $groupName){
            organization
        }
    }
    """
    values = {"groupName": group}
    return client.get(query, freeze(values)).map(
        lambda r: r.map(lambda d: _decode_org(d).unwrap())
    )
