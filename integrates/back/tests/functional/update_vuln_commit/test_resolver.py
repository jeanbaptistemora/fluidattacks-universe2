from . import (
    query,
)
from custom_exceptions import (
    ExpectedVulnToBeOfLinesType,
    InvalidVulnCommitHash,
    InvalidVulnSpecific,
    InvalidVulnWhere,
)
import pytest
from typing import (
    Any,
    Dict,
)

# Constants
STAKEHOLDER_GOOD = "admin@gmail.com"
VULN_COMMIT_GOOD = "12654acf06e5a66913779d1298bbf76063bacecd"
VULN_ID_GOOD = "be09edb7-cd5c-47ed-bee4-97c645acdce8"
VULN_WHERE_GOOD = "a/b"
VULN_SPECIFIC_GOOD = "10"


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_vuln_commit")
async def test_good_user_good_vuln() -> None:
    result: Dict[str, Any] = await query(
        stakeholder=STAKEHOLDER_GOOD,
        vuln_commit=VULN_COMMIT_GOOD,
        vuln_id=VULN_ID_GOOD,
        vuln_where=VULN_WHERE_GOOD,
        vuln_specific=VULN_SPECIFIC_GOOD,
    )
    assert result["data"]["updateVulnCommit"]["success"]


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_vuln_commit")
async def test_good_user_bad_commit() -> None:
    result = await query(
        stakeholder=STAKEHOLDER_GOOD,
        vuln_commit="0123456",
        vuln_id=VULN_ID_GOOD,
        vuln_where=VULN_WHERE_GOOD,
        vuln_specific=VULN_SPECIFIC_GOOD,
    )
    assert result["errors"][0]["message"] == InvalidVulnCommitHash.msg
    result = await query(
        stakeholder=STAKEHOLDER_GOOD,
        vuln_commit="x" * 40,
        vuln_id=VULN_ID_GOOD,
        vuln_where=VULN_WHERE_GOOD,
        vuln_specific=VULN_SPECIFIC_GOOD,
    )
    assert result["errors"][0]["message"] == InvalidVulnCommitHash.msg


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_vuln_commit")
async def test_good_user_bad_id() -> None:
    result = await query(
        stakeholder=STAKEHOLDER_GOOD,
        vuln_commit=VULN_COMMIT_GOOD,
        vuln_id="not-exists",
        vuln_where=VULN_WHERE_GOOD,
        vuln_specific=VULN_SPECIFIC_GOOD,
    )
    assert (
        result["errors"][0]["message"] == "Exception - Vulnerability not found"
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_vuln_commit")
async def test_good_user_bad_where() -> None:
    result = await query(
        stakeholder=STAKEHOLDER_GOOD,
        vuln_commit=VULN_COMMIT_GOOD,
        vuln_id=VULN_ID_GOOD,
        vuln_where="a\\b",
        vuln_specific=VULN_SPECIFIC_GOOD,
    )
    assert result["errors"][0]["message"] == InvalidVulnWhere.msg


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_vuln_commit")
async def test_good_user_bad_specific() -> None:
    result = await query(
        stakeholder=STAKEHOLDER_GOOD,
        vuln_commit=VULN_COMMIT_GOOD,
        vuln_id=VULN_ID_GOOD,
        vuln_where=VULN_WHERE_GOOD,
        vuln_specific="string",
    )
    assert result["errors"][0]["message"] == InvalidVulnSpecific.msg


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_vuln_commit")
async def test_good_user_bad_type() -> None:
    result = await query(
        stakeholder=STAKEHOLDER_GOOD,
        vuln_commit=VULN_COMMIT_GOOD,
        vuln_id="77b88be2-37c8-429b-a519-029b1c32fdcd",
        vuln_where=VULN_WHERE_GOOD,
        vuln_specific=VULN_SPECIFIC_GOOD,
    )
    assert result["errors"][0]["message"] == ExpectedVulnToBeOfLinesType.msg


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_vuln_commit")
async def test_bad_user_good_vuln() -> None:
    result: Dict[str, Any] = await query(
        stakeholder="someone-without-access@gmail.com",
        vuln_commit=VULN_COMMIT_GOOD,
        vuln_id=VULN_ID_GOOD,
        vuln_where=VULN_WHERE_GOOD,
        vuln_specific=VULN_SPECIFIC_GOOD,
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
