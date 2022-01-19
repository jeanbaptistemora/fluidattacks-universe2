from aioextensions import (
    in_process,
)
from lib_path.common import (
    DependencyType,
    SHIELD,
    translate_dependencies_to_vulnerabilities,
)
from model import (
    core_model,
)
from parse_json import (
    loads_blocking as json_loads_blocking,
)
from typing import (
    Any,
    Awaitable,
    Callable,
    Iterator,
    List,
    Set,
)


def _check_npm_package_json(  # pylint: disable=too-many-arguments
    content: str,
    finding: core_model.FindingEnum,
    include_dev: bool,
    include_prod: bool,
    path: str,
    platform: core_model.Platform,
) -> core_model.Vulnerabilities:
    content_json = json_loads_blocking(content, default={})

    keys: Set[str] = set()
    if include_dev:
        keys.add("devDependencies")
    if include_prod:
        keys.add("dependencies")

    dependencies: Iterator[DependencyType] = (
        (product, version)
        for key in content_json
        if key["item"] in keys
        for product, version in content_json[key].items()
    )

    return translate_dependencies_to_vulnerabilities(
        content=content,
        dependencies=dependencies,
        finding=finding,
        path=path,
        platform=platform,
    )


@SHIELD
async def check(
    content: str,
    finding: core_model.FindingEnum,
    include_dev: bool,
    include_prod: bool,
    path: str,
) -> core_model.Vulnerabilities:
    return await in_process(
        _check_npm_package_json,
        content=content,
        finding=finding,
        include_dev=include_dev,
        include_prod=include_prod,
        path=path,
        platform=core_model.Platform.NPM,
    )


def analyze(include_dev: bool, include_prod: bool) -> Any:
    @SHIELD
    async def _analyze(
        content_generator: Callable[[], str],
        finding: core_model.FindingEnum,
        file_name: str,
        file_extension: str,
        path: str,
        **_: None,
    ) -> List[Awaitable[core_model.Vulnerabilities]]:
        if (file_name, file_extension) == ("package", "json"):
            return [
                check(
                    content=content_generator(),
                    finding=finding,
                    include_dev=include_dev,
                    include_prod=include_prod,
                    path=path,
                )
            ]

        return []

    return _analyze
