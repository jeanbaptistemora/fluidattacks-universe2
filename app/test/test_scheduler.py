from django.conf import settings
from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from jose import jwt

from app.scheduler import (
    is_not_a_fluidattacks_email, remove_fluid_from_recipients, get_event,
    is_a_unsolved_event, get_events_submissions, get_unsolved_events,
    extract_info_from_event_dict, get_external_recipients, get_finding_url
    )


class SchedulerTests(TestCase):

    def test_is_not_a_fluid_attacks_email(self):
        fluid_attacks_email = 'test@fluidattacks.com'
        not_fluid_attacks_email = 'test@test.com'
        assert is_not_a_fluidattacks_email(not_fluid_attacks_email)
        assert not is_not_a_fluidattacks_email(fluid_attacks_email)

    def test_remove_fluid_from_recipients(self):
        emails = [
            'test@fluidattacks.com', 'test2@fluidattacks.com', 'test@test.com',
            'test2@test.com'
        ]
        test_data = remove_fluid_from_recipients(emails)
        expected_output = ['test@test.com', 'test2@test.com']
        assert test_data == expected_output

    def test_get_event(self):
        request = RequestFactory().get('/')
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        request.session['username'] = 'unittest'
        request.session['company'] = 'unittest'
        request.session['role'] = 'admin'
        request.COOKIES[settings.JWT_COOKIE_NAME] = jwt.encode(
            {
                'user_email': 'unittest',
                'user_role': 'admin',
                'company': 'unittest'
            },
            algorithm='HS512',
            key=settings.JWT_SECRET,
        )
        event_id = '418900971'
        test_data = get_event(event_id, request)
        assert isinstance(test_data, dict)
        assert len(test_data) == 18
        for field in test_data.values():
            assert field is not None
        assert test_data['id'] == '418900971'
    
    def test_is_a_unsolved_event(self):
        dumb_unsolved_event = {'id': 'testid', 'eventStatus': 'UNSOLVED'}
        dumb_solved_event = {'id': 'testid', 'eventStatus': 'SOLVED'}
        assert is_a_unsolved_event(dumb_unsolved_event)
        assert not is_a_unsolved_event(dumb_solved_event)

    def test_get_events_submissions(self):
        project_name = 'unittesting'
        test_data = get_events_submissions(project_name)
        assert isinstance(test_data, list)
        for item in test_data:
            assert isinstance(item, dict)
            for value in item.values():
                assert value is not None

    def test_get_unsolved_events(self):
        request = RequestFactory().get('/')
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        request.session['username'] = 'unittest'
        request.session['company'] = 'unittest'
        request.session['role'] = 'admin'
        request.COOKIES[settings.JWT_COOKIE_NAME] = jwt.encode(
            {
                'user_email': 'unittest',
                'user_role': 'admin',
                'company': 'unittest'
            },
            algorithm='HS512',
            key=settings.JWT_SECRET,
        )
        project_name = 'unittesting'
        test_data = get_unsolved_events(project_name, request)
        assert isinstance(test_data, list)
        assert isinstance(test_data[0], dict)
        assert test_data[0]['eventId'] == '538745942'

    def test_extract_info_from_event_dict(self):
        dumb_event_dict = {
            'id': 'testid', 'eventType': 'test', 'detail': 'detail'
        }
        test_data = extract_info_from_event_dict(dumb_event_dict)
        expected_output = {'type': 'test', 'details': 'detail'}
        assert test_data == expected_output

    def test_get_finding_url(self):
        dumb_finding_dict = {'project_name': 'test', 'finding_id': 'test'}
        test_data = get_finding_url(dumb_finding_dict)
        expected_output = 'https://fluidattacks.com/integrates/dashboard#!\
/project/test/test/description'
        assert test_data == expected_output
