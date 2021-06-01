from aioextensions import (
    collect,
    CPU_CORES,
)
from lib_path import (
    f001_jpa,
    f009,
    f011,
    f022,
    f024_aws,
    f031_aws,
    f031_cwe378,
    f052,
    f055_aws_missing_encryption,
    f060,
    f061,
    f073,
    f085,
    f117,
)
from model import (
    core_model,
)
from os.path import (
    split,
    splitext,
)
from state.ephemeral import (
    EphemeralStore,
)
from typing import (
    Any,
    Dict,
    Set,
    Tuple,
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

# Constants
MEBIBYTE: int = 1048576
MAX_READ: int = 64 * MEBIBYTE

CHECKS: Tuple[Tuple[core_model.FindingEnum, Any], ...] = (
    (core_model.FindingEnum.F001_JPA, f001_jpa.analyze),
    (core_model.FindingEnum.F009, f009.analyze),
    (core_model.FindingEnum.F011, f011.analyze),
    (core_model.FindingEnum.F022, f022.analyze),
    (core_model.FindingEnum.F024_AWS, f024_aws.analyze),
    (core_model.FindingEnum.F031_AWS, f031_aws.analyze),
    (core_model.FindingEnum.F031_CWE378, f031_cwe378.analyze),
    (core_model.FindingEnum.F052, f052.analyze),
    (
        core_model.FindingEnum.F055_AWS_MISSING_ENCRYPTION,
        f055_aws_missing_encryption.analyze,
    ),
    (core_model.FindingEnum.F060, f060.analyze),
    (core_model.FindingEnum.F061, f061.analyze),
    (core_model.FindingEnum.F073, f073.analyze),
    (core_model.FindingEnum.F085, f085.analyze),
    (core_model.FindingEnum.F117, f117.analyze),
)


async def analyze_one_path(
    *,
    index: int,
    path: str,
    stores: Dict[core_model.FindingEnum, EphemeralStore],
    unique_paths_count: int,
) -> None:
    """Execute all findings against the provided file.

    :param path: Path to the file who's object of analysis
    :type path: str
    """
    await log(
        "info",
        "Analyzing path %s of %s: %s",
        index,
        unique_paths_count,
        path,
    )

    file_content_generator = generate_file_content(path, size=MAX_READ)
    file_raw_content_generator = generate_file_raw_content(path, size=MAX_READ)

    _, file = split(path)
    file_name, file_extension = splitext(file)
    file_extension = file_extension[1:]

    for finding, analyzer in CHECKS:
        if finding not in CTX.config.checks:
            continue

        for vulnerabilities in await analyzer(
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
    stores: Dict[core_model.FindingEnum, EphemeralStore],
) -> None:
    if not any(finding in CTX.config.checks for finding, _ in CHECKS):
        # No findings will be executed, early abort
        return

    unique_paths: Set[str] = await resolve_paths(
        exclude=CTX.config.path.exclude,
        include=CTX.config.path.include,
    )
    unique_paths_count: int = len(unique_paths)

    await collect(
        (
            analyze_one_path(
                index=index,
                path=path,
                stores=stores,
                unique_paths_count=unique_paths_count,
            )
            for index, path in enumerate(unique_paths)
        ),
        workers=CPU_CORES,
    )
