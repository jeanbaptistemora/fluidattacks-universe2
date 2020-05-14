from typing import Set

import pytest
from django.conf import settings
from django.test import TestCase
from backend.domain.user import (
    grant_group_level_role,
    grant_user_level_role,
)
from backend.authz import (
    get_cached_group_service_attributes_policies,
    get_group_access_enforcer,
    get_group_level_enforcer,
    get_group_service_attributes_enforcer,
    get_user_level_enforcer,
    SERVICE_ATTRIBUTES,
)

# Constants
pytestmark = pytest.mark.asyncio


class BasicAbacTest(TestCase):
    enforcer = get_group_access_enforcer()

    global_project_list = {
        'verysensitiveproject',
        'continuoustesting',
        'oneshottest',
        'unittesting',
    }

    async def test_basic_enforcer_user_wrong_role(self):
        """Tests for an user with a wrong role."""
        sub = {
            'user_email': 'someone',
            'role': 'guest',
            'subscribed_projects': {}
        }

        should_deny = self.global_project_list

        for project in should_deny:
            self.assertFalse(await BasicAbacTest.enforcer(sub, project))

    async def test_basic_enforcer_customer(self):
        """Tests for an customer user."""
        sub = {
            'username': 'someone@customer.com',
            'role': 'customer',
            'subscribed_projects': {'oneshottest', 'unittesting'}
        }

        for project in sub['subscribed_projects']:
            self.assertTrue(await BasicAbacTest.enforcer(sub, project))

        should_deny = self.global_project_list - sub['subscribed_projects']

        for project in should_deny:
            self.assertFalse(await BasicAbacTest.enforcer(sub, project))

    async def test_basic_enforcer_admin(self):
        """Tests for an admin user."""
        sub = {
            'username': 'admin@fluidattacks.com',
            'role': 'admin',
            'subscribed_projects': {'oneshottest', 'unittesting'}
        }

        should_allow = self.global_project_list

        for project in should_allow:
            self.assertTrue(await BasicAbacTest.enforcer(sub, project))


