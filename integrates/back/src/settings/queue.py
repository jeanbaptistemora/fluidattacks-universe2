# pylint: disable=unsubscriptable-object
"""Queue management"""
from asyncio.queues import (
    Queue,
)
from functools import (
    partial,
)
from typing import (
    Any,
    Callable,
    Optional,
    TypeVar,
)

# Constants
TVar = TypeVar("TVar")  # pylint: disable=invalid-name
DELAY_QUEUE: Optional[Queue] = None


def init_queue() -> None:
    global DELAY_QUEUE  # pylint: disable=global-statement
    DELAY_QUEUE = Queue()


def enqueue_task(
    func: Callable[..., TVar],
    *args: Any,
    **kwargs: Any,
) -> None:
    if DELAY_QUEUE:
        DELAY_QUEUE.put_nowait((func, args, kwargs))
    else:
        raise RuntimeError("Queue must be initialized")


async def get_task() -> Callable[..., TVar]:
    if DELAY_QUEUE:
        func, args, kwargs = await DELAY_QUEUE.get()
        return partial(func, *args, **kwargs)

    raise RuntimeError("Queue must be initialized")
