import os
import pytest
import pytz
import time
from datetime import datetime, timedelta

from asgiref.sync import async_to_sync
from collections import namedtuple
from django.conf import settings
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from backend import mailer
from backend.domain.finding import (
    add_comment, get_age_finding, update_client_description,
    get_tracking_vulnerabilities, update_treatment,
    handle_acceptation, validate_evidence, mask_finding,
    approve_draft, compare_historic_treatments
)
from backend.domain.vulnerability import list_vulnerabilities_async
from backend.domain.organization import get_max_acceptance_days
from backend.dal import finding as finding_dal
from backend.exceptions import (
    InvalidAcceptanceDays,
    InvalidAcceptanceSeverity,
    InvalidDateFormat,
    InvalidDate,
    InvalidFileType,
    InvalidNumberAcceptations
)

pytestmark = [
    pytest.mark.asyncio,
]


class FindingTests(TestCase):

    def test_get_email_recipients(self):
        comment_type = 'comment'
        finding_id = '436992569'

        test_data = mailer.get_email_recipients(comment_type, finding_id)
        assert isinstance(test_data, list)
        assert isinstance(test_data[0], str)

    async def test_get_tracking_vulnerabilities(self):
        finding_id = '436992569'
        vulnerabilities = await list_vulnerabilities_async([finding_id])
        test_data = await get_tracking_vulnerabilities(vulnerabilities)
        expected_output = {'date': '2019-08-30', 'effectiveness': 0,
                           'open': 1, 'closed': 0, 'cycle': 0}
        assert test_data[0] == expected_output

    @pytest.mark.changes_db
    async def test_update_treatment(self):
        finding_id = '463461507'
        date = datetime.now() + timedelta(days=181)
        date = date.strftime('%Y-%m-%d %H:%M:%S')
        values_in_progress = {'justification': 'This is a test treatment justification',
                              'treatment': 'IN PROGRESS', 'acceptance_date': date}
        test_in_progress = await update_treatment(
            finding_id,
            values_in_progress,
            'integratesuser@gmail.com'
        )
        assert test_in_progress is True
        vulns = await list_vulnerabilities_async([finding_id])
        assert 'treatment_manager' in vulns[0]
        values_new = {'treatment': 'NEW'}
        test_new = await update_treatment(finding_id, values_new, '')
        assert test_new is True
        vulns = await list_vulnerabilities_async([finding_id])
        assert 'treatment_manager' not in vulns[0]
        assert 'treatment_manager' not in vulns[1]

    @pytest.mark.changes_db
    async def test_update_client_description(self):
        finding_id = '463461507'
        org_id = 'ORG#708f518a-d2c3-4441-b367-eec85e53d134'
        info_to_check = {
            'historic_treatment': [{
                    'date': '2020-01-01 12:00:00',
                    'treatment': 'NEW',
                    'user': 'unittest@fluidattacks.com'
                }],
            'severity': 5
        }
        acceptance_date = (
            datetime.now() + timedelta(days=10)
        ).strftime('%Y-%m-%d %H:%M:%S')
        values_accepted = {
            'justification': 'This is a test treatment justification',
            'bts_url': '',
            'treatment': 'ACCEPTED',
            'acceptance_date': acceptance_date
        }
        test_accepted = await update_client_description(
            finding_id,
            values_accepted,
            org_id,
            info_to_check,
            'unittesting@fluidattacks.com',
        )
        assert test_accepted is True

        max_acceptance_days = await get_max_acceptance_days(org_id)
        assert max_acceptance_days == 60
        acceptance_date = (
            datetime.now() + timedelta(days=65)
        ).strftime('%Y-%m-%d %H:%M:%S')
        values_accepted_date_error = {
            'justification': 'This is a test treatment justification',
            'bts_url': '',
            'treatment': 'ACCEPTED',
            'acceptance_date': acceptance_date
        }
        with pytest.raises(InvalidAcceptanceDays):
            assert await update_client_description(
                finding_id,
                values_accepted_date_error,
                org_id,
                info_to_check,
                'unittesting@fluidattacks.com'
            )

        acceptance_date = (
            datetime.now() + timedelta(days=10)
        ).strftime('%Y/%m/%d %H:%M:%S')
        values_accepted_format_error = {
            'justification': 'This is a test treatment justification',
            'bts_url': '',
            'treatment': 'ACCEPTED',
            'acceptance_date': acceptance_date
        }
        with pytest.raises(InvalidDateFormat):
            assert await update_client_description(
                finding_id,
                values_accepted_format_error,
                org_id,
                info_to_check,
                'unittesting@fluidattacks.com'
            )

    @pytest.mark.changes_db
    async def test_add_comment(self):
        finding_id = '463461507'
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        comment_id = int(round(time.time() * 1000))
        comment_data = {
            'comment_type': 'comment',
            'user_id': comment_id,
            'content': 'Test comment',
            'created': current_time,
            'fullname': 'unittesting',
            'modified': current_time,
            'parent': '0'
        }
        assert await add_comment(
            'unittest@fluidattacks.com', comment_data, finding_id, False)

        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        comment_data['created'] = current_time
        comment_data['modified'] = current_time
        comment_data['parent'] = str(comment_id)
        assert await add_comment(
            'unittest@fluidattacks.com', comment_data, finding_id, False)

    @pytest.mark.changes_db
    async def test_handle_acceptation(self):
        finding_id = '463461507'
        observations = 'Test observations'
        user_mail = 'unittest@fluidattacks.com'
        response = 'REJECTED'
        test_data = await handle_acceptation(
            finding_id,
            observations,
            user_mail,
            response
        )
        expected_output = True
        assert isinstance(test_data, bool)
        assert test_data == expected_output

    @pytest.mark.changes_db
    def test_mask_finding(self):
        finding_id = '475041524'
        test_data = mask_finding(finding_id)
        expected_output = True
        assert isinstance(test_data, bool)
        assert test_data == expected_output

        finding = async_to_sync(finding_dal.get_finding)(finding_id)
        assert finding.get('historic_treatment', [{}])[-1].get('user') == 'Masked'

    def test_validate_evidence_exploit(self):
        evidence_id = 'exploit'
        filename = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(filename, '../mock/test-exploit.py')
        with open(filename, 'rb') as test_file:
            uploaded_file = SimpleUploadedFile(name=test_file.name,
                                               content=test_file.read(),
                                               content_type='text/x-python')
        test_data = validate_evidence(evidence_id, uploaded_file)
        expected_output = True
        assert isinstance(test_data, bool)
        assert test_data == expected_output

    def test_validate_evidence_exploit_invalid_type(self):
        evidence_id = 'exploit'
        filename = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(filename, '../mock/test-anim.gif')
        with open(filename, 'rb') as test_file:
            uploaded_file = SimpleUploadedFile(name=test_file.name,
                                               content=test_file.read(),
                                               content_type='image/gif')
        with self.assertRaises(InvalidFileType) as context:
            validate_evidence(evidence_id, uploaded_file)
        self.assertTrue('Exception - Invalid File Type' in str(context.exception))

    def test_validate_evidence_records(self):
        evidence_id = 'fileRecords'
        filename = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(filename, '../mock/test-file-records.csv')
        with open(filename, 'rb') as test_file:
            uploaded_file = SimpleUploadedFile(name=test_file.name,
                                               content=test_file.read(),
                                               content_type='text/csv')
        test_data = validate_evidence(evidence_id, uploaded_file)
        expected_output = True
        assert isinstance(test_data, bool)
        assert test_data == expected_output

    def test_validate_evidence_records_invalid_type(self):
        evidence_id = 'fileRecords'
        filename = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(filename, '../mock/test-anim.gif')
        with open(filename, 'rb') as test_file:
            uploaded_file = SimpleUploadedFile(name=test_file.name,
                                               content=test_file.read(),
                                               content_type='image/gif')
        with self.assertRaises(InvalidFileType) as context:
            validate_evidence(evidence_id, uploaded_file)
        self.assertTrue('Exception - Invalid File Type' in str(context.exception))

    async def test_validate_acceptance_severity(self):
        finding_id = '463461507'
        org_id = 'ORG#708f518a-d2c3-4441-b367-eec85e53d134'
        info_to_check = {
            'historic_treatment': [{
                    'date': '2020-02-01 12:00:00',
                    'treatment': 'NEW',
                    'user': 'unittest@fluidattacks.com'
                }],
            'severity': 8.5
        }
        acceptance_date = (
            datetime.now() + timedelta(days=10)
        ).strftime('%Y-%m-%d %H:%M:%S')
        values_accepted = {
            'justification': 'This is a test treatment justification',
            'bts_url': '',
            'treatment': 'ACCEPTED',
            'acceptance_date': acceptance_date
        }
        with pytest.raises(InvalidAcceptanceSeverity):
            assert await update_client_description(
                finding_id,
                values_accepted,
                org_id,
                info_to_check,
                'unittesting@fluidattacks.com'
            )

    async def test_validate_number_acceptations(self):
        finding_id = '463461507'
        org_id = 'ORG#708f518a-d2c3-4441-b367-eec85e53d134'
        info_to_check = {
            'historic_treatment': [
                {
                    'acceptance_date': '2020-02-01 12:00:00',
                    'date': '2020-01-01 12:00:00',
                    'justification': 'Justification to accept the finding',
                    'treatment': 'ACCEPTED',
                    'user': 'unittest@fluidattacks.com'
                },
                {
                    'date': '2020-02-01 12:00:00',
                    'treatment': 'NEW',
                    'user': 'unittest@fluidattacks.com'
                }
            ],
            'severity': 5
        }
        acceptance_date = (
            datetime.now() + timedelta(days=10)
        ).strftime('%Y-%m-%d %H:%M:%S')
        values_accepted = {
            'justification': 'This is a test treatment justification',
            'bts_url': '',
            'treatment': 'ACCEPTED',
            'acceptance_date': acceptance_date
        }
        with pytest.raises(InvalidNumberAcceptations):
            assert await update_client_description(
                finding_id,
                values_accepted,
                org_id,
                info_to_check,
                'unittesting@fluidattacks.com'
            )

    @pytest.mark.changes_db
    async def test_approve_draft(self):
        finding_id = '475041513'
        reviewer_email = 'unittest@fluidattacks.com'
        test_success, test_date = await approve_draft(
            finding_id, reviewer_email)
        tzn = pytz.timezone(settings.TIME_ZONE)
        today = datetime.now(tz=tzn).today()
        date = str(today.strftime('%Y-%m-%d %H:%M'))
        expected_output =  True, date
        assert isinstance(test_success, bool)
        assert isinstance(test_date, str)
        assert test_success, test_date[-3] == expected_output

    def test_compare_historic_treatments(self):
        test_last_state = {
            'treatment': 'ACCEPTED',
            'date': '2020-01-03 12:46:10',
            'acceptance_date': '2020-01-03 12:46:10',
            'acceptance_status': 'SUBMITTED',
        }
        test_new_state = {
            'treatment': 'IN PROGRESS',
            'date': '2020-01-03 12:46:10',
        }
        test_new_state_date = test_last_state.copy()
        test_new_state_date['acceptance_date'] = '2020-02-03 12:46:10'
        assert compare_historic_treatments(test_last_state, test_new_state)
        assert compare_historic_treatments(test_last_state, test_new_state_date)
