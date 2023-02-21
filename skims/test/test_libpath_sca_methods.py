from collections.abc import (
    Iterator,
)
from lib_path.common import (
    DependencyType,
    format_pkg_dep,
)
from lib_path.f011.composer import (
    composer_json,
    composer_lock,
)
from lib_path.f011.conan import (
    conan_conanfile_txt,
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
    maven_gradle,
    maven_pom_xml,
    maven_sbt,
)
from lib_path.f011.npm import (
    npm_package_json,
    npm_package_lock_json,
    npm_yarn_lock,
)
from lib_path.f011.pip import (
    pip_requirements_txt,
)
from lib_path.f011.pub import (
    pub_pubspec_yaml,
)
from lib_path.f393.composer import (
    composer_json_dev,
    composer_lock_dev,
)
from lib_path.f393.gem import (
    gem_gemfile_dev,
)
from lib_path.f393.npm import (
    npm_package_json as npm_package_json_dev,
    npm_pkg_lock_json as npm_pkg_lock_json_dev,
    npm_yarn_lock_dev,
)
from lib_path.f393.pub import (
    pub_pubspec_yaml_dev,
)
from operator import (
    itemgetter,
)
import pytest
import re


def get_file_info_from_path(path: str) -> str:
    with open(
        path,
        mode="r",
        encoding="latin-1",
    ) as file_handle:
        file_contents: str = file_handle.read(-1)
    return file_contents


@pytest.mark.skims_test_group("unittesting")
def test_gem_gemfile() -> None:
    gemfile_dep: re.Pattern[str] = re.compile(r'\s*gem "(?P<name>[\w\-]+)"')
    path: str = "skims/test/data/lib_path/f011/Gemfile"
    file_contents: str = get_file_info_from_path(path)
    gem_gemfile_fun = gem_gemfile.__wrapped__  # type: ignore
    content: list[str] = file_contents.splitlines()
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
def test_gem_gemfile_dev() -> None:
    path: str = "skims/test/data/lib_path/f011/Gemfile"
    gemfile_dep: re.Pattern[str] = re.compile(r'\s*gem "(?P<name>[\w\-]+)"')
    with open(
        path,
        mode="r",
        encoding="latin-1",
    ) as file_handle:
        file_contents: str = file_handle.read(-1)
    gem_gemfile_fun = gem_gemfile_dev.__wrapped__  # type: ignore
    content: list[str] = file_contents.splitlines()
    generator_gem: Iterator[DependencyType] = gem_gemfile_fun(
        file_contents, path
    )
    assertion: bool = True
    lines_prod_deps = [*range(117, 127), 131, 132, *range(142, 145)]
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
    gem_lock_dep: re.Pattern[str] = re.compile(
        r"^\s{4}(?P<gem>(?P<name>[\w\-]+)\s?(\(.*\))?)"
    )
    path: str = "skims/test/data/lib_path/f011/Gemfile.lock"
    file_contents: str = get_file_info_from_path(path)
    content: list[str] = file_contents.splitlines()
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
def test_go_add_require() -> None:
    req_dict: dict[str, DependencyType] = {}
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
    file_contents: str = get_file_info_from_path(path)
    content: list[str] = file_contents.splitlines()
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
    file_contents: str = get_file_info_from_path(path)
    content: list[str] = file_contents.splitlines()
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
    pom_xml_ver: re.Pattern[str] = re.compile(
        r"<version>(\$\{)?(?P<version>[^\}]*)\}?</version>"
    )
    path = "skims/test/data/lib_path/f011/frst_child/scdn_child/pom.xml"
    file_contents: str = get_file_info_from_path(path)
    generator_dep = maven_pom_xml.__wrapped__(  # type: ignore
        file_contents, path
    )
    assertion: bool = True
    pkg_versions = {
        "junit.version": "4.12",
        "spring.version": "4.2.2.RELEASE",
        "mockito.version": "2.0.31-beta",
        "slf4j.version": "1.7.12",
        "apache.camel.version": "2.6.0",
    }
    for line_num, line in enumerate(file_contents.splitlines(), 1):
        if matched := re.search(pom_xml_ver, line):
            version: str = pkg_versions.get(
                matched.group("version"), matched.group("version")
            )

            try:
                next_dep = next(generator_dep)
                line_d, item = itemgetter("line", "item")(next_dep[1])
            except StopIteration:
                assertion = not assertion
                break
            equal_props: bool = version == item and line_num == line_d
            if not equal_props:
                assertion = not assertion
                break

    assert assertion


