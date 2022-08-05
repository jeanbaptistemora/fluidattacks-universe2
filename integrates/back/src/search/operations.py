from search.client import (
    get_client,
)
from typing import (
    Any,
    Optional,
)


async def search(
    *,
    exact_filters: dict[str, Any],
    index: str,
    query: Optional[str],
) -> tuple[dict[str, Any], ...]:
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
    response: dict[str, Any] = await client.search(body=body, index=index)

    return tuple(hit["_source"] for hit in response["hits"]["hits"])
