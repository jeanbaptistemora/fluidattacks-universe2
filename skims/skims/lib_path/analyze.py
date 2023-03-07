from collections.abc import (
    Set,
)
from concurrent.futures.process import (
    ProcessPoolExecutor,
)
from ctx import (
    CTX,
)
from functools import (
    partial,
)
from lib_path import (
    f009,
    f011,
    f015,
    f022,
    f024,
    f031,
    f037,
    f044,
    f052,
    f055,
    f058,
    f060,
    f065,
    f075,
    f079,
    f086,
    f097,
    f099,
    f117,
    f120,
    f134,
    f135,
    f149,
    f152,
    f153,
    f165,
    f176,
    f183,
    f239,
    f258,
    f259,
    f266,
    f267,
    f281,
    f325,
    f332,
    f333,
    f346,
    f363,
    f371,
    f372,
    f380,
    f393,
    f394,
    f396,
    f400,
    f403,
    f405,
    f406,
    f407,
    f418,
    f426,
    f427,
)
from lib_sast.types import (
    Paths,
)
from model import (
    core_model,
)
import os
from os.path import (
    split,
    splitext,
)
import reactivex
from reactivex import (
    operators as ops,
)
from state.ephemeral import (
    EphemeralStore,
)
from typing import (
    Any,
)
from utils.fs import (
    generate_file_raw_content_blocking,
    get_file_content_block,
)
from utils.logs import (
    log_blocking,
    log_exception_blocking,
)

# Constants
MEBIBYTE: int = 1048576
MAX_READ: int = 64 * MEBIBYTE

CHECKS: tuple[tuple[core_model.FindingEnum, Any], ...] = (
    (core_model.FindingEnum.F009, f009.analyze),
    (core_model.FindingEnum.F011, f011.analyze),
    (core_model.FindingEnum.F015, f015.analyze),
    (core_model.FindingEnum.F022, f022.analyze),
    (core_model.FindingEnum.F024, f024.analyze),
    (core_model.FindingEnum.F031, f031.analyze),
    (core_model.FindingEnum.F037, f037.analyze),
    (core_model.FindingEnum.F044, f044.analyze),
    (core_model.FindingEnum.F052, f052.analyze),
    (core_model.FindingEnum.F055, f055.analyze),
    (core_model.FindingEnum.F058, f058.analyze),
    (core_model.FindingEnum.F060, f060.analyze),
    (core_model.FindingEnum.F065, f065.analyze),
    (core_model.FindingEnum.F075, f075.analyze),
    (core_model.FindingEnum.F079, f079.analyze),
    (core_model.FindingEnum.F086, f086.analyze),
    (core_model.FindingEnum.F097, f097.analyze),
    (core_model.FindingEnum.F099, f099.analyze),
    (core_model.FindingEnum.F117, f117.analyze),
    (core_model.FindingEnum.F120, f120.analyze),
    (core_model.FindingEnum.F134, f134.analyze),
    (core_model.FindingEnum.F135, f135.analyze),
    (core_model.FindingEnum.F149, f149.analyze),
    (core_model.FindingEnum.F152, f152.analyze),
    (core_model.FindingEnum.F153, f153.analyze),
    (core_model.FindingEnum.F165, f165.analyze),
    (core_model.FindingEnum.F176, f176.analyze),
    (core_model.FindingEnum.F183, f183.analyze),
    (core_model.FindingEnum.F239, f239.analyze),
    (core_model.FindingEnum.F258, f258.analyze),
    (core_model.FindingEnum.F259, f259.analyze),
    (core_model.FindingEnum.F266, f266.analyze),
    (core_model.FindingEnum.F267, f267.analyze),
    (core_model.FindingEnum.F281, f281.analyze),
    (core_model.FindingEnum.F325, f325.analyze),
    (core_model.FindingEnum.F332, f332.analyze),
    (core_model.FindingEnum.F333, f333.analyze),
    (core_model.FindingEnum.F346, f346.analyze),
    (core_model.FindingEnum.F363, f363.analyze),
    (core_model.FindingEnum.F371, f371.analyze),
    (core_model.FindingEnum.F372, f372.analyze),
    (core_model.FindingEnum.F380, f380.analyze),
    (core_model.FindingEnum.F393, f393.analyze),
    (core_model.FindingEnum.F394, f394.analyze),
    (core_model.FindingEnum.F396, f396.analyze),
    (core_model.FindingEnum.F400, f400.analyze),
    (core_model.FindingEnum.F403, f403.analyze),
    (core_model.FindingEnum.F405, f405.analyze),
    (core_model.FindingEnum.F406, f406.analyze),
    (core_model.FindingEnum.F407, f407.analyze),
    (core_model.FindingEnum.F418, f418.analyze),
    (core_model.FindingEnum.F426, f426.analyze),
    (core_model.FindingEnum.F427, f427.analyze),
)


