from lib_path.common import (
    DependencyType,
    format_pkg_dep,
    pkg_deps_to_vulns,
)
from model.core_model import (
    MethodsEnum,
    Platform,
)
from typing import (
    Iterator,
)
import yaml


# pylint: disable=unused-argument
@pkg_deps_to_vulns(Platform.COMPOSER, MethodsEnum.COMPOSER_JSON)
def pub_pubspec_yaml(  # NOSONAR
    content: str, path: str
) -> Iterator[DependencyType]:
    dict_yaml = yaml.safe_load(content)
    if "dependencies" in dict_yaml:
        for dep, version in dict_yaml["dependencies"].items():
            if dep == "flutter":
                continue
            yield format_pkg_dep(dep, version, 1, 1)

    return iter([({}, {})])
