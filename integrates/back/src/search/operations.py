from dynamodb.types import (
    PageInfo,
)
from search.client import (
    get_client,
)
from search.enums import (
    Sort,
)
from search.types import (
    SearchResponse,
)
from typing import (
    Any,
)


async def search(  # pylint: disable=too-many-locals
    *,
    exact_filters: dict[str, Any] | None = None,
    index: str,
    limit: int,
    after: str | None = None,
    query: str | None = None,
    should_filters: list[dict[str, Any]] | None = None,
    must_filters: list[dict[str, Any]] | None = None,
    must_match_prefix_filters: list[dict[str, Any]] | None = None,
    range_filters: list[dict[str, Any]] | None = None,
    must_not_filters: list[dict[str, Any]] | None = None,
    sort_by: dict[str, Any] | None = None,
) -> SearchResponse:
    """
    Searches for items matching both the user input (full-text)
    and the provided filters (exact matches)

    https://opensearch.org/docs/1.2/opensearch/query-dsl/index/
    https://opensearch-project.github.io/opensearch-py/api-ref/client.html#opensearchpy.OpenSearch.search
    """
    client = await get_client()
    full_and_filters = []
    full_match_prefix_filters = []
    full_must_not_filters = []
    full_or_filters = []
    query_range = []
    sort = []

    if must_filters:
        full_and_filters = [
            {"match": {key: {"query": value, "operator": "and"}}}
            for attrs in must_filters
            for key, value in attrs.items()
        ]

    if must_not_filters:
        full_must_not_filters = [
            {"match": {key: {"query": value, "operator": "and"}}}
            for attrs in must_not_filters
            for key, value in attrs.items()
        ]

    if should_filters:
        full_or_filters = [
            {"match": {key: value}}
            for attrs in should_filters
            for key, value in attrs.items()
        ]

    if range_filters:
        query_range = [{"range": range} for range in range_filters]

    if must_match_prefix_filters:
        full_match_prefix_filters = [
            {"match_phrase_prefix": {key: value}}
            for attrs in must_match_prefix_filters
            for key, value in attrs.items()
        ]

    full_text_queries = [{"multi_match": {"query": query}}] if query else []
    term_queries = (
        [{"term": {key: value}} for key, value in exact_filters.items()]
        if exact_filters
        else {}
    )

    if sort_by:
        sort = [{key: {"order": value} for key, value in sort_by.items()}]

    body = {
        "query": {
            "bool": {
                "must": [
                    *full_and_filters,
                    *full_text_queries,
                    *query_range,
                    *term_queries,
                    *full_match_prefix_filters,
                ],
                "should": [
                    *full_or_filters,
                ],
                "minimum_should_match": 1 if full_or_filters else 0,
                "must_not": [*full_must_not_filters],
            }
        },
        "sort": [{"_id": {"order": Sort.DESCENDING.value}}, *sort],
    }

    if after:
        body["search_after"] = [after]

    response = await client.search(
        body=body,
        index=index,
        size=limit,
    )
    hits: list[dict[str, Any]] = response["hits"]["hits"]

    return SearchResponse(
        items=tuple(hit["_source"] for hit in hits),
        page_info=PageInfo(
            end_cursor=hits[-1]["_id"] if hits else "",
            has_next_page=len(hits) > 0,
        ),
        total=response["hits"]["total"]["value"],
    )