def analyze_one_path(  # noqa: MC0001
    *,
    index: int,
    path: str,
    unique_nu_paths: Set[str],
    unique_nv_paths: Set[str],
    unique_paths_count: int,
    file_content: str,
) -> dict[core_model.FindingEnum, list[core_model.Vulnerabilities]]:
    """Execute all findings against the provided file.

    :param path: Path to the file who's object of analysis
    :type path: str
    """
    log_blocking(
        "info",
        "Analyzing path %s of %s: %s",
        index,
        unique_paths_count,
        path,
    )

    def file_content_generator() -> str:
        return file_content

    file_raw_content_generator = generate_file_raw_content_blocking(
        path, size=MAX_READ
    )

    _, file_info = split(path)
    file_name, file_extension = splitext(file_info)
    file_extension = file_extension[1:]

    result: dict[core_model.FindingEnum, list[core_model.Vulnerabilities]] = {}

    for finding, analyzer in CHECKS:
        if finding not in CTX.config.checks:
            continue

        if path in unique_nv_paths:
            if finding is not core_model.FindingEnum.F117:
                continue
        else:
            if finding in {
                core_model.FindingEnum.F117,
            }:
                continue

        result[finding] = analyzer(
            content_generator=file_content_generator,
            file_extension=file_extension,
            file_name=file_name,
            finding=finding,
            path=path,
            raw_content_generator=file_raw_content_generator,
            unique_nu_paths=unique_nu_paths,
        )

    return result


def _analyze_one_path(  # noqa: MC0001
    *,
    index: int,
    path: str,
    unique_nu_paths: Set[str],
    unique_nv_paths: Set[str],
    unique_paths_count: int,
) -> dict[core_model.FindingEnum, list[core_model.Vulnerabilities]]:
    content = get_file_content_block(path)
    return analyze_one_path(
        index=index,
        path=path,
        file_content=content,
        unique_nu_paths=unique_nu_paths,
        unique_nv_paths=unique_nv_paths,
        unique_paths_count=unique_paths_count,
    )


def _handle_result(
    stores: dict[core_model.FindingEnum, EphemeralStore],
    result: tuple[core_model.FindingEnum, EphemeralStore],
) -> None:
    stores[result[0]].store(result[1])


def _handle_exception(
    exception: Exception, _observable: reactivex.Observable
) -> reactivex.Observable:
    log_exception_blocking("error", exception)
    return reactivex.of(None)


def analyze(
    *,
    paths: Paths,
    stores: dict[core_model.FindingEnum, EphemeralStore],
) -> None:
    if not any(finding in CTX.config.checks for finding, _ in CHECKS):
        # No findings will be executed, early abort
        return

    all_paths = paths.get_all()
    unique_paths_count: int = len(all_paths)

    with ProcessPoolExecutor(max_workers=os.cpu_count()) as executor:
        reactivex.of(*all_paths).pipe(
            ops.flat_map_indexed(
                lambda path, index: reactivex.from_future(  # type: ignore
                    executor.submit(  # type: ignore
                        _analyze_one_path,
                        index=index,
                        path=path,
                        unique_nu_paths=set(paths.nu_paths),
                        unique_nv_paths=set(paths.nv_paths),
                        unique_paths_count=unique_paths_count,
                    )
                ).pipe(ops.catch(_handle_exception))
            ),
            ops.filter(lambda x: x is not None),  # type: ignore
            ops.flat_map(
                lambda res: reactivex.of(  # type: ignore
                    *[
                        (finding, vuln)
                        for finding, vulns_list in res.items()  # type: ignore
                        for vulns in vulns_list
                        for vuln in vulns
                    ]
                )
            ),
        ).subscribe(
            on_next=partial(_handle_result, stores),
            on_error=lambda e: log_blocking("exception", e),  # type: ignore
        )
