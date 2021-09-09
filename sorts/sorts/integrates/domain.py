from integrates.dal import (  # type: ignore
    get_vulnerabilities,
    Vulnerability,
    VulnerabilityKindEnum,
)
import os
from sorts.utils.logs import (
    log,
)
from sorts.utils.static import (
    read_allowed_names,
)
import time
from typing import (
    List,
    Set,
)


def filter_allowed_files(
    vuln_files: List[str], ignore_repos: List[str]
) -> List[str]:
    """Leave files with allowed names and filter out from ignored repos"""
    allowed_vuln_files: List[str] = []
    extensions, composites = read_allowed_names()
    for vuln_file in vuln_files:
        vuln_repo: str = vuln_file.split(os.path.sep)[0]
        if vuln_repo not in ignore_repos:
            vuln_file_name: str = os.path.basename(vuln_file)
            vuln_file_extension: str = os.path.splitext(vuln_file_name)[
                1
            ].strip(".")
            if (
                vuln_file_extension in extensions
                or vuln_file_name in composites
            ):
                allowed_vuln_files.append(vuln_file)
    return allowed_vuln_files


def get_unique_vuln_files(group: str) -> List[str]:
    """Removes repeated files from group vulnerabilities"""
    unique_vuln_files: Set[str] = set(get_vulnerable_lines(group))
    return sorted(unique_vuln_files)


def get_vulnerable_files(group: str, ignore_repos: List[str]) -> List[str]:
    """Gets vulnerable files to fill the training DataFrame"""
    timer: float = time.time()
    unique_vuln_files: List[str] = get_unique_vuln_files(group)
    allowed_vuln_files: List[str] = filter_allowed_files(
        unique_vuln_files, ignore_repos
    )
    log(
        "info",
        "Vulnerable files extracted after %.2f seconds",
        time.time() - timer,
    )
    return allowed_vuln_files


def get_vulnerable_lines(group: str) -> List[str]:
    """Fetches the vulnerable files from a group"""
    vulnerabilities: List[Vulnerability] = get_vulnerabilities(group)

    return [
        vuln.where
        for vuln in vulnerabilities
        if vuln.kind == VulnerabilityKindEnum.LINES
    ]
