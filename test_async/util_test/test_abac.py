import casbin
from django.conf import settings
from django.test import TestCase


def get_basic_enforcer():
    return settings.ENFORCER_BASIC


def get_action_enforcer():
    return settings.ENFORCER_ACTION_ASYNC


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
        'backend_api_resolvers_resource_resolve_resources',
        'backend_api_resolvers_alert_resolve_alert',
        'backend_api_resolvers_forces_resolve_forces_executions',
        'backend_api_resolvers_project_resolve_project',
        'backend_api_resolvers_finding_resolve_finding',
        'backend_api_resolvers_event_resolve_event',
        'backend_api_resolvers_project_resolve_alive_projects',
        'backend_api_resolvers_internal_project_resolve_internal_project_names',
        'backend_api_resolvers_user_resolve_user_list_projects',
        'backend_api_resolvers_resource_resolve_add_resources',
        'backend_api_resolvers_resource_resolve_update_resources',
        'backend_api_resolvers_resource_resolve_add_files',
        'backend_api_resolvers_resource_resolve_remove_files',
        'backend_api_resolvers_resource_resolve_download_file',
        'backend_api_resolvers_vulnerability_resolve_delete_vulnerability',
        'backend_api_resolvers_vulnerability_resolve_upload_file',
        'backend_api_resolvers_vulnerability_resolve_approve_vulnerability',
        'backend_api_resolvers_vulnerability_resolve_delete_tags',
        'backend_api_resolvers_vulnerability_resolve_update_treatment_vuln',
        'backend_api_resolvers_vulnerability_resolve_request_verification_vuln',
        'backend_api_resolvers_vulnerability_resolve_verify_request_vuln',
        'backend_api_resolvers_vulnerability_resolve_vulnerability_resolve_last_analyst',
        'backend_api_resolvers_vulnerability_resolve_vulnerability_resolve_analyst',
        'backend_api_resolvers_event_resolve_add_event_comment',
        'backend_api_resolvers_event_resolve_download_event_file',
        'backend_api_resolvers_event_resolve_create_event',
        'backend_api_resolvers_event_resolve_update_event',
        'backend_api_resolvers_event_resolve_solve_event',
        'backend_api_resolvers_event_resolve_update_event_evidence',
        'backend_api_resolvers_event_resolve_remove_event_evidence',
        'backend_api_resolvers_alert_resolve_set_alert',
        'backend_api_resolvers_finding_resolve_finding_resolve_historic_state',
        'backend_api_resolvers_finding_resolve_finding_resolve_observations',
        'backend_api_resolvers_finding_resolve_finding_resolve_analyst',
        'backend_api_resolvers_finding_resolve_remove_evidence',
        'backend_api_resolvers_finding_resolve_update_evidence',
        'backend_api_resolvers_finding_resolve_update_evidence_description',
        'backend_api_resolvers_finding_resolve_update_severity',
        'backend_api_resolvers_finding_resolve_verify_finding',
        'backend_api_resolvers_finding_resolve_update_description',
        'backend_api_resolvers_finding_resolve_update_client_description',
        'backend_api_resolvers_finding_resolve_reject_draft',
        'backend_api_resolvers_finding_resolve_delete_finding',
        'backend_api_resolvers_finding_resolve_create_draft',
        'backend_api_resolvers_finding_resolve_submit_draft',
        'backend_api_resolvers_finding_resolve_add_finding_comment',
        'backend_api_resolvers_project_resolve_project_resolve_comments',
        'backend_api_resolvers_project_resolve_project_resolve_events',
        'backend_api_resolvers_project_resolve_add_project_comment',
        'backend_api_resolvers_project_resolve_project_resolve_drafts',
        'backend_api_resolvers_project_resolve_remove_tag',
        'backend_api_resolvers_project_resolve_add_tags',
        'backend_api_resolvers_project_resolve_add_all_project_access',
        'backend_api_resolvers_project_resolve_remove_all_project_access',
        'backend_api_resolvers_project_resolve_request_remove_project',
        'backend_api_resolvers_project_resolve_reject_remove_project',
        'backend_api_resolvers_user_resolve_user_resolve_list_projects',
        'backend_api_resolvers_cache_resolve_invalidate_cache',
        'backend_api_resolvers_project_resolve_create_project',
    }

    analyst_allowed_actions = {
        'backend_api_resolvers_resource_resolve_resources',
        'backend_api_resolvers_alert_resolve_alert',
        'backend_api_resolvers_forces_resolve_forces_executions',
        'backend_api_resolvers_project_resolve_project',
        'backend_api_resolvers_finding_resolve_finding',
        'backend_api_resolvers_event_resolve_event',
        'backend_api_resolvers_vulnerability_resolve_delete_vulnerability',
        'backend_api_resolvers_vulnerability_resolve_upload_file',
        'backend_api_resolvers_vulnerability_resolve_approve_vulnerability',
        'backend_api_resolvers_vulnerability_resolve_vulnerability_resolve_last_analyst',
        'backend_api_resolvers_vulnerability_resolve_vulnerability_resolve_analyst',
        'backend_api_resolvers_event_resolve_add_event_comment',
        'backend_api_resolvers_event_resolve_download_event_file',
        'backend_api_resolvers_event_resolve_create_event',
        'backend_api_resolvers_event_resolve_update_event',
        'backend_api_resolvers_event_resolve_solve_event',
        'backend_api_resolvers_event_resolve_update_event_evidence',
        'backend_api_resolvers_event_resolve_remove_event_evidence',
        'backend_api_resolvers_resource_resolve_download_file',
        'backend_api_resolvers_finding_resolve_finding_resolve_historic_state',
        'backend_api_resolvers_finding_resolve_finding_resolve_observations',
        'backend_api_resolvers_finding_resolve_finding_resolve_analyst',
        'backend_api_resolvers_finding_resolve_remove_evidence',
        'backend_api_resolvers_finding_resolve_update_evidence',
        'backend_api_resolvers_finding_resolve_update_evidence_description',
        'backend_api_resolvers_finding_resolve_update_severity',
        'backend_api_resolvers_finding_resolve_verify_finding',
        'backend_api_resolvers_vulnerability_resolve_verify_request_vuln',
        'backend_api_resolvers_finding_resolve_update_description',
        'backend_api_resolvers_finding_resolve_reject_draft',
        'backend_api_resolvers_finding_resolve_delete_finding',
        'backend_api_resolvers_finding_resolve_create_draft',
        'backend_api_resolvers_finding_resolve_submit_draft',
        'backend_api_resolvers_finding_resolve_add_finding_comment',
        'backend_api_resolvers_project_resolve_project_resolve_comments',
        'backend_api_resolvers_project_resolve_project_resolve_events',
        'backend_api_resolvers_project_resolve_add_project_comment',
        'backend_api_resolvers_project_resolve_project_resolve_drafts',
        'backend_api_resolvers_cache_resolve_invalidate_cache',
    }

    customer_allowed_actions = {
        'backend_api_resolvers_resource_resolve_resources',
        'backend_api_resolvers_alert_resolve_alert',
        'backend_api_resolvers_forces_resolve_forces_executions',
        'backend_api_resolvers_project_resolve_project',
        'backend_api_resolvers_finding_resolve_finding',
        'backend_api_resolvers_event_resolve_event',
        'backend_api_resolvers_resource_resolve_add_resources',
        'backend_api_resolvers_resource_resolve_update_resources',
        'backend_api_resolvers_resource_resolve_add_files',
        'backend_api_resolvers_resource_resolve_remove_files',
        'backend_api_resolvers_resource_resolve_download_file',
        'backend_api_resolvers_event_resolve_add_event_comment',
        'backend_api_resolvers_event_resolve_download_event_file',
        'backend_api_resolvers_vulnerability_resolve_delete_tags',
        'backend_api_resolvers_vulnerability_resolve_update_treatment_vuln',
        'backend_api_resolvers_finding_resolve_add_finding_comment',
        'backend_api_resolvers_finding_resolve_update_client_description',
        'backend_api_resolvers_vulnerability_resolve_request_verification_vuln',
        'backend_api_resolvers_project_resolve_project_resolve_comments',
        'backend_api_resolvers_project_resolve_project_resolve_events',
        'backend_api_resolvers_project_resolve_add_project_comment',
        'backend_api_resolvers_project_resolve_remove_tag',
        'backend_api_resolvers_project_resolve_add_tags',
    }

    customeradmin_allowed_actions = {
        'backend_api_resolvers_user_resolve_user',
        'backend_api_resolvers_user_resolve_grant_user_access',
        'backend_api_resolvers_user_resolve_remove_user_access',
        'backend_api_resolvers_user_resolve_edit_user',
        'backend_api_resolvers_finding_resolve_handle_acceptation',
        'backend_api_resolvers_project_resolve_project_resolve_users',
        'backend_api_resolvers_project_resolve_request_remove_project',
        'backend_api_resolvers_project_resolve_reject_remove_project',
    }
    customeradmin_allowed_actions.update(customer_allowed_actions)

    customeradminfluid_allowed_actions = {
        'backend_api_resolvers_user_resolve_user_list_projects',
        'backend_api_resolvers_alert_resolve_set_alert',
        'backend_api_resolvers_event_resolve_create_event',
        'backend_api_resolvers_user_resolve_user_resolve_list_projects',
        'backend_api_resolvers_project_resolve_create_project',
    }

    customeradminfluid_allowed_actions.update(customer_allowed_actions)
    customeradminfluid_allowed_actions.update(customeradmin_allowed_actions)

    def test_action_wrong_role(self):
        """Tests for an user with a wrong role."""
        enfor = get_action_enforcer()

        class TestItem:
            pass

        sub = TestItem()
        sub.user_email = 'someone@guest.com'
        sub.role = 'guest'
        obj = {
            'project_name': 'unittesting',
            'customeradmin': {
                'admin@customer.com'
            }
        }

        should_deny = self.global_actions

        for action in should_deny:
            self.assertFalse(enfor.enforce(sub, obj, action))

    def test_action_customer_role(self):
        """Tests for an user with a expected role."""
        enfor = get_action_enforcer()

        class TestItem:
            pass

        sub = TestItem()
        sub.user_email = 'someone@customer.com'
        sub.role = 'customer'
        obj = {
            'project_name': 'unittesting',
            'customeradmin': {
                'admin@customer.com'
            }
        }

        should_deny = self.global_actions - self.customer_allowed_actions

        for action in self.customer_allowed_actions:
            self.assertTrue(enfor.enforce(sub, obj, action))

        for action in should_deny:
            self.assertFalse(enfor.enforce(sub, obj, action))

    def test_action_customeradmin_role(self):
        """Tests for an user with a expected role."""
        enfor = get_action_enforcer()

        class TestItem:
            pass

        sub = TestItem()
        sub.user_email = 'admin@customer.com'
        sub.role = 'customeradmin'
        obj = {
            'project_name': 'unittesting',
            'customeradmin': {
                'admin@customer.com'
            }
        }

        should_deny = self.global_actions - self.customeradmin_allowed_actions

        for action in self.customeradmin_allowed_actions:
            self.assertTrue(enfor.enforce(sub, obj, action))

        for action in should_deny:
            self.assertFalse(enfor.enforce(sub, obj, action))

    def test_action_customeradminfluid_role(self):
        """Tests for an user with a expected role."""
        enfor = get_action_enforcer()

        class TestItem:
            pass

        sub = TestItem()
        sub.user_email = 'admin@fluidattacks.com'
        sub.role = 'customeradmin'
        obj = {
            'project_name': 'unittesting',
            'customeradmin': {
                'admin@customer.com',
                'admin@fluidattacks.com'
            }
        }

        should_deny = \
            self.global_actions - self.customeradminfluid_allowed_actions

        for action in self.customeradminfluid_allowed_actions:
            self.assertTrue(enfor.enforce(sub, obj, action))

        for action in should_deny:
            self.assertFalse(enfor.enforce(sub, obj, action))

    def test_action_create_project(self):
        """Tests for an user with a expected role."""
        enfor = get_action_enforcer()

        class TestItem:
            pass

        sub = TestItem()
        sub.user_email = 'admin@fluidattacks.com'
        sub.role = 'customeradmin'
        obj = {'customeradmin': set()}
        action = 'backend_api_resolvers_project_resolve_create_project'

        self.assertTrue(enfor.enforce(sub, obj, action))

    def test_action_analyst_role(self):
        """Tests for an user with a expected role."""
        enfor = get_action_enforcer()

        class TestItem:
            pass

        sub = TestItem()
        sub.user_email = 'analyst@fluidattacks.com'
        sub.role = 'analyst'
        obj = {
            'project_name': 'unittesting',
            'customeradmin': {
                'admin@customer.com'
            }
        }

        should_deny = self.global_actions - self.analyst_allowed_actions

        for action in self.analyst_allowed_actions:
            self.assertTrue(enfor.enforce(sub, obj, action))

        for action in should_deny:
            self.assertFalse(enfor.enforce(sub, obj, action))

    def test_action_admin_role(self):
        """Tests for an user with a expected role."""
        enfor = get_action_enforcer()

        class TestItem:
            pass

        sub = TestItem()
        sub.user_email = 'admin@fluidattacks.com'
        sub.role = 'admin'
        obj = {
            'project_name': 'unittesting',
            'customeradmin': {
                'admin@customer.com',
            }
        }

        should_allow = self.global_actions

        for action in should_allow:
            self.assertTrue(enfor.enforce(sub, obj, action))
