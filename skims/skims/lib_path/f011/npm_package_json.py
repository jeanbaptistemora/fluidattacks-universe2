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


def npm_package_json(
    content: str, finding: FindingEnum, path: str, platform: Platform
) -> Vulnerabilities:

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
        finding=finding,
        path=path,
        platform=platform,
    )