@pytest.mark.skims_test_group("unittesting")
def test_composer_json() -> None:
    patt_dep_info: re.Pattern[str] = re.compile(
        r'"(?P<pkg_name>.*?)": "(?P<version>.*?)"'
    )
    path: str = "skims/test/data/lib_path/f011/composer.json"
    file_contents: str = get_file_info_from_path(path)
    content: list[str] = file_contents.splitlines()
    generator_dep = composer_json.__wrapped__(  # type: ignore
        file_contents, path
    )
    assertion: bool = True
    for line_num in range(16, 39):
        if dep_info := patt_dep_info.search(content[line_num]):
            pkg_name: str = dep_info.group("pkg_name")
            version: str = dep_info.group("version")

            try:
                next_dep = next(generator_dep)
                pkg_item = itemgetter("item")(next_dep[0])
                item_ver = itemgetter("item")(next_dep[1])
            except StopIteration:
                assertion = not assertion
                break
            equal_props: bool = pkg_item == pkg_name and version == item_ver
            if not equal_props:
                assertion = not assertion
                break

    assert assertion


@pytest.mark.skims_test_group("unittesting")
def test_composer_json_dev() -> None:
    patt_dep_info: re.Pattern[str] = re.compile(
        r'"(?P<pkg_name>.*?)": "(?P<version>.*?)"'
    )
    path: str = "skims/test/data/lib_path/f011/composer.json"
    file_contents: str = get_file_info_from_path(path)
    content: list[str] = file_contents.splitlines()
    generator_dep = composer_json_dev.__wrapped__(  # type: ignore
        file_contents, path
    )
    assertion: bool = True
    for line_num in range(41, 46):
        if dep_info := patt_dep_info.search(content[line_num]):
            pkg_name: str = dep_info.group("pkg_name")
            version: str = dep_info.group("version")

            try:
                next_dep = next(generator_dep)
                pkg_item = itemgetter("item")(next_dep[0])
                item_ver = itemgetter("item")(next_dep[1])
            except StopIteration:
                assertion = not assertion
                break
            equal_props: bool = pkg_item == pkg_name and version == item_ver
            if not equal_props:
                assertion = not assertion
                break

    assert assertion


@pytest.mark.skims_test_group("unittesting")
def test_composer_lock() -> None:
    patt_info: re.Pattern[str] = re.compile(r'".*?": "(?P<info>.*?)"')
    path: str = "skims/test/data/lib_path/f011/composer.lock"
    file_contents: str = get_file_info_from_path(path)
    content: list[str] = file_contents.splitlines()
    generator_dep = composer_lock.__wrapped__(  # type: ignore
        file_contents, path
    )
    assertion: bool = True
    for line_num in (9, 85, 165, 241):
        if (pkg_name_match := patt_info.search(content[line_num])) and (
            version_match := patt_info.search(content[line_num + 1])
        ):
            pkg_name = pkg_name_match.group("info")
            version = version_match.group("info")
            try:
                next_dep = next(generator_dep)
                pkg_item = itemgetter("item")(next_dep[0])
                item_ver = itemgetter("item")(next_dep[1])
            except StopIteration:
                assertion = not assertion
                break
            if not (pkg_item == pkg_name and version == item_ver):
                assertion = not assertion
                break
        else:
            assertion = not assertion
            break

    assert assertion


@pytest.mark.skims_test_group("unittesting")
def test_composer_lock_dev() -> None:
    patt_info: re.Pattern[str] = re.compile(r'".*?": "(?P<info>.*?)"')
    path: str = "skims/test/data/lib_path/f011/composer.lock"
    file_contents: str = get_file_info_from_path(path)
    content: list[str] = file_contents.splitlines()
    generator_dep = composer_lock_dev.__wrapped__(  # type: ignore
        file_contents, path
    )
    assertion: bool = True
    for line_num in (365, 440, 510):
        if (pkg_name_match := patt_info.search(content[line_num])) and (
            version_match := patt_info.search(content[line_num + 1])
        ):
            pkg_name = pkg_name_match.group("info")
            version = version_match.group("info")
            try:
                next_dep = next(generator_dep)
                pkg_item = itemgetter("item")(next_dep[0])
                item_ver = itemgetter("item")(next_dep[1])
            except StopIteration:
                assertion = not assertion
                break
            if not (pkg_item == pkg_name and version == item_ver):
                assertion = not assertion
                break
        else:
            assertion = not assertion
            break

    assert assertion


@pytest.mark.skims_test_group("unittesting")
def test_pub_pubspec_yaml() -> None:
    path: str = "skims/test/data/lib_path/f011/pubspec.yaml"
    file_contents: str = get_file_info_from_path(path)
    content: list[str] = file_contents.splitlines()
    gemfile_lock_fun = pub_pubspec_yaml.__wrapped__  # type: ignore
    generator_gem: Iterator[DependencyType] = gemfile_lock_fun(
        file_contents, path
    )
    assertion: bool = True

    for line_num in range(13, 27):
        pkg_name, version = content[line_num].lstrip().split(": ")
        current_dep = next(generator_gem)
        try:
            item = itemgetter("item")(current_dep[0])
            item_version = itemgetter("item")(current_dep[1])
        except StopIteration:
            assertion = not assertion
            break

        if pkg_name != item or version != item_version:
            assertion = not assertion
            break

    assert assertion