class ActionAbacTest(TestCase):
    enforcer = get_group_level_enforcer

    global_actions = {
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
        'backend_api_resolvers_event__do_solve_event',
        'backend_api_resolvers_event__do_update_event_evidence',
        'backend_api_resolvers_event__do_remove_event_evidence',
        'backend_api_resolvers_alert_resolve_set_alert',
        'backend_api_resolvers_finding__get_historic_state',
        'backend_api_resolvers_finding__get_observations',
        'backend_api_resolvers_finding__get_pending_vulns',
        'backend_api_resolvers_finding__get_analyst',
        'backend_api_resolvers_finding__do_remove_evidence',
        'backend_api_resolvers_finding__do_update_evidence',
        'backend_api_resolvers_finding__do_update_evidence_description',
        'backend_api_resolvers_finding__do_update_severity',
        'backend_api_resolvers_finding__do_update_description',
        'backend_api_resolvers_finding__do_update_client_description',
        'backend_api_resolvers_finding__do_reject_draft',
        'backend_api_resolvers_finding__do_delete_finding',
        'backend_api_resolvers_finding__do_approve_draft',
        'backend_api_resolvers_finding__do_create_draft',
        'backend_api_resolvers_finding__do_submit_draft',
        'backend_api_resolvers_finding__do_add_finding_comment',
        'backend_api_resolvers_project__get_comments',
        'backend_api_resolvers_project__get_events',
        'backend_api_resolvers_project__do_add_project_comment',
        'backend_api_resolvers_project__get_drafts',
        'backend_api_resolvers_project__do_remove_tag',
        'backend_api_resolvers_project__do_add_tags',
        'backend_api_resolvers_project__do_add_all_project_access',
        'backend_api_resolvers_project__do_remove_all_project_access',
        'backend_api_resolvers_project__do_request_remove_project',
        'backend_api_resolvers_project__do_reject_remove_project',
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
        'backend_api_resolvers_vulnerability__do_request_verification_vuln',
        'backend_api_resolvers_vulnerability_resolve_vulnerability_resolve_last_analyst',
        'backend_api_resolvers_vulnerability_resolve_vulnerability_resolve_analyst',
        'backend_api_resolvers_event__do_add_event_comment',
        'backend_api_resolvers_event__do_download_event_file',
        'backend_api_resolvers_event__do_create_event',
        'backend_api_resolvers_event__do_solve_event',
        'backend_api_resolvers_event__do_update_event_evidence',
        'backend_api_resolvers_event__do_remove_event_evidence',
        'backend_api_resolvers_resource__do_download_file',
        'backend_api_resolvers_finding__get_historic_state',
        'backend_api_resolvers_finding__get_observations',
        'backend_api_resolvers_finding__get_pending_vulns',
        'backend_api_resolvers_finding__get_analyst',
        'backend_api_resolvers_finding__do_remove_evidence',
        'backend_api_resolvers_finding__do_update_evidence',
        'backend_api_resolvers_finding__do_update_evidence_description',
        'backend_api_resolvers_finding__do_update_severity',
        'backend_api_resolvers_vulnerability__do_verify_request_vuln',
        'backend_api_resolvers_finding__do_update_description',
        'backend_api_resolvers_finding__do_reject_draft',
        'backend_api_resolvers_finding__do_delete_finding',
        'backend_api_resolvers_finding__do_create_draft',
        'backend_api_resolvers_finding__do_submit_draft',
        'backend_api_resolvers_finding__do_add_finding_comment',
        'backend_api_resolvers_project__get_comments',
        'backend_api_resolvers_project__get_events',
        'backend_api_resolvers_project__do_add_project_comment',
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
        'backend_api_resolvers_finding__do_add_finding_comment',
        'backend_api_resolvers_finding__do_update_client_description',
        'backend_api_resolvers_vulnerability__do_request_verification_vuln',
        'backend_api_resolvers_project__get_comments',
        'backend_api_resolvers_project__get_events',
        'backend_api_resolvers_project__do_add_project_comment',
        'backend_api_resolvers_project__do_remove_tag',
        'backend_api_resolvers_project__do_add_tags',
    }

    customeradmin_allowed_actions = {
        'backend_api_resolvers_user_resolve_user',
        'backend_api_resolvers_user__do_grant_user_access',
        'backend_api_resolvers_user__do_remove_user_access',
        'backend_api_resolvers_user__do_edit_user',
        'backend_api_resolvers_finding__do_handle_acceptation',
        'backend_api_resolvers_project__get_users',
        'backend_api_resolvers_project__do_request_remove_project',
        'backend_api_resolvers_project__do_reject_remove_project',
    }
    customeradmin_allowed_actions.update(customer_allowed_actions)

    customeradminfluid_allowed_actions = {
        'backend_api_resolvers_alert_resolve_set_alert',
        'backend_api_resolvers_event__do_create_event',
        'backend_api_resolvers_event__do_solve_event',
        'backend_api_resolvers_project__get_drafts',
    }

    customeradminfluid_allowed_actions.update(customer_allowed_actions)
    customeradminfluid_allowed_actions.update(customeradmin_allowed_actions)

    def _grant_group_level_access(self, sub: str, obj: str, role: str):
        grant_group_level_role(sub, obj, role)

    async def test_action_wrong_role(self):
        """Tests for an user with a wrong role."""
        sub = 'someone@guest.com'
        obj = 'unittesting'

        should_deny = self.global_actions

        for action in should_deny:
            self.assertFalse(await ActionAbacTest.enforcer(sub)(sub, obj, action))

    @pytest.mark.changes_db
    async def test_action_customer_role(self):
        """Tests for an user with a expected role."""
        sub = 'someone@customer.com'
        obj = 'unittesting'

        self._grant_group_level_access(sub, obj, 'customer')

        should_deny = self.global_actions - self.customer_allowed_actions

        for action in self.customer_allowed_actions:
            self.assertTrue(await ActionAbacTest.enforcer(sub)(sub, obj, action))

        for action in should_deny:
            self.assertFalse(await ActionAbacTest.enforcer(sub)(sub, obj, action))

    @pytest.mark.changes_db
    async def test_action_customeradmin_role(self):
        """Tests for an user with a expected role."""
        sub = 'admin@customer.com'
        obj = 'unittesting'

        self._grant_group_level_access(sub, obj, 'customeradmin')

        should_deny = self.global_actions - self.customeradmin_allowed_actions

        for action in self.customeradmin_allowed_actions:
            self.assertTrue(await ActionAbacTest.enforcer(sub)(sub, obj, action))

        for action in should_deny:
            self.assertFalse(await ActionAbacTest.enforcer(sub)(sub, obj, action))

    @pytest.mark.changes_db
    async def test_action_customeradminfluid_role(self):
        """Tests for an user with a expected role."""
        sub = 'customeradmin@fluidattacks.com'
        obj = 'unittesting'

        self._grant_group_level_access(sub, obj, 'group_manager')

        should_deny = \
            self.global_actions - self.customeradminfluid_allowed_actions

        for action in self.customeradminfluid_allowed_actions:
            self.assertTrue(await ActionAbacTest.enforcer(sub)(sub, obj, action))

        for action in should_deny:
            self.assertFalse(await ActionAbacTest.enforcer(sub)(sub, obj, action))

    @pytest.mark.changes_db
    async def test_action_analyst_role(self):
        """Tests for an user with a expected role."""
        sub = 'analyst@fluidattacks.com'
        obj = 'unittesting'

        self._grant_group_level_access(sub, obj, 'analyst')

        should_deny = self.global_actions - self.analyst_allowed_actions

        for action in self.analyst_allowed_actions:
            self.assertTrue(await ActionAbacTest.enforcer(sub)(sub, obj, action))

        for action in should_deny:
            self.assertFalse(await ActionAbacTest.enforcer(sub)(sub, obj, action))

    @pytest.mark.changes_db
    async def test_action_admin_role(self):
        """Tests for an user with a expected role."""
        sub = 'admin@fluidattacks.com'
        obj = 'unittesting'

        self._grant_group_level_access(sub, obj, 'admin')

        should_deny = {
            'backend_api_resolvers_finding__do_handle_acceptation',
            'backend_api_resolvers_finding__do_update_client_description',
            'backend_api_resolvers_vulnerability__do_delete_tags',
            'backend_api_resolvers_vulnerability__do_update_treatment_vuln',
        }
        should_allow = self.global_actions - should_deny

        for action in should_allow:
            self.assertTrue(await ActionAbacTest.enforcer(sub)(sub, obj, action))

        for action in should_deny:
            self.assertFalse(await ActionAbacTest.enforcer(sub)(sub, obj, action))


