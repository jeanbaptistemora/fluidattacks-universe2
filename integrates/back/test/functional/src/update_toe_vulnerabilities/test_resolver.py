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
                    "component": "192.168.1.7",
                    "entryPoint": "77777",
                    "hasVulnerabilities": True,
                }
            },
            {
                "node": {
                    "component": "192.168.1.1",
                    "entryPoint": "2321",
                    "hasVulnerabilities": True,
                }
            },
            {
                "node": {
                    "component": "192.168.1.20",
                    "entryPoint": "9999",
                    "hasVulnerabilities": False,
                }
            },
        ]
    }

    assert result["data"]["group"]["toeLines"] == {
        "edges": [
            {
                "node": {
                    "filename": "test1/test.sh",
                    "hasVulnerabilities": True,
                }
            },
            {
                "node": {
                    "filename": "test2/test#.config",
                    "hasVulnerabilities": True,
                }
            },
            {
                "node": {
                    "filename": "test3/test.sh",
                    "hasVulnerabilities": False,
                }
            },
        ]
    }
