from aioextensions import (
    collect,
    CPU_CORES,
)
from lib_path import (
    f009,
    f011_maven_build_gradle,
    f011_maven_pom_xml,
    f011_npm_package_json,
    f011_npm_package_lock_json,
    f011_npm_yarn_lock,
    f011_nuget_csproj,
    f011_nuget_packages_config,
    f016,
    f022,
    f024_aws,
    f031_aws,
    f052,
    f070,
    f073,
    f079,
    f080,
    f091,
    f099,
    f109,
    f117,
    f200,
    f246,
    f247,
    f250,
    f256,
    f259,
    f281,
    f325,
    f335,
    f372,
    f380,
    f396,
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
DEV: Dict[str, bool] = dict(include_dev=True, include_prod=False)
PROD: Dict[str, bool] = dict(include_dev=False, include_prod=True)

CHECKS: Tuple[Tuple[core_model.FindingEnum, Any], ...] = (
    (core_model.FindingEnum.F009, f009.analyze),
    (core_model.FindingEnum.F011, f011_maven_build_gradle.analyze),
    (core_model.FindingEnum.F011, f011_maven_pom_xml.analyze),
    (core_model.FindingEnum.F011, f011_npm_package_json.analyze(**PROD)),
    (core_model.FindingEnum.F011, f011_npm_package_lock_json.analyze(**PROD)),
    (core_model.FindingEnum.F011, f011_npm_yarn_lock.analyze),
    (core_model.FindingEnum.F011, f011_nuget_csproj.analyze),
    (core_model.FindingEnum.F011, f011_nuget_packages_config.analyze),
    (core_model.FindingEnum.F016, f016.analyze),
    (core_model.FindingEnum.F022, f022.analyze),
    (core_model.FindingEnum.F024, f024_aws.analyze),
    (core_model.FindingEnum.F031, f031_aws.analyze),
    (core_model.FindingEnum.F052, f052.analyze),
    (core_model.FindingEnum.F080, f080.analyze),
    (core_model.FindingEnum.F070, f070.analyze),
    (core_model.FindingEnum.F073, f073.analyze),
    (core_model.FindingEnum.F079, f079.analyze),
    (core_model.FindingEnum.F091, f091.analyze),
    (core_model.FindingEnum.F099, f099.analyze),
    (core_model.FindingEnum.F109, f109.analyze),
    (core_model.FindingEnum.F117, f117.analyze),
    (core_model.FindingEnum.F200, f200.analyze),
    (core_model.FindingEnum.F335, f335.analyze),
    (core_model.FindingEnum.F246, f246.analyze),
    (core_model.FindingEnum.F247, f247.analyze),
    (core_model.FindingEnum.F250, f250.analyze),
    (core_model.FindingEnum.F256, f256.analyze),
    (core_model.FindingEnum.F259, f259.analyze),
    (core_model.FindingEnum.F281, f281.analyze),
    (core_model.FindingEnum.F325, f325.analyze),
    (core_model.FindingEnum.F372, f372.analyze),
    (core_model.FindingEnum.F380, f380.analyze),
    (core_model.FindingEnum.F393, f011_npm_package_json.analyze(**DEV)),
    (core_model.FindingEnum.F393, f011_npm_package_lock_json.analyze(**DEV)),
    (core_model.FindingEnum.F396, f396.analyze),
)


async def analyze_one_path(  # pylint: disable=too-many-locals
    *,
    index: int,
    path: str,
    stores: Dict[core_model.FindingEnum, EphemeralStore],
    unique_nu_paths: Set[str],
    unique_nv_paths: Set[str],
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

        if path in unique_nv_paths:
            if finding is not core_model.FindingEnum.F117:
                continue
        elif path in unique_nu_paths:
            if finding is not core_model.FindingEnum.F079:
                continue
        else:
            if finding in {
                core_model.FindingEnum.F079,
                core_model.FindingEnum.F117,
            }:
                continue

        for vulnerabilities in await analyzer(
            content_generator=file_content_generator,
            file_extension=file_extension,
            file_name=file_name,
            finding=finding,
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

    unique_paths, unique_nu_paths, unique_nv_paths = await resolve_paths(
        exclude=CTX.config.path.exclude,
        include=CTX.config.path.include,
    )
    paths = unique_paths | unique_nu_paths | unique_nv_paths
    unique_paths_count: int = len(paths)

    await collect(
        (
            analyze_one_path(
                index=index,
                path=path,
                stores=stores,
                unique_nu_paths=unique_nu_paths,
                unique_nv_paths=unique_nv_paths,
                unique_paths_count=unique_paths_count,
            )
            for index, path in enumerate(paths, start=1)
        ),
        workers=CPU_CORES,
    )
