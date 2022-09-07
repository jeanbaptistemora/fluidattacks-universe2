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


async def search(
    *,
    exact_filters: dict[str, Any],
    index: str,
    limit: int,
    after: Optional[str] = None,
    query: Optional[str] = None,
) -> SearchResponse:
    """
    Searches for items matching both the user input (full-text)
    and the provided filters (exact matches)

    https://opensearch.org/docs/1.2/opensearch/query-dsl/index/
    https://opensearch-project.github.io/opensearch-py/api-ref/client.html#opensearchpy.OpenSearch.search
    """
    client = await get_client()
    full_text_queries = [{"multi_match": {"query": query}}] if query else []
    term_queries = [
        {"term": {key: value}} for key, value in exact_filters.items()
    ]
    body = {
        "query": {
            "bool": {
                "must": [
                    *full_text_queries,
                    *term_queries,
                ],
            }
        }
    }
    response: dict[str, Any] = (
        await client.scroll(scroll_id=after, scroll=SCROLL_TIME)
        if after
        else await client.search(
            body=body,
            index=index,
            scroll=SCROLL_TIME,
            size=limit,
        )
    )
    hits: list[dict[str, Any]] = response["hits"]["hits"]

    return SearchResponse(
        items=tuple(hit["_source"] for hit in hits),
        page_info=PageInfo(
            end_cursor=response["_scroll_id"],
            has_next_page=len(hits) > 0,
        ),
    )
