from collections.abc import (
    Iterator,
)
from lib_path.common import (
    DependencyType,
    format_pkg_dep,
    pkg_deps_to_vulns,
)
from model.core_model import (
    MethodsEnum,
    Platform,
)
import re

PUB_DEV_DEP: re.Pattern[str] = re.compile(
    r"^\s{2}(?P<pkg>[^\s]+):\s(?P<version>[^\s]*)$"
)


# pylint: disable=unused-argument
@pkg_deps_to_vulns(Platform.PUB, MethodsEnum.PUB_PUBSPEC_YAML_DEV)
def pub_pubspec_yaml_dev(content: str, path: str) -> Iterator[DependencyType]:
    line_deps: bool = False
    for line_number, line in enumerate(content.splitlines(), 1):
        if line.startswith("dev_dependencies:"):
            line_deps = True
        elif line_deps:
            if matched := PUB_DEV_DEP.match(line):
                pkg_name = matched.group("pkg")
                pkg_version = matched.group("version")
                yield format_pkg_dep(
                    pkg_name, pkg_version, line_number, line_number
                )
            elif not line:
                break
