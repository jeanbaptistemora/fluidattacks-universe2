from django.test import TestCase

from app.domain.event import get_event_project_name


class EventTests(TestCase):

    def test_get_event_project_name(self):
        event_id = '418900971'
        test_data = get_event_project_name(event_id)
        expected_output = 'unittesting'
        assert test_data == expected_output
