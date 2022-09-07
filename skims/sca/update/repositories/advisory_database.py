# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

import glob
import json
from typing import (
    Any,
    Dict,
    List,
)

URL_ADVISORY_DATABASE: str = "https://github.com/github/advisory-database.git"
Advisories = Dict[str, Dict[str, str]]


def get_vulnerabilities_ranges(
    affected: List[dict],
    vuln_id: str,
    platform: str,
    advisories: Advisories,
) -> None:
    for pkg_obj in affected:
        package: Dict[str, Any] = pkg_obj.get("package") or {}
        ecosystem: str = str(package.get("ecosystem"))
        if ecosystem.lower() != platform:
            continue
        pkg_name: str = str(package.get("name")).lower()
        ranges: List[Dict[str, Any]] = pkg_obj.get("ranges") or []
        for range_ver in ranges:
            events: List[Dict[str, str]] = range_ver.get("events") or []
            str_range: str
            introduced = f">={events[0].get('introduced')}"
            fixed = f" <{events[1].get('fixed')}" if len(events) > 1 else ""
            str_range = f"{introduced}{fixed}".lower()
            if pkg_name not in advisories:
                advisories.update({pkg_name: {}})
            if ghsa_vuln := advisories[pkg_name].get(vuln_id):
                advisories[pkg_name][vuln_id] = " || ".join(
                    (ghsa_vuln, str_range)
                )
            else:
                advisories[pkg_name].update({vuln_id: str_range})


def get_advisory_database(
    advisories: Advisories, tmp_dirname: str, platform: str
) -> dict:
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
                get_vulnerabilities_ranges(
                    affected, vuln_id, platform, advisories
                )
            except json.JSONDecodeError as exc:
                print(exc)

    return advisories
