from aioextensions import (
    in_process,
)
from frozendict import (  # type: ignore
    frozendict,
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
)


def _check(
    content: str,
    include_dev: bool,
    include_prod: bool,
    path: str,
    platform: core_model.Platform,
) -> core_model.Vulnerabilities:
    def resolve_dependencies(
        obj: frozendict, direct_deps: bool = True
    ) -> Iterator[DependencyType]:
        for key in obj:
            if key["item"] == "dependencies":
                for product, spec in obj[key].items():
                    is_dev: bool = False
                    for spec_key, spec_val in spec.items():
                        if spec_key["item"] == "dev":
                            is_dev = spec_val["item"]
                            break

                    should_include: bool = any(
                        [
                            # Analyze my direct dependencies
                            # if they are from the env I want to check deps for
                            # and they should be included in this environment
                            direct_deps
                            and any(
                                [
                                    include_dev and is_dev,
                                    include_prod and not is_dev,
                                ]
                            ),
                            # Only the prod deps of my deps affect me,
                            # because the dev deps of my deps are not installed
                            not direct_deps and not is_dev,
                        ]
                    )

                    if not should_include:
                        continue

                    for spec_key, spec_val in spec.items():
                        if spec_key["item"] == "version":
                            yield product, spec_val

                    # From this point on, we check the deps of my deps
                    yield from resolve_dependencies(spec, direct_deps=False)

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
        if (file_name, file_extension) == ("package-lock", "json"):
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
