from aioextensions import (
    in_process,
)
from lib_path.common import (
    DependencyType,
    SHIELD,
    translate_dependencies_to_vulnerabilities,
)
from frozendict import (  # type: ignore
    frozendict,
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
    def resolve_dependencies(obj: frozendict) -> Iterator[DependencyType]:
        for key in obj:
            if key["item"] in ("dependencies", "devDependencies"):
                for product, spec in obj[key].items():
                    for spec_key, spec_val in spec.items():
                        if spec_key["item"] == "version":
                            yield product, spec_val
                            yield from resolve_dependencies(spec)

    return translate_dependencies_to_vulnerabilities(
        content=content,
        dependencies=resolve_dependencies(
            obj=json_loads_blocking(content, default={}),
        ),
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
    if (file_name, file_extension) == ("package-lock", "json"):
        return [
            check(
                content=await content_generator(),
                path=path,
            )
        ]

    return []
