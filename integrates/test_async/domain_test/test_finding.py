import os
import pytest
import pytz
import time
from datetime import datetime, timedelta

from asgiref.sync import async_to_sync
from collections import namedtuple
from graphql.type import GraphQLResolveInfo
from starlette.datastructures import UploadFile

from backend import mailer
from backend.domain.finding import (
    add_comment, get_age_finding, update_client_description,
    get_tracking_vulnerabilities, update_treatment,
    handle_acceptation, validate_evidence, mask_finding,
    approve_draft, compare_historic_treatments, list_findings,
    list_drafts
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
from backend.utils import (
    datetime as datetime_utils,
)

from backend_new import settings

from test_async.utils import create_dummy_session

pytestmark = [
    pytest.mark.asyncio,
]


async def test_get_email_recipients():
    comment_type = 'comment'
    finding_id = '436992569'

    test_data = await mailer.get_email_recipients(comment_type, finding_id)
    assert isinstance(test_data, list)
    assert isinstance(test_data[0], str)

async def test_get_tracking_vulnerabilities():
    finding_id = '436992569'
    vulnerabilities = await list_vulnerabilities_async([finding_id])
    test_data = get_tracking_vulnerabilities(vulnerabilities)
    expected_output = [
        {
            "cycle": 0,
            "open": 1,
            "closed": 0,
            "effectiveness": 0,
            "date": "2019-08-30",
            "new": 1,
            "in_progress": 0,
            "accepted": 0,
            "accepted_undefined": 0
        },
        {
            "cycle": 1,
            "open": 16,
            "closed": 0,
            "effectiveness": 0,
            "date": "2019-09-12",
            "new": 1,
            "in_progress": 0,
            "accepted": 0,
            "accepted_undefined": 0
        },
        {
            "cycle": 2,
            "open": 22,
            "closed": 4,
            "effectiveness": 15,
            "date": "2019-09-13",
            "new": 2,
            "in_progress": 0,
            "accepted": 0,
            "accepted_undefined": 0
        },
        {
            "cycle": 3,
            "open": 24,
            "closed": 4,
            "effectiveness": 14,
            "date": "2019-09-16",
            "new": 2,
            "in_progress": 0,
            "accepted": 0,
            "accepted_undefined": 0
        },
        {
            "cycle": 4,
            "open": 24,
            "closed": 4,
            "effectiveness": 14,
            "date": "2020-02-19",
            "new": 2,
            "in_progress": 0,
            "accepted": 0,
            "accepted_undefined": 0
        }
    ]
    assert test_data == expected_output

    finding_id = '463461507'
    vulnerabilities = await list_vulnerabilities_async([finding_id])
    test_data = get_tracking_vulnerabilities(vulnerabilities)
    expected_output = [
        {
            "cycle": 0,
            "open": 1,
            "closed": 0,
            "effectiveness": 0,
            "date": "2019-09-12",
            "new": 0,
            "in_progress": 1,
            "accepted": 0,
            "accepted_undefined": 0
        },
        {
            "cycle": 1,
            "open": 2,
            "closed": 0,
            "effectiveness": 0,
            "date": "2019-09-13",
            "new": 1,
            "in_progress": 0,
            "accepted": 1,
            "accepted_undefined": 0
        }
    ]
    assert test_data == expected_output

    finding_id = '463461507'
    vulnerabilities = await list_vulnerabilities_async([finding_id])
    test_data = get_tracking_vulnerabilities(vulnerabilities)
    expected_output = [
        {
            "cycle": 0,
            "open": 1,
            "closed": 0,
            "effectiveness": 0,
            "date": "2019-09-12",
            "new": 0,
            "in_progress": 1,
            "accepted": 0,
            "accepted_undefined": 0
        },
        {
            "cycle": 1,
            "open": 2,
            "closed": 0,
            "effectiveness": 0,
            "date": "2019-09-13",
            "new": 1,
            "in_progress": 0,
            "accepted": 1,
            "accepted_undefined": 0
        }
    ]
    assert test_data == expected_output

    finding_id = '422286126'
    vulnerabilities = await list_vulnerabilities_async([finding_id])
    test_data = get_tracking_vulnerabilities(vulnerabilities)
    expected_output = [
        {
            "cycle": 0,
            "open": 1,
            "closed": 0,
            "effectiveness": 0,
            "date": "2020-09-09",
            "new": 0,
            "in_progress": 1,
            "accepted": 0,
            "accepted_undefined": 0
        }
    ]
    assert test_data == expected_output

    finding_id = '463558592'
    vulnerabilities = await list_vulnerabilities_async([finding_id])
    test_data = get_tracking_vulnerabilities(vulnerabilities)
    expected_output = [
        {
            "cycle": 0,
            "open": 1,
            "closed": 1,
            "effectiveness": 50,
            "date": "2019-01-15",
            "new": 0,
            "in_progress": 0,
            "accepted": 1,
            "accepted_undefined": 0
        }
    ]
    assert test_data == expected_output

@pytest.mark.changes_db
async def test_update_treatment():
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
    values_new = {'treatment': 'NEW'}
    test_new = await update_treatment(finding_id, values_new, '')
    assert test_new is True

@pytest.mark.changes_db
async def test_update_client_description():
    finding_id = '463461507'
    org_id = 'ORG#f2e2777d-a168-4bea-93cd-d79142b294d2'
    info_to_check = {
        'historic_treatment': [{
                'date': '2020-01-01 12:00:00',
                'treatment': 'NEW',
                'user': 'unittest@fluidattacks.com'
            }],
        'severity': 5
    }
    acceptance_date = datetime_utils.get_as_str(
        datetime_utils.get_now_plus_delta(days=10)
    )
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
    acceptance_date = datetime_utils.get_as_str(
        datetime_utils.get_now_plus_delta(days=65)
    )
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
async def test_add_comment():
    request = await create_dummy_session('unittest@fluidattacks.com')
    info = GraphQLResolveInfo(None , None, None, None, None, None, None, None, None, None, request)
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
        info,
        'unittest@fluidattacks.com',
        comment_data,
        finding_id,
        'unittesting'
    )

    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    comment_data['created'] = current_time
    comment_data['modified'] = current_time
    comment_data['parent'] = str(comment_id)
    assert await add_comment(
        info,
        'unittest@fluidattacks.com',
        comment_data,
        finding_id,
        'unittesting'
    )

