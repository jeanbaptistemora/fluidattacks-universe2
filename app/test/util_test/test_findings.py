import os
from collections import OrderedDict

from django.test import TestCase

from app.utils.findings import (
    _get_evidence, _download_evidence_file, get_records_from_file,
    get_exploit_from_file, format_data
)
from app.dal.finding import get_finding


class FindingsTests(TestCase):

    def test_get_evidence(self):
        name = 'test_name'
        item = [
            {'description': 'desc', 'file_url': 'test.png', 'name': 'test_name'},
            {'description': 'des2', 'file_url': 'test2.png', 'name':  'test_name_2'}]
        
        test_data = _get_evidence(name, item)
        expected_output = {
            'description': 'desc', 'url': 'test.png'
        }
        assert test_data == expected_output

        name = 'non-existing name'
        test_data = _get_evidence(name, item)
        expected_output = {'url': '', 'description': ''}
        assert test_data == expected_output

    def test_download_evidence_file(self):
        project_name = 'unittesting'
        finding_id = '422286126'
        file_name = 'unittesting-422286126-38307222-a.png'
        test_data = _download_evidence_file(
            project_name, finding_id, file_name
        )
        expected_output = os.path.abspath(
            '/tmp/unittesting-422286126-38307222-a.png'
        )
        assert test_data == expected_output

    def test_get_records_from_file(self):
        project_name = 'unittesting'
        finding_id = '422286126'
        file_name = 'unittesting-422286126-49412246-Untitled 1.csv'
        test_data = get_records_from_file(project_name, finding_id, file_name)
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

    def test_get_exploit_from_file(self):
        project_name = 'unittesting'
        finding_id = '422286126'
        file_name = 'unittesting-422286126-38307199-exploit.py'
        test_data = get_exploit_from_file(project_name, finding_id, file_name)
        expected_output = 'print "It works!"\n'
        assert test_data == expected_output

    def test_format_data(self):
        finding_id = '422286126'
        finding_to_test = get_finding(finding_id)
        test_data = list(format_data(finding_to_test).keys())
        expected_keys = [
            'context', 'modifiedSeverityScope', 'availabilityRequirement',
            'evidence', 'releaseDate', 'availabilityImpact','exploit',
            'modifiedPrivilegesRequired', 'verificationRequestDate',
            'modifiedAttackVector', 'testType', 'id', 'affectedSystems',
            'attackVectorDesc', 'requirements', 'severity', 'cvssBasescore',
            'userInteraction', 'actor', 'cvssEnv', 'privilegesRequired',
            'interested', 'treatmentJustification', 'treatment', 'projectName',
            'finding', 'confidentialityImpact', 'integrityRequirement',
            'remediationLevel', 'cwe', 'leader', 'modifiedConfidentialityImpact',
            'files', 'modifiedUserInteraction', 'attackComplexity',
            'attackVector', 'reportConfidence', 'cvssTemporal', 'remediated',
            'clientProject', 'compromisedAttrs', 'findingType', 'exploitable',
            'confidentialityRequirement', 'records', 'recordsNumber',
            'modifiedAttackComplexity', 'treatmentManager', 'severityScope',
            'cvssVersion', 'analyst', 'subscription', 'reportDate',
            'effectSolution', 'reportLevel', 'verificationDate', 'scenario',
            'severityCvss', 'modifiedAvailabilityImpact', 'age', 'vulnerability',
            'findingId', 'threat', 'lastVulnerability', 'integrityImpact',
            'modifiedIntegrityImpact','relatedFindings',
            'exploitability']
        assert True
        # Must be enabled later
        # assert test_data == expected_keys
