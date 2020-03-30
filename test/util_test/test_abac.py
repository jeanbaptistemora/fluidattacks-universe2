from typing import Set

import casbin
from django.conf import settings
from django.test import TestCase


def get_casbin_adapter():
    return settings.CASBIN_ADAPTER


def get_project_access_enforcer():
    return settings.ENFORCER_PROJECT_ACCESS


def get_group_level_enforcer():
    return settings.ENFORCER_GROUP_LEVEL


def get_user_level_enforcer():
    return settings.ENFORCER_USER_LEVEL


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
    adapter = get_casbin_adapter()
    enforcer = get_group_level_enforcer()

    global_actions = {
        'backend_api_query_Query_resolve_resources',
        'backend_api_query_Query_resolve_alert',
        'backend_api_query_Query_resolve_forces_executions',
        'backend_api_query_Query_resolve_project',
        'backend_api_query_Query_resolve_finding',
        'backend_api_query_Query_resolve_event',
        'backend_api_query_Query_resolve_alive_projects',
        'backend_api_query_Query_resolve_user_list_projects',
        'backend_entity_resource_AddResources_mutate',
        'backend_entity_resource_UpdateResources_mutate',
        'backend_entity_resource_AddFiles_mutate',
        'backend_entity_resource_RemoveFiles_mutate',
        'backend_entity_resource_DownloadFile_mutate',
        'backend_entity_vulnerability_DeleteVulnerability_mutate',
        'backend_entity_vulnerability_UploadFile_mutate',
        'backend_entity_vulnerability_ApproveVulnerability_mutate',
        'backend_entity_vulnerability_DeleteTags_mutate',
        'backend_entity_vulnerability_UpdateTreatmentVuln_mutate',
        'backend_entity_vulnerability_RequestVerificationVuln_mutate',
        'backend_entity_vulnerability_VerifyRequestVuln_mutate',
        'backend_entity_vulnerability_Vulnerability_resolve_last_analyst',
        'backend_entity_vulnerability_Vulnerability_resolve_analyst',
        'backend_entity_event_AddEventComment_mutate',
        'backend_entity_event_DownloadEventFile_mutate',
        'backend_entity_event_CreateEvent_mutate',
        'backend_entity_event_UpdateEvent_mutate',
        'backend_entity_event_SolveEvent_mutate',
        'backend_entity_event_UpdateEventEvidence_mutate',
        'backend_entity_event_RemoveEventEvidence_mutate',
        'backend_entity_alert_SetAlert_mutate',
        'backend_entity_finding_Finding_resolve_historic_state',
        'backend_entity_finding_Finding_resolve_observations',
        'backend_entity_finding_Finding_resolve_analyst',
        'backend_entity_finding_RemoveEvidence_mutate',
        'backend_entity_finding_UpdateEvidence_mutate',
        'backend_entity_finding_UpdateEvidenceDescription_mutate',
        'backend_entity_finding_UpdateSeverity_mutate',
        'backend_entity_finding_VerifyFinding_mutate',
        'backend_entity_finding_UpdateDescription_mutate',
        'backend_entity_finding_UpdateClientDescription_mutate',
        'backend_entity_finding_RejectDraft_mutate',
        'backend_entity_finding_DeleteFinding_mutate',
        'backend_entity_finding_CreateDraft_mutate',
        'backend_entity_finding_SubmitDraft_mutate',
        'backend_entity_finding_AddFindingComment_mutate',
        'backend_entity_project_Project_resolve_comments',
        'backend_entity_project_Project_resolve_events',
        'backend_entity_project_AddProjectComment_mutate',
        'backend_entity_project_Project_resolve_drafts',
        'backend_entity_project_RemoveTag_mutate',
        'backend_entity_project_AddTags_mutate',
        'backend_entity_project_AddAllProjectAccess_mutate',
        'backend_entity_project_RemoveAllProjectAccess_mutate',
        'backend_entity_project_RequestRemoveProject_mutate',
        'backend_entity_project_RejectRemoveProject_mutate',
        'backend_entity_user_User_resolve_list_projects',
    }

    analyst_allowed_actions = {
        'backend_api_query_Query_resolve_resources',
        'backend_api_query_Query_resolve_alert',
        'backend_api_query_Query_resolve_forces_executions',
        'backend_api_query_Query_resolve_project',
        'backend_api_query_Query_resolve_finding',
        'backend_api_query_Query_resolve_event',
        'backend_entity_vulnerability_DeleteVulnerability_mutate',
        'backend_entity_vulnerability_UploadFile_mutate',
        'backend_entity_vulnerability_ApproveVulnerability_mutate',
        'backend_entity_vulnerability_Vulnerability_resolve_last_analyst',
        'backend_entity_vulnerability_Vulnerability_resolve_analyst',
        'backend_entity_event_AddEventComment_mutate',
        'backend_entity_event_DownloadEventFile_mutate',
        'backend_entity_event_CreateEvent_mutate',
        'backend_entity_event_UpdateEvent_mutate',
        'backend_entity_event_SolveEvent_mutate',
        'backend_entity_event_UpdateEventEvidence_mutate',
        'backend_entity_event_RemoveEventEvidence_mutate',
        'backend_entity_resource_DownloadFile_mutate',
        'backend_entity_finding_Finding_resolve_historic_state',
        'backend_entity_finding_Finding_resolve_observations',
        'backend_entity_finding_Finding_resolve_analyst',
        'backend_entity_finding_RemoveEvidence_mutate',
        'backend_entity_finding_UpdateEvidence_mutate',
        'backend_entity_finding_UpdateEvidenceDescription_mutate',
        'backend_entity_finding_UpdateSeverity_mutate',
        'backend_entity_finding_VerifyFinding_mutate',
        'backend_entity_vulnerability_VerifyRequestVuln_mutate',
        'backend_entity_finding_UpdateDescription_mutate',
        'backend_entity_finding_RejectDraft_mutate',
        'backend_entity_finding_DeleteFinding_mutate',
        'backend_entity_finding_CreateDraft_mutate',
        'backend_entity_finding_SubmitDraft_mutate',
        'backend_entity_finding_AddFindingComment_mutate',
        'backend_entity_project_Project_resolve_comments',
        'backend_entity_project_Project_resolve_events',
        'backend_entity_project_AddProjectComment_mutate',
        'backend_entity_project_Project_resolve_drafts',
    }

    customer_allowed_actions = {
        'backend_api_query_Query_resolve_resources',
        'backend_api_query_Query_resolve_alert',
        'backend_api_query_Query_resolve_forces_executions',
        'backend_api_query_Query_resolve_project',
        'backend_api_query_Query_resolve_finding',
        'backend_api_query_Query_resolve_event',
        'backend_entity_resource_AddResources_mutate',
        'backend_entity_resource_UpdateResources_mutate',
        'backend_entity_resource_AddFiles_mutate',
        'backend_entity_resource_RemoveFiles_mutate',
        'backend_entity_resource_DownloadFile_mutate',
        'backend_entity_event_AddEventComment_mutate',
        'backend_entity_event_DownloadEventFile_mutate',
        'backend_entity_vulnerability_DeleteTags_mutate',
        'backend_entity_vulnerability_UpdateTreatmentVuln_mutate',
        'backend_entity_finding_AddFindingComment_mutate',
        'backend_entity_finding_UpdateClientDescription_mutate',
        'backend_entity_vulnerability_RequestVerificationVuln_mutate',
        'backend_entity_project_Project_resolve_comments',
        'backend_entity_project_Project_resolve_events',
        'backend_entity_project_AddProjectComment_mutate',
        'backend_entity_project_RemoveTag_mutate',
        'backend_entity_project_AddTags_mutate',
    }

    customeradmin_allowed_actions = {
        'backend_api_query_Query_resolve_user',
        'backend_entity_user_GrantUserAccess_mutate',
        'backend_entity_user_RemoveUserAccess_mutate',
        'backend_entity_user_EditUser_mutate',
        'backend_entity_finding_HandleAcceptation_mutate',
        'backend_entity_project_Project_resolve_users',
        'backend_entity_project_RequestRemoveProject_mutate',
        'backend_entity_project_RejectRemoveProject_mutate',
    }
    customeradmin_allowed_actions.update(customer_allowed_actions)

    customeradminfluid_allowed_actions = {
        'backend_api_query_Query_resolve_user_list_projects',
        'backend_entity_alert_SetAlert_mutate',
        'backend_entity_event_CreateEvent_mutate',
        'backend_entity_user_User_resolve_list_projects',
    }

    customeradminfluid_allowed_actions.update(customer_allowed_actions)
    customeradminfluid_allowed_actions.update(customeradmin_allowed_actions)

    def _grant_group_level_access(self, sub: str, obj: str, role: str):
        self.adapter.add_policy('p', 'p', ['group', sub, obj, role])
        self.enforcer.load_policy()

    def test_action_wrong_role(self):
        """Tests for an user with a wrong role."""
        sub = 'someone@guest.com'
        obj = 'unittesting'

        should_deny = self.global_actions

        for action in should_deny:
            self.assertFalse(self.enforcer.enforce(sub, obj, action))

    def test_action_customer_role(self):
        """Tests for an user with a expected role."""
        sub = 'someone@customer.com'
        obj = 'unittesting'

        self._grant_group_level_access(sub, obj, 'customer')

        should_deny = self.global_actions - self.customer_allowed_actions

        for action in self.customer_allowed_actions:
            self.assertTrue(self.enforcer.enforce(sub, obj, action))

        for action in should_deny:
            self.assertFalse(self.enforcer.enforce(sub, obj, action))

    def test_action_customeradmin_role(self):
        """Tests for an user with a expected role."""
        sub = 'admin@customer.com'
        obj = 'unittesting'

        should_deny = self.global_actions - self.customeradmin_allowed_actions

        self._grant_group_level_access(sub, obj, 'customeradmin')

        for action in self.customeradmin_allowed_actions:
            self.assertTrue(self.enforcer.enforce(sub, obj, action))

        for action in should_deny:
            self.assertFalse(self.enforcer.enforce(sub, obj, action))

    def test_action_customeradminfluid_role(self):
        """Tests for an user with a expected role."""
        sub = 'customeradmin@fluidattacks.com'
        obj = 'unittesting'

        should_deny = \
            self.global_actions - self.customeradminfluid_allowed_actions

        self._grant_group_level_access(sub, obj, 'customeradmin')

        for action in self.customeradminfluid_allowed_actions:
            self.assertTrue(self.enforcer.enforce(sub, obj, action))

        for action in should_deny:
            self.assertFalse(self.enforcer.enforce(sub, obj, action))

    def test_action_analyst_role(self):
        """Tests for an user with a expected role."""
        sub = 'analyst@fluidattacks.com'
        obj = 'unittesting'

        self._grant_group_level_access(sub, obj, 'analyst')

        should_deny = self.global_actions - self.analyst_allowed_actions

        for action in self.analyst_allowed_actions:
            self.assertTrue(self.enforcer.enforce(sub, obj, action))

        for action in should_deny:
            self.assertFalse(self.enforcer.enforce(sub, obj, action))

    def test_action_admin_role(self):
        """Tests for an user with a expected role."""
        sub = 'admin@fluidattacks.com'
        obj = 'unittesting'

        should_allow = self.global_actions

        self._grant_group_level_access(sub, obj, 'admin')

        for action in should_allow:
            self.assertTrue(self.enforcer.enforce(sub, obj, action))

