from db_model.advisories.types import (
    Advisory,
)
import glob
import json
from typing import (
    Any,
    Dict,
    Iterable,
    List,
    Optional,
)
from utils.logs import (
    log_blocking,
)

URL_ADVISORY_DATABASE: str = "https://github.com/github/advisory-database.git"


def get_vulnerabilities_ranges(  # pylint: disable=too-many-locals
    affected: List[dict],
    vuln_id: str,
    platforms: Iterable[str],
    advisories: List[Advisory],
    severity: Optional[str],
) -> None:
    current_advisories: Dict[str, str] = {}
    for pkg_obj in affected:
        package: Dict[str, Any] = pkg_obj.get("package") or {}
        ecosystem: str = str(package.get("ecosystem"))
        if (platform := ecosystem.lower()) not in platforms:
            continue
        pkg_name: str = str(package.get("name")).lower()
        ranges: List[Dict[str, Any]] = pkg_obj.get("ranges") or []
        final_range = ""
        versions: List[str] = pkg_obj.get("versions") or []
        formatted_versions = ["=" + ver for ver in versions]
        if formatted_versions:
            final_range = " || ".join(formatted_versions)
        for range_ver in ranges:
            events: List[Dict[str, str]] = range_ver.get("events") or []
            str_range: str
            introduced = f">={events[0].get('introduced')}"
            fixed = f" <{events[1].get('fixed')}" if len(events) > 1 else ""
            str_range = f"{introduced}{fixed}".lower()
            if final_range == "":
                final_range = str_range
            else:
                final_range = " || ".join((final_range, str_range))
        if pkg_name not in current_advisories:
            current_advisories.update({pkg_name: final_range})
        else:
            cur_range = current_advisories[pkg_name]
            current_advisories.update(
                {pkg_name: " || ".join((cur_range, final_range))}
            )

    for key_pkg, range_val in current_advisories.items():
        advisories.append(
            Advisory(
                associated_advisory=vuln_id,
                package_manager=platform,
                package_name=key_pkg,
                severity=severity,
                source=URL_ADVISORY_DATABASE,
                vulnerable_version=range_val,
            )
        )


def get_advisory_database(
    advisories: List[Advisory], tmp_dirname: str, platforms: Iterable[str]
) -> None:
    filenames = sorted(
        glob.glob(
            f"{tmp_dirname}/advisories/github-reviewed/**/*.json",
            recursive=True,
        )
    )
    print("processing advisory-database")
    for filename in filenames:
        with open(filename, "r", encoding="utf-8") as stream:
            try:
                from_json: dict = json.load(stream)
                vuln_id = str(from_json.get("id"))
                affected = from_json.get("affected") or []
                severity: List[Dict[str, str]] = (
                    from_json.get("severity") or []
                )
                severity_val: Optional[str] = None
                if len(severity) > 0:
                    severity_val = severity[0].get("score")
                get_vulnerabilities_ranges(
                    affected, vuln_id, platforms, advisories, severity_val
                )
            except json.JSONDecodeError as exc:
                log_blocking("error", "%s", exc)