@pytest.mark.changes_db
async def test_handle_acceptation():
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
async def test_mask_finding():
    finding_id = '475041524'
    test_data = await mask_finding(finding_id)
    expected_output = True
    assert isinstance(test_data, bool)
    assert test_data == expected_output

    finding = await finding_dal.get_finding(finding_id)
    assert finding.get('historic_treatment', [{}])[-1].get('user') == 'Masked'

async def test_validate_evidence_exploit():
    evidence_id = 'exploit'
    filename = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(filename, '../mock/test-exploit.py')
    mime_type = 'text/x-python'
    with open(filename, 'rb') as test_file:
        uploaded_file = UploadFile(test_file.name, test_file, mime_type)
        test_data = await validate_evidence(evidence_id, uploaded_file)
    expected_output = True
    assert isinstance(test_data, bool)
    assert test_data == expected_output

async def test_validate_evidence_exploit_invalid_type():
    evidence_id = 'exploit'
    filename = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(filename, '../mock/test-anim.gif')
    mime_type = 'image/gif'
    with open(filename, 'rb') as test_file:
        uploaded_file = UploadFile(test_file.name, test_file, mime_type)
        with pytest.raises(InvalidFileType) as context:
            await validate_evidence(evidence_id, uploaded_file)

async def test_validate_evidence_records():
    evidence_id = 'fileRecords'
    filename = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(filename, '../mock/test-file-records.csv')
    mime_type = 'text/csv'
    with open(filename, 'rb') as test_file:
        uploaded_file = UploadFile(test_file.name, test_file, mime_type)
        test_data = await validate_evidence(evidence_id, uploaded_file)
    expected_output = True
    assert isinstance(test_data, bool)
    assert test_data == expected_output

async def test_validate_evidence_records_invalid_type():
    evidence_id = 'fileRecords'
    filename = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(filename, '../mock/test-anim.gif')
    mime_type = 'image/gif'
    with open(filename, 'rb') as test_file:
        uploaded_file = UploadFile(test_file.name, test_file, mime_type)
        with pytest.raises(InvalidFileType) as context:
            await validate_evidence(evidence_id, uploaded_file)

async def test_validate_acceptance_severity():
    finding_id = '463461507'
    org_id = 'ORG#f2e2777d-a168-4bea-93cd-d79142b294d2'
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

async def test_validate_number_acceptations():
    finding_id = '463461507'
    org_id = 'ORG#f2e2777d-a168-4bea-93cd-d79142b294d2'
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
async def test_approve_draft():
    finding_id = '475041513'
    reviewer_email = 'unittest@fluidattacks.com'
    test_success, test_date = await approve_draft(
        finding_id, reviewer_email)
    tzn = pytz.timezone(settings.TIME_ZONE)
    today = datetime.now(tz=tzn)
    date = str(today.strftime('%Y-%m-%d %H:%M'))
    expected_output =  True, date
    assert isinstance(test_success, bool)
    assert isinstance(test_date, str)
    assert test_success, test_date[-3] == expected_output

def test_compare_historic_treatments():
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


async def test_list_findings() -> None:
    project_name = 'unittesting'
    test_data = await list_findings([project_name])
    expected_output = [
        '988493279', '422286126', '436992569', '463461507', '463558592', '457497316'
    ]
    assert expected_output == test_data[0]


async def test_list_drafts() -> None:
    project_name = 'unittesting'
    test_data = await list_drafts([project_name])
    expected_output = ['560175507']
    assert expected_output == test_data[0]


async def test_list_drafts_deleted() -> None:
    projects_name = ['continuoustesting']
    test_data = await list_drafts(projects_name)
    expected_output = ['818828206', '836530833', '475041524']
    assert sorted(expected_output) == sorted(test_data[0])
    test_data = await list_drafts(projects_name, include_deleted=True)
    expected_output = ['818828206', '836530833', '475041524', '991607942']
    assert sorted(expected_output) == sorted(test_data[0])
