# Local libraries
from typing import (
    Dict, Callable, Awaitable, Any
)
from asyncio import Queue

# Third party libraries
import aiohttp
from aioextensions import rate_limited

# Local libraries
from tap_gitlab.log import log


@rate_limited(
    # Gitlab allows at most 10 per second, not bursted
    max_calls=5,
    max_calls_period=1,
    min_seconds_between_calls=0.2,
)
async def get_json(
    session: aiohttp.ClientSession, endpoint: str, **kargs
) -> Dict[str, Any]:
    """Get as JSON the result of a GET request to endpoint."""
    async with session.get(endpoint, **kargs) as response:
        log('info', f'[{response.status}] {endpoint}')
        response.raise_for_status()

        return await response.json()


async def gitlab_data_emitter(
    get_request: Callable[..., Awaitable[Any]],
    project: str,
    resource: str,
    params: dict,
    api_token: str
) -> Callable[[Queue], Awaitable[None]]:
    """
    Returns Callable that iterates a gitlab resource for project
    and put messages into the queue.
    """
    async def data_emitter(queue: Queue) -> None:
        errors: int = 0
        page: int = 1
        per_page: int = 100
        async with aiohttp.ClientSession() as session:
            while errors <= 10:
                try:
                    params.update({'page': page, 'per_page': per_page})
                    records = await get_request(
                        session,
                        (
                            'https://gitlab.com/api/v4/projects'
                            f'/{project}/{resource}'
                        ),
                        params=params,
                        headers={'Private-Token': api_token}
                    )
                except aiohttp.ClientError as exc:
                    log('error', f'# {errors}: {type(exc).__name__}: {exc}')
                    errors += 1
                else:
                    if not records:
                        break
                    result = {
                        'type': 'gitlab_page_data',
                        'project': project,
                        'resource': resource,
                        'page': page, 'per_page': per_page,
                        'records': records
                    }
                    errors, page = 0, page + 1
                    await queue.put(result)
    return data_emitter
