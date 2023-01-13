from . import (
    get_result,
)
import pytest
from schedulers import (
    update_group_toe_vulns as schedulers_update_group_toe_vulns,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_toe_vulnerabilities")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@fluidattacks.com"],
    ],
)
async def test_update_toe_vulnerabilities(populate: bool, email: str) -> None:
    assert populate
    group_name = "group1"
    await schedulers_update_group_toe_vulns.main()

    result = await get_result(user=email, group_name=group_name)
    assert result["data"]["group"]["toeInputs"] == {
        "edges": [
            {
                "node": {
                    "component": "https://app.fluidattacks.com/",
                    "entryPoint": "button",
                    "hasVulnerabilities": False,
                }
            },
            {
                "node": {
                    "component": "https://app.test.com/",
                    "entryPoint": "button-test",
                    "hasVulnerabilities": True,
                }
            },
        ]
    }

    lines = result["data"]["group"]["toeLines"]["edges"]
    assert lines[0]["node"]["filename"] == "test1/test.sh"
    assert lines[0]["node"]["hasVulnerabilities"] is True

    assert result["data"]["group"]["toePorts"] == {
        "edges": [
            {
                "node": {
                    "address": "192.168.1.7",
                    "hasVulnerabilities": False,
                    "port": 77777,
                }
            },
            {
                "node": {
                    "address": "192.168.1.1",
                    "hasVulnerabilities": True,
                    "port": 2321,
                }
            },
        ]
    }
