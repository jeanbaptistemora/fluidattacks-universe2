from collections.abc import (
    Iterable,
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

GO_DIRECTIVE: re.Pattern[str] = re.compile(
    r"(?P<directive>require|replace) \("
)
GO_MOD_DEP: re.Pattern[str] = re.compile(
    r"^\s+(?P<product>.+?/[\w\-\.~]+?)(/v\d+)?\sv(?P<version>\S+)"
)
GO_REPLACE: re.Pattern[str] = re.compile(
    r"^\s+(?P<old_prod>.+?/[\w\-\.~]+?)(/v\d+)?(\sv(?P<old_ver>\S+))?\s=>"
    r"\s(?P<new_prod>.+?/[\w\-\.~]+?)(/v\d+)?(\sv(?P<new_ver>\S+))?$"
)
GO_REP_DEP: re.Pattern[str] = re.compile(
    r"replace\s(?P<old_prod>.+?/[\w\-\.~]+?)(/v\d+)?(\sv(?P<old_ver>\S+))?\s=>"
    r"\s(?P<new_prod>.+?/[\w\-\.~]+?)(/v\d+)?(\sv(?P<new_ver>\S+))?$"
)
GO_REQ_MOD_DEP: re.Pattern[str] = re.compile(
    r"require\s(?P<product>.+?/[\w\-\.~]+?)(/v\d+)?\sv(?P<version>\S+)"
)
GO_VERSION: re.Pattern[str] = re.compile(
    r"\ngo (?P<major>\d)\.(?P<minor>\d+)(\.\d+)?\n"
)


def add_require(
    matched: re.Match[str],
    req_dict: dict[str, DependencyType],
    line_number: int,
) -> None:
    product = matched.group("product")
    version = matched.group("version")
    req_dict[product] = format_pkg_dep(
        product, version, line_number, line_number
    )


def replace_req(
    req_dict: dict[str, DependencyType],
    replace_list: Iterable[tuple[re.Match[str], int]],
) -> Iterator[DependencyType]:
    for matched, line_number in replace_list:
        old_pkg = matched.group("old_prod")
        old_version = matched.group("old_ver")
        repl_pkg = matched.group("new_prod")
        version = matched.group("new_ver")
        if old_pkg in req_dict:
            if old_version and req_dict[old_pkg][1]["item"] != old_version:
                continue
            req_dict[old_pkg] = format_pkg_dep(
                repl_pkg, version, line_number, line_number
            )
    return iter(req_dict.values())


def resolve_go_deps(content: str) -> Iterator[DependencyType]:
    go_req_directive: str = ""
    replace_list: list[tuple[re.Match[str], int]] = []
    req_dict: dict[str, DependencyType] = {}
    for line_number, line in enumerate(content.splitlines(), 1):
        if matched := GO_REQ_MOD_DEP.search(line):
            add_require(matched, req_dict, line_number)
        elif replace := GO_REP_DEP.search(line):
            replace_list.append((replace, line_number))
        elif not go_req_directive:
            if directive := GO_DIRECTIVE.match(line):
                go_req_directive = directive.group("directive")
        elif go_req_directive == "replace":
            if replace := GO_REPLACE.search(line):
                replace_list.append((replace, line_number))
                continue
            go_req_directive = ""
        elif matched := GO_MOD_DEP.search(line):
            add_require(matched, req_dict, line_number)
        else:
            go_req_directive = ""
    return replace_req(req_dict, replace_list)


# pylint: disable=unused-argument
@pkg_deps_to_vulns(Platform.GO, MethodsEnum.GO_MOD)
def go_mod(content: str, path: str) -> Iterator[DependencyType]:
    go_version = GO_VERSION.search(content)
    if not go_version:
        return iter([({}, {})])
    major = int(go_version.group("major"))
    minor = int(go_version.group("minor"))
    if major >= 2 or (major == 1 and minor >= 17):
        return resolve_go_deps(content)
    return iter([({}, {})])
