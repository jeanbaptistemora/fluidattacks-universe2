from custom_exceptions import (
    InvalidParameter,
    InvalidPath,
    InvalidPort,
    InvalidSource,
    InvalidVulnCommitHash,
    InvalidVulnSpecific,
    InvalidVulnWhere,
)
from db_model.enums import (
    Source,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityType,
)
import pytest
from vulnerabilities.domain.validations import (
    validate_path_deco,
    validate_source_deco,
    validate_specific_deco,
    validate_updated_commit_deco,
    validate_where_deco,
)

pytestmark = [
    pytest.mark.asyncio,
]


def test_validate_source_deco() -> None:
    @validate_source_deco("source")
    def decorated_func(source: Source) -> Source:
        return source

    assert decorated_func(source="ANALYST")
    with pytest.raises(InvalidSource):
        decorated_func(source="USER")


def test_validate_path_deco() -> None:
    @validate_path_deco("path")
    def decorated_func(path: str) -> str:
        return path

    assert decorated_func(path="C:/Program Files/MyApp")
    with pytest.raises(InvalidPath):
        decorated_func(path="C:\\Program Files\\MyApp")


def test_validate_where_deco() -> None:
    @validate_where_deco("where")
    def decorated_func(where: str) -> str:
        return where

    assert decorated_func(where="MyVulnerability")
    with pytest.raises(InvalidVulnWhere):
        decorated_func(where="=MyVulnerability")


def test_validate_specific_deco() -> None:
    @validate_specific_deco("vuln_type", "specific")
    def decorated_func(vuln_type: str, specific: str) -> str:
        return vuln_type + specific

    assert decorated_func(vuln_type=VulnerabilityType.LINES, specific="210")
    assert decorated_func(vuln_type=VulnerabilityType.PORTS, specific="8080")
    with pytest.raises(InvalidVulnSpecific):
        decorated_func(vuln_type=VulnerabilityType.LINES, specific="line 200")
    with pytest.raises(InvalidPort):
        decorated_func(vuln_type=VulnerabilityType.PORTS, specific="70000")
    with pytest.raises(InvalidVulnSpecific):
        decorated_func(vuln_type=VulnerabilityType.PORTS, specific="port 80")


def test_validate_updated_commit_deco() -> None:
    @validate_updated_commit_deco("vuln_type", "commit")
    def decorated_func(vuln_type: str, commit: str) -> str:
        return vuln_type + commit

    assert decorated_func(
        vuln_type=VulnerabilityType.LINES,
        commit="da39a3ee5e6b4b0d3255bfef95601890afd80709",
    )
    with pytest.raises(InvalidParameter):
        decorated_func(
            vuln_type=VulnerabilityType.PORTS,
            commit="da39a3ee5e6b4b0d3255bfef95601890afd80709",
        )
    with pytest.raises(InvalidVulnCommitHash):
        decorated_func(
            vuln_type=VulnerabilityType.LINES,
            commit="da39a3ee5e6b4b0d3255bfey95601890afd80709",
        )
    with pytest.raises(InvalidVulnCommitHash):
        decorated_func(
            vuln_type=VulnerabilityType.LINES,
            commit="da39a3ee5e6b4b0d3255bfef95601890afd80709543",
        )
