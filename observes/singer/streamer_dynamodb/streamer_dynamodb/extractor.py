# Standard libraries
import json
import tempfile
from typing import (
    Any,
    Callable,
    cast,
    Dict,
    FrozenSet,
    IO,
    List,
    NamedTuple,
    Optional,
    Tuple,
)
# Third party libraries
# Local libraries


class TableSegment(NamedTuple):
    table_name: str
    segment: int
    total_segments: int


class PageData(NamedTuple):
    file: IO[str]
    exclusive_start_key: Optional[FrozenSet[Tuple[str, Any]]]


class ScanResponse(NamedTuple):
    response: FrozenSet[Tuple[str, Any]]


def paginate_table(
    db_client,
    table_segment: TableSegment,
    ex_start_key: Dict[str, Any],
) -> ScanResponse:
    table = db_client.Table(table_segment.table_name)
    result = table.scan(
        Limit=1000,
        ConsistentRead=True,
        ExclusiveStartKey=ex_start_key,
        Segment=table_segment.segment,
        TotalSegments=table_segment.total_segments,
    )
    return ScanResponse(result)


def response_to_dpage(scan_response: ScanResponse) -> Optional[PageData]:
    response = dict(scan_response.response)
    if response.get('Count') == 0:
        return None

    last_key: Optional[Dict[str, Any]] = response.get('LastEvaluatedKey', None)
    data = json.dumps(response['Items'])
    file = tempfile.NamedTemporaryFile(mode='w+')
    file.write(data)
    if last_key:
        return PageData(
            file=file,
            exclusive_start_key=frozenset(last_key.items())
        )
    return PageData(
        file=file,
        exclusive_start_key=None
    )


def extract_until_end(
    extract: Callable[
        [Optional[FrozenSet[Tuple[str, Any]]]],
        Optional[PageData]
    ]
) -> List[PageData]:
    last_key: Optional[FrozenSet[Tuple[str, Any]]] = None
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
        d_pages.append(cast(PageData, result))
    return d_pages
