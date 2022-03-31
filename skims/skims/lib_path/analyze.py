from concurrent.futures.process import (
    ProcessPoolExecutor,
)
from concurrent.futures.thread import (
    ThreadPoolExecutor,
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
    f016,
    f022,
    f024,
    f031,
    f052,
    f055,
    f056,
    f058,
    f070,
    f073,
    f075,
    f079,
    f099,
    f101,
    f109,
    f117,
    f157,
    f177,
    f203,
    f246,
    f247,
    f250,
    f256,
    f257,
    f258,
    f259,
    f266,
    f267,
    f281,
    f300,
    f325,
    f333,
    f335,
    f346,
    f363,
    f372,
    f380,
    f393,
    f394,
    f396,
    f400,
    f401,
    f402,
    f406,
    f407,
    f408,
    f409,
    f411,
)
from lib_sast.types import (
    Paths,
)
from model import (
    core_model,
)
import os
from os import (
    cpu_count,
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
    List,
    Set,
    Tuple,
)
from utils.fs import (
    generate_file_raw_content_blocking,
    get_file_content_block,
)
from utils.logs import (
    log_blocking,
)

# Constants
MEBIBYTE: int = 1048576
MAX_READ: int = 64 * MEBIBYTE

CHECKS: Tuple[Tuple[core_model.FindingEnum, Any], ...] = (
    (core_model.FindingEnum.F009, f009.analyze),
    (core_model.FindingEnum.F011, f011.analyze),
    (core_model.FindingEnum.F015, f015.analyze),
    (core_model.FindingEnum.F016, f016.analyze),
    (core_model.FindingEnum.F022, f022.analyze),
    (core_model.FindingEnum.F024, f024.analyze),
    (core_model.FindingEnum.F031, f031.analyze),
    (core_model.FindingEnum.F052, f052.analyze),
    (core_model.FindingEnum.F055, f055.analyze),
    (core_model.FindingEnum.F056, f056.analyze),
    (core_model.FindingEnum.F058, f058.analyze),
    (core_model.FindingEnum.F070, f070.analyze),
    (core_model.FindingEnum.F073, f073.analyze),
    (core_model.FindingEnum.F075, f075.analyze),
    (core_model.FindingEnum.F079, f079.analyze),
    (core_model.FindingEnum.F099, f099.analyze),
    (core_model.FindingEnum.F101, f101.analyze),
    (core_model.FindingEnum.F109, f109.analyze),
    (core_model.FindingEnum.F117, f117.analyze),
    (core_model.FindingEnum.F157, f157.analyze),
    (core_model.FindingEnum.F177, f177.analyze),
    (core_model.FindingEnum.F203, f203.analyze),
    (core_model.FindingEnum.F246, f246.analyze),
    (core_model.FindingEnum.F247, f247.analyze),
    (core_model.FindingEnum.F250, f250.analyze),
    (core_model.FindingEnum.F256, f256.analyze),
    (core_model.FindingEnum.F257, f257.analyze),
    (core_model.FindingEnum.F258, f258.analyze),
    (core_model.FindingEnum.F259, f259.analyze),
    (core_model.FindingEnum.F266, f266.analyze),
    (core_model.FindingEnum.F267, f267.analyze),
    (core_model.FindingEnum.F281, f281.analyze),
    (core_model.FindingEnum.F300, f300.analyze),
    (core_model.FindingEnum.F325, f325.analyze),
    (core_model.FindingEnum.F333, f333.analyze),
    (core_model.FindingEnum.F335, f335.analyze),
    (core_model.FindingEnum.F346, f346.analyze),
    (core_model.FindingEnum.F363, f363.analyze),
    (core_model.FindingEnum.F372, f372.analyze),
    (core_model.FindingEnum.F380, f380.analyze),
    (core_model.FindingEnum.F393, f393.analyze),
    (core_model.FindingEnum.F394, f394.analyze),
    (core_model.FindingEnum.F396, f396.analyze),
    (core_model.FindingEnum.F400, f400.analyze),
    (core_model.FindingEnum.F401, f401.analyze),
    (core_model.FindingEnum.F402, f402.analyze),
    (core_model.FindingEnum.F406, f406.analyze),
    (core_model.FindingEnum.F407, f407.analyze),
    (core_model.FindingEnum.F408, f408.analyze),
    (core_model.FindingEnum.F409, f409.analyze),
    (core_model.FindingEnum.F411, f411.analyze),
)


def analyze_one_path(  # noqa: MC0001
    *,
    index: int,
    path: str,
    unique_nu_paths: Set[str],
    unique_nv_paths: Set[str],
    unique_paths_count: int,
    file_content: str,
) -> Dict[core_model.FindingEnum, List[core_model.Vulnerabilities]]:
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

    file_content_generator = lambda: file_content  # noqa
    file_raw_content_generator = generate_file_raw_content_blocking(
        path, size=MAX_READ
    )

    _, file = split(path)
    file_name, file_extension = splitext(file)
    file_extension = file_extension[1:]

    result: Dict[core_model.FindingEnum, List[core_model.Vulnerabilities]] = {}

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

        result[finding] = analyzer(
            content_generator=file_content_generator,
            file_extension=file_extension,
            file_name=file_name,
            finding=finding,
            path=path,
            raw_content_generator=file_raw_content_generator,
        )

    return result


def _execute_partial_analyze_one_path(
    fun: partial,
) -> Dict[core_model.FindingEnum, List[core_model.Vulnerabilities]]:
    return fun()


def analyze(
    *,
    paths: Paths,
    stores: Dict[core_model.FindingEnum, EphemeralStore],
) -> None:
    if not any(finding in CTX.config.checks for finding, _ in CHECKS):
        # No findings will be executed, early abort
        return

    all_paths = paths.get_all()
    unique_paths_count: int = len(all_paths)

    with ThreadPoolExecutor(max_workers=cpu_count()) as worker:
        contents = list(
            worker.map(lambda x: (x, get_file_content_block(x)), all_paths)
        )

    with ProcessPoolExecutor(max_workers=os.cpu_count()) as executor:

        result: Tuple[
            Dict[core_model.FindingEnum, List[core_model.Vulnerabilities]], ...
        ] = tuple(
            executor.map(
                _execute_partial_analyze_one_path,
                [
                    partial(
                        analyze_one_path,
                        index=index,
                        path=path,
                        file_content=content,
                        unique_nu_paths=paths.nu_paths,
                        unique_nv_paths=paths.nv_paths,
                        unique_paths_count=unique_paths_count,
                    )
                    for index, (path, content) in enumerate(contents, start=1)
                ],
            )
        )
    with ThreadPoolExecutor(max_workers=cpu_count()) as worker:
        for finding, vuln in (
            (finding, vuln)
            for vulns_result in result
            for finding, vulns_list in vulns_result.items()
            for vulns in vulns_list
            for vuln in vulns
        ):
            worker.submit(stores[finding].store, vuln)
