# Standard library
from itertools import chain
from typing import (
    Tuple,
)

# Local imports
from core.lib import (
    path_0038,
)
from model import (
    Vulnerability,
)
from utils.aio import (
    materialize,
)
from utils.fs import (
    recurse,
)


async def skim_paths(paths: Tuple[str, ...]) -> Tuple[Vulnerability, ...]:
    files: Tuple[str, ...] = tuple(set(*(
        await materialize(map(recurse, paths))
    )))

    results: Tuple[Vulnerability, ...] = tuple(chain(*(
        await materialize(
            getattr(module, 'run')(file=file)
            for module in (
                path_0038,
            )
            for file in files
        )
    )))

    return results
