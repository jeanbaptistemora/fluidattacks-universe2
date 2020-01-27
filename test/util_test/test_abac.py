import casbin
from django.conf import settings
from django.test import TestCase

GLOBAL_PROJECT_LIST = {
    'verysensitiveproject',
    'continuoustesting',
    'oneshottest',
    'unittesting',
}


def get_enforcer():
    return casbin.Enforcer(settings.CASBIN_POLICY_MODEL_FILE)


class AbacTest(TestCase):

    def test_enforcer_user_wrong_role(self):
        """Tests for an user with a wrong role."""
        enfor = get_enforcer()

        class TestItem:
            pass

        sub = TestItem()
        sub.user_email = 'someone'
        sub.role = 'guest'
        sub.subscribed_projects = {}

        should_deny = GLOBAL_PROJECT_LIST

        for project in should_deny:
            self.assertFalse(enfor.enforce(sub, project))

    def test_enforcer_customer(self):
        """Tests for an customer user."""
        enfor = get_enforcer()

        class TestItem:
            pass

        sub = TestItem()
        sub.username = 'someone@customer.com'
        sub.role = 'customer'
        sub.subscribed_projects = {'oneshottest', 'unittesting'}

        for project in sub.subscribed_projects:
            self.assertTrue(enfor.enforce(sub, project))

        should_deny = GLOBAL_PROJECT_LIST - sub.subscribed_projects

        for project in should_deny:
            self.assertFalse(enfor.enforce(sub, project))

    def test_enforcer_admin(self):
        """Tests for an admin user."""
        enfor = get_enforcer()

        class TestItem:
            pass

        sub = TestItem()
        sub.username = 'admin@fluidattacks.com'
        sub.role = 'admin'
        sub.subscribed_projects = {'oneshottest', 'unittesting'}

        should_allow = GLOBAL_PROJECT_LIST

        for project in should_allow:
            self.assertTrue(enfor.enforce(sub, project))
