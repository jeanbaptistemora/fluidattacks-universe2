# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from custom_exceptions import (
    InvalidStream,
    InvalidVulnCommitHash,
    InvalidVulnerabilityAlreadyExists,
    InvalidVulnSpecific,
    InvalidVulnWhere,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityType,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
)
import re
from string import (
    hexdigits,
)
from typing import (
    Tuple,
)
from urllib.parse import (
    urlparse,
)
from vulnerabilities.domain.utils import (
    get_hash,
    get_hash_from_typed,
    get_path_from_integrates_vulnerability,
)


def validate_specific(specific: str) -> None:
    if not specific.isdigit():
        raise InvalidVulnSpecific.new()


def validate_uniqueness(
    *,
    finding_vulns_data: Tuple[Vulnerability, ...],
    vulnerability_where: str,
    vulnerability_specific: str,
    vulnerability_type: VulnerabilityType,
    vulnerability_id: str,
    vulnerability_commit: str,
) -> None:
    current_vuln = next(
        (item for item in finding_vulns_data if item.id == vulnerability_id),
        None,
    )
    if not current_vuln:
        return
    new_vuln_hash: int = get_hash(
        specific=vulnerability_specific,
        type_=vulnerability_type.value,
        where=get_path_from_integrates_vulnerability(
            vulnerability_where, vulnerability_type
        )[1]
        if current_vuln.type == VulnerabilityType.INPUTS
        else vulnerability_where,
        root_id=current_vuln.root_id,
    )
    for vuln in finding_vulns_data:
        vuln_hash = get_hash_from_typed(vuln)
        if (
            vuln_hash == new_vuln_hash
            and current_vuln.commit == vulnerability_commit
        ):
            raise InvalidVulnerabilityAlreadyExists.new()


def validate_commit_hash(vuln_commit: str) -> None:
    if len(vuln_commit) != 40 or not set(hexdigits).issuperset(
        set(vuln_commit)
    ):
        raise InvalidVulnCommitHash.new()


def validate_stream(where: str, stream: str) -> bool:
    url_parsed = urlparse(where)
    if (len(url_parsed.path) == 0 or url_parsed.path == "/") and not (
        stream.lower().startswith("home,")
        or stream.lower().startswith("query,")
    ):
        raise InvalidStream()
    return True


def validate_where(where: str) -> None:
    if not re.match("^[^=/]+[^/]*/.+$", where):
        raise InvalidVulnWhere.new()