class UserAbacTest(TestCase):
    adapter = get_casbin_adapter()
    enforcer = get_user_level_enforcer()

    customeratfluid_actions: Set[str] = {
        'backend_entity_project_CreateProject_mutate',
    }

    analyst_actions: Set[str] = {
        'backend_entity_cache_InvalidateCache_mutate',
    }

    admin_actions: Set[str] = {
        'backend_api_query_Query_resolve_internal_project_names',
        'backend_entity_user_AddUser_mutate',
    }
    admin_actions = admin_actions.union(analyst_actions)
    admin_actions = admin_actions.union(customeratfluid_actions)

    all_actions = admin_actions

    def _grant_user_level_access(self, sub: str, role: str):
        self.adapter.add_policy('p', 'p', ['user', sub, 'self', role])
        self.enforcer.load_policy()

    def test_action_wrong_role(self):
        sub = 'someone@guest.com'
        obj = 'self'

        for act in self.all_actions:
            self.assertFalse(self.enforcer.enforce(sub, obj, act))

    def test_action_analyst_role(self):
        sub = 'test_action_analyst_role@gmail.com'
        obj = 'self'

        self._grant_user_level_access(sub, 'analyst')

        for act in self.analyst_actions:
            self.assertTrue(self.enforcer.enforce(sub, obj, act))

    def test_action_customer_role(self):
        sub = 'test_action_customer_role@gmail.com'
        obj = 'self'

        self._grant_user_level_access(sub, 'customer')

        for act in self.customeratfluid_actions:
            self.assertFalse(self.enforcer.enforce(sub, obj, act))

    def test_action_customeratfluid_role(self):
        sub = 'test_action_customeratfluid_role@fluidattacks.com'
        obj = 'self'

        self._grant_user_level_access(sub, 'customer')

        for act in self.customeratfluid_actions:
            self.assertTrue(self.enforcer.enforce(sub, obj, act))

    def test_action_admin_role(self):
        sub = 'integratesmanager@gmail.com'
        obj = 'self'

        self._grant_user_level_access(sub, 'admin')

        for act in self.all_actions:
            self.assertTrue(self.enforcer.enforce(sub, obj, act))
