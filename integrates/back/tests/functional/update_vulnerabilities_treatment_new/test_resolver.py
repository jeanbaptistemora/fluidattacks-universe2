from . import (
    get_result,
)
from freezegun.api import (
    freeze_time,
)
import pytest
from typing import (
    Any,
    Dict,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_vulnerabilities_treatment_new")
@pytest.mark.parametrize(
    ("email", "vulnerability", "treatment"),
    (
        (
            "customer@gmail.com",
            "be09edb7-cd5c-47ed-bee4-97c645acdce8",
            "ACCEPTED",
        ),
        (
            "customeradmin@gmail.com",
            "be09edb7-cd5c-47ed-bee4-97c645acdce9",
            "ACCEPTED_UNDEFINED",
        ),
        (
            "system_owner@fluidattacks.com",
            "be09edb7-cd5c-47ed-bee4-97c645acdc10",
            "IN_PROGRESS",
        ),
    ),
)
@freeze_time("2021-03-31")
async def test_update_vulnerabilities_treatment(
    populate: bool,
    email: str,
    vulnerability: str,
    treatment: str,
) -> None:
    assert populate
    finding_id: str = "475041513"
    result: Dict[str, Any] = await get_result(
        user=email,
        finding=finding_id,
        vulnerability=vulnerability,
        treatment=treatment,
    )
    assert "errors" not in result
    assert result["data"]["updateVulnerabilitiesTreatment"]["success"]


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_vulnerabilities_treatment_new")
@pytest.mark.parametrize(
    ("email", "vulnerability", "treatment"),
    (
        (
            "reattacker@gmail.com",
            "be09edb7-cd5c-47ed-bee4-97c645acdce8",
            "ACCEPTED",
        ),
        (
            "resourcer@gmail.com",
            "be09edb7-cd5c-47ed-bee4-97c645acdce8",
            "ACCEPTED",
        ),
        (
            "reviewer@gmail.com",
            "be09edb7-cd5c-47ed-bee4-97c645acdce8",
            "ACCEPTED",
        ),
    ),
)
@freeze_time("2021-03-31")
async def test_update_vulnerabilities_treatment_fail(
    populate: bool,
    email: str,
    vulnerability: str,
    treatment: str,
) -> None:
    assert populate
    finding_id: str = "475041513"
    result: Dict[str, Any] = await get_result(
        user=email,
        finding=finding_id,
        vulnerability=vulnerability,
        treatment=treatment,
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
