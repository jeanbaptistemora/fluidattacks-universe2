from lib_path.common import (
    get_vulnerabilities_from_iterator_blocking,
    SHIELD,
)
from model import (
    core_model,
)
from state.cache import (
    CACHE_ETERNALLY,
)
from typing import (
    Awaitable,
    Callable,
    List,
    Set,
    Tuple,
)
from utils.function import (
    TIMEOUT_1MIN,
)
from zone import (
    t,
)

ALLOWED: Set[Tuple[str, str]] = {
    ("gradle-wrapper", "jar"),
}


@CACHE_ETERNALLY
@SHIELD
@TIMEOUT_1MIN
async def unverifiable_files(
    file_name: str,
    file_extension: str,
    path: str,
    raw_content: bytes,
) -> core_model.Vulnerabilities:
    if (file_name, file_extension) in ALLOWED:
        return ()

    return get_vulnerabilities_from_iterator_blocking(
        content=raw_content.decode(encoding="utf-8", errors="replace"),
        cwe={"377"},
        description=t(
            key="src.lib_path.f117.unverifiable_files.description",
            path=path,
        ),
        finding=core_model.FindingEnum.F117,
        iterator=iter([(1, 0)]),
        path=path,
    )


@SHIELD
async def analyze(
    file_name: str,
    file_extension: str,
    path: str,
    raw_content_generator: Callable[[], Awaitable[bytes]],
    **_: None,
) -> List[Awaitable[core_model.Vulnerabilities]]:
    coroutines: List[Awaitable[core_model.Vulnerabilities]] = []

    if (
        file_extension
        in {
            "bin",
            "class",
            "dll",
            "DS_Store",
            "exec",
            "hprof",
            "jar",
            "jasper",
            "pdb",
            "pyc",
        }
        or (file_name, file_extension)
        in {
            ("debug", "log"),
            ("org.eclipse.buildship.core.prefs"),
            (".classpath", ""),
            (".project", ""),
            (".vscode", ""),
        }
        or any(
            string in path
            for string in (
                "/.serverless_plugins/",
                "/.settings/",
            )
        )
    ):
        coroutines.append(
            unverifiable_files(
                file_name=file_name,
                file_extension=file_extension,
                path=path,
                raw_content=await raw_content_generator(),
            )
        )

    return coroutines
