from custom_exceptions import (
    InvalidStream,
    InvalidVulnCommitHash,
    InvalidVulnerabilityAlreadyExists,
    InvalidVulnSpecific,
    InvalidVulnWhere,
)
from custom_types import (
    Vulnerability,
)
import re
from string import (
    hexdigits,
)
from typing import (
    List,
    Set,
)
from urllib.parse import (
    urlparse,
)
from vulnerabilities.domain.utils import (
    get_hash,
    get_hash_from_dict,
)


def validate_specific(specific: str) -> None:
    if not specific.isdigit():
        raise InvalidVulnSpecific.new()


def validate_uniqueness(
    *,
    finding_vulns_data: List[Vulnerability],
    vuln_where: str,
    vuln_specific: str,
    vuln_type: str,
) -> None:
    finding_vulns_hashes: Set[int] = set(
        map(get_hash_from_dict, finding_vulns_data)
    )
    vuln_hash: int = get_hash(
        specific=vuln_specific,
        type_=vuln_type,
        where=vuln_where,
    )

    if vuln_hash in finding_vulns_hashes:
        raise InvalidVulnerabilityAlreadyExists.new()


def validate_commit_hash(vuln_commit: str) -> None:
    if len(vuln_commit) != 40 or not set(hexdigits).issuperset(
        set(vuln_commit)
    ):
        raise InvalidVulnCommitHash.new()


def validate_stream(where: str, stream: str) -> bool:
    url_parsed = urlparse(where)
    if (
        len(url_parsed.path) == 0 or url_parsed.path == "/"
    ) and not stream.lower().startswith("home,"):
        raise InvalidStream()
    return True


def validate_where(where: str) -> None:
    if not re.match("^(?!=)+[^/]+/.+$", where):
        raise InvalidVulnWhere.new()
