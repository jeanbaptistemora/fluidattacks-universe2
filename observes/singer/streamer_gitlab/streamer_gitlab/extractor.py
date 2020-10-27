# Standard libraries
import json

from typing import (
    Any,
    Awaitable,
    Callable,
    cast,
    Dict,
    List,
)
from asyncio import (
    create_task,
    Queue
)

# Third party libraries
import urllib.parse
import aiohttp
from aioextensions import (
    collect,
    in_thread,
)

# Local libraries
from streamer_gitlab import api_client
from streamer_gitlab.log import log


def gitlab_data_emitter(  # pylint: disable=too-many-arguments
    get_request: Callable[..., Awaitable[Any]],
    project: str,
    resource: str,
    params: dict,
    api_token: str,
    max_pags: int,
    per_page: int = 100,
    offset_page: int = 1
) -> Callable[[Queue], Awaitable[None]]:
    """
    Returns Callable that iterates a gitlab resource for project
    and put messages into the queue.
    """
    async def data_emitter(queue: Queue) -> None:
        errors: int = 0
        page: int = 1
        async with aiohttp.ClientSession() as session:
            while errors <= 10:
                try:
                    params.update({
                        'page': page + offset_page - 1, 'per_page': per_page
                    })
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
                    if page > max_pags:
                        break
    return data_emitter


def emit(stream: str, records: Any, file=None) -> None:
    """Emit as special format so tap-json can consume it from stdin."""
    for record in records:
        msg = json.dumps({'stream': stream, 'record': record})
        if file:
            print(msg, file=file, flush=True)
        else:
            print(msg, flush=True)


async def emitter(queue: Queue) -> None:
    """Watch the queue and emit messages put into it.

    `None` is a sentinel value drained from the Queue that marks the end.
    """
    while True:
        item = await queue.get()
        if item is None:
            break
        if queue.full():
            log('warning', 'Queue is full and performance may be impacted!')

        stream = item['resource']
        records = item['records']

        await in_thread(emit, stream, records)


async def main(projects: List[str], api_token: str, max_pags: int) -> None:
    queue: Queue = Queue(maxsize=1024)
    emitter_task = create_task(emitter(queue))
    await collect([
        gitlab_data_emitter(
            api_client.get_json,
            urllib.parse.quote(project, safe=''),
            resource,
            cast(Dict[str, str], params),
            api_token,
            max_pags
        )(queue)
        for project in projects
        for resource, params in [
            ('jobs', {}),
            ('merge_requests', {'scope': 'all'}),
        ]
    ])
    await queue.put(None)
    await emitter_task
