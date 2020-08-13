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
    resolve,
)

# Local imports
from lib_path import (
    f009,
    f011,
    f060,
    f061,
    f117,
)
from state.ephemeral import (
    EphemeralStore,
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
    FindingEnum,
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


async def resolve_paths(
    *,
    exclude: Tuple[str, ...],
    include: Tuple[str, ...],
) -> Set[str]:
    """Compute a set of unique paths based on the include/exclude rules.

    Paths will be un-globed, normalized and entered if needed.

    :param exclude: Paths to exclude
    :type exclude: Tuple[str, ...]
    :param include: Paths to include
    :type include: Tuple[str, ...]
    :raises SystemExit: If any critical error occurs
    :return: A set of unique paths
    :rtype: Set[str]
    """

    def normalize(path: str) -> str:
        return normpath(path)

    def evaluate(path: str) -> Iterator[str]:
        if path.startswith('glob(') and path.endswith(')'):
            yield from glob(path[5:-1], recursive=True)
        else:
            yield path

    try:
        unique_paths: Set[str] = set(map(normalize, chain.from_iterable(
            await collect(map(
                recurse, chain.from_iterable(map(evaluate, include)),
            )),
        ))) - set(map(normalize, chain.from_iterable(
            await collect(map(
                recurse, chain.from_iterable(map(evaluate, exclude)),
            )),
        )))
    except FileNotFoundError as exc:
        raise SystemExit(f'File does not exist: {exc.filename}')
    else:
        await log('info', 'Files to be tested: %s', len(unique_paths))

    return unique_paths


async def analyze(
    *,
    paths_to_exclude: Tuple[str, ...],
    paths_to_include: Tuple[str, ...],
    stores: Dict[FindingEnum, EphemeralStore],
) -> Dict[FindingEnum, EphemeralStore]:
    unique_paths: Set[str] = await resolve_paths(
        exclude=paths_to_exclude,
        include=paths_to_include,
    )

    results: Awaitable[Tuple[Vulnerability, ...]]
    for results in resolve(map(analyze_one_path, unique_paths), workers=8):
        for result in await results:
            await stores[result.finding].store(result)

    return stores
