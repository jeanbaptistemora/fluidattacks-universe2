import os
import pytest
from collections import OrderedDict

from backend.dal.finding import get_finding
from newutils.findings import (
    _download_evidence_file,
    _get_evidence,
    format_data,
    get_exploit_from_file,
    get_reattack_requesters,
    get_records_from_file,
)


pytestmark = [
    pytest.mark.asyncio,
]

async def test_get_evidence():
    finding = await get_finding('422286126')
    name = 'test_name'
    item = [
        {'description': 'desc', 'file_url': 'test.png', 'name': 'test_name'},
        {'description': 'des2', 'file_url': 'test2.png', 'name':  'test_name_2'}]

    test_data = _get_evidence(name, item, finding)
    expected_output = {
        'description': 'desc', 'date': '2018-07-09 00:00:00', 'url': 'test.png'
    }
    assert test_data == expected_output

    name = 'non-existing name'
    test_data = _get_evidence(name, item, finding)
    expected_output = {'url': '', 'description': ''}
    assert test_data == expected_output

async def test_download_evidence_file():
    project_name = 'unittesting'
    finding_id = '422286126'
    file_name = 'unittesting-422286126-evidence_route_1.png'
    test_data = await _download_evidence_file(
        project_name, finding_id, file_name
    )
    expected_output = os.path.abspath(
        '/tmp/unittesting-422286126-evidence_route_1.png'
    )
    assert test_data == expected_output

async def test_get_records_from_file():
    project_name = 'unittesting'
    finding_id = '422286126'
    file_name = 'unittesting-422286126-evidence_file.csv'
    test_data = await get_records_from_file(project_name, finding_id, file_name)
    expected_output = [
        OrderedDict(
            [('song', 'a million little pieces'),
                ('artist', 'placebo'),
                ('year', '2010')]),
        OrderedDict(
            [('song', 'heart shaped box'),
                ('artist', 'nirvana'),
                ('year', '1992')]),
        OrderedDict(
            [('song', 'zenith'),
                ('artist', 'ghost'),
                ('year', '2015')]),
        OrderedDict(
            [('song', 'hysteria'),
                ('artist', 'def leppard'),
                ('year', '1987')])]

    assert test_data == expected_output

async def test_get_exploit_from_file():
    project_name = 'unittesting'
    finding_id = '422286126'
    file_name = 'unittesting-422286126-exploit.py'
    test_data = await get_exploit_from_file(project_name, finding_id, file_name)
    expected_output = 'print "It works!"\n'
    assert test_data == expected_output

async def test_format_data():
    finding_id = '422286126'
    finding_to_test = await get_finding(finding_id)
    test_data = list(format_data(finding_to_test).keys())
    expected_keys = [
        'context', 'modifiedSeverityScope', 'availabilityRequirement',
        'evidence', 'availabilityImpact','exploit',
        'modifiedPrivilegesRequired',
        'modifiedAttackVector', 'testType', 'id', 'affectedSystems',
        'attackVectorDesc', 'requirements', 'severity', 'cvssBasescore',
        'userInteraction', 'actor', 'cvssEnv', 'privilegesRequired',
        'interested', 'projectName',
        'finding', 'confidentialityImpact', 'integrityRequirement',
        'remediationLevel', 'cwe', 'leader', 'modifiedConfidentialityImpact',
        'files', 'modifiedUserInteraction', 'attackComplexity',
        'attackVector', 'reportConfidence', 'cvssTemporal', 'remediated',
        'clientProject', 'compromisedAttrs', 'findingType', 'historicState',
        'exploitable', 'confidentialityRequirement', 'records',
        'recordsNumber', 'modifiedAttackComplexity', 'severityScope',
        'cvssVersion', 'analyst', 'subscription',
        'effectSolution', 'reportLevel', 'scenario',
        'severityCvss', 'modifiedAvailabilityImpact', 'vulnerability',
        'findingId', 'threat', 'integrityImpact',
        'modifiedIntegrityImpact','relatedFindings',
        'exploitability']

    assert sorted(test_data) == sorted(expected_keys)

async def test_get_reattack_requesters():
    finding = await get_finding('463558592')
    recipients = get_reattack_requesters(
        finding.get('historic_verification', []),
        ['3bcdb384-5547-4170-a0b6-3b397a245465']
    )
    assert recipients == ['integratesuser@gmail.com']
