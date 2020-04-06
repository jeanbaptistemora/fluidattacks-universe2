from typing import Set

import casbin
from django.conf import settings
from django.test import TestCase
from backend.domain.user import (
    grant_group_level_role,
    grant_user_level_role,
)
from backend.utils.authorization import (
    get_group_level_authorization_enforcer_async,
    get_user_level_authorization_enforcer_async,
)


def get_project_access_enforcer():
    return settings.ENFORCER_PROJECT_ACCESS


class BasicAbacTest(TestCase):
    global_project_list = {
        'verysensitiveproject',
        'continuoustesting',
        'oneshottest',
        'unittesting',
    }

    def test_basic_enforcer_user_wrong_role(self):
        """Tests for an user with a wrong role."""
        enfor = get_project_access_enforcer()

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
        enfor = get_project_access_enforcer()

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
        enfor = get_project_access_enforcer()

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
    enforcer = get_group_level_authorization_enforcer_async

    global_actions = {
        'backend_api_resolvers_resource_resolve_resources',
        'backend_api_resolvers_alert_resolve_alert',
        'backend_api_resolvers_forces_resolve_forces_executions',
        'backend_api_resolvers_project_resolve_project',
        'backend_api_resolvers_finding_resolve_finding',
        'backend_api_resolvers_event_resolve_event',
        'backend_api_resolvers_project_resolve_alive_projects',
        'backend_api_resolvers_user_resolve_user_list_projects',
        'backend_api_resolvers_resource_resolve_add_resources',
        'backend_api_resolvers_resource__do_add_repositories',
        'backend_api_resolvers_resource__do_add_environments',
        'backend_api_resolvers_resource__do_update_environment',
        'backend_api_resolvers_resource__do_update_repository',
        'backend_api_resolvers_resource__do_add_files',
        'backend_api_resolvers_resource__do_remove_files',
        'backend_api_resolvers_resource__do_download_file',
        'backend_api_resolvers_vulnerability__do_delete_vulnerability',
        'backend_api_resolvers_vulnerability__do_upload_file',
        'backend_api_resolvers_vulnerability__do_approve_vulnerability',
        'backend_api_resolvers_vulnerability__do_delete_tags',
        'backend_api_resolvers_vulnerability__do_update_treatment_vuln',
        'backend_api_resolvers_vulnerability__do_request_verification_vuln',
        'backend_api_resolvers_vulnerability__do_verify_request_vuln',
        'backend_api_resolvers_vulnerability_resolve_vulnerability_resolve_last_analyst',
        'backend_api_resolvers_vulnerability_resolve_vulnerability_resolve_analyst',
        'backend_api_resolvers_event__do_add_event_comment',
        'backend_api_resolvers_event__do_download_event_file',
        'backend_api_resolvers_event__do_create_event',
        'backend_api_resolvers_event__do_update_event',
        'backend_api_resolvers_event__do_solve_event',
        'backend_api_resolvers_event__do_update_event_evidence',
        'backend_api_resolvers_event__do_remove_event_evidence',
        'backend_api_resolvers_alert_resolve_set_alert',
        'backend_api_dataloaders_finding__get_historic_state',
        'backend_api_dataloaders_finding__get_observations',
        'backend_api_dataloaders_finding__get_analyst',
        'backend_api_resolvers_finding__do_remove_evidence',
        'backend_api_resolvers_finding__do_update_evidence',
        'backend_api_resolvers_finding__do_update_evidence_description',
        'backend_api_resolvers_finding__do_update_severity',
        'backend_api_resolvers_finding__do_verify_finding',
        'backend_api_resolvers_finding__do_update_description',
        'backend_api_resolvers_finding__do_update_client_description',
        'backend_api_resolvers_finding__do_reject_draft',
        'backend_api_resolvers_finding__do_delete_finding',
        'backend_api_resolvers_finding__do_approve_draft',
        'backend_api_resolvers_finding__do_create_draft',
        'backend_api_resolvers_finding__do_submit_draft',
        'backend_api_resolvers_finding_resolve_add_finding_comment',
        'backend_api_resolvers_project__get_comments',
        'backend_api_resolvers_project__get_events',
        'backend_api_resolvers_project_resolve_add_project_comment',
        'backend_api_resolvers_project__get_drafts',
        'backend_api_resolvers_project_resolve_remove_tag',
        'backend_api_resolvers_project_resolve_add_tags',
        'backend_api_resolvers_project_resolve_add_all_project_access',
        'backend_api_resolvers_project_resolve_remove_all_project_access',
        'backend_api_resolvers_project_resolve_request_remove_project',
        'backend_api_resolvers_project_resolve_reject_remove_project',
        'backend_api_resolvers_user_resolve_user_resolve_list_projects',
    }

    analyst_allowed_actions = {
        'backend_api_resolvers_resource_resolve_resources',
        'backend_api_resolvers_alert_resolve_alert',
        'backend_api_resolvers_forces_resolve_forces_executions',
        'backend_api_resolvers_project_resolve_project',
        'backend_api_resolvers_finding_resolve_finding',
        'backend_api_resolvers_event_resolve_event',
        'backend_api_resolvers_vulnerability__do_delete_vulnerability',
        'backend_api_resolvers_vulnerability__do_upload_file',
        'backend_api_resolvers_vulnerability__do_approve_vulnerability',
        'backend_api_resolvers_vulnerability_resolve_vulnerability_resolve_last_analyst',
        'backend_api_resolvers_vulnerability_resolve_vulnerability_resolve_analyst',
        'backend_api_resolvers_event__do_add_event_comment',
        'backend_api_resolvers_event__do_download_event_file',
        'backend_api_resolvers_event__do_create_event',
        'backend_api_resolvers_event__do_update_event',
        'backend_api_resolvers_event__do_solve_event',
        'backend_api_resolvers_event__do_update_event_evidence',
        'backend_api_resolvers_event__do_remove_event_evidence',
        'backend_api_resolvers_resource__do_download_file',
        'backend_api_dataloaders_finding__get_historic_state',
        'backend_api_dataloaders_finding__get_observations',
        'backend_api_dataloaders_finding__get_analyst',
        'backend_api_resolvers_finding__do_remove_evidence',
        'backend_api_resolvers_finding__do_update_evidence',
        'backend_api_resolvers_finding__do_update_evidence_description',
        'backend_api_resolvers_finding__do_update_severity',
        'backend_api_resolvers_finding__do_verify_finding',
        'backend_api_resolvers_vulnerability__do_verify_request_vuln',
        'backend_api_resolvers_finding__do_update_description',
        'backend_api_resolvers_finding__do_reject_draft',
        'backend_api_resolvers_finding__do_delete_finding',
        'backend_api_resolvers_finding__do_create_draft',
        'backend_api_resolvers_finding__do_submit_draft',
        'backend_api_resolvers_finding_resolve_add_finding_comment',
        'backend_api_resolvers_project__get_comments',
        'backend_api_resolvers_project__get_events',
        'backend_api_resolvers_project_resolve_add_project_comment',
        'backend_api_resolvers_project__get_drafts',
    }

    customer_allowed_actions = {
        'backend_api_resolvers_resource_resolve_resources',
        'backend_api_resolvers_alert_resolve_alert',
        'backend_api_resolvers_forces_resolve_forces_executions',
        'backend_api_resolvers_project_resolve_project',
        'backend_api_resolvers_finding_resolve_finding',
        'backend_api_resolvers_event_resolve_event',
        'backend_api_resolvers_resource_resolve_add_resources',
        'backend_api_resolvers_resource__do_add_repositories',
        'backend_api_resolvers_resource__do_add_environments',
        'backend_api_resolvers_resource__do_update_environment',
        'backend_api_resolvers_resource__do_update_repository',
        'backend_api_resolvers_resource__do_add_files',
        'backend_api_resolvers_resource__do_remove_files',
        'backend_api_resolvers_resource__do_download_file',
        'backend_api_resolvers_event__do_add_event_comment',
        'backend_api_resolvers_event__do_download_event_file',
        'backend_api_resolvers_vulnerability__do_delete_tags',
        'backend_api_resolvers_vulnerability__do_update_treatment_vuln',
        'backend_api_resolvers_finding_resolve_add_finding_comment',
        'backend_api_resolvers_finding__do_update_client_description',
        'backend_api_resolvers_vulnerability__do_request_verification_vuln',
        'backend_api_resolvers_project__get_comments',
        'backend_api_resolvers_project__get_events',
        'backend_api_resolvers_project_resolve_add_project_comment',
        'backend_api_resolvers_project_resolve_remove_tag',
        'backend_api_resolvers_project_resolve_add_tags',
    }

    customeradmin_allowed_actions = {
        'backend_api_resolvers_user_resolve_user',
        'backend_api_resolvers_user_resolve_grant_user_access',
        'backend_api_resolvers_user_resolve_remove_user_access',
        'backend_api_resolvers_user_resolve_edit_user',
        'backend_api_resolvers_finding__do_handle_acceptation',
        'backend_api_resolvers_project__get_users',
        'backend_api_resolvers_project_resolve_request_remove_project',
        'backend_api_resolvers_project_resolve_reject_remove_project',
    }
    customeradmin_allowed_actions.update(customer_allowed_actions)

    customeradminfluid_allowed_actions = {
        'backend_api_resolvers_user_resolve_user_list_projects',
        'backend_api_resolvers_alert_resolve_set_alert',
        'backend_api_resolvers_event__do_create_event',
        'backend_api_resolvers_user_resolve_user_resolve_list_projects',
    }

    customeradminfluid_allowed_actions.update(customer_allowed_actions)
    customeradminfluid_allowed_actions.update(customeradmin_allowed_actions)

    def _grant_group_level_access(self, sub: str, obj: str, role: str):
        grant_group_level_role(sub, obj, role)

    def test_action_wrong_role(self):
        """Tests for an user with a wrong role."""
        sub = 'someone@guest.com'
        obj = 'unittesting'

        should_deny = self.global_actions

        for action in should_deny:
            self.assertFalse(UserAbacTest.enforcer(sub).enforce(sub, obj, action))

    def test_action_customer_role(self):
        """Tests for an user with a expected role."""
        sub = 'someone@customer.com'
        obj = 'unittesting'

        self._grant_group_level_access(sub, obj, 'customer')

        should_deny = self.global_actions - self.customer_allowed_actions

        for action in self.customer_allowed_actions:
            self.assertTrue(ActionAbacTest.enforcer(sub).enforce(sub, obj, action))

        for action in should_deny:
            self.assertFalse(ActionAbacTest.enforcer(sub).enforce(sub, obj, action))

    def test_action_customeradmin_role(self):
        """Tests for an user with a expected role."""
        sub = 'admin@customer.com'
        obj = 'unittesting'

        self._grant_group_level_access(sub, obj, 'customeradmin')

        should_deny = self.global_actions - self.customeradmin_allowed_actions

        for action in self.customeradmin_allowed_actions:
            self.assertTrue(ActionAbacTest.enforcer(sub).enforce(sub, obj, action))

        for action in should_deny:
            self.assertFalse(ActionAbacTest.enforcer(sub).enforce(sub, obj, action))

    def test_action_customeradminfluid_role(self):
        """Tests for an user with a expected role."""
        sub = 'customeradmin@fluidattacks.com'
        obj = 'unittesting'

        self._grant_group_level_access(sub, obj, 'customeradmin')

        should_deny = \
            self.global_actions - self.customeradminfluid_allowed_actions

        for action in self.customeradminfluid_allowed_actions:
            self.assertTrue(ActionAbacTest.enforcer(sub).enforce(sub, obj, action))

        for action in should_deny:
            self.assertFalse(ActionAbacTest.enforcer(sub).enforce(sub, obj, action))

    def test_action_analyst_role(self):
        """Tests for an user with a expected role."""
        sub = 'analyst@fluidattacks.com'
        obj = 'unittesting'

        self._grant_group_level_access(sub, obj, 'analyst')

        should_deny = self.global_actions - self.analyst_allowed_actions

        for action in self.analyst_allowed_actions:
            self.assertTrue(ActionAbacTest.enforcer(sub).enforce(sub, obj, action))

        for action in should_deny:
            self.assertFalse(ActionAbacTest.enforcer(sub).enforce(sub, obj, action))

    def test_action_admin_role(self):
        """Tests for an user with a expected role."""
        sub = 'admin@fluidattacks.com'
        obj = 'unittesting'

        self._grant_group_level_access(sub, obj, 'admin')

        should_allow = self.global_actions

        for action in should_allow:
            self.assertTrue(ActionAbacTest.enforcer(sub).enforce(sub, obj, action))