@pytest.mark.skims_test_group("unittesting")
def test_pub_pubspec_yaml_dev() -> None:
    path: str = "skims/test/data/lib_path/f011/pubspec.yaml"
    file_contents: str = get_file_info_from_path(path)
    content: list[str] = file_contents.splitlines()
    gemfile_lock_fun = pub_pubspec_yaml_dev.__wrapped__  # type: ignore
    generator_gem: Iterator[DependencyType] = gemfile_lock_fun(
        file_contents, path
    )
    assertion: bool = True

    for line_num in range(31, 33):
        pkg_name, version = content[line_num].lstrip().split(": ")
        current_dep = next(generator_gem)
        try:
            item = itemgetter("item")(current_dep[0])
            item_version = itemgetter("item")(current_dep[1])
        except StopIteration:
            assertion = not assertion
            break

        if pkg_name != item or version != item_version:
            assertion = not assertion
            break

    assert assertion


@pytest.mark.skims_test_group("unittesting")
def test_npm_package_json_dev() -> None:
    path = "skims/test/data/lib_path/f011/package.json"
    file_contents: str = get_file_info_from_path(path)
    generator_dep = npm_package_json_dev.__wrapped__(  # type: ignore
        file_contents, path
    )
    assertion: bool = True
    pkg_info = ("xmldom", "0.4.0")
    try:
        next_dep = next(generator_dep)
        product = itemgetter("item")(next_dep[0])
        version = itemgetter("item")(next_dep[1])
    except StopIteration:
        assertion = not assertion
    if not (product == pkg_info[0] and version == pkg_info[1]):
        assertion = not assertion

    assert assertion


@pytest.mark.skims_test_group("unittesting")
def test_npm_yarn_lock_dev() -> None:
    path: str = "skims/test/data/lib_path/f011/yarn.lock"
    file_contents: str = get_file_info_from_path(path)
    generator_dep = npm_yarn_lock_dev.__wrapped__(  # type: ignore
        file_contents, path
    )
    assertion: bool = True
    pkg_info = ("xmldom", "0.4.0")
    try:
        next_dep = next(generator_dep)
        pkg_item = itemgetter("item")(next_dep[0])
        item_ver = itemgetter("item")(next_dep[1])
    except StopIteration:
        assertion = not assertion
    if not (pkg_item == pkg_info[0] and pkg_info[1] == item_ver):
        assertion = not assertion

    assert assertion


@pytest.mark.skims_test_group("unittesting")
def test_npm_pkg_lock_json_dev() -> None:
    path: str = "skims/test/data/lib_path/f011/package-lock.json"
    file_contents: str = get_file_info_from_path(path)
    generator_dep = npm_pkg_lock_json_dev.__wrapped__(  # type: ignore
        file_contents, path
    )
    assertion: bool = True
    packages = (("@babel/dev", "7.11.0.4"), ("hoek", "5.0.0.3"))
    for product, version in packages:
        try:
            next_dep = next(generator_dep)
            pkg_item = itemgetter("item")(next_dep[0])
            item_ver = itemgetter("item")(next_dep[1])
        except StopIteration:
            assertion = not assertion
        if not (pkg_item == product and version == item_ver):
            assertion = not assertion

    assert assertion


@pytest.mark.skims_test_group("unittesting")
def test_npm_package_json() -> None:
    path: str = "skims/test/data/lib_path/f011/package.json"
    file_contents: str = get_file_info_from_path(path)
    generator_dep = npm_package_json.__wrapped__(  # type: ignore
        file_contents, path
    )
    assertion: bool = True
    packages = (
        ("@angular/core", "^13.3.3"),
        ("cloudron-sysadmin", "1.0.0"),
        ("script-manager", "0.8.6"),
        ("slug", "0.9.0"),
    )
    for product, version in packages:
        try:
            next_dep = next(generator_dep)
            pkg_item = itemgetter("item")(next_dep[0])
            item_ver = itemgetter("item")(next_dep[1])
        except StopIteration:
            assertion = not assertion
        if not (pkg_item == product and version == item_ver):
            assertion = not assertion

    assert assertion


