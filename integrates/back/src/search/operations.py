from search.client import (
    get_client,
)
from typing import (
    Any,
    Optional,
)


async def search(*, query: str) -> Optional[dict[str, Any]]:
    client = await get_client()
    response = await client.search(
        body={"query": {"multi_match": {"query": query}}}
    )

    return response
