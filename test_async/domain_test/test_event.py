import os
from time import time
import pytest
from aniso8601 import parse_datetime

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from backend.domain import event as event_domain
from backend.exceptions import (
    EventAlreadyClosed, EventNotFound, InvalidCommentParent,
    InvalidFileType
)


class EventTests(TestCase):

    @pytest.mark.no_changes_db
    def test_get_event(self):
        event_id = '418900971'
        test_data = event_domain.get_event(event_id)
        expected_output = 'unittesting'
        assert test_data.get('project_name') == expected_output
        with pytest.raises(EventNotFound):
            event_domain.get_event('000001111')

    @pytest.mark.changes_db
    def test_create_event(self):
        attrs = {
            'action_after_blocking': 'TRAINING',
            'action_before_blocking': 'DOCUMENT_PROJECT',
            'accessibility': 'REPOSITORY',
            'analyst_email': 'unittesting@fluidattacks.com',
            'context': 'OTHER',
            'detail': 'Something happened.',
            'event_date': parse_datetime('2019-12-09T05:00:00.000Z'),
            'event_type': 'CLIENT_DETECTS_ATTACK',
            'project_name': 'unittesting'
        }
        assert event_domain.create_event(**attrs)

    @pytest.mark.changes_db
    def test_create_event_file_image(self):
        attrs = {
            'action_after_blocking': 'TRAINING',
            'action_before_blocking': 'DOCUMENT_PROJECT',
            'accessibility': 'REPOSITORY',
            'analyst_email': 'unittesting@fluidattacks.com',
            'context': 'OTHER',
            'detail': 'Something happened.',
            'event_date': parse_datetime('2019-12-09T05:00:00.000Z'),
            'event_type': 'CLIENT_DETECTS_ATTACK',
            'project_name': 'unittesting'
        }
        filename = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(filename, '../mock/test-file-records.csv')
        with open(filename, 'rb') as test_file:
            uploaded_file = SimpleUploadedFile(name=test_file.name,
                                                content=test_file.read(),
                                                content_type='text/csv')
        imagename = os.path.dirname(os.path.abspath(__file__))
        imagename = os.path.join(imagename, '../mock/test-anim.gif')
        with open(imagename, 'rb') as image_test:
            uploaded_image = SimpleUploadedFile(name=image_test.name,
                                                content=image_test.read(),
                                                content_type='image/gif')
        test_data = event_domain.create_event(**attrs, file=uploaded_file, image=uploaded_image)
        expected_output = True
        assert isinstance(test_data, bool)
        assert test_data == expected_output

    @pytest.mark.changes_db
    def test_solve_event(self):
        assert event_domain.solve_event(
            event_id='538745942',
            affectation=1,
            analyst_email='unittesting@fluidattacks.com',
            date=parse_datetime('2019-12-09T05:00:00.000Z'))
        event = event_domain.get_event('538745942')
        assert event['historic_state'][-1]['state'] == 'SOLVED'
        with pytest.raises(EventAlreadyClosed):
            assert event_domain.solve_event(
                event_id='538745942',
                affectation=1,
                analyst_email='unittesting@fluidattacks.com',
                date=parse_datetime('2019-12-09T05:00:00.000Z'))

    @pytest.mark.changes_db
    def test_add_comment(self):
        comment_id = int(round(time() * 1000))
        comment_id, success = event_domain.add_comment(
            comment_id=comment_id,
            content='comment test',
            event_id='538745942',
            parent='0',
            user_info={
                'user_email': 'unittesting@fluidattacks.com',
                'first_name': 'Unit',
                'last_name': 'test'
            })
        assert success
        assert comment_id

        comment_id, success = event_domain.add_comment(
            comment_id=int(round(time() * 1000)),
            content='comment test 2',
            event_id='538745942',
            parent=str(comment_id),
            user_info={
                'user_email': 'unittesting@fluidattacks.com',
                'first_name': 'Unit',
                'last_name': 'test'
            })
        assert success
        assert comment_id

        with pytest.raises(InvalidCommentParent):
            assert event_domain.add_comment(
                comment_id=int(round(time() * 1000)),
                content='comment test 2',
                event_id='538745942',
                parent=str(comment_id + 1),
                user_info={
                    'user_email': 'unittesting@fluidattacks.com',
                    'first_name': 'Unit',
                    'last_name': 'test'
                })

    @pytest.mark.changes_db
    def test_update_evidence(self):
        event_id = '418900978'
        evidence_type = 'records'
        filename = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(filename, '../mock/test-file-records.csv')
        with open(filename, 'rb') as test_file:
            uploaded_file = SimpleUploadedFile(name=test_file.name,
                                                content=test_file.read(),
                                                content_type='text/csv')
        test_data = event_domain.update_evidence(event_id, evidence_type, uploaded_file)
        expected_output = True
        assert isinstance(test_data, bool)
        assert test_data == expected_output

    @pytest.mark.changes_db
    def test_update_evidence_attribute_error(self):
        event_id = '418900978'
        evidence_type = 'records'
        test_data = event_domain.update_evidence(event_id, evidence_type, '')
        expected_output = False
        assert isinstance(test_data, bool)
        assert test_data == expected_output

    @pytest.mark.no_changes_db
    def test_validate_evidence_invalid_image_type(self):
        evidence_type = 'evidence'
        filename = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(filename, '../mock/test-file-records.csv')
        with open(filename, 'rb') as test_file:
            uploaded_file = SimpleUploadedFile(name=test_file.name,
                                                content=test_file.read(),
                                                content_type='text/csv')
        with self.assertRaises(InvalidFileType) as context:
            event_domain.validate_evidence(evidence_type, uploaded_file)
        self.assertTrue('Exception - Invalid File Type: EVENT_IMAGE' in str(context.exception))
