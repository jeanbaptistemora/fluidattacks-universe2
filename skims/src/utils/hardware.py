# Standard library
from resource import (
    getrusage,
    RUSAGE_CHILDREN,
    RUSAGE_SELF,
)

# Useful notes
# https://manpages.debian.org/getrusage(2)


def get_max_memory_usage() -> float:
    kilobytes: int = sum(getrusage(resource).ru_maxrss for resource in (
        RUSAGE_CHILDREN,
        RUSAGE_SELF,
    ))

    return round(kilobytes / 1e6, ndigits=2)
