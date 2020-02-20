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
        'backend_api_query_Query_resolve_resources',
        'backend_api_query_Query_resolve_alert',
        'backend_api_query_Query_resolve_project',
        'backend_api_query_Query_resolve_finding',
        'backend_api_query_Query_resolve_event',
        'backend_api_query_Query_resolve_alive_projects',
        'backend_api_query_Query_resolve_internal_project_names',
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
        'backend_entity_finding_RequestVerification_mutate',
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
        'backend_entity_project_RemoveProject_mutate',
        'backend_entity_user_User_resolve_list_projects',
        'backend_entity_cache_InvalidateCache_mutate',
        'backend_entity_project_CreateProject_mutate',
    }

    analyst_allowed_actions = {
        'backend_api_query_Query_resolve_resources',
        'backend_api_query_Query_resolve_alert',
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
        'backend_entity_cache_InvalidateCache_mutate',
    }

    customer_allowed_actions = {
        'backend_api_query_Query_resolve_resources',
        'backend_api_query_Query_resolve_alert',
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
        'backend_entity_finding_RequestVerification_mutate',
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
    }
    customeradmin_allowed_actions.update(customer_allowed_actions)

    customeradminfluid_allowed_actions = {
        'backend_api_query_Query_resolve_user_list_projects',
        'backend_entity_alert_SetAlert_mutate',
        'backend_entity_event_CreateEvent_mutate',
        'backend_entity_project_RemoveProject_mutate',
        'backend_entity_user_User_resolve_list_projects',
        'backend_entity_project_CreateProject_mutate',
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
        action = 'backend_entity_project_CreateProject_mutate'

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
