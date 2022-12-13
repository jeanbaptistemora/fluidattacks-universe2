from lib_path.common import (
    DependencyType,
    format_pkg_dep,
)
from lib_path.f011.gem import (
    gem_gemfile,
    gem_gemfile_lock,
)
from lib_path.f011.go import (
    add_require,
    go_mod,
    GO_REQ_MOD_DEP,
)
from lib_path.f011.maven import (
    maven_pom_xml,
)
from lib_path.f011.pip import (
    pip_requirements_txt,
)
from lib_path.f393.gem import (
    gem_gemfile_dev,
)
from lib_path.f393.npm import (
    npm_yarn_lock_dev,
)
from operator import (
    itemgetter,
)
import pytest
import re
from typing import (
    Dict,
    Iterator,
    List,
    Pattern,
    Tuple,
)


@pytest.mark.skims_test_group("unittesting")
def test_gem_gemfile() -> None:
    path: str = "skims/test/data/lib_path/f011/Gemfile"
    gemfile_dep: Pattern[str] = re.compile(r'\s*gem "(?P<name>[\w\-]+)"')
    with open(
        path,
        mode="r",
        encoding="latin-1",
    ) as file_handle:
        file_contents: str = file_handle.read(-1)
    gem_gemfile_fun = gem_gemfile.__wrapped__  # type: ignore
    content: List[str] = file_contents.splitlines()
    generator_gem: Iterator[DependencyType] = gem_gemfile_fun(
        file_contents, path
    )
    assertion: bool = True
    lines_prod_deps = [*range(116), 130, 133, 136, 139, *range(148, 182)]
    for line_num in lines_prod_deps:
        if matched := re.search(gemfile_dep, content[line_num]):
            pkg_name: str = matched.group("name")

            try:
                line, item = itemgetter("line", "item")(next(generator_gem)[0])
            except StopIteration:
                assertion = not assertion
                break
            equal_props: bool = pkg_name == item and line_num + 1 == line
            if not equal_props:
                assertion = not assertion
                break

    assert assertion


@pytest.mark.skims_test_group("unittesting")
def test_gem_gemfile_lock() -> None:
    gem_lock_dep: Pattern[str] = re.compile(
        r"^\s{4}(?P<gem>(?P<name>[\w\-]+)\s?(\(.*\))?)"
    )
    path: str = "skims/test/data/lib_path/f011/Gemfile.lock"
    with open(
        path,
        mode="r",
        encoding="latin-1",
    ) as file_handle:
        file_contents: str = file_handle.read(-1)
    content: List[str] = file_contents.splitlines()
    gemfile_lock_fun = gem_gemfile_lock.__wrapped__  # type: ignore
    generator_gem: Iterator[DependencyType] = gemfile_lock_fun(
        file_contents, path
    )
    assertion: bool = True

    for line_num in range(22, 219):
        if matched := re.search(gem_lock_dep, content[line_num]):
            pkg_name: str = matched.group("name")
            try:
                line, item = itemgetter("line", "item")(next(generator_gem)[0])
            except StopIteration:
                assertion = not assertion
                break
            if pkg_name != item or line_num + 1 != line:
                assertion = not assertion
                break

    assert assertion


@pytest.mark.skims_test_group("unittesting")
def test_gem_gemfile_dev() -> None:
    path: str = "skims/test/data/lib_path/f011/Gemfile"

    with open(
        path,
        mode="r",
        encoding="latin-1",
    ) as file_handle:
        file_contents: str = file_handle.read(-1)
        gem_gemfile_unwrapped = gem_gemfile_dev.__wrapped__  # type: ignore

    expected: Tuple[Tuple[str, str, int], ...] = (
        ("minitest-bisect", "1.0.0", 118),
        ("minitest-ci", "", 119),
        ("minitest-retry", "", 120),
        ("stackprof", "=1.4.2", 123),
        ("debug", ">=1.1.0", 124),
        ("benchmark-ips", "", 127),
        ("devise", "=1.4.2", 132),
        ("rubocop", "=1.35.1", 133),
        ("pg", "^1.3", 143),
        ("mysql2", "^0.5", 144),
        ("pry", "=1.0.1", 145),
    )
    reports: Iterator[DependencyType] = gem_gemfile_unwrapped(
        file_contents, path
    )
    assertion: bool = True
    for num, report in enumerate(reports):
        product = report[0].get("item")
        line = report[0].get("line")
        version = report[1].get("item")
        if (product, version, line) != expected[num]:
            assertion = not assertion
            break

    assert assertion


