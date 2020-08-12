# Standard library
from glob import (
    iglob as glob,
)
from os.path import (
    normpath,
    split,
    splitext,
)
from itertools import chain
from typing import (
    Awaitable,
    Callable,
    Dict,
    Iterator,
    Set,
    Tuple,
)

# Third party libraries
from aioextensions import (
    collect,
)

# Local imports
from lib_path import (
    f009,
    f011,
    f060,
    f061,
    f117,
)
from utils.function import (
    never_concurrent,
)
from utils.fs import (
    generate_file_content,
    generate_file_raw_content,
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


def generate_char_to_yx_map(
    file_content_generator: Callable[[], Awaitable[str]],
) -> Callable[[], Awaitable[Dict[int, Tuple[int, int]]]]:
    data: Dict[str, Dict[int, Tuple[int, int]]] = {}

    @never_concurrent
    async def get_one() -> Dict[int, Tuple[int, int]]:
        if not data:
            content = await file_content_generator()
            data['mapping'] = await get_char_to_yx_map(
                lines=tuple(content.splitlines()),
            )
        return data['mapping']

    return get_one


async def analyze_one_path(path: str) -> Tuple[Vulnerability, ...]:
    """Execute all findings against the provided file.

    :param path: Path to the file who's object of analysis
    :type path: str
    :return: Tuple with the vulnerabilities found
    :rtype: Tuple[Vulnerability, ...]
    """
    file_content_generator = generate_file_content(path)
    file_raw_content_generator = generate_file_raw_content(path)
    char_to_yx_map_generator = generate_char_to_yx_map(file_content_generator)

    results: Tuple[Vulnerability, ...] = tuple(chain.from_iterable(
        await collect(tuple(chain.from_iterable((
            (
                f009.analyze(
                    char_to_yx_map_generator=char_to_yx_map_generator,
                    content_generator=file_content_generator,
                    file_extension=file_extension,
                    path=path,
                ),
                f011.analyze(
                    content_generator=file_content_generator,
                    file_name=file_name,
                    file_extension=file_extension,
                    path=path,
                ),
                f060.analyze(
                    char_to_yx_map_generator=char_to_yx_map_generator,
                    content_generator=file_content_generator,
                    file_extension=file_extension,
                    path=path,
                ),
                f061.analyze(
                    char_to_yx_map_generator=char_to_yx_map_generator,
                    content_generator=file_content_generator,
                    file_extension=file_extension,
                    path=path,
                ),
                f117.analyze(
                    file_name=file_name,
                    file_extension=file_extension,
                    path=path,
                    raw_content_generator=file_raw_content_generator,
                ),
            )
            for folder, file in [split(path)]
            for file_name, file_extension in [splitext(file)]
            for file_extension in [file_extension[1:]]
        ))))
    ))

    return results


async def analyze(
    *,
    paths_to_exclude: Tuple[str, ...],
    paths_to_include: Tuple[str, ...],
) -> Tuple[Vulnerability, ...]:

    def normalize(path: str) -> str:
        return normpath(path)

    def resolve(path: str) -> Iterator[str]:
        if path.startswith('glob(') and path.endswith(')'):
            yield from glob(path[5:-1], recursive=True)
        else:
            yield path

    try:
        unique_paths: Set[str] = set(map(normalize, chain.from_iterable(
            await collect(map(
                recurse, chain.from_iterable(map(resolve, paths_to_include)),
            )),
        ))) - set(map(normalize, chain.from_iterable(
            await collect(map(
                recurse, chain.from_iterable(map(resolve, paths_to_exclude)),
            )),
        )))
    except FileNotFoundError as exc:
        await log('critical', 'File does not exist: %s', exc.filename)
        raise SystemExit()
    else:
        await log('info', 'Files to be tested: %s', len(unique_paths))

    results: Tuple[Vulnerability, ...] = tuple(chain.from_iterable(
        await collect(map(analyze_one_path, unique_paths), workers=64)
    ))

    return results
