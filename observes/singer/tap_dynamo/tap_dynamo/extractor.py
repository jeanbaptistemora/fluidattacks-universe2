from dataclasses import (
    dataclass,
)
from fa_purity.cmd import (
    Cmd,
    unsafe_unwrap,
)
from fa_purity.cmd.transform import (
    merge,
)
from fa_purity.frozen import (
    chain as chain_list,
    FrozenDict,
    FrozenList,
)
from fa_purity.json.factory import (
    load,
)
from fa_purity.json.value.transform import (
    Unfolder,
)
from fa_purity.pure_iter.factory import (
    from_flist,
    from_range,
)
from fa_purity.stream.factory import (
    from_piter,
)
from fa_purity.stream.transform import (
    chain,
    consume,
)
from pathos.pools import (
    ThreadPool,
)
from purity.adapters.fa_purity.from_returns import (
    to_cmd,
)
from purity.adapters.fa_purity.to_legacy import (
    to_jval_v1,
)
import simplejson  # type: ignore
from singer_io.singer2 import (
    SingerEmitter,
    SingerMessage,
    SingerRecord,
)
from tap_dynamo.client import (
    Client,
    ScanArgs,
)
import tempfile
from typing import (
    Any,
    Callable,
    cast,
    Dict,
    IO as FILE,
    List,
    Optional,
    TypeVar,
)

_K = TypeVar("_K")
_P = TypeVar("_P")


@dataclass(frozen=True)
class TableSegment:
    table_name: str
    segment: int
    total_segments: int


@dataclass(frozen=True)
class PageData:
    t_segment: TableSegment
    file: FILE[str]
    exclusive_start_key: Optional[FrozenDict[str, Any]]


@dataclass(frozen=True)
class ScanResponse:
    t_segment: TableSegment
    response: FrozenDict[str, Any]


def paginate_table(
    client: Client,
    table_segment: TableSegment,
    ex_start_key: Optional[Any],
) -> Cmd[ScanResponse]:
    table = client.table(table_segment.table_name)
    scan_args = ScanArgs(
        1000,
        False,
        table_segment.segment,
        table_segment.total_segments,
        ex_start_key,
    )
    result = table.scan(scan_args)
    return result.map(
        lambda r: ScanResponse(t_segment=table_segment, response=r)
    )


class SetEncoder(simplejson.JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, set):
            return list(o)
        return simplejson.JSONEncoder.default(self, o)


def response_to_dpage(scan_response: ScanResponse) -> Optional[PageData]:
    response = dict(scan_response.response)
    if response.get("Count") == 0:
        return None

    last_key: Optional[Dict[str, Any]] = response.get("LastEvaluatedKey", None)
    data = simplejson.dumps(response, cls=SetEncoder)
    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as file:
        file.write(data)
        if last_key:
            return PageData(
                t_segment=scan_response.t_segment,
                file=file,
                exclusive_start_key=FrozenDict(last_key),
            )
        return PageData(
            t_segment=scan_response.t_segment,
            file=file,
            exclusive_start_key=None,
        )


def _extract_until_end_action(
    getter: Callable[[Optional[_K]], Cmd[Optional[_P]]],
    extract_next: Callable[[_P], Optional[_K]],
) -> FrozenList[_P]:
    last_key: Optional[_K] = None
    end_reached: bool = False
    d_pages: List[_P] = []
    while not end_reached:
        result: Optional[_P] = unsafe_unwrap(getter(last_key))
        if not result:
            end_reached = True
            continue

        last_key = extract_next(result)
        if not last_key:
            end_reached = True
        d_pages.append(result)
    return tuple(d_pages)


def extract_until_end(
    getter: Callable[[Optional[_K]], Cmd[Optional[_P]]],
    extract_next: Callable[[_P], Optional[_K]],
) -> Cmd[FrozenList[_P]]:
    return Cmd.from_cmd(
        lambda: _extract_until_end_action(getter, extract_next)
    )


def extract_segment(
    db_client: Client, segment: TableSegment
) -> Cmd[FrozenList[PageData]]:
    def getter(
        last_key: Optional[FrozenDict[str, Any]]
    ) -> Cmd[Optional[PageData]]:
        response = paginate_table(db_client, segment, last_key)
        return response.map(response_to_dpage)

    def extract(page: PageData) -> Optional[FrozenDict[str, Any]]:
        return page.exclusive_start_key

    return extract_until_end(getter, extract)


def extract_table(
    db_client: Client, table_name: str, segments: int
) -> Cmd[FrozenList[PageData]]:
    pool = ThreadPool()
    cmds = (
        from_range(range(segments))
        .map(
            lambda i: extract_segment(
                db_client, TableSegment(table_name, i, segments)
            )
        )
        .to_list()
    )
    merged = merge(
        lambda u, l: cast(FrozenList[FrozenList[PageData]], pool.map(u, l)),
        cmds,
    ).map(
        lambda i: chain_list(i)  # pylint: disable=unnecessary-lambda
    )
    return merged


def to_singer(page: PageData) -> FrozenList[SingerRecord]:
    with open(page.file.name, encoding="utf-8") as file:
        data = load(file).unwrap()
        return tuple(
            SingerRecord(
                page.t_segment.table_name,
                {
                    k: to_jval_v1(v)
                    for k, v in Unfolder(item).to_json().unwrap().items()
                },
            )
            for item in Unfolder(data["Items"]).to_list().unwrap()
        )


def stream_tables(
    client: Client, tables: FrozenList[str], segmentation: int
) -> Cmd[None]:
    # pylint: disable=unnecessary-lambda
    emitter = SingerEmitter()
    pages = from_piter(
        from_flist(tables).map(
            lambda t: extract_table(client, t, segmentation).map(
                lambda x: from_flist(x)
            )
        )
    )
    records = (
        chain(pages)
        .map(to_singer)
        .map(lambda x: from_flist(x))
        .transform(lambda x: chain(x))
    )

    def emit(msg: SingerMessage) -> Cmd[None]:
        return to_cmd(lambda: emitter.emit(msg))

    return consume(records.map(emit))
