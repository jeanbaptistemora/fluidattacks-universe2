# Standard library
import os
from itertools import chain
from typing import (
    AsyncGenerator,
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
    generate_file_content,
    recurse,
)
from utils.model import (
    Vulnerability,
)


async def analyze_one_path(path: str) -> Tuple[Vulnerability, ...]:
    file_content_generator: AsyncGenerator[str, None] = generate_file_content(
        path,
    )

    results: Tuple[Vulnerability, ...] = tuple(chain(*(
        await materialize(
            getattr(module, 'analyze')(
                extension=os.path.splitext(path)[1][1:],
                file_content_generator=file_content_generator,
                path=path,
            )
            for module in (
                f0034,
            )
        )
    )))

    await file_content_generator.aclose()

    return results


async def analyze(paths: Tuple[str, ...]) -> Tuple[Vulnerability, ...]:
    unique_paths: Set[str] = set(*(
        await materialize(map(recurse, paths))
    ))

    results: Tuple[Vulnerability, ...] = tuple(chain(*(
        await materialize(map(analyze_one_path, unique_paths))
    )))

    return results
