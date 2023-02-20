from ._raw_client import (
    GraphQlAsmClient,
)
from dataclasses import (
    dataclass,
)
from fa_purity import (
    Cmd,
    FrozenList,
    JsonObj,
    JsonValue,
    ResultE,
)
from fa_purity.frozen import (
    freeze,
)
from fa_purity.json.value.transform import (
    Unfolder,
)
from fa_purity.pure_iter.factory import (
    from_flist,
)
from fa_purity.result.transform import (
    all_ok,
)
from fa_purity.utils import (
    raise_exception,
)
from typing import (
    FrozenSet,
)


@dataclass(frozen=True)
class IgnoredPath:
    group: str
    nickname: str
    file_path: str


def _decode_ignored_paths(
    raw: JsonObj, group: str
) -> ResultE[FrozenList[IgnoredPath]]:
    nickname = (
        Unfolder(JsonValue(raw))
        .uget("nickname")
        .bind(lambda u: u.to_primitive(str).alt(Exception))
    )
    files = (
        Unfolder(JsonValue(raw))
        .uget("gitignore")
        .bind(lambda u: u.to_list_of(str).alt(Exception))
    )
    return nickname.bind(
        lambda n: files.map(
            lambda fs: tuple(IgnoredPath(group, n, f) for f in fs)
        )
    ).alt(lambda e: Exception(f"decode_ignored_paths failed i.e. {e}"))


def _decode_raw_ignored_paths(
    raw: JsonObj, group: str
) -> ResultE[FrozenList[IgnoredPath]]:
    return (
        Unfolder(JsonValue(raw))
        .uget("group")
        .bind(
            lambda u: u.uget("roots").bind(
                lambda uu: uu.to_unfolder_list()
                .alt(Exception)
                .bind(
                    lambda q: from_flist(q)
                    .map(
                        lambda i: i.to_json()
                        .alt(Exception)
                        .bind(lambda x: _decode_ignored_paths(x, group))
                    )
                    .transform(lambda p: all_ok(p.to_list()))
                )
            )
        )
        .map(lambda i: from_flist(i).bind(lambda x: from_flist(x)).to_list())
        .alt(lambda e: Exception(f"decode_raw_ignored_paths failed i.e. {e}"))
    )


def get_ignored_paths(
    client: GraphQlAsmClient, group: str
) -> Cmd[FrozenSet[IgnoredPath]]:
    query = """
    query IgnoredPaths($groupName: String!){
        group(groupName: $groupName){
            roots {
                ...on GitRoot{
                    nickname
                    gitignore
                }
            }
        }
    }
    """
    values = {"groupName": group}
    return (
        client.get(query, freeze(values))
        .map(lambda j: j.alt(raise_exception).unwrap())
        .map(
            lambda j: _decode_raw_ignored_paths(j, group)
            .alt(raise_exception)
            .unwrap()
        )
        .map(frozenset)
    )
