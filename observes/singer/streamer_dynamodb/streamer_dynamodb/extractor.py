from typing import (
    Any,
    Callable,
    cast,
    Dict,
    IO,
    List,
    NamedTuple,
    Optional,
)


class TableSegment(NamedTuple):
    table_name: str
    segment: int
    total_segments: int


class PageData(NamedTuple):
    file: IO[str]
    exclusive_start_key: Optional[Dict[str, Any]]


def paginate_table(
    db_client,
    table_segment: TableSegment,
    ex_start_key: Dict[str, Any],
) -> Dict[str, Any]:
    table = db_client.Table(table_segment.table_name)
    return table.scan(
        Limit=1000,
        ConsistentRead=True,
        ExclusiveStartKey=ex_start_key,
        Segment=table_segment.segment,
        TotalSegments=table_segment.total_segments,
    )


def extract_until_end(
    extract: Callable[[Optional[Dict[str, Any]]], Optional[PageData]]
) -> List[PageData]:
    last_key: Optional[Dict[str, Any]] = None
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
