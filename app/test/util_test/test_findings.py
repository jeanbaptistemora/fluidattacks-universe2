import os
from collections import OrderedDict

from django.test import TestCase

from app.utils.findings import (
    _get_evidence, _download_evidence_file, get_records_from_file,
    get_exploit_from_file
)


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
                [(u'song', u'a million little pieces'),
                 (u'artist', u'placebo'),
                 (u'year', u'2010')]),
            OrderedDict(
                [(u'song', u'heart shaped box'),
                 (u'artist', u'nirvana'),
                 (u'year', u'1992')]),
            OrderedDict(
                [(u'song', u'zenith'),
                 (u'artist', u'ghost'),
                 (u'year', u'2015')]),
            OrderedDict(
                [(u'song', u'hysteria'),
                 (u'artist', u'def leppard'),
                 (u'year', u'1987')])]
        assert test_data == expected_output

    def test_get_exploit_from_file(self):
        project_name = 'unittesting'
        finding_id = '422286126'
        file_name = 'unittesting-422286126-38307199-exploit.py'
        test_data = get_exploit_from_file(project_name, finding_id, file_name)
        expected_output = 'print "It works!"\n'
        assert test_data == expected_output
