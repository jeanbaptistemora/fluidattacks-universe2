from git import (
    Repo,
)
import glob
import re
import tempfile
from typing import (
    Any,
    Dict,
    Pattern,
)
from utils.logs import (
    log_blocking,
)
import yaml

RE_RANGES: Pattern[str] = re.compile(r"(?=[\(\[]).+?(?<=[\)\]])")
URL_ADVISORIES_COMMUNITY: str = (
    "https://gitlab.com/gitlab-org/advisories-community.git"
)


def format_range(range: str) -> str:
    prefix = range[0]
    suffix = range[-1]
    values = range[1:-1].split(",")
    if len(values) < 2:
        return values[0]
    min_r, max_r = values
    min_operator = ""
    max_operator = ""
    if min_r == "":
        min_r = 0
        min_operator = ">="
    else:
        min_operator = ">" if prefix == "(" else ">="
    if max_r == "":
        return f"{min_operator}{min_r}"
    max_operator = "<" if suffix == ")" else "<="
    return f"{min_operator}{min_r} {max_operator}{max_r}"


def fix_npm_range(range: str) -> str:
    return range.replace("||", " || ")


def format_ranges(language: str, range: str) -> str:
    if language in ("maven", "nuget"):
        ranges = re.findall(RE_RANGES, range)
        str_ranges = [format_range(ra) for ra in ranges]
        return " || ".join(str_ranges)
    if language == "npm":
        return fix_npm_range(range)


def get_community_advisories(
    advisories: Dict[str, Any], language: str
) -> dict:
    with tempfile.TemporaryDirectory() as tmp_dirname:
        log_blocking("info", "Cloning repository: advisories-community")
        Repo.clone_from(URL_ADVISORIES_COMMUNITY, tmp_dirname)
        filenames = sorted(
            glob.glob(f"{tmp_dirname}/{language}/**/*.yml", recursive=True)
        )
        log_blocking("info", "Processing vulnerabilities")
        for filename in filenames:
            with open(filename, "r") as stream:
                try:
                    parsed_yaml: dict = yaml.safe_load(stream)
                    if (
                        cve_key := parsed_yaml.get("identifier")
                    ) and cve_key.startswith("GMS"):
                        continue
                    package_slug: str = parsed_yaml.get("package_slug")
                    package_key = package_slug.replace(
                        f"{language}/", "", 1
                    ).lower()
                    if language in (
                        "maven",
                        "npm",
                    ) and not package_key.startswith("@"):
                        package_key = package_key.replace("/", ":")
                    if package_key not in advisories:
                        advisories.update({package_key: {}})
                    if cve_key not in advisories[package_key]:
                        formatted_ranges = format_ranges(
                            language, parsed_yaml.get("affected_range")
                        )
                        advisories[package_key].update(
                            {cve_key: formatted_ranges}
                        )
                except yaml.YAMLError as exc:
                    print(exc)

    return advisories
