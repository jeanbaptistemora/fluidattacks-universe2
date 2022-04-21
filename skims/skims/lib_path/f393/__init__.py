from lib_path.common import (
    SHIELD_BLOCKING,
)
from lib_path.f393.npm import (
    npm_package_json,
    npm_pkg_lock_json,
    npm_yarn_lock_dev,
)
from model.core_model import (
    Vulnerabilities,
)
from typing import (
    Callable,
    Tuple,
)


@SHIELD_BLOCKING
def run_npm_package_json(content: str, path: str) -> Vulnerabilities:
    return npm_package_json(content=content, path=path)


@SHIELD_BLOCKING
def run_npm_pkg_lock_json(content: str, path: str) -> Vulnerabilities:
    return npm_pkg_lock_json(content=content, path=path)


@SHIELD_BLOCKING
def run_npm_yarn_lock_dev(content: str, path: str) -> Vulnerabilities:
    return npm_yarn_lock_dev(content=content, path=path)


@SHIELD_BLOCKING
def analyze(
    content_generator: Callable[[], str],
    file_name: str,
    file_extension: str,
    path: str,
    **_: None,
) -> Tuple[Vulnerabilities, ...]:

    if (file_name, file_extension) == ("package", "json"):
        return (run_npm_package_json(content_generator(), path),)

    if (file_name, file_extension) == ("yarn", "lock"):
        return (run_npm_yarn_lock_dev(content_generator(), path),)

    if (file_name, file_extension) == ("package-lock", "json"):
        return (run_npm_pkg_lock_json(content_generator(), path),)

    return ()
