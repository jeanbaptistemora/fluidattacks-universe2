from collections.abc import (
    Iterator,
)
from gemfileparser import (
    GemfileParser,
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
from parse_gemfile import (
    parse_line,
)
import re

GEMFILE_DEP: re.Pattern[str] = re.compile(
    r'^\s*(?P<gem>gem ".*?",?( "[><~=]{0,2}\s?[\d\.]+",?){0,2})'
)
NOT_PROD_DEP: re.Pattern[str] = re.compile(
    r":group => \[?[:\w\-, ]*(:development|:test)"
)
NOT_PROD_GROUP: re.Pattern[str] = re.compile(r"(\s*)group :(test|development)")


# pylint: disable=unused-argument
@pkg_deps_to_vulns(Platform.GEM, MethodsEnum.GEM_GEMFILE_DEV)
def gem_gemfile_dev(content: str, path: str) -> Iterator[DependencyType]:
    line_group: bool = False
    end_line: str = ""
    for line_number, line in enumerate(content.splitlines(), 1):
        if line_group:
            if line == end_line:
                line_group = False
                end_line = ""
            elif matched := GEMFILE_DEP.search(line):
                line = GemfileParser.preprocess(matched.group("gem"))
                line = line[3:]
                product, version = parse_line(line, gem_file=True)
                yield format_pkg_dep(
                    product, version, line_number, line_number
                )
        elif match_group := NOT_PROD_GROUP.search(line):
            line_group = True
            blank = match_group.group(1)
            end_line = f"{blank}end"
        elif matched := GEMFILE_DEP.search(line):
            if not NOT_PROD_DEP.search(line):
                continue
            line = GemfileParser.preprocess(matched.group("gem"))
            line = line[3:]
            product, version = parse_line(line, gem_file=True)
            yield format_pkg_dep(product, version, line_number, line_number)
