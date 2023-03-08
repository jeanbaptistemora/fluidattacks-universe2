from db_model.advisories.types import (
    Advisory,
)
import glob
import re
import yaml

RE_RANGES: re.Pattern[str] = re.compile(r"(?=[\(\[]).+?(?<=[\)\]])")  # NOSONAR
URL_ADVISORIES_COMMUNITY: str = (
    "https://gitlab.com/gitlab-org/advisories-community.git"
)
PLATFORMS = {
    "maven": "maven",
    "nuget": "nuget",
    "npm": "npm",
    "pypi": "pip",
    "gem": "gem",
    "go": "go",
    "packagist": "composer",
    "conan": "conan",
}
ALLOWED_RANGES = ("=", "<", ">", ">=", "<=")


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


def fix_npm_gem_go_range(unformatted_range: str) -> str:
    return unformatted_range.replace("||", " || ")


def fix_pip_composer_range(str_range: str) -> str:
    vals_to_change: dict[str, str] = {"||": " || ", ",": " ", "==": "="}

    for target, replacement in vals_to_change.items():
        fixed_range = str_range.replace(target, replacement)

    return fixed_range


def _format_ranges(platform: str, range_str: str) -> str:
    if platform in ("maven", "nuget"):
        ranges = re.findall(RE_RANGES, range_str)
        str_ranges = [format_range(ra) for ra in ranges]
        return " || ".join(str_ranges)
    if platform in ("pypi", "packagist"):
        return fix_pip_composer_range(range_str)
    return fix_npm_gem_go_range(range_str)


def format_ranges(platform: str, range_str: str) -> str:
    formatted = _format_ranges(platform, range_str)
    versions = formatted.split("||")
    fixed_versions = []
    for version in versions:
        fixed_items = []
        split_ver = version.split()
        for index, item in enumerate(split_ver):
            if item not in ALLOWED_RANGES and not item.startswith(
                ALLOWED_RANGES
            ):
                previous = split_ver[index - 1] if index > 0 else None
                operator = previous if previous in ALLOWED_RANGES else "="
                fixed_item = operator + item
                fixed_items.append(fixed_item)
            elif item not in ALLOWED_RANGES:
                fixed_items.append(item)

        fixed_versions.append(" ".join(fixed_items))

    return " || ".join(fixed_versions)


def get_platform_advisories(
    advisories: list[Advisory], tmp_dirname: str, platform: str
) -> None:
    filenames = sorted(
        glob.glob(
            f"{tmp_dirname}/{platform}/**/*.yml",
            recursive=True,
        )
    )
    for filename in filenames:
        with open(filename, "r", encoding="utf-8") as stream:
            try:
                parsed_yaml: dict = yaml.safe_load(stream)
                if not (cve_key := parsed_yaml.get("identifier")):
                    continue
                package_slug = str(parsed_yaml.get("package_slug"))
                severity: str | None = parsed_yaml.get("cvss_v3")
                package_key = package_slug.replace(
                    f"{platform}/", "", 1
                ).lower()
                if platform in (
                    "maven",
                    "npm",
                ) and not package_key.startswith("@"):
                    package_key = package_key.replace("/", ":")
                affected_range = str(parsed_yaml.get("affected_range"))
                formatted_ranges = (
                    format_ranges(
                        platform,
                        affected_range,
                    ).lower()
                    if affected_range != ""
                    else ">=0"
                )
                advisories.append(
                    Advisory(
                        associated_advisory=cve_key,
                        package_manager=PLATFORMS[platform],
                        package_name=package_key,
                        severity=severity,
                        source=URL_ADVISORIES_COMMUNITY,
                        vulnerable_version=formatted_ranges,
                    )
                )
            except yaml.YAMLError as exc:
                print(exc)


def get_advisories_community(
    advisories: list[Advisory], tmp_dirname: str
) -> None:
    print("processing advisories-community")
    # pylint: disable=consider-iterating-dictionary
    for platform in PLATFORMS.keys():
        get_platform_advisories(advisories, tmp_dirname, platform)
