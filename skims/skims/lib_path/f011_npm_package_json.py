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


def _check(
    content: str,
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
        path=path,
        platform=platform,
    )


@SHIELD
async def check(
    content: str,
    include_dev: bool,
    include_prod: bool,
    path: str,
) -> core_model.Vulnerabilities:
    return await in_process(
        _check,
        content=content,
        include_dev=include_dev,
        include_prod=include_prod,
        path=path,
        platform=core_model.Platform.NPM,
    )


def analyze(include_dev: bool, include_prod: bool) -> Any:
    @SHIELD
    async def _analyze(
        content_generator: Callable[[], Awaitable[str]],
        file_name: str,
        file_extension: str,
        path: str,
        **_: None,
    ) -> List[Awaitable[core_model.Vulnerabilities]]:
        if (file_name, file_extension) == ("package", "json"):
            return [
                check(
                    content=await content_generator(),
                    include_dev=include_dev,
                    include_prod=include_prod,
                    path=path,
                )
            ]

        return []

    return _analyze
