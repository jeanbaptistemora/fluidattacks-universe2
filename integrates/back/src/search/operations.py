from search.client import (
    get_client,
)
from typing import (
    Any,
)


async def search(*, query: str) -> tuple[dict[str, Any], ...]:
    """
    Searches for items matching the arbitrary user input

    https://opensearch-project.github.io/opensearch-py/api-ref/client.html#opensearchpy.OpenSearch.search
    """
    client = await get_client()
    response: dict[str, Any] = await client.search(
        body={"query": {"multi_match": {"query": query}}}
    )

    return tuple(hit["_source"] for hit in response["hits"]["hits"])
