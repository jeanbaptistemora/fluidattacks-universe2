from django.test import TestCase

from app.domain.event import get_event


class EventTests(TestCase):

    def test_get_event(self):
        event_id = '418900971'
        test_data = get_event(event_id)
        expected_output = 'unittesting'
        assert test_data.get('project_name') == expected_output
