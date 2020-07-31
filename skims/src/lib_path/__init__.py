# Standard library
from glob import (
    iglob as glob,
)
import os
from itertools import chain
from typing import (
    AsyncGenerator,
    Dict,
    Iterator,
    Set,
    Tuple,
)

# Local imports
from lib_path import (
    f0034,
)
from utils.aio import (
    materialize,
)
from utils.fs import (
    generate_file_content,
    recurse,
)
from utils.logs import (
    log,
)
from utils.model import (
    Vulnerability,
)
from utils.string import (
    get_char_to_yx_map,
)


async def generate_char_to_yx_map(
    file_content_generator: AsyncGenerator[str, None],
) -> AsyncGenerator[Dict[int, Tuple[int, int]], None]:
    file_content: str = await file_content_generator.__anext__()

    mapping: Dict[int, Tuple[int, int]] = await get_char_to_yx_map(
        lines=tuple(file_content.splitlines()),
    )

    while True:
        yield mapping


async def analyze_one_path(path: str) -> Tuple[Vulnerability, ...]:
    file_content_generator: AsyncGenerator[str, None] = generate_file_content(
        path,
    )
    char_to_yx_map_generator: (
        AsyncGenerator[Dict[int, Tuple[int, int]], None]
    ) = generate_char_to_yx_map(
        file_content_generator=file_content_generator,
    )

    results: Tuple[Vulnerability, ...] = tuple(chain(
        *await materialize(
            getattr(module, 'analyze')(
                char_to_yx_map_generator=char_to_yx_map_generator,
                content_generator=file_content_generator,
                extension=os.path.splitext(path)[1][1:],
                path=path,
            )
            for module in (
                f0034,
            )
        )
    ))

    await char_to_yx_map_generator.aclose()
    await file_content_generator.aclose()

    return results


async def analyze(
    *,
    paths_to_exclude: Tuple[str, ...],
    paths_to_include: Tuple[str, ...],
) -> Tuple[Vulnerability, ...]:

    def resolve(path: str) -> Iterator[str]:
        if path.startswith('glob(') and path.endswith(')'):
            yield from glob(path[5:-1])
        else:
            yield path

    try:
        unique_paths: Set[str] = set(chain(
            *await materialize(
                map(recurse, chain(*map(resolve, paths_to_include))),
            ),
        )) - set(chain(
            *await materialize(
                map(recurse, chain(*map(resolve, paths_to_exclude))),
            ),
        ))
    except FileNotFoundError as exc:
        await log('critical', 'File does not exist: %s', exc.filename)
        raise SystemExit()
    else:
        await log('info', 'Files to be tested: %s', len(unique_paths))

    results: Tuple[Vulnerability, ...] = tuple(chain(
        *await materialize(map(analyze_one_path, unique_paths))
    ))

    return results
