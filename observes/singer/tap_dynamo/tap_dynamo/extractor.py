from purity.v1 import (
    FrozenDict,
    FrozenList,
    JsonFactory,
)
from purity.v1.pure_iter.factory import (
    from_flist,
)
from purity.v1.pure_iter.transform import (
    chain,
)
from purity.v1.pure_iter.transform.io import (
    consume,
)
from returns.io import (
    IO,
)
import simplejson  # type: ignore
from singer_io.singer2 import (
    SingerEmitter,
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
    Dict,
    IO as FILE,
    List,
    NamedTuple,
    Optional,
)


class TableSegment(NamedTuple):
    table_name: str
    segment: int
    total_segments: int


class PageData(NamedTuple):
    t_segment: TableSegment
    file: FILE[str]
    exclusive_start_key: Optional[FrozenDict[str, Any]]


class ScanResponse(NamedTuple):
    t_segment: TableSegment
    response: FrozenDict[str, Any]


def paginate_table(
    client: Client,
    table_segment: TableSegment,
    ex_start_key: Optional[Any],
) -> ScanResponse:
    table = client.table(table_segment.table_name)
    scan_args = ScanArgs(
        1000,
        False,
        table_segment.segment,
        table_segment.total_segments,
        ex_start_key,
    )
    result = table.scan(scan_args)
    return ScanResponse(t_segment=table_segment, response=result)


def response_to_dpage(scan_response: ScanResponse) -> Optional[PageData]:
    response = dict(scan_response.response)
    if response.get("Count") == 0:
        return None

    last_key: Optional[Dict[str, Any]] = response.get("LastEvaluatedKey", None)
    data = simplejson.dumps(response)
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


def extract_until_end(
    extract: Callable[[Optional[FrozenDict[str, Any]]], Optional[PageData]]
) -> FrozenList[PageData]:
    last_key: Optional[FrozenDict[str, Any]] = None
    end_reached: bool = False
    d_pages: List[PageData] = []
    while not end_reached:
        result: Optional[PageData] = extract(last_key)
        if not result:
            end_reached = True
            continue

        last_key = result.exclusive_start_key
        if not last_key:
            end_reached = True
        d_pages.append(result)
    return tuple(d_pages)


def extract_segment(
    db_client: Client, segment: TableSegment
) -> FrozenList[PageData]:
    def extract(
        last_key: Optional[FrozenDict[str, Any]]
    ) -> Optional[PageData]:
        response: ScanResponse = paginate_table(db_client, segment, last_key)
        return response_to_dpage(response)

    return extract_until_end(extract=extract)


def to_singer(page: PageData) -> FrozenList[SingerRecord]:
    with open(page.file.name, encoding="utf-8") as file:
        data = JsonFactory.load(file)
        return tuple(
            SingerRecord(page.t_segment.table_name, item.to_json())
            for item in data["Items"].to_list()
        )


def stream_tables(client: Client, tables: FrozenList[str]) -> IO[None]:
    # pylint: disable=unnecessary-lambda
    emitter = SingerEmitter()
    pages = chain(
        from_flist(tables)
        .map(lambda t: extract_segment(client, TableSegment(t, 0, 1)))
        .map(lambda x: from_flist(x))
    )
    records = chain(pages.map(to_singer).map(lambda x: from_flist(x)))
    return consume(records.map(emitter.emit))
