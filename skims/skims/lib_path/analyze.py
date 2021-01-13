# Standard library
from os.path import (
    split,
    splitext,
)
from typing import (
    Dict,
    Set,
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
    f034,
    f037,
    f047_aws,
    f052,
    f055_aws,
    f060,
    f061,
    f063_path_traversal,
    f073,
    f085,
    f117,
)
from state.ephemeral import (
    EphemeralStore,
)
from utils.ctx import (
    CTX,
)
from utils.fs import (
    generate_file_content,
    generate_file_raw_content,
    resolve_paths,
)
from utils.logs import (
    log,
)
from model.core_model import (
    FindingEnum,
)

# Constants
MEBIBYTE: int = 1048576
MAX_READ: int = 64 * MEBIBYTE


async def analyze_one_path(
    *,
    index: int,
    path: str,
    stores: Dict[FindingEnum, EphemeralStore],
    unique_paths_count: int,
) -> None:
    """Execute all findings against the provided file.

    :param path: Path to the file who's object of analysis
    :type path: str
    """
    await log(
        'info',
        'Analyzing path %s of %s: %s',
        index,
        unique_paths_count,
        path,
    )

    file_content_generator = generate_file_content(path, size=MAX_READ)
    file_raw_content_generator = generate_file_raw_content(path, size=MAX_READ)

    _, file = split(path)
    file_name, file_extension = splitext(file)
    file_extension = file_extension[1:]

    for finding, analyzer in (
        (FindingEnum.F001_JPA, f001_jpa.analyze),
        (FindingEnum.F009, f009.analyze),
        (FindingEnum.F011, f011.analyze),
        (FindingEnum.F022, f022.analyze),
        (FindingEnum.F031_AWS, f031_aws.analyze),
        (FindingEnum.F031_CWE378, f031_cwe378.analyze),
        (FindingEnum.F034, f034.analyze),
        (FindingEnum.F037, f037.analyze),
        (FindingEnum.F047_AWS, f047_aws.analyze),
        (FindingEnum.F052, f052.analyze),
        (FindingEnum.F055_AWS, f055_aws.analyze),
        (FindingEnum.F060, f060.analyze),
        (FindingEnum.F061, f061.analyze),
        (FindingEnum.F063_PATH_TRAVERSAL, f063_path_traversal.analyze),
        (FindingEnum.F073, f073.analyze),
        (FindingEnum.F085, f085.analyze),
        (FindingEnum.F117, f117.analyze),
    ):
        for vulnerabilities in await analyzer(  # type: ignore
            content_generator=file_content_generator,
            file_extension=file_extension,
            file_name=file_name,
            path=path,
            raw_content_generator=file_raw_content_generator,
        ):
            for vulnerability in await vulnerabilities:
                await stores[finding].store(vulnerability)


async def analyze(
    *,
    stores: Dict[FindingEnum, EphemeralStore],
) -> None:
    unique_paths: Set[str] = await resolve_paths(
        exclude=CTX.config.path.exclude,
        include=CTX.config.path.include,
    )
    unique_paths_count: int = len(unique_paths)

    await collect((
        analyze_one_path(
            index=index,
            path=path,
            stores=stores,
            unique_paths_count=unique_paths_count,
        )
        for index, path in enumerate(unique_paths)
    ), workers=CPU_CORES)
