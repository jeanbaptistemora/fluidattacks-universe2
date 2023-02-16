from collections.abc import (
    Iterable,
)
from gemfileparser import (
    Dependency,
    GemfileParser,
)


def format_requirements(requirements: list[str]) -> str:
    formatted: str = ""
    if len(requirements) == 0:
        return formatted
    requirements = [req.replace(" ", "") for req in requirements]
    first_req = requirements[0]
    if "~" in first_req:
        if len(requirements) == 1:
            dot_times = first_req.count(".")
            if dot_times <= 1:
                formatted = first_req.replace("~>", "^")
            else:
                formatted = first_req.replace("~>", "~")
        elif len(requirements) == 2:
            sec_req = requirements[1]
            if ">=" in sec_req:
                formatted = sec_req.replace(">=", "^")
            elif "!=" in sec_req:
                sec_ver = sec_req.replace("!=", "")
                first_ver = first_req.replace("!=", "")
                formatted = f">={first_ver} <{sec_ver}  || >{sec_ver}"
    else:
        formatted = " ".join(requirements)
    return formatted


def match_dep_criteria(
    column_list: Iterable[str],
) -> Dependency:
    dep = Dependency()
    for column in column_list:
        for criteria, criteria_regex in GemfileParser.gemfile_regexes.items():
            match = criteria_regex.match(column)
            if match:
                if criteria == "requirement":
                    dep.requirement.append(match.group(criteria))
                else:
                    setattr(dep, criteria, match.group(criteria))
                break
    return dep


def parse_line(in_line: str, gem_file: bool) -> tuple[str, str]:
    line: list[str] = []
    if gem_file:
        line = in_line.split(",")
    else:
        line = in_line.split(" ", maxsplit=1)
        if len(line) > 1 and (", " in line[1]):
            line = [line[0], *line[1].split(", ")]

    column_list: list[str] = []
    for column in line:
        stripped_column = (
            column.replace("'", "")
            .replace('"', "")
            .replace("%q<", "")
            .replace("(", "")
            .replace(")", "")
            .replace("[", "")
            .replace("]", "")
            .strip()
        )
        column_list.append(stripped_column)

    deps = match_dep_criteria(column_list)
    deps_dict = deps.to_dict()
    product: str = deps_dict["name"]
    version: str = format_requirements(deps_dict["requirement"])
    return product, version
