# Third party libraries
import pytest

# Local libraries
from forces.report import (
    create_findings_dict,
    generate_report,
    process,
)


@pytest.mark.asyncio  # type: ignore
async def test_create_findings_dict(test_group: str, test_token: str):
    findings_dict_1 = await create_findings_dict(
        project=test_group, verbose_level=1, api_token=test_token)
    for find in findings_dict_1.values():
        assert 'vulnerabilities' not in find
        for key in ('open', 'closed', 'accepted'):
            key in find

    findings_dict_2 = await create_findings_dict(
        project=test_group, verbose_level=2, api_token=test_token)
    for find in findings_dict_2.values():
        assert 'vulnerabilities' in find
        for key in ('open', 'closed', 'accepted'):
            key in find


@pytest.mark.asyncio  # type: ignore
async def test_generate_report1(test_group: str, test_token: str,
                                test_finding: str):
    report = await generate_report(
        project=test_group, verbose_level=1, api_token=test_token)
    assert report['summary']['total'] == 5
    assert report['summary']['open'] == 3
    assert report['summary']['closed'] == 2

    findings = [
        find for find in report['findings'] if find['id'] == test_finding
    ]
    assert len(findings) == 1
    assert 'vulnerabilities' not in findings[0]


@pytest.mark.asyncio  # type: ignore
async def test_generate_report2(test_group: str, test_token: str,
                                test_finding: str):
    report = await generate_report(
        project=test_group, verbose_level=2, api_token=test_token)
    findings = [
        find for find in report['findings'] if find['id'] == test_finding
    ]
    assert len(findings[0]['vulnerabilities']) == 3


@pytest.mark.asyncio  # type: ignore
async def test_generate_report2(test_group: str, test_token: str,
                                test_finding: str):
    report = await generate_report(
        project=test_group, verbose_level=3, api_token=test_token)
    findings = [
        find for find in report['findings'] if find['id'] == test_finding
    ]
    assert len(findings[0]['vulnerabilities']) == 5


def test_proccess(test_group: str, test_token: str,
                  test_finding: str):
    result = process(project=test_group, verbose_level=3)
    assert result['summary']['total'] == 5
    assert result['summary']['open'] == 3
    assert result['summary']['closed'] == 2
