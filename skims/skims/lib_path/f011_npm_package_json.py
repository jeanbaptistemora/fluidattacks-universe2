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
    Awaitable,
    Callable,
    Iterator,
    List,
)


def _check(
    content: str,
    path: str,
    platform: core_model.Platform,
) -> core_model.Vulnerabilities:
    content_json = json_loads_blocking(content, default={})

    dependencies: Iterator[DependencyType] = (
        (product, version)
        for key in content_json
        if key["item"] == "dependencies"
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
    path: str,
) -> core_model.Vulnerabilities:
    return await in_process(
        _check,
        content=content,
        path=path,
        platform=core_model.Platform.NPM,
    )


@SHIELD
async def analyze(
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
                path=path,
            )
        ]

    return []
