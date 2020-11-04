# Third party libraries
import pytest

# Local libraries
from forces.report import (
    create_findings_dict,
    generate_report,
)
from forces.utils.model import ForcesConfig


@pytest.mark.asyncio  # type: ignore
async def test_create_findings_dict(
    test_group: str,
    test_token: str,
) -> None:
    findings_dict_1 = await create_findings_dict(
        project=test_group, api_token=test_token)
    for find in findings_dict_1.values():
        for key in ('open', 'closed', 'accepted'):
            assert key in find

    findings_dict_2 = await create_findings_dict(
        project=test_group, api_token=test_token)
    for find in findings_dict_2.values():
        for key in ('open', 'closed', 'accepted'):
            assert key in find


@pytest.mark.asyncio  # type: ignore
async def test_generate_report1(
    test_group: str,
    test_token: str,
    test_finding: str,
) -> None:
    config = ForcesConfig(group=test_group)
    report = await generate_report(
        config=config,
        api_token=test_token,
    )
    assert report['summary']['total'] == 5
    assert report['summary']['open']['total'] == 3
    assert report['summary']['closed']['total'] == 2

    findings = [
        find for find in report['findings'] if find['id'] == test_finding
    ]
    assert len(findings) == 1


@pytest.mark.asyncio  # type: ignore
async def test_generate_report2(
    test_group: str,
    test_token: str,
    test_finding: str,
) -> None:
    config = ForcesConfig(group=test_group)
    report = await generate_report(
        config=config,
        api_token=test_token,
    )
    findings = [
        find for find in report['findings'] if find['id'] == test_finding
    ]
    assert len(findings[0]['vulnerabilities']) == 5
