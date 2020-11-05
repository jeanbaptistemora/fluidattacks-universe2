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
    t_segment: TableSegment
    file: IO[str]
    exclusive_start_key: Optional[FrozenSet[Tuple[str, Any]]]


class ScanResponse(NamedTuple):
    t_segment: TableSegment
    response: FrozenSet[Tuple[str, Any]]


def paginate_table(
    db_client,
    table_segment: TableSegment,
    ex_start_key: Optional[FrozenSet[Tuple[str, Any]]],
) -> ScanResponse:
    table = db_client.Table(table_segment.table_name)
    scan_args: Dict[str, Any] = {
        'Limit': 1000,
        'ConsistentRead': True,
        'Segment': table_segment.segment,
        'TotalSegments': table_segment.total_segments,
    }
    if ex_start_key:
        scan_args.update({'ExclusiveStartKey': ex_start_key})
    result = table.scan(**scan_args)
    return ScanResponse(
        t_segment=table_segment,
        response=result
    )


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
            t_segment=scan_response.t_segment,
            file=file,
            exclusive_start_key=frozenset(last_key.items())
        )
    return PageData(
        t_segment=scan_response.t_segment,
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


def extract_segment(db_client, segment: TableSegment) -> List[PageData]:
    def extract(
        last_key: Optional[FrozenSet[Tuple[str, Any]]]
    ) -> Optional[PageData]:
        response: ScanResponse = paginate_table(
            db_client, segment, last_key
        )
        return response_to_dpage(response)
    return extract_until_end(
        extract=extract
    )