class UserAbacTest(TestCase):
    enforcer = get_user_level_authorization_enforcer_async

    customeradmin_actions: Set[str] = {
        'backend_api_resolvers_me__get_tags',
    }

    customeratfluid_actions: Set[str] = {
        'backend_api_resolvers_project_resolve_create_project',
    }

    analyst_actions: Set[str] = {
        'backend_api_resolvers_cache_resolve_invalidate_cache',
    }

    admin_actions: Set[str] = {
        'backend_api_resolvers_internal_project_resolve_project_name',
        'backend_api_resolvers_user_resolve_add_user',
        'backend_api_resolvers_subscription__do_post_broadcast_message'
    }
    admin_actions = admin_actions.union(analyst_actions)
    admin_actions = admin_actions.union(customeratfluid_actions)

    all_actions = admin_actions

    def _grant_user_level_access(self, sub: str, role: str):
        grant_user_level_role(sub, role)

    def test_action_wrong_role(self):
        sub = 'someone@guest.com'
        obj = 'self'

        for act in self.all_actions:
            self.assertFalse(UserAbacTest.enforcer(sub).enforce(sub, obj, act))

    def test_action_analyst_role(self):
        sub = 'test_action_analyst_role@gmail.com'
        obj = 'self'

        self._grant_user_level_access(sub, 'analyst')

        for act in self.analyst_actions:
            self.assertTrue(UserAbacTest.enforcer(sub).enforce(sub, obj, act))

    def test_action_customer_role(self):
        sub = 'test_action_customer_role@gmail.com'
        obj = 'self'

        self._grant_user_level_access(sub, 'customer')

        for act in self.customeratfluid_actions.union(
            self.customeradmin_actions):
            self.assertFalse(UserAbacTest.enforcer(sub).enforce(sub, obj, act))

    def test_action_customeratfluid_role(self):
        sub = 'test_action_customeratfluid_role@fluidattacks.com'
        obj = 'self'

        self._grant_user_level_access(sub, 'customer')

        for act in self.customeratfluid_actions:
            self.assertTrue(UserAbacTest.enforcer(sub).enforce(sub, obj, act))

    def test_action_customeradmin_role(self):
        sub = 'test_action_customeradmin_role@gmail.com'
        obj = 'self'

        self._grant_user_level_access(sub, 'customeradmin')

        for act in self.customeradmin_actions:
            self.assertTrue(UserAbacTest.enforcer(sub).enforce(sub, obj, act))

    def test_action_admin_role(self):
        sub = 'integratesmanager@gmail.com'
        obj = 'self'

        self._grant_user_level_access(sub, 'admin')

        for act in self.all_actions:
            self.assertTrue(UserAbacTest.enforcer(sub).enforce(sub, obj, act))
