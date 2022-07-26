from search.client import (
    get_client,
)
from typing import (
    Any,
)


async def search(
    *,
    exact_filters: dict[str, Any],
    query: str,
) -> tuple[dict[str, Any], ...]:
    """
    Searches for items matching the arbitrary user input

    https://opensearch-project.github.io/opensearch-py/api-ref/client.html#opensearchpy.OpenSearch.search
    """
    client = await get_client()
    term_queries = [
        {"term": {key: value}} for key, value in exact_filters.items()
    ]
    body = {
        "query": {
            "bool": {
                "must": [
                    {"multi_match": {"query": query}},
                    *term_queries,
                ],
            }
        }
    }
    response: dict[str, Any] = await client.search(body=body)

    return tuple(hit["_source"] for hit in response["hits"]["hits"])
