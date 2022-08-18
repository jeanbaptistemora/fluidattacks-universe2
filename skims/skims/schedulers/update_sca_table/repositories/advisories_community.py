from db_model.advisories.types import (
    Advisory,
)
import glob
import re
from typing import (
    Dict,
    Iterable,
    List,
    Optional,
    Pattern,
)
import yaml  # type: ignore

RE_RANGES: Pattern[str] = re.compile(r"(?=[\(\[]).+?(?<=[\)\]])")
URL_ADVISORIES_COMMUNITY: str = (
    "https://gitlab.com/gitlab-org/advisories-community.git"
)


def format_range(unformatted_range: str) -> str:
    prefix = unformatted_range[0]
    suffix = unformatted_range[-1]
    values = unformatted_range[1:-1].split(",")
    if len(values) < 2:
        return f"={values[0]}"
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
    vals_to_change: Dict[str, str] = {"||": " || ", ",": " ", "==": "="}

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


def get_platform_advisories(
    advisories: List[Advisory], tmp_dirname: str, platform: str
) -> None:
    if platform == "pip":
        platform = "pypi"
    filenames = sorted(
        glob.glob(f"{tmp_dirname}/{platform}/**/*.yml", recursive=True)
    )
    for filename in filenames:
        with open(filename, "r", encoding="utf-8") as stream:
            try:
                parsed_yaml: dict = yaml.safe_load(stream)
                if not (cve_key := parsed_yaml.get("identifier")):
                    continue
                package_slug = str(parsed_yaml.get("package_slug"))
                severity: Optional[str] = parsed_yaml.get("cvss_v3")
                package_key = package_slug.replace(
                    f"{platform}/", "", 1
                ).lower()
                if platform in (
                    "maven",
                    "npm",
                ) and not package_key.startswith("@"):
                    package_key = package_key.replace("/", ":")
                formatted_ranges = format_ranges(
                    platform, str(parsed_yaml.get("affected_range"))
                ).lower()
                advisories.append(
                    Advisory(
                        associated_advisory=cve_key,
                        package_manager=platform,
                        package_name=package_key,
                        severity=severity,
                        source=URL_ADVISORIES_COMMUNITY,
                        vulnerable_version=formatted_ranges,
                    )
                )
            except yaml.YAMLError as exc:
                print(exc)


def get_advisories_community(
    advisories: List[Advisory], tmp_dirname: str, platforms: Iterable[str]
) -> None:
    print("processing advisories-community")
    for platform in platforms:
        get_platform_advisories(advisories, tmp_dirname, platform)
