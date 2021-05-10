# Standard library
import re
from string import (
    hexdigits,
)

# Local libraries
from custom_exceptions import (
    InvalidVulnCommitHash,
    InvalidVulnSpecific,
    InvalidVulnWhere,
)


def validate_specific(specific: str) -> None:
    if not specific.isdigit():
        raise InvalidVulnSpecific.new()


def validate_commit_hash(vuln_commit: str) -> None:
    if len(vuln_commit) != 40 or not set(hexdigits).issuperset(
        set(vuln_commit)
    ):
        raise InvalidVulnCommitHash.new()


def validate_where(where: str) -> None:
    if not re.match("^(?!=)+[^/]+/.+$", where):
        raise InvalidVulnWhere.new()
