from aioextensions import (
    in_process,
)
from lib_path.common import (
    SHIELD,
)
from lib_path.f393.npm_package_json import (
    npm_package_json,
)
from lib_path.f393.npm_pkg_lock_json import (
    npm_pkg_lock_json,
)
from model.core_model import (
    Vulnerabilities,
)
from typing import (
    Awaitable,
    Callable,
    List,
)


@SHIELD
async def run_npm_package_json(content: str, path: str) -> Vulnerabilities:
    return await in_process(
        npm_package_json,
        content=content,
        path=path,
    )


@SHIELD
async def run_npm_pkg_lock_json(content: str, path: str) -> Vulnerabilities:
    return await in_process(
        npm_pkg_lock_json,
        content=content,
        path=path,
    )


@SHIELD
async def analyze(
    content_generator: Callable[[], str],
    file_name: str,
    file_extension: str,
    path: str,
    **_: None,
) -> List[Awaitable[Vulnerabilities]]:

    if (file_name, file_extension) == ("package", "json"):
        return [run_npm_package_json(content_generator(), path)]

    if (file_name, file_extension) == ("package-lock", "json"):
        return [run_npm_pkg_lock_json(content_generator(), path)]

    return []
