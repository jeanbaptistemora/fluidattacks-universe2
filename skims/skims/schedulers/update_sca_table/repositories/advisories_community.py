import re
from typing import (
    Dict,
    Pattern,
)

RE_RANGES: Pattern[str] = re.compile(r"(?=[\(\[]).+?(?<=[\)\]])")
URL_ADVISORIES_COMMUNITY: str = (
    "https://gitlab.com/gitlab-org/advisories-community.git"
)


def format_range(unformatted_range: str) -> str:
    prefix = unformatted_range[0]
    suffix = unformatted_range[-1]
    values = unformatted_range[1:-1].split(",")
    if len(values) < 2:
        return values[0]
    min_r, max_r = values
    min_operator = ""
    max_operator = ""
    if min_r == "":
        min_r = "0"
        min_operator = ">="
    else:
        min_operator = ">" if prefix == "(" else ">="
    if max_r == "":
        return f"{min_operator}{min_r}"
    max_operator = "<" if suffix == ")" else "<="
    return f"{min_operator}{min_r} {max_operator}{max_r}"


def fix_npm_range(unformatted_range: str) -> str:
    return unformatted_range.replace("||", " || ")


def fix_pip_range(pip_range: str) -> str:
    vals_to_change: Dict[str, str] = {"||": " || ", ",": " ", "==": ""}

    for target, replacement in vals_to_change.items():
        pip_range = pip_range.replace(target, replacement)

    return pip_range


def format_ranges(platform: str, range_str: str) -> str:
    if platform in ("maven", "nuget"):
        ranges = re.findall(RE_RANGES, range_str)
        str_ranges = [format_range(ra) for ra in ranges]
        return " || ".join(str_ranges)
    if platform == "pypi":
        return fix_pip_range(range_str)
    return fix_npm_range(range_str)  # npm
