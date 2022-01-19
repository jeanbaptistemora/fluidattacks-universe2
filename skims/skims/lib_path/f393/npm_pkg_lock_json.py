from frozendict import (  # type: ignore
    frozendict,
)
from lib_path.common import (
    DependencyType,
    translate_dependencies_to_vulnerabilities,
)
from model.core_model import (
    FindingEnum,
    Platform,
    Vulnerabilities,
)
from parse_json import (
    loads_blocking as json_loads_blocking,
)
from typing import (
    Iterator,
)


def npm_pkg_lock_json(content: str, path: str) -> Vulnerabilities:
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
                            # if they are from the dev env
                            # they should be included there
                            direct_deps and is_dev,
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
        finding=FindingEnum.F393,
        path=path,
        platform=Platform.NPM,
    )
