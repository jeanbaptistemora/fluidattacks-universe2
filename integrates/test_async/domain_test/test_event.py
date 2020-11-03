import os
from time import time
import pytest
from aniso8601 import parse_datetime

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from backend.domain import event as event_domain
from backend.dal import (
    comment as comment_dal,
    event as event_dal
)
from backend.exceptions import (
    EventAlreadyClosed, EventNotFound, InvalidCommentParent,
    InvalidFileType, InvalidFileSize
)

pytestmark = [
    pytest.mark.asyncio,
]


async def test_get_event():
    event_id = '418900971'
    test_data = await event_domain.get_event(event_id)
    expected_output = 'unittesting'
    assert test_data.get('project_name') == expected_output
    with pytest.raises(EventNotFound):
        await event_domain.get_event('000001111')

@pytest.mark.changes_db
async def test_create_event():
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
    assert await event_domain.create_event(**attrs)

@pytest.mark.changes_db
async def test_create_event_file_image():
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
    imagename = os.path.dirname(os.path.abspath(__file__))
    imagename = os.path.join(imagename, '../mock/test-anim.gif')
    with open(filename, 'rb') as test_file:
        uploaded_file = SimpleUploadedFile(name=test_file.name,
                                           content=test_file.read(),
                                           content_type='text/csv')
        with open(imagename, 'rb') as image_test:
            uploaded_image = SimpleUploadedFile(name=image_test.name,
                                                content=image_test.read(),
                                                content_type='image/gif')
            test_data = await event_domain.create_event(
                **attrs,
                file=uploaded_file,
                image=uploaded_image
            )
    expected_output = True
    assert isinstance(test_data, bool)
    assert test_data == expected_output

@pytest.mark.changes_db
async def test_solve_event():
    assert await event_domain.solve_event(
        event_id='538745942',
        affectation=1,
        analyst_email='unittesting@fluidattacks.com',
        date=parse_datetime('2019-12-09T05:00:00.000Z'))
    event = await event_domain.get_event('538745942')
    assert event['historic_state'][-1]['state'] == 'SOLVED'
    with pytest.raises(EventAlreadyClosed):
        assert await event_domain.solve_event(
            event_id='538745942',
            affectation=1,
            analyst_email='unittesting@fluidattacks.com',
            date=parse_datetime('2019-12-09T05:00:00.000Z'))

@pytest.mark.changes_db
async def test_add_comment():
    event_id = '538745942'
    user_email = 'integratesmanager@gmail.com'
    comment_id = int(round(time() * 1000))
    parent = '0'
    comment_data = {
        'comment_type': 'event',
        'parent': parent,
        'content': 'comment test',
        'user_id': comment_id
    }
    comment_id, success = await event_domain.add_comment(
        user_email,
        comment_data,
        event_id,
        parent
    )
    assert success
    assert comment_id

    comment_data['content'] = 'comment test 2'
    comment_data['parent'] = str(comment_id)
    comment_data['user_id'] = int(round(time() * 1000))
    comment_id, success = await event_domain.add_comment(
        user_email,
        comment_data,
        event_id,
        parent=str(comment_id)
    )
    assert success
    assert comment_id

    with pytest.raises(InvalidCommentParent):
        comment_data['parent'] = str(comment_id + 1)
        comment_data['user_id'] = int(round(time() * 1000))
        assert await event_domain.add_comment(
            user_email,
            comment_data,
            event_id,
            parent=str(comment_id + 1)
        )

@pytest.mark.changes_db
async def test_update_evidence():
    event_id = '418900978'
    evidence_type = 'records'
    filename = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(filename, '../mock/test-file-records.csv')
    with open(filename, 'rb') as test_file:
        uploaded_file = SimpleUploadedFile(name=test_file.name,
                                            content=test_file.read(),
                                            content_type='text/csv')
        test_data = await event_domain.update_evidence(
            event_id, evidence_type, uploaded_file)
    expected_output = True
    assert isinstance(test_data, bool)
    assert test_data == expected_output

@pytest.mark.changes_db
async def test_update_evidence_attribute_error():
    event_id = '418900978'
    evidence_type = 'records'
    test_data = await event_domain.update_evidence(
        event_id, evidence_type, '')
    expected_output = False
    assert isinstance(test_data, bool)
    assert test_data == expected_output

async def test_validate_evidence_invalid_image_type():
    evidence_type = 'evidence'
    filename = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(filename, '../mock/test-file-records.csv')
    with open(filename, 'rb') as test_file:
        uploaded_file = SimpleUploadedFile(name=test_file.name,
                                            content=test_file.read(),
                                            content_type='text/csv')
        with pytest.raises(InvalidFileType) as context:
            await event_domain.validate_evidence(evidence_type, uploaded_file)
        assert 'Exception - Invalid File Type: EVENT_IMAGE' in str(context.value)

async def test_validate_evidence_invalid_file_size():
    evidence_type = 'evidence'
    filename = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(filename, '../mock/test-big-image.jpg')
    with open(filename, 'rb') as test_file:
        uploaded_file = SimpleUploadedFile(name=test_file.name,
                                            content=test_file.read(),
                                            content_type='image/jpg')
        with pytest.raises(InvalidFileSize) as context:
            await event_domain.validate_evidence(evidence_type, uploaded_file)
        assert 'Exception - Invalid File Size' in str(context.value)

@pytest.mark.changes_db
async def test_mask_event():
    event_id = '418900971'
    comment_id = int(round(time() * 1000))
    comment_data = {
        'comment_type': 'event',
        'parent': '0',
        'content': 'comment test',
        'user_id': comment_id
    }
    comment_id, success = await event_domain.add_comment(
        'integratesmanager@gmail.com',
        comment_data,
        event_id,
        parent='0'
    )
    evidence_type = 'records'
    filename = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(filename, '../mock/test-file-records.csv')
    with open(filename, 'rb') as test_file:
        uploaded_file = SimpleUploadedFile(
            name=test_file.name,
            content=test_file.read(),
            content_type='text/csv'
        )
        await event_domain.update_evidence(
            event_id,
            evidence_type,
            uploaded_file
        )
    evidence_prefix = f'unittesting/{event_id}'

    assert success
    assert len(await comment_dal.get_comments('event', int(event_id))) >= 1
    assert len(await event_dal.search_evidence(evidence_prefix)) >=1

    test_data = await event_domain.mask(event_id)
    expected_output = True

    assert isinstance(test_data, bool)
    assert test_data == expected_output
    assert len(await comment_dal.get_comments('event', int(event_id))) == 0
    assert len(await event_dal.search_evidence(evidence_prefix)) == 0

    event = await event_domain.get_event(event_id)
    assert event.get('detail') == 'Masked'
