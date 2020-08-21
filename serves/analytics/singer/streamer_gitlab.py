# Local libraries
from asyncio import (
    create_task,
    Queue,
)
import json
from os import (
    environ,
)
import sys
import urllib.parse
from typing import (
    Any,
)

# Third party libraries
from aioextensions import (
    collect,
    in_process,
    rate_limited,
    run,
)
import aiohttp


def log(level: str, msg: str) -> None:
    """Print something to console, the user can see it as progress."""
    print(f'[{level.upper()}]', msg, file=sys.stderr, flush=True)


def emit(stream: str, records: Any) -> None:
    """Emit as Singer records so tap-json can consume it from stdin."""
    for record in records:
        msg = json.dumps({'stream': stream, 'record': record})
        print(msg, file=sys.stdout, flush=True)


async def emitter(queue: Queue) -> None:
    """Watch the queue and emit messages put into it.

    `None` is a sentinel value drained from the Queue that marks the end.
    """
    while True:
        item = await queue.get()
        if item is None:
            break
        if queue.full():
            log('warning', f'Queue is full and performance may be impacted!')

        stream, records = item
        await in_process(emit, stream, records)


@rate_limited(
    # Gitlab allows at most 10 per second, not bursted
    max_calls=5,
    max_calls_period=1,
    min_seconds_between_calls=0.2,
)
async def get(session: aiohttp.ClientSession, endpoint: str) -> Any:
    """Get as JSON the result of a GET request to endpoint."""
    async with session.get(
        endpoint,
        headers={
            'Private-Token': API_TOKEN,
        },
    ) as response:
        log('info', f'[{response.status}] {endpoint}')
        response.raise_for_status()

        return await response.json()


async def paginate(
    queue: Queue,
    project: str,
    resource: str,
    params: str,
) -> None:
    """Iterate a gitlab resource for project and put messages into the queue.
    """
    errors: int = 0
    page: int = 1
    async with aiohttp.ClientSession() as session:
        while errors <= 10:
            try:
                records = await get(
                    session,
                    f'https://gitlab.com/api/v4/projects/{project}/{resource}'
                    f'?page={page}'
                    f'&per_page=100'
                    f'{params}'
                )
            except aiohttp.ClientError as exc:
                log('error', f'# {errors}: {type(exc).__name__}: {exc}')
                errors += 1
            else:
                if not records:
                    break

                errors, page = 0, page + 1
                await queue.put((resource, records))


async def main() -> None:
    """Create concurrent tasks of paginators and coordinate a result queue."""
    queue = Queue(maxsize=1024)
    emitter_task = create_task(emitter(queue))

    for project in sys.argv[1:]:
        log('info', f'Executing {project}')

    await collect([
        paginate(queue, urllib.parse.quote(project, safe=''), resource, params)
        for project in sys.argv[1:]
        for resource, params in [
            ('jobs', ''),
            ('merge_requests', '&scope=all'),
        ]
    ])

    await queue.put(None)
    await emitter_task


if __name__ == '__main__':
    try:
        API_TOKEN = environ['GITLAB_API_TOKEN']
    except KeyError:
        log('critical', 'Export GITLAB_API_TOKEN as environment variable')
        sys.exit(1)
    else:
        run(main())
