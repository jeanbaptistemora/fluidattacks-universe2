import casbin
from django.conf import settings
from django.test import TestCase


def get_enforcer():
    return casbin.Enforcer(settings.CASBIN_POLICY_MODEL_FILE)


class AbacTest(TestCase):

    def test_enforcer_anonymous(self):
        """Tests for an anonymous user."""
        enfor = get_enforcer()

        class TestItem:
            pass

        sub = TestItem()
        sub.username = ''

        should_deny = (
            '/integrates/export_all_vulnerabilities',
            '/integrates/12312313/download_vulnerabilities',
            '/integrates/registration',
            '/integrates/dashboard',
            '/integrates/xls/',
            '/integrates/pdf/',
            '/integrates/logout'
        )

        for url in should_deny:
            self.assertFalse(enfor.enforce(sub, url))

    def test_enforcer_user_wrong_role(self):
        """Tests for an user with a wrong role."""
        enfor = get_enforcer()

        class TestItem:
            pass

        sub = TestItem()
        sub.username = 'someone'
        sub.role = 'guest'

        should_deny = (
            '/integrates/export_all_vulnerabilities',
            '/integrates/12312313/download_vulnerabilities',
            '/integrates/xls/',
            '/integrates/pdf/',
        )

        for url in should_deny:
            self.assertFalse(enfor.enforce(sub, url))


    def test_enforcer_customer(self):
        """Tests for an customer user."""
        enfor = get_enforcer()

        class TestItem:
            pass

        sub = TestItem()
        sub.username = 'someone@customer.com'
        sub.role = 'customer'

        should_deny = (
            '/integrates/export_all_vulnerabilities',
            '/integrates/12312313/download_vulnerabilities',
        )

        for url in should_deny:
            self.assertFalse(enfor.enforce(sub, url))

        should_allow = (
            '/integrates/registration',
            '/integrates/dashboard',
            '/integrates/xls/',
            '/integrates/pdf/',
            '/integrates/logout'
        )

        for url in should_allow:
            self.assertTrue(enfor.enforce(sub, url))

    def test_enforcer_analyst(self):
        """Tests for an analyst user."""
        enfor = get_enforcer()

        class TestItem:
            pass

        sub = TestItem()
        sub.username = 'someone@fluidattacks.com'
        sub.role = 'analyst'

        should_deny = (
            '/integrates/export_all_vulnerabilities',
        )

        for url in should_deny:
            self.assertFalse(enfor.enforce(sub, url))

        should_allow = (
            '/integrates/12312313/download_vulnerabilities',
            '/integrates/registration',
            '/integrates/dashboard',
            '/integrates/xls/',
            '/integrates/pdf/',
            '/integrates/logout'
        )

        for url in should_allow:
            self.assertTrue(enfor.enforce(sub, url))

    def test_enforcer_admin(self):
        """Tests for an admin user."""
        enfor = get_enforcer()

        class TestItem:
            pass

        sub = TestItem()
        sub.username = 'admin@fluidattacks.com'
        sub.role = 'admin'

        should_allow = (
            '/integrates/export_all_vulnerabilities',
            '/integrates/12312313/download_vulnerabilities',
            '/integrates/registration',
            '/integrates/dashboard',
            '/integrates/xls/',
            '/integrates/pdf/',
            '/integrates/logout'
        )

        for url in should_allow:
            self.assertTrue(enfor.enforce(sub, url))
