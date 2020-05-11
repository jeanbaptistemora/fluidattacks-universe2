import pytest

from django.test import TestCase

from backend.domain.alert import set_company_alert

class AlertTests(TestCase):

    @pytest.mark.changes_db
    def test_set_company_alert(self):
        assert set_company_alert('fluid', 'DEACTIVATE', 'unittesting')
        assert set_company_alert('fluid', 'DEACTIVATE', 'all')
        assert set_company_alert('fluid', 'ACTIVATE', 'unittesting')
        assert set_company_alert('unknown', 'test', 'unittesting')