@pytest.mark.skims_test_group("unittesting")
def test_npm_package_lock_json() -> None:
    path: str = "skims/test/data/lib_path/f011/package-lock.json"
    file_contents: str = get_file_info_from_path(path)
    generator_dep = npm_package_lock_json.__wrapped__(  # type: ignore
        file_contents, path
    )
    assertion: bool = True
    packages = (
        ("@babel/prod", "7.11.0.8"),
        ("hoek", "5.0.0.7"),
        ("hoek", "5.0.0.6"),
    )
    for product, version in packages:
        try:
            next_dep = next(generator_dep)
            pkg_item = itemgetter("item")(next_dep[0])
            item_ver = itemgetter("item")(next_dep[1])
        except StopIteration:
            assertion = not assertion
        if not (pkg_item == product and version == item_ver):
            assertion = not assertion

    assert assertion


@pytest.mark.skims_test_group("unittesting")
def test_npm_yarn_lock() -> None:
    path: str = "skims/test/data/lib_path/f011/yarn.lock"
    file_contents: str = get_file_info_from_path(path)
    generator_dep = npm_yarn_lock.__wrapped__(  # type: ignore
        file_contents, path
    )
    dependencies = list(generator_dep)
    assertion: bool = True
    packages = {
        "asn1": "0.2.6",
        "jsbn": "0.1.1",
        "uuid": "3.3.2",
    }
    for num in (2, 30, 58):
        next_dep = dependencies[num]
        pkg_item = itemgetter("item")(next_dep[0])
        item_ver = itemgetter("item")(next_dep[1])
        if not (pkg_item in packages and item_ver == packages[pkg_item]):
            assertion = not assertion

    assert assertion


@pytest.mark.skims_test_group("unittesting")
def test_maven_gradle() -> None:
    path: str = "skims/test/data/lib_path/f011/build.gradle"
    file_contents: str = get_file_info_from_path(path)
    generator_dep = maven_gradle.__wrapped__(  # type: ignore
        file_contents, path
    )
    assertion: bool = True
    packages = (
        ("io.springfox:springfox-swagger-ui", "2.6.1"),
        ("org.apache.logging.log4j:log4j-core", "2.13.2"),
        ("org.json:json", "20160810"),
        ("javax.mail:mail", "1.4"),
    )
    for product, version in packages:
        try:
            next_dep = next(generator_dep)
            pkg_item = itemgetter("item")(next_dep[0])
            item_ver = itemgetter("item")(next_dep[1])
        except StopIteration:
            assertion = not assertion
        if not (pkg_item == product and version == item_ver):
            assertion = not assertion

    assert assertion


@pytest.mark.skims_test_group("unittesting")
def test_maven_sbt() -> None:
    sbt_dep: re.Pattern[str] = re.compile(
        r'"(?P<pkg>[\w\.\-]+)"\s+%\s+"(?P<module>[\w\.\-]+)"'
        r'\s+%\s+"(?P<version>[\d\.]+)"'
    )
    path: str = "skims/test/data/lib_path/f011/build.sbt"
    file_contents: str = get_file_info_from_path(path)
    content: list[str] = file_contents.splitlines()
    generator_dep = maven_sbt.__wrapped__(file_contents, path)  # type: ignore
    assertion: bool = True
    for line_num in [*range(3, 8), 10, *range(14, 18), *range(20, 22), 23]:
        if pkg_info := sbt_dep.search(content[line_num]):
            pkg_name = f'{pkg_info.group("pkg")}:{pkg_info.group("module")}'
            version = pkg_info.group("version")

            try:
                next_dep = next(generator_dep)
                pkg_item = itemgetter("item")(next_dep[0])
                item = itemgetter("item")(next_dep[1])
            except StopIteration:
                assertion = not assertion
                break
            if not (pkg_item in pkg_name and version == item):
                assertion = not assertion
                break

    assert assertion


@pytest.mark.skims_test_group("unittesting")
def test_conan_conanfile_txt() -> None:
    conan_dep: re.Pattern[str] = re.compile(
        r"^(?P<product>[\w\-]+)\/\[?(?P<version>[^\],]+)"
    )
    path: str = "skims/test/data/lib_path/f011/conanfile.txt"
    file_contents: str = get_file_info_from_path(path)
    content: list[str] = file_contents.splitlines()
    generator_dep = conan_conanfile_txt.__wrapped__(  # type: ignore
        file_contents, path
    )
    assertion: bool = True
    for line_num in range(1, 13):
        if pkg_info := conan_dep.search(content[line_num]):
            pkg_name = pkg_info.group("product")
            version = pkg_info.group("version")

            try:
                next_dep = next(generator_dep)
                pkg_item = itemgetter("item")(next_dep[0])
                item = itemgetter("item")(next_dep[1])
            except StopIteration:
                assertion = not assertion
                break
            if not (pkg_item in pkg_name and version == item):
                assertion = not assertion
                break

    assert assertion
