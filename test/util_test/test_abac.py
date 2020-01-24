import casbin
from django.conf import settings
from django.test import TestCase

GLOBAL_URL_LIST = {
    '/integrates/export_all_vulnerabilities',
    '/integrates/12312313/download_vulnerabilities',
    '/integrates/registration',
    '/integrates/dashboard',
    '/integrates/project/BWAPP/12345/evidence/file1.png',
    '/integrates/xls/',
    '/integrates/pdf/',
    '/integrates/logout'
}


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

        should_deny = GLOBAL_URL_LIST

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

        should_allow = {
            '/integrates/registration',
            '/integrates/dashboard',
            '/integrates/logout'
        }
        should_deny = GLOBAL_URL_LIST - should_allow

        for url in should_deny:
            self.assertFalse(enfor.enforce(sub, url))

        for url in should_allow:
            self.assertTrue(enfor.enforce(sub, url))

    def test_enforcer_customer(self):
        """Tests for an customer user."""
        enfor = get_enforcer()

        class TestItem:
            pass

        sub = TestItem()
        sub.username = 'someone@customer.com'
        sub.role = 'customer'

        should_allow = {
            '/integrates/registration',
            '/integrates/dashboard',
            '/integrates/xls/',
            '/integrates/pdf/',
            '/integrates/project/BWAPP/12345/evidence/file1.png',
            '/integrates/logout'
        }

        for url in should_allow:
            self.assertTrue(enfor.enforce(sub, url))

        should_deny = GLOBAL_URL_LIST - should_allow

        for url in should_deny:
            self.assertFalse(enfor.enforce(sub, url))

    def test_enforcer_analyst(self):
        """Tests for an analyst user."""
        enfor = get_enforcer()

        class TestItem:
            pass

        sub = TestItem()
        sub.username = 'someone@fluidattacks.com'
        sub.role = 'analyst'

        should_allow = {
            '/integrates/12312313/download_vulnerabilities',
            '/integrates/registration',
            '/integrates/dashboard',
            '/integrates/project/BWAPP/12345/evidence/file1.png',
            '/integrates/xls/',
            '/integrates/pdf/',
            '/integrates/logout'
        }

        for url in should_allow:
            self.assertTrue(enfor.enforce(sub, url))

        should_deny = GLOBAL_URL_LIST - should_allow

        for url in should_deny:
            self.assertFalse(enfor.enforce(sub, url))

    def test_enforcer_admin(self):
        """Tests for an admin user."""
        enfor = get_enforcer()

        class TestItem:
            pass

        sub = TestItem()
        sub.username = 'admin@fluidattacks.com'
        sub.role = 'admin'

        should_allow = GLOBAL_URL_LIST

        for url in should_allow:
            self.assertTrue(enfor.enforce(sub, url))
