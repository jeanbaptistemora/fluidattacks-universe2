from aioextensions import (
    in_thread,
)
from asyncio import (
    Queue,
)
import json
import logging
from typing import (
    Any,
    IO,
    List,
    Optional,
)

LOG = logging.getLogger(__name__)


def emit(
    stream: str, records: List[Any], file: Optional[IO[str]] = None
) -> None:
    """Emit as special format so tap-json can consume it from stdin."""
    for record in records:
        msg = json.dumps({"stream": stream, "record": record})
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
            LOG.warning("Queue is full and performance may be impacted!")

        stream = item["resource"]
        records = item["records"]

        await in_thread(emit, stream, records)
