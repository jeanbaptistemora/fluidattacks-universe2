# Standard library
import os
from itertools import chain
from typing import (
    Set,
    Tuple,
)

# Local imports
from lib_path.findings import (
    f0034,
)
from utils.aio import (
    materialize,
)
from utils.fs import (
    recurse,
)
from utils.model import (
    Vulnerability,
)


async def analyze(paths: Tuple[str, ...]) -> Tuple[Vulnerability, ...]:
    unique_paths: Set[str] = set(*(
        await materialize(map(recurse, paths))
    ))

    results: Tuple[Vulnerability, ...] = tuple(chain(*(
        await materialize(
            getattr(module, 'analyze')(
                extension=os.path.splitext(path)[1][1:],
                path=path,
            )
            for module in (
                f0034,
            )
            for path in unique_paths
        )
    )))

    return results
