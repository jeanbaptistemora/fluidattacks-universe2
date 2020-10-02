# Standard library
from glob import (
    iglob as glob,
)
from os.path import (
    normpath,
    split,
    splitext,
)
from itertools import (
    chain,
)
from typing import (
    Dict,
    Iterator,
    Set,
    Tuple,
)

# Third party libraries
from aioextensions import (
    CPU_CORES,
    collect,
)

# Local imports
from lib_path import (
    f001_jpa,
    f009,
    f011,
    f022,
    f031_aws,
    f031_cwe378,
    f052,
    f060,
    f061,
    f073,
    f085,
    f117,
)
from state.ephemeral import (
    EphemeralStore,
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
)

# Constants
MEBIBYTE: int = 1048576
MAX_READ: int = 64 * MEBIBYTE


async def analyze_one_path(
    path: str,
    stores: Dict[FindingEnum, EphemeralStore],
) -> None:
    """Execute all findings against the provided file.

    :param path: Path to the file who's object of analysis
    :type path: str
    """
    file_content_generator = generate_file_content(path, size=MAX_READ)
    file_raw_content_generator = generate_file_raw_content(path, size=MAX_READ)

    _, file = split(path)
    file_name, file_extension = splitext(file)
    file_extension = file_extension[1:]

    await collect((
        f001_jpa.analyze(
            content_generator=file_content_generator,
            file_extension=file_extension,
            path=path,
            store=stores[FindingEnum.F001_JPA],
        ),
        f009.analyze(
            content_generator=file_content_generator,
            file_extension=file_extension,
            file_name=file_name,
            path=path,
            store=stores[FindingEnum.F009],
        ),
        f011.analyze(
            content_generator=file_content_generator,
            file_extension=file_extension,
            file_name=file_name,
            path=path,
            store=stores[FindingEnum.F011],
        ),
        f022.analyze(
            content_generator=file_content_generator,
            file_extension=file_extension,
            path=path,
            store=stores[FindingEnum.F022],
        ),
        f031_aws.analyze(
            content_generator=file_content_generator,
            file_extension=file_extension,
            path=path,
            store=stores[FindingEnum.F031_AWS],
        ),
        f031_cwe378.analyze(
            content_generator=file_content_generator,
            file_extension=file_extension,
            path=path,
            store=stores[FindingEnum.F031_CWE378],
        ),
        f052.analyze(
            content_generator=file_content_generator,
            file_extension=file_extension,
            path=path,
            store=stores[FindingEnum.F052],
        ),
        f060.analyze(
            content_generator=file_content_generator,
            file_extension=file_extension,
            path=path,
            store=stores[FindingEnum.F060],
        ),
        f061.analyze(
            content_generator=file_content_generator,
            file_extension=file_extension,
            path=path,
            store=stores[FindingEnum.F061],
        ),
        f073.analyze(
            content_generator=file_content_generator,
            file_extension=file_extension,
            path=path,
            store=stores[FindingEnum.F073],
        ),
        f085.analyze(
            content_generator=file_content_generator,
            file_extension=file_extension,
            path=path,
            store=stores[FindingEnum.F085],
        ),
        f117.analyze(
            file_name=file_name,
            file_extension=file_extension,
            path=path,
            raw_content_generator=file_raw_content_generator,
            store=stores[FindingEnum.F117],
        ),
    ))


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
) -> None:
    unique_paths: Set[str] = await resolve_paths(
        exclude=paths_to_exclude,
        include=paths_to_include,
    )

    await collect(
        (analyze_one_path(path, stores) for path in unique_paths),
        workers=CPU_CORES,
    )
