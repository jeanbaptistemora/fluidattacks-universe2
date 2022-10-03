# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from dynamodb.types import (
    PageInfo,
)
from search.client import (
    get_client,
)
from search.types import (
    SearchResponse,
)
from typing import (
    Any,
    Optional,
)

SCROLL_TIME = "10m"


async def search(  # pylint: disable=too-many-locals
    *,
    exact_filters: Optional[dict[str, Any]] = None,
    index: str,
    limit: int,
    after: Optional[str] = None,
    query: Optional[str] = None,
    should_filters: Optional[list[dict[str, Any]]] = None,
    must_filters: Optional[list[dict[str, Any]]] = None,
    range_filters: Optional[list[dict[str, Any]]] = None,
    must_not_filters: Optional[list[dict[str, Any]]] = None,
    sort_by: Optional[dict[str, Any]] = None,
) -> SearchResponse:
    """
    Searches for items matching both the user input (full-text)
    and the provided filters (exact matches)

    https://opensearch.org/docs/1.2/opensearch/query-dsl/index/
    https://opensearch-project.github.io/opensearch-py/api-ref/client.html#opensearchpy.OpenSearch.search
    """
    client = await get_client()
    full_and_filters = []
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
                ],
                "should": [
                    *full_or_filters,
                ],
                "must_not": [*full_must_not_filters],
            }
        },
        "sort": [*sort],
    }
    scroll = None if limit == 0 else SCROLL_TIME
    response: dict[str, Any] = (
        await client.scroll(scroll_id=after, scroll=scroll)
        if after and scroll
        else await client.search(
            body=body,
            index=index,
            scroll=scroll,
            size=limit,
        )
    )
    hits: list[dict[str, Any]] = response["hits"]["hits"]

    return SearchResponse(
        items=tuple(hit["_source"] for hit in hits),
        page_info=PageInfo(
            end_cursor=response.get("_scroll_id", ""),
            has_next_page=len(hits) > 0,
        ),
        total=response["hits"]["total"]["value"],
    )
