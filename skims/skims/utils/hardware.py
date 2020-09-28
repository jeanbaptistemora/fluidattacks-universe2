# Standard library
from typing import (
    Iterator,
)
from resource import (
    getrusage,
    RUSAGE_CHILDREN,
    RUSAGE_SELF,
)

# Third party libraries
from aioextensions import (
    BoundedSemaphore,
)

# Useful notes
# https://manpages.debian.org/getrusage(2)

# Constants
_MEMORY_SEMAPHORE: BoundedSemaphore = None  # type: ignore


def get_max_memory_usage() -> float:
    kilobytes: int = sum(getrusage(resource).ru_maxrss for resource in (
        RUSAGE_CHILDREN,
        RUSAGE_SELF,
    ))

    return round(kilobytes / 1e6, ndigits=2)


def get_host_memory() -> int:
    """Return the available host memory, in GiB."""
    # Let's hard code it to 8 for now
    return 8


def get_memory_semaphore() -> BoundedSemaphore:
    """Returns the memory semaphore and initialize it if not yet created."""
    # This is required to be lazily initialized
    # We want to initialize it once we are inside the event loop, otherwise it
    # will hold a reference to a different event loop and wont work
    global _MEMORY_SEMAPHORE  # pylint: disable=global-statement
    if _MEMORY_SEMAPHORE is None:
        _MEMORY_SEMAPHORE = BoundedSemaphore(get_host_memory())

    return _MEMORY_SEMAPHORE


def iterate_host_memory_levels() -> Iterator[int]:
    """Return the available host memory, in GiB."""
    for memory in range(1, get_host_memory() + 1):
        yield memory
