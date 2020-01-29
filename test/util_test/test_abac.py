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
        'backend.api.query.Query.resolve_resources',
        'backend.api.query.Query.resolve_alert',
        'backend.api.query.Query.resolve_project',
        'backend.api.query.Query.resolve_finding',
        'backend.api.query.Query.resolve_event',
        'backend.entity.resource.AddResources.mutate',
        'backend.entity.resource.UpdateResources.mutate',
        'backend.entity.resource.AddFiles.mutate',
        'backend.entity.resource.RemoveFiles.mutate',
        'backend.entity.resource.DownloadFile.mutate',
        'backend.entity.vulnerability.DeleteVulnerability.mutate',
        'backend.entity.vulnerability.UploadFile.mutate',
        'backend.entity.vulnerability.ApproveVulnerability.mutate',
        'backend.entity.vulnerability.DeleteTags.mutate',
        'backend.entity.vulnerability.UpdateTreatmentVuln.mutate',
        'backend.entity.vulnerability.Vulnerability.resolve_last_analyst',
        'backend.entity.vulnerability.Vulnerability.resolve_analyst',
        'backend.entity.event.AddEventComment.mutate',
        'backend.entity.event.DownloadEventFile.mutate',
        'backend.entity.event.UpdateEvent.mutate',
        'backend.entity.event.SolveEvent.mutate',
        'backend.entity.event.UpdateEventEvidence.mutate',
        'backend.entity.event.RemoveEventEvidence.mutate',
        'backend.entity.finding.Finding.resolve_historic_state',
        'backend.entity.finding.Finding.resolve_observations',
        'backend.entity.finding.Finding.resolve_analyst',
        'backend.entity.finding.RemoveEvidence.mutate',
        'backend.entity.finding.UpdateEvidence.mutate',
        'backend.entity.finding.UpdateEvidenceDescription.mutate',
        'backend.entity.finding.UpdateSeverity.mutate',
        'backend.entity.finding.VerifyFinding.mutate',
        'backend.entity.finding.UpdateDescription.mutate',
        'backend.entity.finding.UpdateClientDescription.mutate',
        'backend.entity.finding.RejectDraft.mutate',
        'backend.entity.finding.DeleteFinding.mutate',
        'backend.entity.finding.CreateDraft.mutate',
        'backend.entity.finding.SubmitDraft.mutate',
        'backend.entity.finding.AddFindingComment.mutate',
        'backend.entity.finding.RequestVerification.mutate',
        'backend.entity.project.Project.resolve_comments',
        'backend.entity.project.Project.resolve_events',
        'backend.entity.project.AddProjectComment.mutate',
        'backend.entity.project.Project.resolve_drafts',
        'backend.entity.project.RemoveTag.mutate',
        'backend.entity.project.AddTags.mutate',
        'backend.entity.project.AddAllProjectAccess.mutate',
        'backend.entity.project.RemoveAllProjectAccess.mutate',
    }

    def test_action_wrong_role(self):
        """Tests for an user with a wrong role."""
        enfor = get_action_enforcer()

        class TestItem:
            pass

        sub = TestItem()
        sub.user_email = 'someone@guest.com'
        sub.role = 'guest'
        obj = 'unittesting'
        action = 'backend.api.query.resolve_resources'

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
        obj = 'unittesting'

        should_allow = {
            'backend.api.query.Query.resolve_resources',
            'backend.api.query.Query.resolve_alert',
            'backend.api.query.Query.resolve_project',
            'backend.api.query.Query.resolve_finding',
            'backend.api.query.Query.resolve_event',
            'backend.entity.resource.AddResources.mutate',
            'backend.entity.resource.UpdateResources.mutate',
            'backend.entity.resource.AddFiles.mutate',
            'backend.entity.resource.RemoveFiles.mutate',
            'backend.entity.resource.DownloadFile.mutate',
            'backend.entity.event.AddEventComment.mutate',
            'backend.entity.event.DownloadEventFile.mutate',
            'backend.entity.vulnerability.DeleteTags.mutate',
            'backend.entity.vulnerability.UpdateTreatmentVuln.mutate',
            'backend.entity.finding.AddFindingComment.mutate',
            'backend.entity.finding.UpdateClientDescription.mutate',
            'backend.entity.finding.RequestVerification.mutate',
            'backend.entity.project.Project.resolve_comments',
            'backend.entity.project.Project.resolve_events',
            'backend.entity.project.AddProjectComment.mutate',
            'backend.entity.project.RemoveTag.mutate',
            'backend.entity.project.AddTags.mutate',
        }

        should_deny = self.global_actions - should_allow

        for action in should_allow:
            self.assertTrue(enfor.enforce(sub, obj, action))

        for action in should_deny:
            self.assertFalse(enfor.enforce(sub, obj, action))

    def test_action_analyst_role(self):
        """Tests for an user with a expected role."""
        enfor = get_action_enforcer()

        class TestItem:
            pass

        sub = TestItem()
        sub.user_email = 'analyst@fluidattacks.com'
        sub.role = 'analyst'
        obj = 'unittesting'

        should_allow = {
            'backend.api.query.Query.resolve_resources',
            'backend.api.query.Query.resolve_alert',
            'backend.api.query.Query.resolve_project',
            'backend.api.query.Query.resolve_finding',
            'backend.api.query.Query.resolve_event',
            'backend.entity.vulnerability.DeleteVulnerability.mutate',
            'backend.entity.vulnerability.UploadFile.mutate',
            'backend.entity.vulnerability.ApproveVulnerability.mutate',
            'backend.entity.vulnerability.Vulnerability.resolve_last_analyst',
            'backend.entity.vulnerability.Vulnerability.resolve_analyst',
            'backend.entity.event.AddEventComment.mutate',
            'backend.entity.event.DownloadEventFile.mutate',
            'backend.entity.event.UpdateEvent.mutate',
            'backend.entity.event.SolveEvent.mutate',
            'backend.entity.event.UpdateEventEvidence.mutate',
            'backend.entity.event.RemoveEventEvidence.mutate',
            'backend.entity.resource.DownloadFile.mutate',
            'backend.entity.finding.Finding.resolve_historic_state',
            'backend.entity.finding.Finding.resolve_observations',
            'backend.entity.finding.Finding.resolve_analyst',
            'backend.entity.finding.RemoveEvidence.mutate',
            'backend.entity.finding.UpdateEvidence.mutate',
            'backend.entity.finding.UpdateEvidenceDescription.mutate',
            'backend.entity.finding.UpdateSeverity.mutate',
            'backend.entity.finding.VerifyFinding.mutate',
            'backend.entity.finding.UpdateDescription.mutate',
            'backend.entity.finding.RejectDraft.mutate',
            'backend.entity.finding.DeleteFinding.mutate',
            'backend.entity.finding.CreateDraft.mutate',
            'backend.entity.finding.SubmitDraft.mutate',
            'backend.entity.finding.AddFindingComment.mutate',
            'backend.entity.project.Project.resolve_comments',
            'backend.entity.project.Project.resolve_events',
            'backend.entity.project.AddProjectComment.mutate',
            'backend.entity.project.Project.resolve_drafts',
        }

        should_deny = self.global_actions - should_allow

        for action in should_allow:
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
        obj = 'unittesting'

        should_allow = self.global_actions

        for action in should_allow:
            self.assertTrue(enfor.enforce(sub, obj, action))