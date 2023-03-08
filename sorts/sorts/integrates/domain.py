from concurrent.futures import (
    ThreadPoolExecutor,
)
from integrates.dal import (
    get_finding_ids,
    get_vulnerabilities,
)
from integrates.typing import (
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
    open_vulnerability_files: List[str] = [
        vuln.where
        for vuln in get_vulnerable_lines(group)
        if (
            vuln.kind.value == VulnerabilityKindEnum.LINES.value
            and vuln.current_state == "VULNERABLE"
        )
    ]
    unique_vuln_files: Set[str] = set(open_vulnerability_files)

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


def get_vulnerable_lines(group: str) -> List[Vulnerability]:
    """Fetches the vulnerable files from a group"""
    vulnerabilities: List[Vulnerability] = []
    finding_ids: List[str] = get_finding_ids(group)
    with ThreadPoolExecutor(max_workers=8) as executor:
        for finding_vulnerabilities in executor.map(
            get_vulnerabilities, finding_ids
        ):
            vulnerabilities.extend(finding_vulnerabilities)  # type: ignore

    return vulnerabilities