@pytest.mark.skims_test_group("unittesting")
def test_go_add_require() -> None:
    req_dict: Dict[str, DependencyType] = {}
    dep_line: str = "require gorm.io/gorm v1.24.0"
    line_number: int = 24
    if matched := re.search(GO_REQ_MOD_DEP, dep_line):
        add_require(matched, req_dict, line_number)
    exp_dict = {
        "gorm.io/gorm": format_pkg_dep(
            "gorm.io/gorm", "1.24.0", line_number, line_number
        )
    }
    assert exp_dict == req_dict


@pytest.mark.skims_test_group("unittesting")
def test_go_mod() -> None:
    path: str = "skims/test/data/lib_path/f011/go.mod"
    with open(
        path,
        mode="r",
        encoding="latin-1",
    ) as file_handle:
        file_contents: str = file_handle.read(-1)
    content: List[str] = file_contents.splitlines()
    generator_dep = go_mod.__wrapped__(file_contents, path)  # type: ignore
    assertion: bool = True
    for line_num in [*range(5, 28), *range(31, 85), 91, 94, 95]:
        if line_num in (91, 94, 95):
            dep_splitted_info = content[line_num].split("=> ")[1].split()
        else:
            dep_splitted_info = content[line_num].strip().split()
        pkg_name: str = dep_splitted_info[0]
        version: str = dep_splitted_info[1][1:]

        try:
            next_dep = next(generator_dep)
            pkg_item = itemgetter("item")(next_dep[0])
            line, item = itemgetter("line", "item")(next_dep[1])
        except StopIteration:
            assertion = not assertion
            break
        equal_props: bool = (
            pkg_item in pkg_name and version == item and line_num + 1 == line
        )
        if not equal_props:
            assertion = not assertion
            break

    assert assertion


@pytest.mark.skims_test_group("unittesting")
def test_pip_requirements_txt() -> None:
    path: str = "skims/test/data/lib_path/f011/requirements.txt"
    with open(
        path,
        mode="r",
        encoding="latin-1",
    ) as file_handle:
        file_contents: str = file_handle.read(-1)
    content: List[str] = file_contents.splitlines()
    generator_dep = pip_requirements_txt.__wrapped__(  # type: ignore
        file_contents, path
    )
    assertion: bool = True
    for line_num, line in enumerate(content, 1):
        pkg_name, version = line.split("==")

        try:
            next_dep = next(generator_dep)
            pkg_item = itemgetter("item")(next_dep[0])
            line_dep, item = itemgetter("line", "item")(next_dep[1])
        except StopIteration:
            assertion = not assertion
            break
        equal_props: bool = (
            pkg_item in pkg_name and version == item and line_num == line_dep
        )
        if not equal_props:
            assertion = not assertion
            break

    assert assertion


@pytest.mark.skims_test_group("unittesting")
def test_maven_pom_xml() -> None:
    pom_xml_ver: Pattern[str] = re.compile(
        r"<version>(\$\{)?(?P<version>[^\}]*)\}?</version>"
    )
    path = "skims/test/data/lib_path/f011/frst_child/scdn_child/pom.xml"
    with open(
        path,
        mode="r",
        encoding="latin-1",
    ) as file_handle:
        file_contents: str = file_handle.read(-1)
    generator_dep = maven_pom_xml.__wrapped__(  # type: ignore
        file_contents, path
    )
    assertion: bool = True
    pkg_ver = (
        "junit.version",
        "spring.version",
        "mockito.version",
        "slf4j.version",
        "apache.camel.version",
    )
    for line_num, line in enumerate(file_contents.splitlines(), 1):
        if matched := re.search(pom_xml_ver, line):
            version: str = matched.group("version")

            try:
                next_dep = next(generator_dep)
                line_d, item = itemgetter("line", "item")(next_dep[1])
            except StopIteration:
                assertion = not assertion
                break
            equal_props: bool = (
                version == item or version in pkg_ver
            ) and line_num == line_d
            if not equal_props:
                assertion = not assertion
                break

    assert assertion


@pytest.mark.skims_test_group("unittesting")
def test_npm_yarn_lock_dev() -> None:
    path = "skims/test/data/lib_path/f011/yarn.lock"
    with open(
        path,
        mode="r",
        encoding="latin-1",
    ) as file_handle:
        file_contents: str = file_handle.read(-1)
    generator_dep = npm_yarn_lock_dev.__wrapped__(  # type: ignore
        file_contents, path
    )
    assertion: bool = True
    pkg_info = ("xmldom", "0.4.0", 483)
    try:
        next_dep = next(generator_dep)
        pkg_item = itemgetter("item")(next_dep[0])
        line_dep, version = itemgetter("line", "item")(next_dep[1])
    except StopIteration:
        assertion = not assertion
    equal_props: bool = pkg_info == (pkg_item, version, line_dep)
    if not equal_props:
        assertion = not assertion

    assert assertion