class UserAbacTest(TestCase):
    enforcer = get_user_level_enforcer

    customer_actions: Set[str] = {
        'backend_api_resolvers_internal_project_resolve_project_name',
        'backend_api_resolvers_project__do_create_project',
    }

    customeradmin_actions: Set[str] = {
        'backend_api_resolvers_internal_project_resolve_project_name',
        'backend_api_resolvers_me__get_tags',
        'backend_api_resolvers_project__do_create_project',
        'backend_api_resolvers_tag_resolve_tag',
        'backend_api_resolvers_user_resolve_user_list_projects',
    }

    internal_manager_actions: Set[str] = {
        'backend_api_resolvers_internal_project_resolve_project_name',
        'backend_api_resolvers_me__get_tags',
        'backend_api_resolvers_project__do_create_project',
        'backend_api_resolvers_tag_resolve_tag',
        'backend_api_resolvers_user_resolve_user_list_projects',
    }

    analyst_actions: Set[str] = {
        'backend_api_resolvers_cache_resolve_invalidate_cache',
        'backend_api_resolvers_internal_project_resolve_project_name',
        'backend_api_resolvers_project__do_create_project',
    }

    admin_actions: Set[str] = {
        'backend_api_resolvers_internal_project_resolve_project_name',
        'backend_api_resolvers_user__do_add_user',
        'backend_api_resolvers_subscription__do_post_broadcast_message',
        'backend_api_resolvers_project_resolve_alive_projects'
    }
    admin_actions = admin_actions.union(customer_actions)
    admin_actions = admin_actions.union(customeradmin_actions)
    admin_actions = admin_actions.union(internal_manager_actions)
    admin_actions = admin_actions.union(analyst_actions)

    all_actions = admin_actions

    def _grant_user_level_access(self, sub: str, role: str):
        grant_user_level_role(sub, role)

    async def test_action_wrong_role(self):
        sub = 'someone@guest.com'
        obj = 'self'

        enforcer = UserAbacTest.enforcer(sub)

        for action in self.all_actions:
            assert not await enforcer(sub, obj, action), action

    @pytest.mark.changes_db
    async def test_action_analyst_role(self):
        sub = 'test_action_analyst_role@gmail.com'
        obj = 'self'

        self._grant_user_level_access(sub, 'analyst')
        enforcer = UserAbacTest.enforcer(sub)

        for action in self.analyst_actions:
            assert await enforcer(sub, obj, action), action

        for action in self.all_actions - self.analyst_actions:
            assert not await enforcer(sub, obj, action), action

    @pytest.mark.changes_db
    async def test_action_customer_role(self):
        sub = 'test_action_customer_role@gmail.com'
        obj = 'self'

        self._grant_user_level_access(sub, 'customer')
        enforcer = UserAbacTest.enforcer(sub)

        for action in self.customer_actions:
            assert await enforcer(sub, obj, action), action

        for action in self.all_actions - self.customer_actions:
            assert not await enforcer(sub, obj, action), action

    @pytest.mark.changes_db
    async def test_action_internal_manager_role(self):
        sub = 'test_action_internal_manager_role@fluidattacks.com'
        obj = 'self'

        self._grant_user_level_access(sub, 'internal_manager')
        enforcer = UserAbacTest.enforcer(sub)

        for action in self.internal_manager_actions:
            assert await enforcer(sub, obj, action), action

        for action in self.all_actions - self.internal_manager_actions:
            assert not await enforcer(sub, obj, action), action

    @pytest.mark.changes_db
    async def test_action_customeradmin_role(self):
        sub = 'test_action_customeradmin_role@gmail.com'
        obj = 'self'

        self._grant_user_level_access(sub, 'customeradmin')
        enforcer = UserAbacTest.enforcer(sub)

        for action in self.customeradmin_actions:
            assert await enforcer(sub, obj, action), action

        for action in self.all_actions - self.customeradmin_actions:
            assert not await enforcer(sub, obj, action), action

    @pytest.mark.changes_db
    async def test_action_admin_role(self):
        sub = 'integratesmanager@gmail.com'
        obj = 'self'

        self._grant_user_level_access(sub, 'admin')
        enforcer = UserAbacTest.enforcer(sub)

        for action in self.all_actions:
            assert await enforcer(sub, obj, action), action


