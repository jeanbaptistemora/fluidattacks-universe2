from back.tests.functional.service_forces.utils import (
    get_result,
)
from dataloaders import (
    get_new_context,
)
import pytest


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("old")
async def test_group() -> None:
    context = get_new_context()
    group_name = "unittesting"

    query = f"""
        query {{
            group(groupName: "{group_name}"){{
                name
                hasSquad
                hasForces
                findings {{
                    id
                }}
                hasAsm
                openVulnerabilities
                closedVulnerabilities
                lastClosingVuln
                maxSeverity
                meanRemediate
                meanRemediateLowSeverity
                meanRemediateMediumSeverity
                openFindings
                totalFindings
                totalTreatment
                subscription
                deletionDate
                userDeletion
                tags
                description
                __typename
            }}
        }}
    """
    data = {"query": query}
    result = await get_result(data, context=context)
    assert "errors" not in result
    assert result["data"]["group"]["closedVulnerabilities"] == 8
    assert result["data"]["group"]["deletionDate"] == ""
    assert (
        result["data"]["group"]["description"]
        == "Integrates unit test project"
    )
    assert len(result["data"]["group"]["findings"]) == 6
    assert result["data"]["group"]["hasSquad"]
    assert result["data"]["group"]["hasForces"]
    assert result["data"]["group"]["hasAsm"]
    assert result["data"]["group"]["lastClosingVuln"] == 23
    assert result["data"]["group"]["maxSeverity"] == 6.3
    assert result["data"]["group"]["meanRemediate"] == 245
    assert result["data"]["group"]["meanRemediateLowSeverity"] == 232
    assert result["data"]["group"]["meanRemediateMediumSeverity"] == 287
    assert result["data"]["group"]["name"] == group_name
    assert result["data"]["group"]["openFindings"] == 5
    assert result["data"]["group"]["openVulnerabilities"] == 31
    assert result["data"]["group"]["subscription"] == "continuous"
    assert result["data"]["group"]["tags"] == ["test-projects"]
    assert result["data"]["group"]["totalFindings"] == 6
    assert (
        result["data"]["group"]["totalTreatment"]
        == '{"accepted": 1, "inProgress": 4, '
        '"acceptedUndefined": 2, "undefined": 25}'
    )
    assert result["data"]["group"]["userDeletion"] == ""
