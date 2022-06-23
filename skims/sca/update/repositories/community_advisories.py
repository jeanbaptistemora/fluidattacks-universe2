from git import (
    Repo,
)
import glob
import re
import tempfile
from typing import (
    Dict,
    Pattern,
)
from utils.logs import (
    log_blocking,
)
import yaml  # type: ignore

RE_RANGES: Pattern[str] = re.compile(r"(?=[\(\[]).+?(?<=[\)\]])")
URL_ADVISORIES_COMMUNITY: str = (
    "https://gitlab.com/gitlab-org/advisories-community.git"
)

Advisories = Dict[str, Dict[str, str]]


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


def format_ranges(platform: str, range_str: str) -> str:
    if platform in ("maven", "nuget"):
        ranges = re.findall(RE_RANGES, range_str)
        str_ranges = [format_range(ra) for ra in ranges]
        return " || ".join(str_ranges)

    return fix_npm_range(range_str)  # npm


def get_community_advisories(advisories: Advisories, platform: str) -> dict:
    with tempfile.TemporaryDirectory() as tmp_dirname:
        log_blocking("info", "Cloning repository: advisories-community")
        Repo.clone_from(URL_ADVISORIES_COMMUNITY, tmp_dirname)
        filenames = sorted(
            glob.glob(f"{tmp_dirname}/{platform}/**/*.yml", recursive=True)
        )
        log_blocking("info", "Processing vulnerabilities")
        for filename in filenames:
            with open(filename, "r", encoding="utf-8") as stream:
                try:
                    parsed_yaml: dict = yaml.safe_load(stream)
                    if not (
                        cve_key := parsed_yaml.get("identifier")
                    ) or cve_key.startswith("GMS"):
                        continue
                    package_slug = str(parsed_yaml.get("package_slug"))
                    package_key = package_slug.replace(
                        f"{platform}/", "", 1
                    ).lower()
                    if platform in (
                        "maven",
                        "npm",
                    ) and not package_key.startswith("@"):
                        package_key = package_key.replace("/", ":")
                    if package_key not in advisories:
                        advisories.update({package_key: {}})
                    if cve_key not in advisories[package_key]:
                        formatted_ranges = format_ranges(
                            platform, str(parsed_yaml.get("affected_range"))
                        )
                        advisories[package_key].update(
                            {cve_key: formatted_ranges}
                        )
                except yaml.YAMLError as exc:
                    print(exc)

    return advisories