class ServiceAttributesAbacTest(TestCase):

    async def test_get_cached_group_service_attributes_policies(self):
        assert sorted(get_cached_group_service_attributes_policies('not-exists... probably')) == [
        ]
        assert sorted(get_cached_group_service_attributes_policies('oneshottest')) == [
            ('oneshottest', 'drills_black'),
            ('oneshottest', 'integrates'),
        ]
        assert sorted(get_cached_group_service_attributes_policies('unittesting')) == [
            ('unittesting', 'drills_white'),
            ('unittesting', 'forces'),
            ('unittesting', 'integrates'),
        ]

    async def test_service_attributes(self):
        # All attributes must be tested for this test to succeed
        # This prevents someone to add a new attribute without testing it

        attributes_remaining_to_test: Set[str] = {
            (group, attr)
            for group in ('unittesting', 'oneshottest', 'non_existing')
            for attrs in SERVICE_ATTRIBUTES.values()
            for attr in set(attrs).union({'non_existing_attribute'})
        }

        for group, attribute, result in [
            ('unittesting', 'is_fluidattacks_customer', True),
            ('unittesting', 'must_only_have_fluidattacks_hackers', True),
            ('unittesting', 'non_existing_attribute', False),

            ('oneshottest', 'is_fluidattacks_customer', True),
            ('oneshottest', 'must_only_have_fluidattacks_hackers', True),
            ('oneshottest', 'non_existing_attribute', False),

            ('non_existing', 'is_fluidattacks_customer', False),
            ('non_existing', 'must_only_have_fluidattacks_hackers', False),
            ('non_existing', 'non_existing_attribute', False),
        ]:

            enforcer = get_group_service_attributes_enforcer(group)
            assert await enforcer(group, attribute) == result
            attributes_remaining_to_test.remove((group, attribute))

        assert not attributes_remaining_to_test, 'Please add more tests here!!'
