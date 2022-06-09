from git import (
    Repo,
)
import glob
import re
import tempfile
from typing import (
    Pattern,
)
from utils.logs import (
    log_blocking,
)
import yaml

RE_MAVEN_RANGES: Pattern[str] = re.compile(r"(?=[\(\[]).+?(?<=[\)\]])")


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


def format_ranges(language: str, range: str) -> str:
    if language == "maven":
        ranges = re.findall(RE_MAVEN_RANGES, range)
        str_ranges = [format_range(ra) for ra in ranges]
        return " || ".join(str_ranges)


def get_remote_advisories(language: str) -> dict:
    advisories: dict = {}
    with tempfile.TemporaryDirectory() as tmp_dirname:
        log_blocking("info", "Cloning repository: advisories-community")
        Repo.clone_from(
            "https://gitlab.com/gitlab-org/advisories-community.git",
            tmp_dirname,
        )
        filenames = sorted(
            glob.glob(f"{tmp_dirname}/{language}/**/*yml", recursive=True)
        )
        log_blocking("info", "Processing vulnerabilities")
        for filename in filenames:
            with open(filename, "r") as stream:
                try:
                    parsed_yaml = yaml.safe_load(stream)
                    key = filename.replace(
                        f"{tmp_dirname}/{language}/", ""
                    ).replace("/", ":")
                    package_key = key.rsplit(":", 1)[0]
                    cve_key = parsed_yaml["identifier"]
                    if package_key not in advisories:
                        advisories.update({package_key: {}})
                    if cve_key not in advisories[package_key]:
                        formatted_ranges = format_ranges(
                            language, parsed_yaml["affected_range"]
                        )
                        advisories[package_key].update(
                            {cve_key: formatted_ranges}
                        )
                except yaml.YAMLError as exc:
                    print(exc)

    return advisories
