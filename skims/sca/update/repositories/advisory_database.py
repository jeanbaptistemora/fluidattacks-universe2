from git import (
    Repo,
)
import glob
import json
import tempfile
from typing import (
    Any,
    Dict,
    List,
)
from utils.logs import (
    log_blocking,
)

URL_ADVISORY_DATABASE: str = "https://github.com/github/advisory-database.git"


def get_vulnerabilities_ranges(
    affected: List[dict],
    vuln_id: str,
    language: str,
    advisories: Dict[str, Any],
) -> None:
    for pkg_obj in affected:
        package: dict = pkg_obj.get("package")
        ecosystem: str = package.get("ecosystem")
        if ecosystem.lower() != language:
            continue
        pkg_name: str = package.get("name").lower()
        ranges: List[dict] = pkg_obj.get("ranges") or []
        for range in ranges:
            events: List[dict] = range.get("events")
            str_range: str
            introduced = f">={events[0].get('introduced')}"
            fixed = f" <{events[1].get('fixed')}" if len(events) > 1 else ""
            str_range = f"{introduced}{fixed}"
            if pkg_name not in advisories:
                advisories.update({pkg_name: {}})
            if ghsa_vuln := advisories[pkg_name].get(vuln_id):
                advisories[pkg_name][vuln_id] = " || ".join(
                    (ghsa_vuln, str_range)
                )
            else:
                advisories[pkg_name].update({vuln_id: str_range})


def get_advisory_database(advisories: Dict[str, Any], language: str) -> dict:
    with tempfile.TemporaryDirectory() as tmp_dirname:
        log_blocking("info", "Cloning repository: advisory-database")
        Repo.clone_from(URL_ADVISORY_DATABASE, tmp_dirname, depth=1)
        filenames = sorted(
            glob.glob(
                f"{tmp_dirname}/advisories/github-reviewed/**/*.json",
                recursive=True,
            )
        )
        log_blocking("info", "Processing vulnerabilities")
        for filename in filenames:
            with open(filename, "r") as stream:
                try:
                    from_json: dict = json.load(stream)
                    vuln_id = from_json.get("id")
                    affected = from_json.get("affected")
                    get_vulnerabilities_ranges(
                        affected, vuln_id, language, advisories
                    )
                except json.JSONDecodeError as exc:
                    print(exc)

    return advisories
