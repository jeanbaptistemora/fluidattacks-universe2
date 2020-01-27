import casbin
from django.conf import settings
from django.test import TestCase


def get_basic_enforcer():
    return casbin.Enforcer(settings.CASBIN_BASIC_POLICY_MODEL_FILE)


def get_action_enforcer():
    return casbin.Enforcer(settings.CASBIN_ACTION_POLICY_MODEL_FILE)


class BasicAbacTest(TestCase):
    global_project_list = {
        'verysensitiveproject',
        'continuoustesting',
        'oneshottest',
        'unittesting',
    }

    def test_basic_enforcer_user_wrong_role(self):
        """Tests for an user with a wrong role."""
        enfor = get_basic_enforcer()

        class TestItem:
            pass

        sub = TestItem()
        sub.user_email = 'someone'
        sub.role = 'guest'
        sub.subscribed_projects = {}

        should_deny = self.global_project_list

        for project in should_deny:
            self.assertFalse(enfor.enforce(sub, project))

    def test_basic_enforcer_customer(self):
        """Tests for an customer user."""
        enfor = get_basic_enforcer()

        class TestItem:
            pass

        sub = TestItem()
        sub.username = 'someone@customer.com'
        sub.role = 'customer'
        sub.subscribed_projects = {'oneshottest', 'unittesting'}

        for project in sub.subscribed_projects:
            self.assertTrue(enfor.enforce(sub, project))

        should_deny = self.global_project_list - sub.subscribed_projects

        for project in should_deny:
            self.assertFalse(enfor.enforce(sub, project))

    def test_basic_enforcer_admin(self):
        """Tests for an admin user."""
        enfor = get_basic_enforcer()

        class TestItem:
            pass

        sub = TestItem()
        sub.username = 'admin@fluidattacks.com'
        sub.role = 'admin'
        sub.subscribed_projects = {'oneshottest', 'unittesting'}

        should_allow = self.global_project_list

        for project in should_allow:
            self.assertTrue(enfor.enforce(sub, project))


class ActionAbacTest(TestCase):
    global_actions = {
        'backend.api.query.resolve_resources',
    }

    def test_action_wrong_role(self):
        """Tests for an user with a wrong role."""
        enfor = get_action_enforcer()

        class TestItem:
            pass

        sub = TestItem()
        sub.user_email = 'someone'
        sub.role = 'guest'
        obj = 'unittesting'
        action = 'backend.api.query.resolve_resources'

        should_deny = self.global_actions

        for action in should_deny:
            self.assertFalse(enfor.enforce(sub, obj, action))

    def test_action_correct_role(self):
        """Tests for an user with a expected role."""
        enfor = get_action_enforcer()

        class TestItem:
            pass

        sub = TestItem()
        sub.user_email = 'someone'
        sub.role = 'customer'
        obj = 'unittesting'
        action = 'backend.api.query.resolve_resources'

        should_allow = self.global_actions

        for action in should_allow:
            self.assertTrue(enfor.enforce(sub, obj, action))
