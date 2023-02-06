# pylint: disable=too-many-lines
from dataloaders import (
    apply_context_attrs,
)
from datetime import (
    datetime,
    timedelta,
)
from db_model import (
    stakeholders as stakeholders_model,
)
from db_model.companies.types import (
    Company,
    Trial,
)
from db_model.credentials.types import (
    Credentials,
    CredentialsState,
    OauthGitlabSecret,
    SshSecret,
)
from db_model.enums import (
    CredentialType,
    GitCloningStatus,
    Source,
    StateRemovalJustification,
)
from db_model.event_comments.types import (
    EventComment,
)
from db_model.events.enums import (
    EventStateStatus,
    EventType,
)
from db_model.events.types import (
    Event,
    EventEvidences,
    EventState,
    EventUnreliableIndicators,
)
from db_model.findings.enums import (
    DraftRejectionReason,
    FindingSorts,
    FindingStateStatus,
    FindingStatus,
    FindingVerificationStatus,
)
from db_model.findings.types import (
    DraftRejection,
    Finding,
    Finding31Severity,
    FindingEvidence,
    FindingEvidences,
    FindingState,
    FindingTreatmentSummary,
    FindingUnreliableIndicators,
    FindingVerification,
    FindingVerificationSummary,
)
from db_model.group_access.types import (
    GroupAccess,
    GroupAccessState,
    GroupInvitation,
)
from db_model.groups.enums import (
    GroupLanguage,
    GroupManaged,
    GroupService,
    GroupStateStatus,
    GroupSubscriptionType,
    GroupTier,
)
from db_model.groups.types import (
    Group,
    GroupFile,
    GroupState,
)
from db_model.organizations.enums import (
    OrganizationStateStatus,
)
from db_model.organizations.types import (
    Organization,
    OrganizationDocuments,
    OrganizationPaymentMethods,
    OrganizationState,
)
from db_model.roots.enums import (
    RootStatus,
    RootType,
)
from db_model.roots.types import (
    GitRoot,
    GitRootCloning,
    GitRootState,
    RootUnreliableIndicators,
)
from db_model.stakeholders.types import (
    NotificationsParameters,
    NotificationsPreferences,
    Stakeholder,
    StakeholderAccessToken,
    StakeholderMetadataToUpdate,
    StakeholderPhone,
    StakeholderSessionToken,
    StakeholderState,
    StakeholderTours,
    StateSessionType,
)
from db_model.types import (
    Policies,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityAcceptanceStatus,
    VulnerabilityStateStatus,
    VulnerabilityToolImpact,
    VulnerabilityTreatmentStatus,
    VulnerabilityType,
    VulnerabilityVerificationStatus,
    VulnerabilityZeroRiskStatus,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
    VulnerabilityState,
    VulnerabilityTool,
    VulnerabilityTreatment,
    VulnerabilityUnreliableIndicators,
    VulnerabilityVerification,
    VulnerabilityZeroRisk,
)
from decimal import (
    Decimal,
)
from graphql import (
    GraphQLResolveInfo,
)
import json
from newutils.datetime import (
    get_now_minus_delta,
)
import os
from re import (
    search,
)
from requests import (
    Request,
)
from sessions import (
    domain as sessions_domain,
    utils as sessions_utils,
)
from settings import (
    JWT_COOKIE_NAME,
    SESSION_COOKIE_AGE,
)
from typing import (
    Any,
    Dict,
    List,
    Optional,
)
from unittest.mock import (
    AsyncMock,
)
import uuid

mocked_paths: Dict[str, str] = {
    "add_stakeholder": "organizations.domain.add_stakeholder",
    "authz.grant_organization_level_role": "authz.grant_organization_level_role",  # noqa: E501 pylint: disable=line-too-long
    "authz.validate_handle_comment_scope": "authz.validate_handle_comment_scope",  # noqa: E501 pylint: disable=line-too-long
    "comments_domain.remove_comments": "finding_comments.domain.remove_comments",  # noqa: E501 pylint: disable=line-too-long
    "credentials_model.remove_organization_credentials": "db_model.credentials.remove_organization_credentials",  # noqa: E501 pylint: disable=line-too-long
    "download_evidence_file": "findings.domain.evidence.download_evidence_file",  # noqa: E501 pylint: disable=line-too-long
    "dynamodb_ops.delete_item": "dynamodb.operations_legacy.delete_item",
    "dynamodb_ops.put_item": "dynamodb.operations_legacy.put_item",
    "dynamodb_ops.query": "dynamodb.operations_legacy.query",
    "dynamodb_ops.scan": "dynamodb.operations_legacy.scan",
    "event_comments_domain.add": "event_comments.domain.add",
    "event_comments_domain.remove_comments": "event_comments.domain.remove_comments",  # noqa: E501 pylint: disable=line-too-long
    "events_model.add": "db_model.events.add",
    "events_model.remove": "db_model.events.remove",
    "events_model.update_state": "db_model.events.update_state",
    "events_model.update_evidence": "db_model.events.update_evidence",
    "exists": "organizations.domain.exists",
    "files_utils.assert_uploaded_file_mime": "newutils.files.assert_uploaded_file_mime",  # noqa: E501 pylint: disable=line-too-long
    "findings_model.remove": "db_model.findings.remove",
    "findings_storage.download_evidence": "findings.storage.download_evidence",
    "findings_storage.search_evidence": "findings.storage.search_evidence",
    "finding_vulns_loader.load_many_chained": "db_model.vulnerabilities.get.FindingVulnerabilitiesReleasedNonZeroRiskLoader.load_many_chained",  # noqa: E501 pylint: disable=line-too-long
    "get_group_names": "organizations.domain.get_group_names",
    "get_open_vulnerabilities": "findings.domain.core.get_open_vulnerabilities",  # noqa: E501 pylint: disable=line-too-long
    "get_stakeholders_emails": "organizations.domain.get_stakeholders_emails",
    "get_user_level_role": "authz.policy.get_user_level_role",
    "grant_user_level_role": "authz.policy.grant_user_level_role",
    "group_access_domain.add_access": "group_access.domain.add_access",
    "group_access_domain.get_managers": "group_access.domain.get_managers",
    "group_access_domain.get_stakeholders_email_by_preferences": "group_access.domain.get_stakeholders_email_by_preferences",  # noqa: E501 pylint: disable=line-too-long
    "group_access_model.update_metadata": "db_model.group_access.update_metadata",  # noqa: E501 pylint: disable=line-too-long
    "group_access_model.remove": "db_model.group_access.remove",
    "group_comments_model.add": "db_model.group_comments.add",
    "groups_domain.update_metadata": "groups.domain.update_metadata",
    "groups_mail.send_mail_devsecops_agent_token": "mailer.groups.send_mail_devsecops_agent_token",  # noqa: E501 pylint: disable=line-too-long
    "loaders.company.load": "db_model.companies.get.CompanyLoader.load",
    "loaders.event.load": "db_model.events.get.EventLoader.load",
    "loaders.event_comments.load": "db_model.event_comments.get.EventCommentsLoader.load",  # noqa: E501 pylint: disable=line-too-long
    "loaders.event_vulnerabilities_loader.load": "db_model.vulnerabilities.get.EventVulnerabilitiesLoader.load",  # noqa: E501 pylint: disable=line-too-long
    "loaders.finding.load": "db_model.findings.get.FindingLoader.load",
    "loaders.finding_vulnerabilities_released_nzr.load": "db_model.vulnerabilities.get.FindingVulnerabilitiesReleasedNonZeroRiskLoader.load",  # noqa: E501 pylint: disable=line-too-long
    "loaders.finding_vulnerabilities.load_many_chained": "db_model.vulnerabilities.get.FindingVulnerabilitiesNonDeletedLoader.load_many_chained",  # noqa: E501 pylint: disable=line-too-long
    "loaders.finding_vulnerabilities_all.load": "db_model.vulnerabilities.get.FindingVulnerabilitiesLoader.load",  # noqa: E501 pylint: disable=line-too-long
    "loaders.group.load": "db_model.groups.get.GroupLoader.load",
    "loaders.group_access.load": "db_model.group_access.get.GroupAccessLoader.load",  # noqa: E501 pylint: disable=line-too-long
    "loaders.group_drafts_and_findings.load": "db_model.findings.get.GroupDraftsAndFindingsLoader.load",  # noqa: E501 pylint: disable=line-too-long
    "loaders.group_findings.load": "db_model.findings.get.GroupFindingsLoader.load",  # noqa: E501 pylint: disable=line-too-long
    "loaders.me_drafts.load": "db_model.findings.get.MeDraftsLoader.load",
    "loaders.me_vulnerabilities.load": "db_model.vulnerabilities.get.AssignedVulnerabilitiesLoader.load",  # noqa: E501 pylint: disable=line-too-long
    "loaders.organization.load": "db_model.organizations.get.OrganizationLoader.load",  # noqa: E501 pylint: disable=line-too-long
    "loaders.organization_credentials.load": "db_model.credentials.get.OrganizationCredentialsLoader.load",  # noqa: E501 pylint: disable=line-too-long
    "loaders.root.load": "db_model.roots.get.RootLoader.load",
    "loaders.stakeholder.load": "db_model.stakeholders.get.StakeholderLoader.load",  # noqa: E501 pylint: disable=line-too-long
    "loaders.stakeholder_with_fallback.load": "db_model.stakeholders.get.StakeholderWithFallbackLoader.load",  # noqa: E501 pylint: disable=line-too-long
    "operations.put_item": "dynamodb.operations.put_item",
    "operations.update_item": "dynamodb.operations.update_item",
    "org_access_model.update_metadata": "db_model.organization_access.update_metadata",  # noqa: E501 pylint: disable=line-too-long
    "orgs_model.add": "db_model.organizations.add",
    "orgs_model.remove": "db_model.organizations.remove",
    "orgs_model.update_policies": "db_model.organizations.update_policies",
    "orgs_model.update_state": "db_model.organizations.update_state",
    "policies_model.remove_org_finding_policies": "db_model.organization_finding_policies.remove_org_finding_policies",  # noqa: E501 pylint: disable=line-too-long
    "portfolios_model.remove_organization_portfolios": "db_model.portfolios.remove_organization_portfolios",  # noqa: E501 pylint: disable=line-too-long
    "remove_access": "organizations.domain.remove_access",
    "remove_all_evidences": "findings.domain.core.remove_all_evidences",
    "remove_file_evidence": "events.domain.remove_file_evidence",
    "replace_different_format": "events.domain.replace_different_format",
    "save_evidence": "events.domain.save_evidence",
    "search_evidence": "events.domain.search_evidence",
    "stakeholders_model.update_metadata": "db_model.stakeholders.update_metadata",  # noqa: E501 pylint: disable=line-too-long
    "s3_ops.list_files": "s3.operations.list_files",
    "s3_ops.remove_file": "s3.operations.remove_file",
    "s3_ops.sign_url": "s3.operations.sign_url",
    "s3_ops.upload_memory_file": "s3.operations.upload_memory_file",
    "update_evidence": "events.domain.update_evidence",
    "update_me_draft_index": "group_access.domain.update_me_draft_index",
    "update_state": "groups.domain.update_state",
    "validate_acceptance_severity_range": "organizations.domain.validate_acceptance_severity_range",  # noqa: E501 pylint: disable=line-too-long
    "validate_evidence": "events.domain.validate_evidence",
    "vulns_domain.mask_vulnerability": "vulnerabilities.domain.mask_vulnerability",  # noqa: E501 pylint: disable=line-too-long
    "vulns_model.remove": "db_model.vulnerabilities.remove",
}

mocked_responses: Dict[str, Dict[str, Any]] = {
    "authz.enforcer.get_user_level_role": {
        '["integrateshacker@fluidattacks.com"]': "hacker"
    },
    "authz.grant_organization_level_role": {
        '["org_testgroupmanager2@fluidattacks.com", '
        '"ORG#f2e2777d-a168-4bea-93cd-d79142b294d2", '
        '"customer_manager"]': None,
    },
    "authz.policy.get_user_level_role": {
        '["integrateshacker@fluidattacks.com"]': "hacker",
        '["integratesuser@gmail.com"]': "user_manager",
        '["test@test.com"]': None,
        '["test2@test.com"]': "user",
        '["test_admin@gmail.com"]': "admin",
        '["test_email@gmail.com"]': "",
        '["unittest@fluidattacks.com"]': "admin",
    },
    "authz.policy.grant_user_level_role": {
        '["test@test.com", "user"]': None,
        '["test2@test.com", "user_manager"]': None,
    },
    "authz.validate_handle_comment_scope": {
        '["comment test", "integratesmanager@gmail.com",'
        ' "unittesting", "0"]': None,
        '["comment test", "integratesmanager@gmail.com",'
        ' "unittesting", "1"]': None,
        '["Test comment", "unittest@fluidattacks.com",'
        ' "unittesting", "0"]': None,
    },
    "db_model.companies.get.CompanyLoader.load": {
        '["esdeath"]': Company(
            domain="gmail.com",
            trial=Trial(
                completed=True,
                extension_date=datetime.fromisoformat(
                    "2022-08-04T22:21:45.938286+00:00"
                ),
                extension_days=0,
                start_date=datetime.fromisoformat(
                    "2022-08-04T22:21:45.946275+00:00"
                ),
            ),
        ),
    },
    "db_model.credentials.get.OrganizationCredentialsLoader.load": {
        '["1a5dacda-1d52-465c-9158-f6fd5dfe0998"]': [
            Credentials(
                id="1a5dacda-1d52-465c-9158-f6fd5dfe0998",
                organization_id="ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                owner="admin@gmail.com",
                state=CredentialsState(
                    modified_by="admin@gmail.com",
                    modified_date=datetime.fromisoformat(
                        "2022-02-12T14:58:10+00:00"
                    ),
                    name="oauth lab token",
                    type=CredentialType.OAUTH,
                    secret=OauthGitlabSecret(
                        refresh_token="UFUzdCBTU0gK",
                        redirect_uri="",
                        access_token="TETzdCBTU0gK",
                        valid_until=get_now_minus_delta(hours=2),
                    ),
                    is_pat=False,
                ),
            )
        ],
    },
    "db_model.credentials.remove_organization_credentials": {
        '["ORG#fe80d2d4-ccb7-46d1-8489-67c6360581de"]': None,
    },
    "db_model.events.add": {
        '["unittesting", "unittesting@fluidattacks.com", '
        '"4039d098-ffc5-4984-8ed3-eb17bca98e19"]': None,
    },
    "db_model.events.remove": {
        '["418900978"]': None,
        '["538745942"]': None,
    },
    "db_model.events.get.EventLoader.load": {
        '["418900978"]': Event(
            client="Test client",
            created_by="unittest@fluidattacks.com",
            created_date=datetime.fromisoformat("2020-01-02T19:40:05+00:00"),
            description="Oneshot event test",
            event_date=datetime.fromisoformat("2020-01-02T12:00:00+00:00"),
            evidences=EventEvidences(
                file_1=None,
                image_1=None,
                image_2=None,
                image_3=None,
                image_4=None,
                image_5=None,
                image_6=None,
            ),
            group_name="oneshottest",
            hacker="unittest@fluidattacks.com",
            id="418900978",
            state=EventState(
                modified_by="unittest@fluidattacks.com",
                modified_date=datetime.fromisoformat(
                    "2020-01-02T19:40:05+00:00"
                ),
                status=EventStateStatus.CREATED,
                comment_id=None,
                other=None,
                reason=None,
            ),
            type=EventType.OTHER,
            root_id=None,
            unreliable_indicators=EventUnreliableIndicators(
                unreliable_solving_date=None
            ),
        ),
        '["538745942"]': Event(
            client="test",
            created_by="unittest@fluidattacks.com",
            created_date=datetime.fromisoformat("2019-09-19T15:43:43+00:00"),
            description="Esta eventualidad fue levantada para "
            "poder realizar pruebas de unittesting",
            event_date=datetime.fromisoformat("2019-09-19T13:09:00+00:00"),
            evidences=EventEvidences(
                file_1=None,
                image_1=None,
                image_2=None,
                image_3=None,
                image_4=None,
                image_5=None,
                image_6=None,
            ),
            group_name="unittesting",
            hacker="unittest@fluidattacks.com",
            id="538745942",
            state=EventState(
                modified_by="unittest@fluidattacks.com",
                modified_date=datetime.fromisoformat(
                    "2019-09-19T15:43:43+00:00"
                ),
                status=EventStateStatus.CREATED,
                comment_id=None,
                other=None,
                reason=None,
            ),
            type=EventType.AUTHORIZATION_SPECIAL_ATTACK,
            root_id=None,
            unreliable_indicators=EventUnreliableIndicators(
                unreliable_solving_date=None
            ),
        ),
        '["418900978", "Already closed"]': Event(
            client="Test client",
            created_by="unittest@fluidattacks.com",
            created_date=datetime.fromisoformat("2020-01-02T19:40:05+00:00"),
            description="Oneshot event test",
            event_date=datetime.fromisoformat("2020-01-02T12:00:00+00:00"),
            evidences=EventEvidences(
                file_1=None,
                image_1=None,
                image_2=None,
                image_3=None,
                image_4=None,
                image_5=None,
                image_6=None,
            ),
            group_name="oneshottest",
            hacker="unittest@fluidattacks.com",
            id="418900978",
            state=EventState(
                modified_by="unittest@fluidattacks.com",
                modified_date=datetime.fromisoformat(
                    "2020-01-02T19:40:05+00:00"
                ),
                status=EventStateStatus.SOLVED,
                comment_id=None,
                other=None,
                reason=None,
            ),
            type=EventType.OTHER,
            root_id=None,
            unreliable_indicators=EventUnreliableIndicators(
                unreliable_solving_date=None
            ),
        ),
        '["538745942", "Already closed"]': Event(
            client="test",
            created_by="unittest@fluidattacks.com",
            created_date=datetime.fromisoformat("2019-09-19T15:43:43+00:00"),
            description="Esta eventualidad fue levantada para "
            "poder realizar pruebas de unittesting",
            event_date=datetime.fromisoformat("2019-09-19T13:09:00+00:00"),
            evidences=EventEvidences(
                file_1=None,
                image_1=None,
                image_2=None,
                image_3=None,
                image_4=None,
                image_5=None,
                image_6=None,
            ),
            group_name="unittesting",
            hacker="unittest@fluidattacks.com",
            id="538745942",
            state=EventState(
                modified_by="unittest@fluidattacks.com",
                modified_date=datetime.fromisoformat(
                    "2019-09-19T15:43:43+00:00"
                ),
                status=EventStateStatus.SOLVED,
                comment_id=None,
                other=None,
                reason=None,
            ),
            type=EventType.AUTHORIZATION_SPECIAL_ATTACK,
            root_id=None,
            unreliable_indicators=EventUnreliableIndicators(
                unreliable_solving_date=None
            ),
        ),
    },
    "db_model.events.update_evidence": {
        '["418900978", "test-file-records.csv", '
        '"2022-12-29 14:14:19.182591+00:00", "FILE_1"]': None,
        '["538745942", "test-file-records.csv", '
        '"2022-12-29 14:14:19.182591+00:00", "FILE_1"]': None,
    },
    "db_model.events.update_state": {
        '["unittesting", "unittesting@fluidattacks.com", '
        '"4039d098-ffc5-4984-8ed3-eb17bca98e19"]': None,
        '["418900978", "unittest@fluidattacks.com", "OTHER", '
        '"Other info", "oneshottest"]': None,
        '["538745942", "unittesting@fluidattacks.com", "PERMISSION_GRANTED", '
        '"Other info", "unittesting"]': None,
    },
    "db_model.event_comments.get.EventCommentsLoader.load": {
        '["538745942"]': (
            EventComment(
                event_id="538745942",
                id="1672323259183",
                parent_id="0",
                creation_date=datetime.fromisoformat(
                    "2022-12-29 14:14:19.182591+00:00"
                ),
                content="comment test",
                email="integratesmanager@gmail.com",
                full_name="John Doe",
            ),
        )
    },
    "db_model.findings.get.FindingLoader.load": {
        '["422286126"]': Finding(
            hacker_email="unittest@fluidattacks.com",
            group_name="unittesting",
            id="422286126",
            state=FindingState(
                modified_by="integratesmanager@gmail.com",
                modified_date=datetime.fromisoformat(
                    "2018-07-09T05:00:00+00:00"
                ),
                source=Source.ASM,
                status=FindingStateStatus.APPROVED,
                rejection=None,
                justification=StateRemovalJustification.NO_JUSTIFICATION,
            ),
            title="060. Insecure service configuration - Host verification",
            approval=FindingState(
                modified_by="integratesmanager@gmail.com",
                modified_date=datetime.fromisoformat(
                    "2018-07-09T05:00:00+00:00"
                ),
                source=Source.ASM,
                status=FindingStateStatus.APPROVED,
                rejection=None,
                justification=StateRemovalJustification.NO_JUSTIFICATION,
            ),
            attack_vector_description="This is an attack vector",
            creation=FindingState(
                modified_by="integratesmanager@gmail.com",
                modified_date=datetime.fromisoformat(
                    "2018-04-08T00:43:18+00:00"
                ),
                source=Source.ASM,
                status=FindingStateStatus.CREATED,
                rejection=None,
                justification=StateRemovalJustification.NO_JUSTIFICATION,
            ),
            description="The source code uses generic exceptions to "
            "handle unexpected errors. Catching generic exceptions "
            "obscures the problem that caused the error and promotes "
            "a generic way to handle different categories or sources "
            "of error. This may cause security vulnerabilities to "
            "materialize, as some special flows go unnoticed.",
            evidences=FindingEvidences(
                animation=FindingEvidence(
                    modified_date=datetime.fromisoformat(
                        "2018-07-09T05:00:00+00:00"
                    ),
                    description="Test description",
                    url="unittesting-422286126-animation.gif",
                ),
                evidence1=FindingEvidence(
                    modified_date=datetime.fromisoformat(
                        "2018-07-09T05:00:00+00:00"
                    ),
                    description="this is a test description",
                    url="unittesting-422286126-evidence_route_1.png",
                ),
                evidence2=FindingEvidence(
                    modified_date=datetime.fromisoformat(
                        "2018-07-09T05:00:00+00:00"
                    ),
                    description="exception",
                    url="unittesting-422286126-evidence_route_2.jpg",
                ),
                evidence3=FindingEvidence(
                    modified_date=datetime.fromisoformat(
                        "2018-07-09T05:00:00+00:00"
                    ),
                    description="Description",
                    url="unittesting-422286126-evidence_route_3.png",
                ),
                evidence4=FindingEvidence(
                    modified_date=datetime.fromisoformat(
                        "2018-07-09T05:00:00+00:00"
                    ),
                    description="changed for testing purposes",
                    url="unittesting-422286126-evidence_route_4.png",
                ),
                evidence5=FindingEvidence(
                    modified_date=datetime.fromisoformat(
                        "2018-07-09T05:00:00+00:00"
                    ),
                    description="Test description",
                    url="unittesting-422286126-evidence_route_5.png",
                ),
                exploitation=FindingEvidence(
                    modified_date=datetime.fromisoformat(
                        "2018-07-09T05:00:00+00:00"
                    ),
                    description="test",
                    url="unittesting-422286126-exploitation.png",
                ),
                records=FindingEvidence(
                    modified_date=datetime.fromisoformat(
                        "2018-07-09T05:00:00+00:00"
                    ),
                    description="test",
                    url="unittesting-422286126-evidence_file.csv",
                ),
            ),
            min_time_to_remediate=18,
            recommendation="Implement password policies with the best "
            "practicies for strong passwords.",
            requirements="R359. Avoid using generic exceptions.",
            severity=Finding31Severity(
                attack_complexity=Decimal("0.77"),
                integrity_impact=Decimal("0.22"),
                integrity_requirement=Decimal("1"),
                modified_confidentiality_impact=Decimal("0"),
                modified_user_interaction=Decimal("0.85"),
                modified_severity_scope=Decimal("0"),
                modified_availability_impact=Decimal("0"),
                report_confidence=Decimal("0.92"),
                modified_integrity_impact=Decimal("0.22"),
                attack_vector=Decimal("0.62"),
                modified_attack_complexity=Decimal("0.77"),
                privileges_required=Decimal("0.62"),
                availability_impact=Decimal("0"),
                modified_privileges_required=Decimal("0.62"),
                confidentiality_requirement=Decimal("1"),
                modified_attack_vector=Decimal("0.62"),
                user_interaction=Decimal("0.85"),
                confidentiality_impact=Decimal("0"),
                exploitability=Decimal("0.91"),
                remediation_level=Decimal("0.97"),
                severity_scope=Decimal("0"),
                availability_requirement=Decimal("1"),
            ),
            sorts=FindingSorts.NO,
            submission=FindingState(
                modified_by="integratesmanager@gmail.com",
                justification=StateRemovalJustification.NO_JUSTIFICATION,
                source=Source.ASM,
                modified_date=datetime.fromisoformat(
                    "2018-04-08T00:45:11+00:00"
                ),
                status=FindingStateStatus.SUBMITTED,
            ),
            threat="An attacker can get passwords of users and "
            "impersonate them or used the credentials for practices "
            "malicious.",
            unreliable_indicators=FindingUnreliableIndicators(
                unreliable_closed_vulnerabilities=0,
                unreliable_newest_vulnerability_report_date=(
                    datetime.fromisoformat("2020-01-03T17:46:10+00:00")
                ),
                unreliable_oldest_open_vulnerability_report_date=(
                    datetime.fromisoformat("2020-01-03T17:46:10+00:00")
                ),
                unreliable_oldest_vulnerability_report_date=(
                    datetime.fromisoformat("2020-01-03T17:46:10+00:00")
                ),
                unreliable_open_vulnerabilities=1,
                unreliable_status=FindingStatus.VULNERABLE,
                unreliable_treatment_summary=FindingTreatmentSummary(
                    accepted=0,
                    untreated=0,
                    in_progress=1,
                    accepted_undefined=0,
                ),
                unreliable_verification_summary=FindingVerificationSummary(
                    verified=0,
                    requested=0,
                    on_hold=0,
                ),
                unreliable_where="test/data/lib_path/f060/csharp.cs",
            ),
        ),
    },
    "db_model.findings.get.GroupDraftsAndFindingsLoader.load": {
        '["unittesting"]': tuple(
            [
                Finding(
                    hacker_email="unittest@fluidattacks.com",
                    group_name="unittesting",
                    id="422286126",
                    state=FindingState(
                        modified_by="integratesmanager@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2018-07-09T05:00:00+00:00"
                        ),
                        source=Source.ASM,
                        status=FindingStateStatus.APPROVED,
                        rejection=None,
                        justification=StateRemovalJustification.NO_JUSTIFICATION,  # noqa: E501 pylint: disable=line-too-long
                    ),
                    title="060. Insecure service configuration - Host "
                    "verification",
                    approval=FindingState(
                        modified_by="integratesmanager@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2018-07-09T05:00:00+00:00"
                        ),
                        source=Source.ASM,
                        status=FindingStateStatus.APPROVED,
                        rejection=None,
                        justification=StateRemovalJustification.NO_JUSTIFICATION,  # noqa: E501 pylint: disable=line-too-long
                    ),
                    attack_vector_description="This is an attack vector",
                    creation=FindingState(
                        modified_by="integratesmanager@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2018-04-08T00:43:18+00:00"
                        ),
                        source=Source.ASM,
                        status=FindingStateStatus.CREATED,
                        rejection=None,
                        justification=StateRemovalJustification.NO_JUSTIFICATION,  # noqa: E501 pylint: disable=line-too-long
                    ),
                    description="The source code uses generic exceptions to "
                    "handle unexpected errors. Catching generic exceptions "
                    "obscures the problem that caused the error and promotes "
                    "a generic way to handle different categories or sources "
                    "of error. This may cause security vulnerabilities to "
                    "materialize, as some special flows go unnoticed.",
                    evidences=FindingEvidences(
                        animation=FindingEvidence(
                            modified_date=datetime.fromisoformat(
                                "2018-07-09T05:00:00+00:00"
                            ),
                            description="Test description",
                            url="unittesting-422286126-animation.gif",
                        ),
                        evidence1=FindingEvidence(
                            modified_date=datetime.fromisoformat(
                                "2018-07-09T05:00:00+00:00"
                            ),
                            description="this is a test description",
                            url="unittesting-422286126-evidence_route_1.png",
                        ),
                        evidence2=FindingEvidence(
                            modified_date=datetime.fromisoformat(
                                "2018-07-09T05:00:00+00:00"
                            ),
                            description="exception",
                            url="unittesting-422286126-evidence_route_2.jpg",
                        ),
                        evidence3=FindingEvidence(
                            modified_date=datetime.fromisoformat(
                                "2018-07-09T05:00:00+00:00"
                            ),
                            description="Description",
                            url="unittesting-422286126-evidence_route_3.png",
                        ),
                        evidence4=FindingEvidence(
                            modified_date=datetime.fromisoformat(
                                "2018-07-09T05:00:00+00:00"
                            ),
                            description="changed for testing purposes",
                            url="unittesting-422286126-evidence_route_4.png",
                        ),
                        evidence5=FindingEvidence(
                            modified_date=datetime.fromisoformat(
                                "2018-07-09T05:00:00+00:00"
                            ),
                            description="Test description",
                            url="unittesting-422286126-evidence_route_5.png",
                        ),
                        exploitation=FindingEvidence(
                            modified_date=datetime.fromisoformat(
                                "2018-07-09T05:00:00+00:00"
                            ),
                            description="test",
                            url="unittesting-422286126-exploitation.png",
                        ),
                        records=FindingEvidence(
                            modified_date=datetime.fromisoformat(
                                "2018-07-09T05:00:00+00:00"
                            ),
                            description="test",
                            url="unittesting-422286126-evidence_file.csv",
                        ),
                    ),
                    min_time_to_remediate=18,
                    recommendation="Implement password policies with the best "
                    "practicies for strong passwords.",
                    requirements="R359. Avoid using generic exceptions.",
                    severity=Finding31Severity(
                        attack_complexity=Decimal("0.77"),
                        integrity_impact=Decimal("0.22"),
                        integrity_requirement=Decimal("1"),
                        modified_confidentiality_impact=Decimal("0"),
                        modified_user_interaction=Decimal("0.85"),
                        modified_severity_scope=Decimal("0"),
                        modified_availability_impact=Decimal("0"),
                        report_confidence=Decimal("0.92"),
                        modified_integrity_impact=Decimal("0.22"),
                        attack_vector=Decimal("0.62"),
                        modified_attack_complexity=Decimal("0.77"),
                        privileges_required=Decimal("0.62"),
                        availability_impact=Decimal("0"),
                        modified_privileges_required=Decimal("0.62"),
                        confidentiality_requirement=Decimal("1"),
                        modified_attack_vector=Decimal("0.62"),
                        user_interaction=Decimal("0.85"),
                        confidentiality_impact=Decimal("0"),
                        exploitability=Decimal("0.91"),
                        remediation_level=Decimal("0.97"),
                        severity_scope=Decimal("0"),
                        availability_requirement=Decimal("1"),
                    ),
                    sorts=FindingSorts.NO,
                    submission=FindingState(
                        modified_by="integratesmanager@gmail.com",
                        justification=StateRemovalJustification.NO_JUSTIFICATION,  # noqa: E501 pylint: disable=line-too-long
                        source=Source.ASM,
                        modified_date=datetime.fromisoformat(
                            "2018-04-08T00:45:11+00:00"
                        ),
                        status=FindingStateStatus.SUBMITTED,
                    ),
                    threat="An attacker can get passwords of users and "
                    "impersonate them or used the credentials for practices "
                    "malicious.",
                    unreliable_indicators=FindingUnreliableIndicators(
                        unreliable_closed_vulnerabilities=0,
                        unreliable_newest_vulnerability_report_date=(
                            datetime.fromisoformat("2020-01-03T17:46:10+00:00")
                        ),
                        unreliable_oldest_open_vulnerability_report_date=(
                            datetime.fromisoformat("2020-01-03T17:46:10+00:00")
                        ),
                        unreliable_oldest_vulnerability_report_date=(
                            datetime.fromisoformat("2020-01-03T17:46:10+00:00")
                        ),
                        unreliable_open_vulnerabilities=1,
                        unreliable_status=FindingStatus.VULNERABLE,
                        unreliable_treatment_summary=FindingTreatmentSummary(
                            accepted=0,
                            untreated=0,
                            in_progress=1,
                            accepted_undefined=0,
                        ),
                        unreliable_verification_summary=FindingVerificationSummary(  # noqa: E501 pylint: disable=line-too-long
                            verified=0,
                            requested=0,
                            on_hold=0,
                        ),
                        unreliable_where="test/data/lib_path/f060/csharp.cs",
                    ),
                ),
                Finding(
                    hacker_email="unittest@fluidattacks.com",
                    group_name="unittesting",
                    id="436992569",
                    state=FindingState(
                        modified_by="integratesmanager@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2019-04-08T05:00:00+00:00"
                        ),
                        source=Source.ASM,
                        status=FindingStateStatus.APPROVED,
                        rejection=None,
                        justification=StateRemovalJustification.NO_JUSTIFICATION,  # noqa: E501 pylint: disable=line-too-long
                    ),
                    title="038. Business information leak",
                    approval=FindingState(
                        modified_by="integratesmanager@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2019-04-08T05:00:00+00:00"
                        ),
                        source=Source.ASM,
                        status=FindingStateStatus.APPROVED,
                        rejection=None,
                        justification=StateRemovalJustification.NO_JUSTIFICATION,  # noqa: E501 pylint: disable=line-too-long
                    ),
                    attack_vector_description="Attack vector",
                    creation=FindingState(
                        modified_by="integratesmanager@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2019-04-08T05:00:00+00:00"
                        ),
                        source=Source.ASM,
                        status=FindingStateStatus.CREATED,
                        rejection=None,
                        justification=StateRemovalJustification.NO_JUSTIFICATION,  # noqa: E501 pylint: disable=line-too-long
                    ),
                    description="Se obtiene información de negocio, como: "
                    "lista de usuarios, información estratégica, "
                    "información de empleados, información de clientes, "
                    "información de proveedores",
                    evidences=FindingEvidences(
                        animation=FindingEvidence(
                            description="Animation descriptions",
                            modified_date=datetime.fromisoformat(
                                "2019-04-08T05:00:00+00:00"
                            ),
                            url="unittesting-436992569-animation.webm",
                        ),
                        evidence1=FindingEvidence(
                            description="Comm1",
                            modified_date=datetime.fromisoformat(
                                "2019-04-08T05:00:00+00:00"
                            ),
                            url="unittesting-436992569-evidence_route_1.png",
                        ),
                        evidence2=FindingEvidence(
                            description="Comm2",
                            modified_date=datetime.fromisoformat(
                                "2019-04-08T05:00:00+00:00"
                            ),
                            url="unittesting-436992569-evidence_route_2.jpg",
                        ),
                        evidence3=FindingEvidence(
                            description="Comm3",
                            modified_date=datetime.fromisoformat(
                                "2019-04-08T05:00:00+00:00"
                            ),
                            url="unittesting-436992569-evidence_route_3.png",
                        ),
                        evidence4=FindingEvidence(
                            description="Comm4",
                            modified_date=datetime.fromisoformat(
                                "2019-04-08T05:00:00+00:00"
                            ),
                            url="unittesting-436992569-evidence_route_4.png",
                        ),
                        evidence5=FindingEvidence(
                            description="Comm5",
                            modified_date=datetime.fromisoformat(
                                "2019-04-08T05:00:00+00:00"
                            ),
                            url="unittesting-436992569-evidence_route_5.png",
                        ),
                        exploitation=FindingEvidence(
                            description="Exploitation description",
                            modified_date=datetime.fromisoformat(
                                "2019-04-08T05:00:00+00:00"
                            ),
                            url="unittesting-436992569-exploitation.png",
                        ),
                        records=None,
                    ),
                    min_time_to_remediate=18,
                    recommendation="De acuerdo a la clasificación de la "
                    "información encontrada, establecer los controles "
                    "necesarios para que la información sea accesible sólo a "
                    "las personas indicadas.",
                    requirements="REQ.0176. El sistema debe restringir el "
                    "acceso a objetos del sistema que tengan contenido "
                    "sensible. Sólo permitirá su acceso a usuarios "
                    "autorizados.",
                    severity=Finding31Severity(
                        attack_complexity=Decimal("0.44"),
                        attack_vector=Decimal("0.62"),
                        availability_impact=Decimal("0.22"),
                        availability_requirement=Decimal("1.5"),
                        confidentiality_impact=Decimal("0"),
                        confidentiality_requirement=Decimal("1.5"),
                        exploitability=Decimal("0.97"),
                        integrity_impact=Decimal("0"),
                        integrity_requirement=Decimal("0.5"),
                        modified_attack_complexity=Decimal("0.77"),
                        modified_attack_vector=Decimal("0.85"),
                        modified_availability_impact=Decimal("0"),
                        modified_confidentiality_impact=Decimal("0"),
                        modified_integrity_impact=Decimal("0"),
                        modified_privileges_required=Decimal("0.85"),
                        modified_user_interaction=Decimal("0.85"),
                        modified_severity_scope=Decimal("0"),
                        privileges_required=Decimal("0.85"),
                        remediation_level=Decimal("0.97"),
                        report_confidence=Decimal("0.96"),
                        severity_scope=Decimal("1"),
                        user_interaction=Decimal("0.62"),
                    ),
                    sorts=FindingSorts.NO,
                    submission=FindingState(
                        modified_by="integratesmanager@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2019-04-08T05:00:00+00:00"
                        ),
                        source=Source.ASM,
                        status=FindingStateStatus.SUBMITTED,
                        rejection=None,
                        justification=StateRemovalJustification.NO_JUSTIFICATION,  # noqa: E501 pylint: disable=line-too-long
                    ),
                    threat="Risk.",
                    unreliable_indicators=FindingUnreliableIndicators(
                        unreliable_closed_vulnerabilities=4,
                        unreliable_newest_vulnerability_report_date=datetime.fromisoformat(  # noqa: E501 pylint: disable=line-too-long
                            "2019-09-16T21:01:24+00:00"
                        ),
                        unreliable_oldest_open_vulnerability_report_date=datetime.fromisoformat(  # noqa: E501 pylint: disable=line-too-long
                            "2019-08-30T14:30:13+00:00"
                        ),
                        unreliable_oldest_vulnerability_report_date=datetime.fromisoformat(  # noqa: E501 pylint: disable=line-too-long
                            "2019-08-30T14:30:13+00:00"
                        ),
                        unreliable_open_vulnerabilities=24,
                        unreliable_status=FindingStatus.VULNERABLE,
                        unreliable_treatment_summary=FindingTreatmentSummary(
                            accepted=0,
                            accepted_undefined=0,
                            in_progress=0,
                            untreated=24,
                        ),
                        unreliable_verification_summary=FindingVerificationSummary(  # noqa: E501 pylint: disable=line-too-long
                            requested=1,
                            on_hold=2,
                            verified=1,
                        ),
                        unreliable_where="192.168.1.10, 192.168.1.12, "
                        "192.168.1.13, 192.168.1.14, 192.168.1.15, "
                        "192.168.1.16, 192.168.1.17, 192.168.1.2, 192.168.1.3,"
                        " 192.168.1.4, 192.168.1.5, 192.168.1.6, 192.168.1.7, "
                        "192.168.1.8, 192.168.1.9, 192.168.100.101, "
                        "192.168.100.104, 192.168.100.105, 192.168.100.108, "
                        "192.168.100.111",
                    ),
                    verification=FindingVerification(
                        comment_id="1558048727111",
                        modified_by="integrateshacker@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2020-02-21T15:41:04+00:00"
                        ),
                        status=FindingVerificationStatus.VERIFIED,
                        vulnerability_ids={
                            "15375781-31f2-4953-ac77-f31134225747"
                        },
                    ),
                ),
                Finding(
                    hacker_email="unittest@fluidattacks.com",
                    group_name="unittesting",
                    id="457497316",
                    state=FindingState(
                        modified_by="integratesmanager@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2018-11-27T05:00:00+00:00"
                        ),
                        source=Source.ASM,
                        status=FindingStateStatus.APPROVED,
                        rejection=None,
                        justification=StateRemovalJustification.NO_JUSTIFICATION,  # noqa: E501 pylint: disable=line-too-long
                    ),
                    title="037. Technical information leak",
                    approval=FindingState(
                        modified_by="integratesmanager@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2018-11-27T05:00:00+00:00"
                        ),
                        source=Source.ASM,
                        status=FindingStateStatus.APPROVED,
                        rejection=None,
                        justification=StateRemovalJustification.NO_JUSTIFICATION,  # noqa: E501 pylint: disable=line-too-long
                    ),
                    attack_vector_description="Test description",
                    creation=FindingState(
                        modified_by="integratesmanager@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2018-04-08T00:43:18+00:00"
                        ),
                        source=Source.ASM,
                        status=FindingStateStatus.CREATED,
                        rejection=None,
                        justification=StateRemovalJustification.NO_JUSTIFICATION,  # noqa: E501 pylint: disable=line-too-long
                    ),
                    description="Descripción de fuga de información técnica",
                    evidences=FindingEvidences(
                        animation=None,
                        evidence1=None,
                        evidence2=FindingEvidence(
                            description="Test description",
                            modified_date=datetime.fromisoformat(
                                "2018-11-27T05:00:00+00:00"
                            ),
                            url="unittesting-457497316-evidence_route_2.jpg",
                        ),
                        evidence3=FindingEvidence(
                            description="Comentario",
                            modified_date=datetime.fromisoformat(
                                "2018-11-27T05:00:00+00:00"
                            ),
                            url="unittesting-457497316-evidence_route_3.png",
                        ),
                        evidence4=None,
                        evidence5=None,
                        exploitation=None,
                        records=None,
                    ),
                    min_time_to_remediate=18,
                    recommendation="Eliminar el banner de los servicios con "
                    "fuga de información, Verificar que los encabezados HTTP "
                    "no expongan ningún nombre o versión.",
                    requirements="REQ.0077. La aplicación no debe revelar "
                    "detalles del sistema interno como stack traces, "
                    "fragmentos de sentencias SQL y nombres de base de datos "
                    "o tablas. REQ.0176. El sistema debe restringir el acceso "
                    "a objetos del sistema que tengan contenido sensible. "
                    "Sólo permitirá su acceso a usuarios autorizados.",
                    severity=Finding31Severity(
                        attack_complexity=Decimal("0.44"),
                        attack_vector=Decimal("0.62"),
                        availability_impact=Decimal("0.22"),
                        availability_requirement=Decimal("1"),
                        confidentiality_impact=Decimal("0.22"),
                        confidentiality_requirement=Decimal("1"),
                        exploitability=Decimal("0.94"),
                        integrity_impact=Decimal("0.22"),
                        integrity_requirement=Decimal("1"),
                        modified_attack_complexity=Decimal("0.44"),
                        modified_attack_vector=Decimal("0.62"),
                        modified_availability_impact=Decimal("0.22"),
                        modified_confidentiality_impact=Decimal("0.22"),
                        modified_integrity_impact=Decimal("0.22"),
                        modified_privileges_required=Decimal("0.62"),
                        modified_user_interaction=Decimal("0.85"),
                        modified_severity_scope=Decimal("0"),
                        privileges_required=Decimal("0.62"),
                        remediation_level=Decimal("0.96"),
                        report_confidence=Decimal("0.92"),
                        severity_scope=Decimal("0"),
                        user_interaction=Decimal("0.85"),
                    ),
                    sorts=FindingSorts.NO,
                    submission=FindingState(
                        modified_by="integratesmanager@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2018-04-08T00:45:11+00:00"
                        ),
                        source=Source.ASM,
                        status=FindingStateStatus.SUBMITTED,
                        rejection=None,
                        justification=StateRemovalJustification.NO_JUSTIFICATION,  # noqa: E501 pylint: disable=line-too-long
                    ),
                    threat="Amenaza.",
                    unreliable_indicators=FindingUnreliableIndicators(
                        unreliable_closed_vulnerabilities=1,
                        unreliable_newest_vulnerability_report_date=datetime.fromisoformat(  # noqa: E501 pylint: disable=line-too-long
                            "2018-11-27T19:54:08+00:00"
                        ),
                        unreliable_oldest_open_vulnerability_report_date=datetime.fromisoformat(  # noqa: E501 pylint: disable=line-too-long
                            "2018-11-27T19:54:08+00:00"
                        ),
                        unreliable_oldest_vulnerability_report_date=datetime.fromisoformat(  # noqa: E501 pylint: disable=line-too-long
                            "2018-11-27T19:54:08+00:00"
                        ),
                        unreliable_open_vulnerabilities=0,
                        unreliable_status=FindingStatus.SAFE,
                        unreliable_treatment_summary=FindingTreatmentSummary(
                            accepted=0,
                            accepted_undefined=0,
                            in_progress=0,
                            untreated=0,
                        ),
                        unreliable_verification_summary=FindingVerificationSummary(  # noqa: E501 pylint: disable=line-too-long
                            requested=0, on_hold=0, verified=0
                        ),
                        unreliable_where="",
                    ),
                    verification=None,
                ),
                Finding(
                    hacker_email="unittest@fluidattacks.com",
                    group_name="unittesting",
                    id="463461507",
                    state=FindingState(
                        modified_by="integratesmanager@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2019-01-10T05:00:00+00:00"
                        ),
                        source=Source.ASM,
                        status=FindingStateStatus.APPROVED,
                        rejection=None,
                        justification=StateRemovalJustification.NO_JUSTIFICATION,  # noqa: E501 pylint: disable=line-too-long
                    ),
                    title="083. XML injection (XXE)",
                    approval=FindingState(
                        modified_by="integratesmanager@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2019-01-10T05:00:00+00:00"
                        ),
                        source=Source.ASM,
                        status=FindingStateStatus.APPROVED,
                        rejection=None,
                        justification=StateRemovalJustification.NO_JUSTIFICATION,  # noqa: E501 pylint: disable=line-too-long
                    ),
                    attack_vector_description="Test attack vector.",
                    creation=FindingState(
                        modified_by="integratesmanager@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2018-04-08T00:43:18+00:00"
                        ),
                        source=Source.ASM,
                        status=FindingStateStatus.CREATED,
                        rejection=None,
                        justification=StateRemovalJustification.NO_JUSTIFICATION,  # noqa: E501 pylint: disable=line-too-long
                    ),
                    description="La aplicacion afectada permite la inyecion "
                    "de codigo XML que es ejecutado de forma remota y permite "
                    "la exfiltracion de archivos o ejecucioemota de comandos "
                    "en el servidor.",
                    evidences=FindingEvidences(
                        animation=FindingEvidence(
                            description="Animation test",
                            modified_date=datetime.fromisoformat(
                                "2019-01-10T05:00:00+00:00"
                            ),
                            url="unittesting-463461507-animation.webm",
                        ),
                        evidence1=None,
                        evidence2=FindingEvidence(
                            description="A2 test",
                            modified_date=datetime.fromisoformat(
                                "2019-01-10T05:00:00+00:00"
                            ),
                            url="unittesting-463461507-evidence_route_2.jpg",
                        ),
                        evidence3=FindingEvidence(
                            description="123A",
                            modified_date=datetime.fromisoformat(
                                "2019-01-10T05:00:00+00:00"
                            ),
                            url="unittesting-463461507-evidence_route_3.png",
                        ),
                        evidence4=FindingEvidence(
                            description="AAA1",
                            modified_date=datetime.fromisoformat(
                                "2019-01-10T05:00:00+00:00"
                            ),
                            url="unittesting-463461507-evidence_route_4.png",
                        ),
                        evidence5=FindingEvidence(
                            description="sdasdasda",
                            modified_date=datetime.fromisoformat(
                                "2019-01-10T05:00:00+00:00"
                            ),
                            url="unittesting-463461507-evidence_route_5.png",
                        ),
                        exploitation=None,
                        records=None,
                    ),
                    min_time_to_remediate=18,
                    recommendation="Filtrar la informacioue recibe y envia la "
                    "aplicacioor medio de listas blancas",
                    requirements="REQ.0173. El sistema debe descartar toda la "
                    "informacion potencialmente insegura que sea recibida "
                    "por entradas de datos.",
                    severity=Finding31Severity(
                        attack_complexity=Decimal("0.44"),
                        attack_vector=Decimal("0.62"),
                        availability_impact=Decimal("0.22"),
                        availability_requirement=Decimal("1"),
                        confidentiality_impact=Decimal("0.22"),
                        confidentiality_requirement=Decimal("1.5"),
                        exploitability=Decimal("0.94"),
                        integrity_impact=Decimal("0"),
                        integrity_requirement=Decimal("1"),
                        modified_attack_complexity=Decimal("0.44"),
                        modified_attack_vector=Decimal("0.62"),
                        modified_availability_impact=Decimal("0.22"),
                        modified_confidentiality_impact=Decimal("0.22"),
                        modified_integrity_impact=Decimal("0"),
                        modified_privileges_required=Decimal("0.85"),
                        modified_user_interaction=Decimal("0.62"),
                        modified_severity_scope=Decimal("0"),
                        privileges_required=Decimal("0.85"),
                        remediation_level=Decimal("0.95"),
                        report_confidence=Decimal("0.96"),
                        severity_scope=Decimal("0"),
                        user_interaction=Decimal("0.62"),
                    ),
                    sorts=FindingSorts.NO,
                    submission=FindingState(
                        modified_by="integratesmanager@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2018-04-08T00:45:11+00:00"
                        ),
                        source=Source.ASM,
                        status=FindingStateStatus.SUBMITTED,
                        rejection=None,
                        justification=StateRemovalJustification.NO_JUSTIFICATION,  # noqa: E501 pylint: disable=line-too-long
                    ),
                    threat="Test threat",
                    unreliable_indicators=FindingUnreliableIndicators(
                        unreliable_closed_vulnerabilities=0,
                        unreliable_newest_vulnerability_report_date=datetime.fromisoformat(  # noqa: E501 pylint: disable=line-too-long
                            "2019-09-13T14:58:38+00:00"
                        ),
                        unreliable_oldest_open_vulnerability_report_date=datetime.fromisoformat(  # noqa: E501 pylint: disable=line-too-long
                            "2019-09-12T13:45:48+00:00"
                        ),
                        unreliable_oldest_vulnerability_report_date=datetime.fromisoformat(  # noqa: E501 pylint: disable=line-too-long
                            "2019-09-12T13:45:48+00:00"
                        ),
                        unreliable_open_vulnerabilities=2,
                        unreliable_status=FindingStatus.VULNERABLE,
                        unreliable_treatment_summary=FindingTreatmentSummary(
                            accepted=1,
                            accepted_undefined=0,
                            in_progress=0,
                            untreated=1,
                        ),
                        unreliable_verification_summary=FindingVerificationSummary(  # noqa: E501 pylint: disable=line-too-long
                            requested=0, on_hold=0, verified=0
                        ),
                        unreliable_where="192.168.1.18, 192.168.100.105",
                    ),
                    verification=None,
                ),
                Finding(
                    hacker_email="unittest@fluidattacks.com",
                    group_name="unittesting",
                    id="463558592",
                    state=FindingState(
                        modified_by="integratesmanager@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2018-12-17T05:00:00+00:00"
                        ),
                        source=Source.ASM,
                        status=FindingStateStatus.APPROVED,
                        rejection=None,
                        justification=StateRemovalJustification.NO_JUSTIFICATION,  # noqa: E501 pylint: disable=line-too-long
                    ),
                    title="007. Cross-site request forgery",
                    approval=FindingState(
                        modified_by="integratesmanager@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2018-12-17T05:00:00+00:00"
                        ),
                        source=Source.ASM,
                        status=FindingStateStatus.APPROVED,
                        rejection=None,
                        justification=StateRemovalJustification.NO_JUSTIFICATION,  # noqa: E501 pylint: disable=line-too-long
                    ),
                    attack_vector_description="Test description",
                    creation=FindingState(
                        modified_by="integratesmanager@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2018-04-08T00:43:18+00:00"
                        ),
                        source=Source.ASM,
                        status=FindingStateStatus.CREATED,
                        rejection=None,
                        justification=StateRemovalJustification.NO_JUSTIFICATION,  # noqa: E501 pylint: disable=line-too-long
                    ),
                    description="La aplicación permite engañar a un usuario "
                    "autenticado por medio de links manipulados para ejecutar "
                    "acciones sobre la aplicación sin su consentimiento.",
                    evidences=FindingEvidences(
                        animation=None,
                        evidence1=FindingEvidence(
                            description="This is test description",
                            modified_date=datetime.fromisoformat(
                                "2018-12-17T05:00:00+00:00"
                            ),
                            url="unittesting-463558592-evidence_route_1.png",
                        ),
                        evidence2=FindingEvidence(
                            description="Test descrip",
                            modified_date=datetime.fromisoformat(
                                "2018-12-17T05:00:00+00:00"
                            ),
                            url="unittesting-463558592-evidence_route_2.jpg",
                        ),
                        evidence3=FindingEvidence(
                            description="Test description number 3",
                            modified_date=datetime.fromisoformat(
                                "2018-12-17T05:00:00+00:00"
                            ),
                            url="unittesting-463558592-evidence_route_3.png",
                        ),
                        evidence4=FindingEvidence(
                            description="An error",
                            modified_date=datetime.fromisoformat(
                                "2018-12-17T05:00:00+00:00"
                            ),
                            url="unittesting-463558592-evidence_route_4.png",
                        ),
                        evidence5=FindingEvidence(
                            description="Test descip 4",
                            modified_date=datetime.fromisoformat(
                                "2018-12-17T05:00:00+00:00"
                            ),
                            url="unittesting-463558592-evidence_route_5.png",
                        ),
                        exploitation=None,
                        records=None,
                    ),
                    min_time_to_remediate=18,
                    recommendation="Hacer uso de tokens en los formularios "
                    "para la verificación de las peticiones realizadas por "
                    "usuarios legítimos.",
                    requirements="REQ.0174. La aplicación debe garantizar que "
                    "las peticiones que ejecuten transacciones no sigan un "
                    "patrón discernible.",
                    severity=Finding31Severity(
                        attack_complexity=Decimal("0.44"),
                        attack_vector=Decimal("0.62"),
                        availability_impact=Decimal("0"),
                        availability_requirement=Decimal("1"),
                        confidentiality_impact=Decimal("0.56"),
                        confidentiality_requirement=Decimal("1"),
                        exploitability=Decimal("0.91"),
                        integrity_impact=Decimal("0.22"),
                        integrity_requirement=Decimal("1.5"),
                        modified_attack_complexity=Decimal("0.44"),
                        modified_attack_vector=Decimal("0.62"),
                        modified_availability_impact=Decimal("0"),
                        modified_confidentiality_impact=Decimal("0.56"),
                        modified_integrity_impact=Decimal("0.22"),
                        modified_privileges_required=Decimal("0.62"),
                        modified_user_interaction=Decimal("0.62"),
                        modified_severity_scope=Decimal("0"),
                        privileges_required=Decimal("0.62"),
                        remediation_level=Decimal("0.95"),
                        report_confidence=Decimal("0.96"),
                        severity_scope=Decimal("0"),
                        user_interaction=Decimal("0.62"),
                    ),
                    sorts=FindingSorts.NO,
                    submission=FindingState(
                        modified_by="integratesmanager@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2018-04-08T00:45:11+00:00"
                        ),
                        source=Source.ASM,
                        status=FindingStateStatus.SUBMITTED,
                        rejection=None,
                        justification=StateRemovalJustification.NO_JUSTIFICATION,  # noqa: E501 pylint: disable=line-too-long
                    ),
                    threat="Test.",
                    unreliable_indicators=FindingUnreliableIndicators(
                        unreliable_closed_vulnerabilities=1,
                        unreliable_newest_vulnerability_report_date=datetime.fromisoformat(  # noqa: E501 pylint: disable=line-too-long
                            "2019-01-15T16:04:14+00:00"
                        ),
                        unreliable_oldest_open_vulnerability_report_date=datetime.fromisoformat(  # noqa: E501 pylint: disable=line-too-long
                            "2019-01-15T16:04:14+00:00"
                        ),
                        unreliable_oldest_vulnerability_report_date=datetime.fromisoformat(  # noqa: E501 pylint: disable=line-too-long
                            "2019-01-15T16:04:14+00:00"
                        ),
                        unreliable_open_vulnerabilities=1,
                        unreliable_status=FindingStatus.VULNERABLE,
                        unreliable_treatment_summary=FindingTreatmentSummary(
                            accepted=1,
                            accepted_undefined=0,
                            in_progress=0,
                            untreated=0,
                        ),
                        unreliable_verification_summary=FindingVerificationSummary(  # noqa: E501 pylint: disable=line-too-long
                            requested=0, on_hold=0, verified=0
                        ),
                        unreliable_where="path/to/file2.ext",
                    ),
                    verification=FindingVerification(
                        comment_id="1558048727999",
                        modified_by="integratesuser@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2020-01-19T15:41:04+00:00"
                        ),
                        status=FindingVerificationStatus.REQUESTED,
                        vulnerability_ids={
                            "74632c0c-db08-47c2-b013-c70e5b67c49f",
                            "3bcdb384-5547-4170-a0b6-3b397a245465",
                        },
                    ),
                ),
                Finding(
                    hacker_email="unittest@fluidattacks.com",
                    group_name="unittesting",
                    id="560175507",
                    state=FindingState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2019-02-07T17:46:10+00:00"
                        ),
                        source=Source.ASM,
                        status=FindingStateStatus.REJECTED,
                        rejection=DraftRejection(
                            other="Test",
                            reasons={DraftRejectionReason.OMISSION},
                            rejected_by="customer_manager@fluidattacks.com",
                            rejection_date=datetime.fromisoformat(
                                "2019-02-07T17:46:10+00:00"
                            ),
                            submitted_by="unittest@fluidattacks.com",
                        ),
                        justification=StateRemovalJustification.NO_JUSTIFICATION,  # noqa: E501 pylint: disable=line-too-long
                    ),
                    title="006. Authentication mechanism absence or evasion",
                    approval=None,
                    attack_vector_description="Test attack vector.",
                    creation=FindingState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2019-02-07T17:46:10+00:00"
                        ),
                        source=Source.ASM,
                        status=FindingStateStatus.CREATED,
                        rejection=None,
                        justification=StateRemovalJustification.NO_JUSTIFICATION,  # noqa: E501 pylint: disable=line-too-long
                    ),
                    description="La aplicación afectada permite la inyeccion "
                    "de XML que es ejecutado de forma remota y permite la "
                    "exfiltracion de archivos o ejecucio remota de comandos "
                    "en el servidor.",
                    evidences=FindingEvidences(
                        animation=None,
                        evidence1=None,
                        evidence2=None,
                        evidence3=None,
                        evidence4=None,
                        evidence5=None,
                        exploitation=None,
                        records=None,
                    ),
                    min_time_to_remediate=18,
                    recommendation="Filtrar la informacion recibe y envia la "
                    "aplicacion medio de listas blancas",
                    requirements="REQ.0173. El sistema debe descartar toda la "
                    "informacion potencialmente insegura que sea recibida por "
                    "entradas de datos.",
                    severity=Finding31Severity(
                        attack_complexity=Decimal("0.44"),
                        attack_vector=Decimal("0.62"),
                        availability_impact=Decimal("0.22"),
                        availability_requirement=Decimal("1"),
                        confidentiality_impact=Decimal("0.22"),
                        confidentiality_requirement=Decimal("1.5"),
                        exploitability=Decimal("0.94"),
                        integrity_impact=Decimal("0"),
                        integrity_requirement=Decimal("1"),
                        modified_attack_complexity=Decimal("0.44"),
                        modified_attack_vector=Decimal("0.62"),
                        modified_availability_impact=Decimal("0.22"),
                        modified_confidentiality_impact=Decimal("0.22"),
                        modified_integrity_impact=Decimal("0"),
                        modified_privileges_required=Decimal("0.85"),
                        modified_user_interaction=Decimal("0.62"),
                        modified_severity_scope=Decimal("0"),
                        privileges_required=Decimal("0.85"),
                        remediation_level=Decimal("0.95"),
                        report_confidence=Decimal("0.96"),
                        severity_scope=Decimal("0"),
                        user_interaction=Decimal("0.62"),
                    ),
                    sorts=FindingSorts.NO,
                    submission=None,
                    threat="Test threat",
                    unreliable_indicators=FindingUnreliableIndicators(
                        unreliable_closed_vulnerabilities=0,
                        unreliable_newest_vulnerability_report_date=datetime.fromisoformat(  # noqa: E501 pylint: disable=line-too-long
                            "2019-09-13T14:58:38+00:00"
                        ),
                        unreliable_oldest_open_vulnerability_report_date=datetime.fromisoformat(  # noqa: E501 pylint: disable=line-too-long
                            "2020-09-12T13:45:48+00:00"
                        ),
                        unreliable_oldest_vulnerability_report_date=datetime.fromisoformat(  # noqa: E501 pylint: disable=line-too-long
                            "2020-09-12T13:45:48+00:00"
                        ),
                        unreliable_open_vulnerabilities=0,
                        unreliable_status=FindingStatus.SAFE,
                        unreliable_treatment_summary=FindingTreatmentSummary(
                            accepted=0,
                            accepted_undefined=0,
                            in_progress=0,
                            untreated=0,
                        ),
                        unreliable_verification_summary=FindingVerificationSummary(  # noqa: E501 pylint: disable=line-too-long
                            requested=0, on_hold=0, verified=0
                        ),
                        unreliable_where="",
                    ),
                    verification=None,
                ),
                Finding(
                    hacker_email="unittest@fluidattacks.com",
                    group_name="unittesting",
                    id="563827909",
                    state=FindingState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2022-08-22T17:46:10+00:00"
                        ),
                        source=Source.ASM,
                        status=FindingStateStatus.CREATED,
                        rejection=None,
                        justification=StateRemovalJustification.NO_JUSTIFICATION,  # noqa: E501 pylint: disable=line-too-long
                    ),
                    title="379. Inappropriate coding practices - "
                    "Unnecessary imports",
                    approval=None,
                    attack_vector_description="Test attack vector.",
                    creation=FindingState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2022-08-22T17:46:10+00:00"
                        ),
                        source=Source.ASM,
                        status=FindingStateStatus.CREATED,
                        rejection=None,
                        justification=StateRemovalJustification.NO_JUSTIFICATION,  # noqa: E501 pylint: disable=line-too-long
                    ),
                    description="The application imports modules that are not "
                    "used. This is a bad practice because it loads modules "
                    "that will not be used, and doing so unnecessarily "
                    "increases the load.",
                    evidences=FindingEvidences(
                        animation=None,
                        evidence1=None,
                        evidence2=None,
                        evidence3=None,
                        evidence4=None,
                        evidence5=None,
                        exploitation=None,
                        records=None,
                    ),
                    min_time_to_remediate=15,
                    recommendation="Import only the modules necessary for the "
                    "correct functionality of the application.",
                    requirements="158. System source code must be implemented "
                    "in a stable, updated, tested and free of known "
                    "vulnerabilities version of the chosen programming "
                    "language.",
                    severity=Finding31Severity(
                        attack_complexity=Decimal("0.44"),
                        attack_vector=Decimal("0.85"),
                        availability_impact=Decimal("0.22"),
                        availability_requirement=Decimal("1"),
                        confidentiality_impact=Decimal("0"),
                        confidentiality_requirement=Decimal("1.5"),
                        exploitability=Decimal("0.91"),
                        integrity_impact=Decimal("0"),
                        integrity_requirement=Decimal("1"),
                        modified_attack_complexity=Decimal("0.44"),
                        modified_attack_vector=Decimal("0.62"),
                        modified_availability_impact=Decimal("0.22"),
                        modified_confidentiality_impact=Decimal("0.22"),
                        modified_integrity_impact=Decimal("0"),
                        modified_privileges_required=Decimal("0.85"),
                        modified_user_interaction=Decimal("0.62"),
                        modified_severity_scope=Decimal("0"),
                        privileges_required=Decimal("0.62"),
                        remediation_level=Decimal("0.95"),
                        report_confidence=Decimal("0.96"),
                        severity_scope=Decimal("0"),
                        user_interaction=Decimal("0.85"),
                    ),
                    sorts=FindingSorts.NO,
                    submission=None,
                    threat="Authorized attacker from the Internet with access "
                    "to the application.",
                    unreliable_indicators=FindingUnreliableIndicators(
                        unreliable_closed_vulnerabilities=0,
                        unreliable_newest_vulnerability_report_date=datetime.fromisoformat(  # noqa: E501 pylint: disable=line-too-long
                            "2019-09-13T14:58:38+00:00"
                        ),
                        unreliable_oldest_open_vulnerability_report_date=datetime.fromisoformat(  # noqa: E501 pylint: disable=line-too-long
                            "2020-09-12T13:45:48+00:00"
                        ),
                        unreliable_oldest_vulnerability_report_date=datetime.fromisoformat(  # noqa: E501 pylint: disable=line-too-long
                            "2020-09-12T13:45:48+00:00"
                        ),
                        unreliable_open_vulnerabilities=0,
                        unreliable_status=FindingStatus.SAFE,
                        unreliable_treatment_summary=FindingTreatmentSummary(
                            accepted=0,
                            accepted_undefined=0,
                            in_progress=0,
                            untreated=0,
                        ),
                        unreliable_verification_summary=FindingVerificationSummary(  # noqa: E501 pylint: disable=line-too-long
                            requested=0, on_hold=0, verified=0
                        ),
                        unreliable_where="",
                    ),
                    verification=None,
                ),
                Finding(
                    hacker_email="integratesmanager@gmail.com",
                    group_name="unittesting",
                    id="988493279",
                    state=FindingState(
                        modified_by="integratesmanager@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2019-04-08T00:45:15+00:00"
                        ),
                        source=Source.ASM,
                        status=FindingStateStatus.APPROVED,
                        rejection=None,
                        justification=StateRemovalJustification.NO_JUSTIFICATION,  # noqa: E501 pylint: disable=line-too-long
                    ),
                    title="014. Insecure functionality",
                    approval=FindingState(
                        modified_by="integratesmanager@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2019-04-08T00:45:15+00:00"
                        ),
                        source=Source.ASM,
                        status=FindingStateStatus.APPROVED,
                        rejection=None,
                        justification=StateRemovalJustification.NO_JUSTIFICATION,  # noqa: E501 pylint: disable=line-too-long
                    ),
                    attack_vector_description="Test description",
                    creation=FindingState(
                        modified_by="integratesmanager@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2019-04-08T00:43:18+00:00"
                        ),
                        source=Source.ASM,
                        status=FindingStateStatus.CREATED,
                        rejection=None,
                        justification=StateRemovalJustification.NO_JUSTIFICATION,  # noqa: E501 pylint: disable=line-too-long
                    ),
                    description="Insecure funtionality",
                    evidences=FindingEvidences(
                        animation=None,
                        evidence1=None,
                        evidence2=None,
                        evidence3=None,
                        evidence4=None,
                        evidence5=None,
                        exploitation=FindingEvidence(
                            description="Exploitation description",
                            modified_date=datetime.fromisoformat(
                                "2019-04-08T00:45:15+00:00"
                            ),
                            url="unittesting-988493279-exploitation.png",
                        ),
                        records=None,
                    ),
                    min_time_to_remediate=20,
                    recommendation="Test recomendation",
                    requirements="REQ.0266. La organización debe deshabilitar "
                    "las funciones inseguras de un sistema. "
                    "(hardening de sistemas)",
                    severity=Finding31Severity(
                        attack_complexity=Decimal("0.77"),
                        attack_vector=Decimal("0.85"),
                        availability_impact=Decimal("0.22"),
                        availability_requirement=Decimal("0.5"),
                        confidentiality_impact=Decimal("0.22"),
                        confidentiality_requirement=Decimal("1.5"),
                        exploitability=Decimal("0.94"),
                        integrity_impact=Decimal("0.22"),
                        integrity_requirement=Decimal("1"),
                        modified_attack_complexity=Decimal("0.77"),
                        modified_attack_vector=Decimal("0.55"),
                        modified_availability_impact=Decimal("0"),
                        modified_confidentiality_impact=Decimal("0"),
                        modified_integrity_impact=Decimal("0"),
                        modified_privileges_required=Decimal("0.62"),
                        modified_user_interaction=Decimal("0.85"),
                        modified_severity_scope=Decimal("0"),
                        privileges_required=Decimal("0.85"),
                        remediation_level=Decimal("0.95"),
                        report_confidence=Decimal("0.96"),
                        severity_scope=Decimal("0"),
                        user_interaction=Decimal("0.85"),
                    ),
                    sorts=FindingSorts.NO,
                    submission=FindingState(
                        modified_by="integratesmanager@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2019-04-08T00:45:11+00:00"
                        ),
                        source=Source.ASM,
                        status=FindingStateStatus.SUBMITTED,
                        rejection=None,
                        justification=StateRemovalJustification.NO_JUSTIFICATION,  # noqa: E501 pylint: disable=line-too-long
                    ),
                    threat="Test threat",
                    unreliable_indicators=FindingUnreliableIndicators(
                        unreliable_closed_vulnerabilities=1,
                        unreliable_newest_vulnerability_report_date=datetime.fromisoformat(  # noqa: E501 pylint: disable=line-too-long
                            "2019-04-08T00:45:15+00:00"
                        ),
                        unreliable_oldest_open_vulnerability_report_date=datetime.fromisoformat(  # noqa: E501 pylint: disable=line-too-long
                            "2019-04-08T00:45:15+00:00"
                        ),
                        unreliable_oldest_vulnerability_report_date=datetime.fromisoformat(  # noqa: E501 pylint: disable=line-too-long
                            "2019-04-08T00:45:15+00:00"
                        ),
                        unreliable_open_vulnerabilities=1,
                        unreliable_status=FindingStatus.VULNERABLE,
                        unreliable_treatment_summary=FindingTreatmentSummary(
                            accepted=0,
                            accepted_undefined=1,
                            in_progress=0,
                            untreated=0,
                        ),
                        unreliable_verification_summary=FindingVerificationSummary(  # noqa: E501 pylint: disable=line-too-long
                            requested=0, on_hold=0, verified=0
                        ),
                        unreliable_where="192.168.1.19",
                    ),
                    verification=None,
                ),
            ]
        )
    },
    "db_model.findings.get.GroupFindingsLoader.load": {
        '["unittesting"]': tuple(
            [
                Finding(
                    hacker_email="unittest@fluidattacks.com",
                    group_name="unittesting",
                    id="422286126",
                    state=FindingState(
                        modified_by="integratesmanager@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2018-07-09T05:00:00+00:00"
                        ),
                        source=Source.ASM,
                        status=FindingStateStatus.APPROVED,
                        rejection=None,
                        justification=StateRemovalJustification.NO_JUSTIFICATION,  # noqa: E501 pylint: disable=line-too-long
                    ),
                    title="060. Insecure service configuration - Host "
                    "verification",
                    approval=FindingState(
                        modified_by="integratesmanager@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2018-07-09T05:00:00+00:00"
                        ),
                        source=Source.ASM,
                        status=FindingStateStatus.APPROVED,
                        rejection=None,
                        justification=StateRemovalJustification.NO_JUSTIFICATION,  # noqa: E501 pylint: disable=line-too-long
                    ),
                    attack_vector_description="This is an attack vector",
                    creation=FindingState(
                        modified_by="integratesmanager@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2018-04-08T00:43:18+00:00"
                        ),
                        source=Source.ASM,
                        status=FindingStateStatus.CREATED,
                        rejection=None,
                        justification=StateRemovalJustification.NO_JUSTIFICATION,  # noqa: E501 pylint: disable=line-too-long
                    ),
                    description="The source code uses generic exceptions to "
                    "handle unexpected errors. Catching generic exceptions "
                    "obscures the problem that caused the error and promotes "
                    "a generic way to handle different categories or sources "
                    "of error. This may cause security vulnerabilities to "
                    "materialize, as some special flows go unnoticed.",
                    evidences=FindingEvidences(
                        animation=FindingEvidence(
                            modified_date=datetime.fromisoformat(
                                "2018-07-09T05:00:00+00:00"
                            ),
                            description="Test description",
                            url="unittesting-422286126-animation.gif",
                        ),
                        evidence1=FindingEvidence(
                            modified_date=datetime.fromisoformat(
                                "2018-07-09T05:00:00+00:00"
                            ),
                            description="this is a test description",
                            url="unittesting-422286126-evidence_route_1.png",
                        ),
                        evidence2=FindingEvidence(
                            modified_date=datetime.fromisoformat(
                                "2018-07-09T05:00:00+00:00"
                            ),
                            description="exception",
                            url="unittesting-422286126-evidence_route_2.jpg",
                        ),
                        evidence3=FindingEvidence(
                            modified_date=datetime.fromisoformat(
                                "2018-07-09T05:00:00+00:00"
                            ),
                            description="Description",
                            url="unittesting-422286126-evidence_route_3.png",
                        ),
                        evidence4=FindingEvidence(
                            modified_date=datetime.fromisoformat(
                                "2018-07-09T05:00:00+00:00"
                            ),
                            description="changed for testing purposes",
                            url="unittesting-422286126-evidence_route_4.png",
                        ),
                        evidence5=FindingEvidence(
                            modified_date=datetime.fromisoformat(
                                "2018-07-09T05:00:00+00:00"
                            ),
                            description="Test description",
                            url="unittesting-422286126-evidence_route_5.png",
                        ),
                        exploitation=FindingEvidence(
                            modified_date=datetime.fromisoformat(
                                "2018-07-09T05:00:00+00:00"
                            ),
                            description="test",
                            url="unittesting-422286126-exploitation.png",
                        ),
                        records=FindingEvidence(
                            modified_date=datetime.fromisoformat(
                                "2018-07-09T05:00:00+00:00"
                            ),
                            description="test",
                            url="unittesting-422286126-evidence_file.csv",
                        ),
                    ),
                    min_time_to_remediate=18,
                    recommendation="Implement password policies with the best "
                    "practicies for strong passwords.",
                    requirements="R359. Avoid using generic exceptions.",
                    severity=Finding31Severity(
                        attack_complexity=Decimal("0.77"),
                        integrity_impact=Decimal("0.22"),
                        integrity_requirement=Decimal("1"),
                        modified_confidentiality_impact=Decimal("0"),
                        modified_user_interaction=Decimal("0.85"),
                        modified_severity_scope=Decimal("0"),
                        modified_availability_impact=Decimal("0"),
                        report_confidence=Decimal("0.92"),
                        modified_integrity_impact=Decimal("0.22"),
                        attack_vector=Decimal("0.62"),
                        modified_attack_complexity=Decimal("0.77"),
                        privileges_required=Decimal("0.62"),
                        availability_impact=Decimal("0"),
                        modified_privileges_required=Decimal("0.62"),
                        confidentiality_requirement=Decimal("1"),
                        modified_attack_vector=Decimal("0.62"),
                        user_interaction=Decimal("0.85"),
                        confidentiality_impact=Decimal("0"),
                        exploitability=Decimal("0.91"),
                        remediation_level=Decimal("0.97"),
                        severity_scope=Decimal("0"),
                        availability_requirement=Decimal("1"),
                    ),
                    sorts=FindingSorts.NO,
                    submission=FindingState(
                        modified_by="integratesmanager@gmail.com",
                        justification=StateRemovalJustification.NO_JUSTIFICATION,  # noqa: E501 pylint: disable=line-too-long
                        source=Source.ASM,
                        modified_date=datetime.fromisoformat(
                            "2018-04-08T00:45:11+00:00"
                        ),
                        status=FindingStateStatus.SUBMITTED,
                    ),
                    threat="An attacker can get passwords of users and "
                    "impersonate them or used the credentials for practices "
                    "malicious.",
                    unreliable_indicators=FindingUnreliableIndicators(
                        unreliable_closed_vulnerabilities=0,
                        unreliable_newest_vulnerability_report_date=(
                            datetime.fromisoformat("2020-01-03T17:46:10+00:00")
                        ),
                        unreliable_oldest_open_vulnerability_report_date=(
                            datetime.fromisoformat("2020-01-03T17:46:10+00:00")
                        ),
                        unreliable_oldest_vulnerability_report_date=(
                            datetime.fromisoformat("2020-01-03T17:46:10+00:00")
                        ),
                        unreliable_open_vulnerabilities=1,
                        unreliable_status=FindingStatus.VULNERABLE,
                        unreliable_treatment_summary=FindingTreatmentSummary(
                            accepted=0,
                            untreated=0,
                            in_progress=1,
                            accepted_undefined=0,
                        ),
                        unreliable_verification_summary=FindingVerificationSummary(  # noqa: E501 pylint: disable=line-too-long
                            verified=0,
                            requested=0,
                            on_hold=0,
                        ),
                        unreliable_where="test/data/lib_path/f060/csharp.cs",
                    ),
                ),
                Finding(
                    hacker_email="unittest@fluidattacks.com",
                    group_name="unittesting",
                    id="436992569",
                    state=FindingState(
                        modified_by="integratesmanager@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2019-04-08T05:00:00+00:00"
                        ),
                        source=Source.ASM,
                        status=FindingStateStatus.APPROVED,
                        rejection=None,
                        justification=StateRemovalJustification.NO_JUSTIFICATION,  # noqa: E501 pylint: disable=line-too-long
                    ),
                    title="038. Business information leak",
                    approval=FindingState(
                        modified_by="integratesmanager@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2019-04-08T05:00:00+00:00"
                        ),
                        source=Source.ASM,
                        status=FindingStateStatus.APPROVED,
                        rejection=None,
                        justification=StateRemovalJustification.NO_JUSTIFICATION,  # noqa: E501 pylint: disable=line-too-long
                    ),
                    attack_vector_description="Attack vector",
                    creation=FindingState(
                        modified_by="integratesmanager@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2019-04-08T05:00:00+00:00"
                        ),
                        source=Source.ASM,
                        status=FindingStateStatus.CREATED,
                        rejection=None,
                        justification=StateRemovalJustification.NO_JUSTIFICATION,  # noqa: E501 pylint: disable=line-too-long
                    ),
                    description="Se obtiene información de negocio, como: "
                    "lista de usuarios, información estratégica, "
                    "información de empleados, información de clientes, "
                    "información de proveedores",
                    evidences=FindingEvidences(
                        animation=FindingEvidence(
                            description="Animation descriptions",
                            modified_date=datetime.fromisoformat(
                                "2019-04-08T05:00:00+00:00"
                            ),
                            url="unittesting-436992569-animation.webm",
                        ),
                        evidence1=FindingEvidence(
                            description="Comm1",
                            modified_date=datetime.fromisoformat(
                                "2019-04-08T05:00:00+00:00"
                            ),
                            url="unittesting-436992569-evidence_route_1.png",
                        ),
                        evidence2=FindingEvidence(
                            description="Comm2",
                            modified_date=datetime.fromisoformat(
                                "2019-04-08T05:00:00+00:00"
                            ),
                            url="unittesting-436992569-evidence_route_2.jpg",
                        ),
                        evidence3=FindingEvidence(
                            description="Comm3",
                            modified_date=datetime.fromisoformat(
                                "2019-04-08T05:00:00+00:00"
                            ),
                            url="unittesting-436992569-evidence_route_3.png",
                        ),
                        evidence4=FindingEvidence(
                            description="Comm4",
                            modified_date=datetime.fromisoformat(
                                "2019-04-08T05:00:00+00:00"
                            ),
                            url="unittesting-436992569-evidence_route_4.png",
                        ),
                        evidence5=FindingEvidence(
                            description="Comm5",
                            modified_date=datetime.fromisoformat(
                                "2019-04-08T05:00:00+00:00"
                            ),
                            url="unittesting-436992569-evidence_route_5.png",
                        ),
                        exploitation=FindingEvidence(
                            description="Exploitation description",
                            modified_date=datetime.fromisoformat(
                                "2019-04-08T05:00:00+00:00"
                            ),
                            url="unittesting-436992569-exploitation.png",
                        ),
                        records=None,
                    ),
                    min_time_to_remediate=18,
                    recommendation="De acuerdo a la clasificación de la "
                    "información encontrada, establecer los controles "
                    "necesarios para que la información sea accesible sólo a "
                    "las personas indicadas.",
                    requirements="REQ.0176. El sistema debe restringir el "
                    "acceso a objetos del sistema que tengan contenido "
                    "sensible. Sólo permitirá su acceso a usuarios "
                    "autorizados.",
                    severity=Finding31Severity(
                        attack_complexity=Decimal("0.44"),
                        attack_vector=Decimal("0.62"),
                        availability_impact=Decimal("0.22"),
                        availability_requirement=Decimal("1.5"),
                        confidentiality_impact=Decimal("0"),
                        confidentiality_requirement=Decimal("1.5"),
                        exploitability=Decimal("0.97"),
                        integrity_impact=Decimal("0"),
                        integrity_requirement=Decimal("0.5"),
                        modified_attack_complexity=Decimal("0.77"),
                        modified_attack_vector=Decimal("0.85"),
                        modified_availability_impact=Decimal("0"),
                        modified_confidentiality_impact=Decimal("0"),
                        modified_integrity_impact=Decimal("0"),
                        modified_privileges_required=Decimal("0.85"),
                        modified_user_interaction=Decimal("0.85"),
                        modified_severity_scope=Decimal("0"),
                        privileges_required=Decimal("0.85"),
                        remediation_level=Decimal("0.97"),
                        report_confidence=Decimal("0.96"),
                        severity_scope=Decimal("1"),
                        user_interaction=Decimal("0.62"),
                    ),
                    sorts=FindingSorts.NO,
                    submission=FindingState(
                        modified_by="integratesmanager@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2019-04-08T05:00:00+00:00"
                        ),
                        source=Source.ASM,
                        status=FindingStateStatus.SUBMITTED,
                        rejection=None,
                        justification=StateRemovalJustification.NO_JUSTIFICATION,  # noqa: E501 pylint: disable=line-too-long
                    ),
                    threat="Risk.",
                    unreliable_indicators=FindingUnreliableIndicators(
                        unreliable_closed_vulnerabilities=4,
                        unreliable_newest_vulnerability_report_date=datetime.fromisoformat(  # noqa: E501 pylint: disable=line-too-long
                            "2019-09-16T21:01:24+00:00"
                        ),
                        unreliable_oldest_open_vulnerability_report_date=datetime.fromisoformat(  # noqa: E501 pylint: disable=line-too-long
                            "2019-08-30T14:30:13+00:00"
                        ),
                        unreliable_oldest_vulnerability_report_date=datetime.fromisoformat(  # noqa: E501 pylint: disable=line-too-long
                            "2019-08-30T14:30:13+00:00"
                        ),
                        unreliable_open_vulnerabilities=24,
                        unreliable_status=FindingStatus.VULNERABLE,
                        unreliable_treatment_summary=FindingTreatmentSummary(
                            accepted=0,
                            accepted_undefined=0,
                            in_progress=0,
                            untreated=24,
                        ),
                        unreliable_verification_summary=FindingVerificationSummary(  # noqa: E501 pylint: disable=line-too-long
                            requested=1,
                            on_hold=2,
                            verified=1,
                        ),
                        unreliable_where="192.168.1.10, 192.168.1.12, "
                        "192.168.1.13, 192.168.1.14, 192.168.1.15, "
                        "192.168.1.16, 192.168.1.17, 192.168.1.2, 192.168.1.3,"
                        " 192.168.1.4, 192.168.1.5, 192.168.1.6, 192.168.1.7, "
                        "192.168.1.8, 192.168.1.9, 192.168.100.101, "
                        "192.168.100.104, 192.168.100.105, 192.168.100.108, "
                        "192.168.100.111",
                    ),
                    verification=FindingVerification(
                        comment_id="1558048727111",
                        modified_by="integrateshacker@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2020-02-21T15:41:04+00:00"
                        ),
                        status=FindingVerificationStatus.VERIFIED,
                        vulnerability_ids={
                            "15375781-31f2-4953-ac77-f31134225747"
                        },
                    ),
                ),
                Finding(
                    hacker_email="unittest@fluidattacks.com",
                    group_name="unittesting",
                    id="457497316",
                    state=FindingState(
                        modified_by="integratesmanager@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2018-11-27T05:00:00+00:00"
                        ),
                        source=Source.ASM,
                        status=FindingStateStatus.APPROVED,
                        rejection=None,
                        justification=StateRemovalJustification.NO_JUSTIFICATION,  # noqa: E501 pylint: disable=line-too-long
                    ),
                    title="037. Technical information leak",
                    approval=FindingState(
                        modified_by="integratesmanager@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2018-11-27T05:00:00+00:00"
                        ),
                        source=Source.ASM,
                        status=FindingStateStatus.APPROVED,
                        rejection=None,
                        justification=StateRemovalJustification.NO_JUSTIFICATION,  # noqa: E501 pylint: disable=line-too-long
                    ),
                    attack_vector_description="Test description",
                    creation=FindingState(
                        modified_by="integratesmanager@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2018-04-08T00:43:18+00:00"
                        ),
                        source=Source.ASM,
                        status=FindingStateStatus.CREATED,
                        rejection=None,
                        justification=StateRemovalJustification.NO_JUSTIFICATION,  # noqa: E501 pylint: disable=line-too-long
                    ),
                    description="Descripción de fuga de información técnica",
                    evidences=FindingEvidences(
                        animation=None,
                        evidence1=None,
                        evidence2=FindingEvidence(
                            description="Test description",
                            modified_date=datetime.fromisoformat(
                                "2018-11-27T05:00:00+00:00"
                            ),
                            url="unittesting-457497316-evidence_route_2.jpg",
                        ),
                        evidence3=FindingEvidence(
                            description="Comentario",
                            modified_date=datetime.fromisoformat(
                                "2018-11-27T05:00:00+00:00"
                            ),
                            url="unittesting-457497316-evidence_route_3.png",
                        ),
                        evidence4=None,
                        evidence5=None,
                        exploitation=None,
                        records=None,
                    ),
                    min_time_to_remediate=18,
                    recommendation="Eliminar el banner de los servicios con "
                    "fuga de información, Verificar que los encabezados HTTP "
                    "no expongan ningún nombre o versión.",
                    requirements="REQ.0077. La aplicación no debe revelar "
                    "detalles del sistema interno como stack traces, "
                    "fragmentos de sentencias SQL y nombres de base de datos "
                    "o tablas. REQ.0176. El sistema debe restringir el acceso "
                    "a objetos del sistema que tengan contenido sensible. "
                    "Sólo permitirá su acceso a usuarios autorizados.",
                    severity=Finding31Severity(
                        attack_complexity=Decimal("0.44"),
                        attack_vector=Decimal("0.62"),
                        availability_impact=Decimal("0.22"),
                        availability_requirement=Decimal("1"),
                        confidentiality_impact=Decimal("0.22"),
                        confidentiality_requirement=Decimal("1"),
                        exploitability=Decimal("0.94"),
                        integrity_impact=Decimal("0.22"),
                        integrity_requirement=Decimal("1"),
                        modified_attack_complexity=Decimal("0.44"),
                        modified_attack_vector=Decimal("0.62"),
                        modified_availability_impact=Decimal("0.22"),
                        modified_confidentiality_impact=Decimal("0.22"),
                        modified_integrity_impact=Decimal("0.22"),
                        modified_privileges_required=Decimal("0.62"),
                        modified_user_interaction=Decimal("0.85"),
                        modified_severity_scope=Decimal("0"),
                        privileges_required=Decimal("0.62"),
                        remediation_level=Decimal("0.96"),
                        report_confidence=Decimal("0.92"),
                        severity_scope=Decimal("0"),
                        user_interaction=Decimal("0.85"),
                    ),
                    sorts=FindingSorts.NO,
                    submission=FindingState(
                        modified_by="integratesmanager@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2018-04-08T00:45:11+00:00"
                        ),
                        source=Source.ASM,
                        status=FindingStateStatus.SUBMITTED,
                        rejection=None,
                        justification=StateRemovalJustification.NO_JUSTIFICATION,  # noqa: E501 pylint: disable=line-too-long
                    ),
                    threat="Amenaza.",
                    unreliable_indicators=FindingUnreliableIndicators(
                        unreliable_closed_vulnerabilities=1,
                        unreliable_newest_vulnerability_report_date=datetime.fromisoformat(  # noqa: E501 pylint: disable=line-too-long
                            "2018-11-27T19:54:08+00:00"
                        ),
                        unreliable_oldest_open_vulnerability_report_date=datetime.fromisoformat(  # noqa: E501 pylint: disable=line-too-long
                            "2018-11-27T19:54:08+00:00"
                        ),
                        unreliable_oldest_vulnerability_report_date=datetime.fromisoformat(  # noqa: E501 pylint: disable=line-too-long
                            "2018-11-27T19:54:08+00:00"
                        ),
                        unreliable_open_vulnerabilities=0,
                        unreliable_status=FindingStatus.SAFE,
                        unreliable_treatment_summary=FindingTreatmentSummary(
                            accepted=0,
                            accepted_undefined=0,
                            in_progress=0,
                            untreated=0,
                        ),
                        unreliable_verification_summary=FindingVerificationSummary(  # noqa: E501 pylint: disable=line-too-long
                            requested=0, on_hold=0, verified=0
                        ),
                        unreliable_where="",
                    ),
                    verification=None,
                ),
                Finding(
                    hacker_email="unittest@fluidattacks.com",
                    group_name="unittesting",
                    id="463461507",
                    state=FindingState(
                        modified_by="integratesmanager@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2019-01-10T05:00:00+00:00"
                        ),
                        source=Source.ASM,
                        status=FindingStateStatus.APPROVED,
                        rejection=None,
                        justification=StateRemovalJustification.NO_JUSTIFICATION,  # noqa: E501 pylint: disable=line-too-long
                    ),
                    title="083. XML injection (XXE)",
                    approval=FindingState(
                        modified_by="integratesmanager@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2019-01-10T05:00:00+00:00"
                        ),
                        source=Source.ASM,
                        status=FindingStateStatus.APPROVED,
                        rejection=None,
                        justification=StateRemovalJustification.NO_JUSTIFICATION,  # noqa: E501 pylint: disable=line-too-long
                    ),
                    attack_vector_description="Test attack vector.",
                    creation=FindingState(
                        modified_by="integratesmanager@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2018-04-08T00:43:18+00:00"
                        ),
                        source=Source.ASM,
                        status=FindingStateStatus.CREATED,
                        rejection=None,
                        justification=StateRemovalJustification.NO_JUSTIFICATION,  # noqa: E501 pylint: disable=line-too-long
                    ),
                    description="La aplicacion afectada permite la inyecion "
                    "de codigo XML que es ejecutado de forma remota y permite "
                    "la exfiltracion de archivos o ejecucioemota de comandos "
                    "en el servidor.",
                    evidences=FindingEvidences(
                        animation=FindingEvidence(
                            description="Animation test",
                            modified_date=datetime.fromisoformat(
                                "2019-01-10T05:00:00+00:00"
                            ),
                            url="unittesting-463461507-animation.webm",
                        ),
                        evidence1=None,
                        evidence2=FindingEvidence(
                            description="A2 test",
                            modified_date=datetime.fromisoformat(
                                "2019-01-10T05:00:00+00:00"
                            ),
                            url="unittesting-463461507-evidence_route_2.jpg",
                        ),
                        evidence3=FindingEvidence(
                            description="123A",
                            modified_date=datetime.fromisoformat(
                                "2019-01-10T05:00:00+00:00"
                            ),
                            url="unittesting-463461507-evidence_route_3.png",
                        ),
                        evidence4=FindingEvidence(
                            description="AAA1",
                            modified_date=datetime.fromisoformat(
                                "2019-01-10T05:00:00+00:00"
                            ),
                            url="unittesting-463461507-evidence_route_4.png",
                        ),
                        evidence5=FindingEvidence(
                            description="sdasdasda",
                            modified_date=datetime.fromisoformat(
                                "2019-01-10T05:00:00+00:00"
                            ),
                            url="unittesting-463461507-evidence_route_5.png",
                        ),
                        exploitation=None,
                        records=None,
                    ),
                    min_time_to_remediate=18,
                    recommendation="Filtrar la informacioue recibe y envia la "
                    "aplicacioor medio de listas blancas",
                    requirements="REQ.0173. El sistema debe descartar toda la "
                    "informacion potencialmente insegura que sea recibida "
                    "por entradas de datos.",
                    severity=Finding31Severity(
                        attack_complexity=Decimal("0.44"),
                        attack_vector=Decimal("0.62"),
                        availability_impact=Decimal("0.22"),
                        availability_requirement=Decimal("1"),
                        confidentiality_impact=Decimal("0.22"),
                        confidentiality_requirement=Decimal("1.5"),
                        exploitability=Decimal("0.94"),
                        integrity_impact=Decimal("0"),
                        integrity_requirement=Decimal("1"),
                        modified_attack_complexity=Decimal("0.44"),
                        modified_attack_vector=Decimal("0.62"),
                        modified_availability_impact=Decimal("0.22"),
                        modified_confidentiality_impact=Decimal("0.22"),
                        modified_integrity_impact=Decimal("0"),
                        modified_privileges_required=Decimal("0.85"),
                        modified_user_interaction=Decimal("0.62"),
                        modified_severity_scope=Decimal("0"),
                        privileges_required=Decimal("0.85"),
                        remediation_level=Decimal("0.95"),
                        report_confidence=Decimal("0.96"),
                        severity_scope=Decimal("0"),
                        user_interaction=Decimal("0.62"),
                    ),
                    sorts=FindingSorts.NO,
                    submission=FindingState(
                        modified_by="integratesmanager@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2018-04-08T00:45:11+00:00"
                        ),
                        source=Source.ASM,
                        status=FindingStateStatus.SUBMITTED,
                        rejection=None,
                        justification=StateRemovalJustification.NO_JUSTIFICATION,  # noqa: E501 pylint: disable=line-too-long
                    ),
                    threat="Test threat",
                    unreliable_indicators=FindingUnreliableIndicators(
                        unreliable_closed_vulnerabilities=0,
                        unreliable_newest_vulnerability_report_date=datetime.fromisoformat(  # noqa: E501 pylint: disable=line-too-long
                            "2019-09-13T14:58:38+00:00"
                        ),
                        unreliable_oldest_open_vulnerability_report_date=datetime.fromisoformat(  # noqa: E501 pylint: disable=line-too-long
                            "2019-09-12T13:45:48+00:00"
                        ),
                        unreliable_oldest_vulnerability_report_date=datetime.fromisoformat(  # noqa: E501 pylint: disable=line-too-long
                            "2019-09-12T13:45:48+00:00"
                        ),
                        unreliable_open_vulnerabilities=2,
                        unreliable_status=FindingStatus.VULNERABLE,
                        unreliable_treatment_summary=FindingTreatmentSummary(
                            accepted=1,
                            accepted_undefined=0,
                            in_progress=0,
                            untreated=1,
                        ),
                        unreliable_verification_summary=FindingVerificationSummary(  # noqa: E501 pylint: disable=line-too-long
                            requested=0, on_hold=0, verified=0
                        ),
                        unreliable_where="192.168.1.18, 192.168.100.105",
                    ),
                    verification=None,
                ),
                Finding(
                    hacker_email="unittest@fluidattacks.com",
                    group_name="unittesting",
                    id="463558592",
                    state=FindingState(
                        modified_by="integratesmanager@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2018-12-17T05:00:00+00:00"
                        ),
                        source=Source.ASM,
                        status=FindingStateStatus.APPROVED,
                        rejection=None,
                        justification=StateRemovalJustification.NO_JUSTIFICATION,  # noqa: E501 pylint: disable=line-too-long
                    ),
                    title="007. Cross-site request forgery",
                    approval=FindingState(
                        modified_by="integratesmanager@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2018-12-17T05:00:00+00:00"
                        ),
                        source=Source.ASM,
                        status=FindingStateStatus.APPROVED,
                        rejection=None,
                        justification=StateRemovalJustification.NO_JUSTIFICATION,  # noqa: E501 pylint: disable=line-too-long
                    ),
                    attack_vector_description="Test description",
                    creation=FindingState(
                        modified_by="integratesmanager@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2018-04-08T00:43:18+00:00"
                        ),
                        source=Source.ASM,
                        status=FindingStateStatus.CREATED,
                        rejection=None,
                        justification=StateRemovalJustification.NO_JUSTIFICATION,  # noqa: E501 pylint: disable=line-too-long
                    ),
                    description="La aplicación permite engañar a un usuario "
                    "autenticado por medio de links manipulados para ejecutar "
                    "acciones sobre la aplicación sin su consentimiento.",
                    evidences=FindingEvidences(
                        animation=None,
                        evidence1=FindingEvidence(
                            description="This is test description",
                            modified_date=datetime.fromisoformat(
                                "2018-12-17T05:00:00+00:00"
                            ),
                            url="unittesting-463558592-evidence_route_1.png",
                        ),
                        evidence2=FindingEvidence(
                            description="Test descrip",
                            modified_date=datetime.fromisoformat(
                                "2018-12-17T05:00:00+00:00"
                            ),
                            url="unittesting-463558592-evidence_route_2.jpg",
                        ),
                        evidence3=FindingEvidence(
                            description="Test description number 3",
                            modified_date=datetime.fromisoformat(
                                "2018-12-17T05:00:00+00:00"
                            ),
                            url="unittesting-463558592-evidence_route_3.png",
                        ),
                        evidence4=FindingEvidence(
                            description="An error",
                            modified_date=datetime.fromisoformat(
                                "2018-12-17T05:00:00+00:00"
                            ),
                            url="unittesting-463558592-evidence_route_4.png",
                        ),
                        evidence5=FindingEvidence(
                            description="Test descip 4",
                            modified_date=datetime.fromisoformat(
                                "2018-12-17T05:00:00+00:00"
                            ),
                            url="unittesting-463558592-evidence_route_5.png",
                        ),
                        exploitation=None,
                        records=None,
                    ),
                    min_time_to_remediate=18,
                    recommendation="Hacer uso de tokens en los formularios "
                    "para la verificación de las peticiones realizadas por "
                    "usuarios legítimos.",
                    requirements="REQ.0174. La aplicación debe garantizar que "
                    "las peticiones que ejecuten transacciones no sigan un "
                    "patrón discernible.",
                    severity=Finding31Severity(
                        attack_complexity=Decimal("0.44"),
                        attack_vector=Decimal("0.62"),
                        availability_impact=Decimal("0"),
                        availability_requirement=Decimal("1"),
                        confidentiality_impact=Decimal("0.56"),
                        confidentiality_requirement=Decimal("1"),
                        exploitability=Decimal("0.91"),
                        integrity_impact=Decimal("0.22"),
                        integrity_requirement=Decimal("1.5"),
                        modified_attack_complexity=Decimal("0.44"),
                        modified_attack_vector=Decimal("0.62"),
                        modified_availability_impact=Decimal("0"),
                        modified_confidentiality_impact=Decimal("0.56"),
                        modified_integrity_impact=Decimal("0.22"),
                        modified_privileges_required=Decimal("0.62"),
                        modified_user_interaction=Decimal("0.62"),
                        modified_severity_scope=Decimal("0"),
                        privileges_required=Decimal("0.62"),
                        remediation_level=Decimal("0.95"),
                        report_confidence=Decimal("0.96"),
                        severity_scope=Decimal("0"),
                        user_interaction=Decimal("0.62"),
                    ),
                    sorts=FindingSorts.NO,
                    submission=FindingState(
                        modified_by="integratesmanager@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2018-04-08T00:45:11+00:00"
                        ),
                        source=Source.ASM,
                        status=FindingStateStatus.SUBMITTED,
                        rejection=None,
                        justification=StateRemovalJustification.NO_JUSTIFICATION,  # noqa: E501 pylint: disable=line-too-long
                    ),
                    threat="Test.",
                    unreliable_indicators=FindingUnreliableIndicators(
                        unreliable_closed_vulnerabilities=1,
                        unreliable_newest_vulnerability_report_date=datetime.fromisoformat(  # noqa: E501 pylint: disable=line-too-long
                            "2019-01-15T16:04:14+00:00"
                        ),
                        unreliable_oldest_open_vulnerability_report_date=datetime.fromisoformat(  # noqa: E501 pylint: disable=line-too-long
                            "2019-01-15T16:04:14+00:00"
                        ),
                        unreliable_oldest_vulnerability_report_date=datetime.fromisoformat(  # noqa: E501 pylint: disable=line-too-long
                            "2019-01-15T16:04:14+00:00"
                        ),
                        unreliable_open_vulnerabilities=1,
                        unreliable_status=FindingStatus.VULNERABLE,
                        unreliable_treatment_summary=FindingTreatmentSummary(
                            accepted=1,
                            accepted_undefined=0,
                            in_progress=0,
                            untreated=0,
                        ),
                        unreliable_verification_summary=FindingVerificationSummary(  # noqa: E501 pylint: disable=line-too-long
                            requested=0, on_hold=0, verified=0
                        ),
                        unreliable_where="path/to/file2.ext",
                    ),
                    verification=FindingVerification(
                        comment_id="1558048727999",
                        modified_by="integratesuser@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2020-01-19T15:41:04+00:00"
                        ),
                        status=FindingVerificationStatus.REQUESTED,
                        vulnerability_ids={
                            "74632c0c-db08-47c2-b013-c70e5b67c49f",
                            "3bcdb384-5547-4170-a0b6-3b397a245465",
                        },
                    ),
                ),
                Finding(
                    hacker_email="integratesmanager@gmail.com",
                    group_name="unittesting",
                    id="988493279",
                    state=FindingState(
                        modified_by="integratesmanager@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2019-04-08T00:45:15+00:00"
                        ),
                        source=Source.ASM,
                        status=FindingStateStatus.APPROVED,
                        rejection=None,
                        justification=StateRemovalJustification.NO_JUSTIFICATION,  # noqa: E501 pylint: disable=line-too-long
                    ),
                    title="014. Insecure functionality",
                    approval=FindingState(
                        modified_by="integratesmanager@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2019-04-08T00:45:15+00:00"
                        ),
                        source=Source.ASM,
                        status=FindingStateStatus.APPROVED,
                        rejection=None,
                        justification=StateRemovalJustification.NO_JUSTIFICATION,  # noqa: E501 pylint: disable=line-too-long
                    ),
                    attack_vector_description="Test description",
                    creation=FindingState(
                        modified_by="integratesmanager@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2019-04-08T00:43:18+00:00"
                        ),
                        source=Source.ASM,
                        status=FindingStateStatus.CREATED,
                        rejection=None,
                        justification=StateRemovalJustification.NO_JUSTIFICATION,  # noqa: E501 pylint: disable=line-too-long
                    ),
                    description="Insecure funtionality",
                    evidences=FindingEvidences(
                        animation=None,
                        evidence1=None,
                        evidence2=None,
                        evidence3=None,
                        evidence4=None,
                        evidence5=None,
                        exploitation=FindingEvidence(
                            description="Exploitation description",
                            modified_date=datetime.fromisoformat(
                                "2019-04-08T00:45:15+00:00"
                            ),
                            url="unittesting-988493279-exploitation.png",
                        ),
                        records=None,
                    ),
                    min_time_to_remediate=20,
                    recommendation="Test recomendation",
                    requirements="REQ.0266. La organización debe deshabilitar "
                    "las funciones inseguras de un sistema. "
                    "(hardening de sistemas)",
                    severity=Finding31Severity(
                        attack_complexity=Decimal("0.77"),
                        attack_vector=Decimal("0.85"),
                        availability_impact=Decimal("0.22"),
                        availability_requirement=Decimal("0.5"),
                        confidentiality_impact=Decimal("0.22"),
                        confidentiality_requirement=Decimal("1.5"),
                        exploitability=Decimal("0.94"),
                        integrity_impact=Decimal("0.22"),
                        integrity_requirement=Decimal("1"),
                        modified_attack_complexity=Decimal("0.77"),
                        modified_attack_vector=Decimal("0.55"),
                        modified_availability_impact=Decimal("0"),
                        modified_confidentiality_impact=Decimal("0"),
                        modified_integrity_impact=Decimal("0"),
                        modified_privileges_required=Decimal("0.62"),
                        modified_user_interaction=Decimal("0.85"),
                        modified_severity_scope=Decimal("0"),
                        privileges_required=Decimal("0.85"),
                        remediation_level=Decimal("0.95"),
                        report_confidence=Decimal("0.96"),
                        severity_scope=Decimal("0"),
                        user_interaction=Decimal("0.85"),
                    ),
                    sorts=FindingSorts.NO,
                    submission=FindingState(
                        modified_by="integratesmanager@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2019-04-08T00:45:11+00:00"
                        ),
                        source=Source.ASM,
                        status=FindingStateStatus.SUBMITTED,
                        rejection=None,
                        justification=StateRemovalJustification.NO_JUSTIFICATION,  # noqa: E501 pylint: disable=line-too-long
                    ),
                    threat="Test threat",
                    unreliable_indicators=FindingUnreliableIndicators(
                        unreliable_closed_vulnerabilities=1,
                        unreliable_newest_vulnerability_report_date=datetime.fromisoformat(  # noqa: E501 pylint: disable=line-too-long
                            "2019-04-08T00:45:15+00:00"
                        ),
                        unreliable_oldest_open_vulnerability_report_date=datetime.fromisoformat(  # noqa: E501 pylint: disable=line-too-long
                            "2019-04-08T00:45:15+00:00"
                        ),
                        unreliable_oldest_vulnerability_report_date=datetime.fromisoformat(  # noqa: E501 pylint: disable=line-too-long
                            "2019-04-08T00:45:15+00:00"
                        ),
                        unreliable_open_vulnerabilities=1,
                        unreliable_status=FindingStatus.VULNERABLE,
                        unreliable_treatment_summary=FindingTreatmentSummary(
                            accepted=0,
                            accepted_undefined=1,
                            in_progress=0,
                            untreated=0,
                        ),
                        unreliable_verification_summary=FindingVerificationSummary(  # noqa: E501 pylint: disable=line-too-long
                            requested=0, on_hold=0, verified=0
                        ),
                        unreliable_where="192.168.1.19",
                    ),
                    verification=None,
                ),
            ]
        )
    },
    "db_model.findings.get.MeDraftsLoader.load": {
        '["unittest@fluidattacks.com"]': tuple(
            [
                Finding(
                    hacker_email="unittest@fluidattacks.com",
                    group_name="oneshottest",
                    id="475041513",
                    state=FindingState(
                        modified_by="integratesmanager@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2018-04-08T00:45:11+00:00"
                        ),
                        source=Source.ASM,
                        status=FindingStateStatus.SUBMITTED,
                        rejection=None,
                        justification=StateRemovalJustification.NO_JUSTIFICATION,  # noqa: E501 pylint: disable=line-too-long
                    ),
                    title="081. Lack of multi-factor authentication",
                    approval=None,
                    attack_vector_description="Los servicios críticos sobre la"
                    " red interna como acceso a bases de datos, recursos "
                    "compartidos con información sensible y/o web services, "
                    "no cuentan con un doble factor de autenticación lo cual "
                    "hace más fácil para un atacante con un usuario "
                    "comprometido acceder a estos",
                    creation=FindingState(
                        modified_by="integratesmanager@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2018-04-08T00:43:18+00:00"
                        ),
                        source=Source.ASM,
                        status=FindingStateStatus.CREATED,
                        rejection=None,
                        justification=StateRemovalJustification.NO_JUSTIFICATION,  # noqa: E501 pylint: disable=line-too-long
                    ),
                    description="Los servicios críticos sobre la red interna "
                    "como acceso a bases de datos, recursos compartidos con "
                    "información sensible y/o web services, no cuentan con un "
                    "doble factor de autenticación lo cual hace más fácil "
                    "para un atacante con un usuario comprometido acceder "
                    "a estos.",
                    evidences=FindingEvidences(
                        animation=None,
                        evidence1=FindingEvidence(
                            description="Evidencia",
                            modified_date=datetime.fromisoformat(
                                "2018-04-08T00:43:18+00:00"
                            ),
                            url="continuoustesting-475041513-evidence_route_1",
                        ),
                        evidence2=FindingEvidence(
                            description="AAAAAAAAAAAA",
                            modified_date=datetime.fromisoformat(
                                "2018-04-08T00:43:18+00:00"
                            ),
                            url="continuoustesting-475041513-evidence_route_2",
                        ),
                        evidence3=None,
                        evidence4=None,
                        evidence5=None,
                        exploitation=None,
                        records=None,
                    ),
                    min_time_to_remediate=18,
                    recommendation="Implementar un doble factor de "
                    "autenticación ya sea por software o hardware para "
                    "incrementar el nivel de protección de la autenticación "
                    "de los recursos críticos.",
                    requirements="REQ.0229. El sistema debe solicitar a "
                    "cualquier actor que intenta autenticarse, como mínimo un "
                    "nombre de usuario y una contraseña.",
                    severity=Finding31Severity(
                        attack_complexity=Decimal("0.44"),
                        attack_vector=Decimal("0.2"),
                        availability_impact=Decimal("0.22"),
                        availability_requirement=Decimal("0.5"),
                        confidentiality_impact=Decimal("0.22"),
                        confidentiality_requirement=Decimal("0.5"),
                        exploitability=Decimal("0.94"),
                        integrity_impact=Decimal("0.22"),
                        integrity_requirement=Decimal("1"),
                        modified_attack_complexity=Decimal("0.44"),
                        modified_attack_vector=Decimal("0.85"),
                        modified_availability_impact=Decimal("0.22"),
                        modified_confidentiality_impact=Decimal("0.22"),
                        modified_integrity_impact=Decimal("0"),
                        modified_privileges_required=Decimal("0.27"),
                        modified_user_interaction=Decimal("0.62"),
                        modified_severity_scope=Decimal("0"),
                        privileges_required=Decimal("0.62"),
                        remediation_level=Decimal("0.95"),
                        report_confidence=Decimal("1"),
                        severity_scope=Decimal("0"),
                        user_interaction=Decimal("0.85"),
                    ),
                    sorts=FindingSorts.NO,
                    submission=FindingState(
                        modified_by="integratesmanager@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2018-04-08T00:45:11+00:00"
                        ),
                        source=Source.ASM,
                        status=FindingStateStatus.SUBMITTED,
                        rejection=None,
                        justification=StateRemovalJustification.NO_JUSTIFICATION,  # noqa: E501 pylint: disable=line-too-long
                    ),
                    threat="Los servicios críticos sobre la red interna como "
                    "acceso a bases de datos, recursos compartidos con "
                    "información sensible y/o web services, no cuentan con un "
                    "doble factor de autenticación lo cual hace más fácil "
                    "para un atacante con un usuario comprometido acceder a "
                    "estos.",
                    unreliable_indicators=FindingUnreliableIndicators(
                        unreliable_closed_vulnerabilities=1,
                        unreliable_newest_vulnerability_report_date=datetime.fromisoformat(  # noqa: E501 pylint: disable=line-too-long
                            "2019-04-12T13:45:48+00:00"
                        ),
                        unreliable_oldest_open_vulnerability_report_date=datetime.fromisoformat(  # noqa: E501 pylint: disable=line-too-long
                            "2019-04-12T13:45:48+00:00"
                        ),
                        unreliable_oldest_vulnerability_report_date=datetime.fromisoformat(  # noqa: E501 pylint: disable=line-too-long
                            "2019-04-12T13:45:48+00:00"
                        ),
                        unreliable_open_vulnerabilities=1,
                        unreliable_status=FindingStatus.VULNERABLE,
                        unreliable_treatment_summary=FindingTreatmentSummary(
                            accepted=0,
                            accepted_undefined=0,
                            in_progress=0,
                            untreated=1,
                        ),
                        unreliable_verification_summary=FindingVerificationSummary(  # noqa: E501 pylint: disable=line-too-long
                            requested=0, on_hold=0, verified=0
                        ),
                        unreliable_where="path/to/file4.ext",
                    ),
                    verification=None,
                ),
                Finding(
                    hacker_email="unittest@fluidattacks.com",
                    group_name="continuoustesting",
                    id="475041524",
                    state=FindingState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2019-02-04T17:46:10+00:00"
                        ),
                        source=Source.ASM,
                        status=FindingStateStatus.CREATED,
                        rejection=None,
                        justification=StateRemovalJustification.NO_JUSTIFICATION,  # noqa: E501 pylint: disable=line-too-long
                    ),
                    title="081. Lack of multi-factor authentication",
                    approval=None,
                    attack_vector_description="Los servicios críticos sobre "
                    "la red interna como acceso a bases de datos, recursos "
                    "compartidos con información sensible y/o web services, "
                    "no cuentan con un doble factor de autenticación lo cual "
                    "hace más fácil para un atacante con un usuario "
                    "comprometido acceder a estos",
                    creation=FindingState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2019-02-04T17:46:10+00:00"
                        ),
                        source=Source.ASM,
                        status=FindingStateStatus.CREATED,
                        rejection=None,
                        justification=StateRemovalJustification.NO_JUSTIFICATION,  # noqa: E501 pylint: disable=line-too-long
                    ),
                    description="Los servicios críticos sobre la red interna "
                    "como acceso a bases de datos, recursos compartidos con "
                    "información sensible y/o web services, no cuentan con un "
                    "doble factor de autenticación lo cual hace más fácil "
                    "para un atacante con un usuario comprometido acceder a "
                    "estos.",
                    evidences=FindingEvidences(
                        animation=None,
                        evidence1=FindingEvidence(
                            description="Evidencia",
                            modified_date=datetime.fromisoformat(
                                "2019-02-04T17:46:10+00:00"
                            ),
                            url="continuoustesting-475041524-evidence_route_1.png",  # noqa: E501 pylint: disable=line-too-long
                        ),
                        evidence2=FindingEvidence(
                            description="AAAAAAAAAAAA",
                            modified_date=datetime.fromisoformat(
                                "2019-02-04T17:46:10+00:00"
                            ),
                            url="continuoustesting-475041524-evidence_route_2.png",  # noqa: E501 pylint: disable=line-too-long
                        ),
                        evidence3=None,
                        evidence4=None,
                        evidence5=None,
                        exploitation=None,
                        records=None,
                    ),
                    min_time_to_remediate=25,
                    recommendation="Implementar un doble factor de "
                    "autenticación ya sea por software o hardware para "
                    "incrementar el nivel de protección de la autenticación "
                    "de los recursos críticos.",
                    requirements="REQ.0229. El sistema debe solicitar a "
                    "cualquier actor que intenta autenticarse, como mínimo un "
                    "nombre de usuario y una contraseña.",
                    severity=Finding31Severity(
                        attack_complexity=Decimal("0.44"),
                        attack_vector=Decimal("0.2"),
                        availability_impact=Decimal("0.22"),
                        availability_requirement=Decimal("0.5"),
                        confidentiality_impact=Decimal("0.22"),
                        confidentiality_requirement=Decimal("0.5"),
                        exploitability=Decimal("0.94"),
                        integrity_impact=Decimal("0.22"),
                        integrity_requirement=Decimal("1"),
                        modified_attack_complexity=Decimal("0.44"),
                        modified_attack_vector=Decimal("0.85"),
                        modified_availability_impact=Decimal("0.22"),
                        modified_confidentiality_impact=Decimal("0.22"),
                        modified_integrity_impact=Decimal("0"),
                        modified_privileges_required=Decimal("0.27"),
                        modified_user_interaction=Decimal("0.62"),
                        modified_severity_scope=Decimal("0"),
                        privileges_required=Decimal("0.62"),
                        remediation_level=Decimal("0.95"),
                        report_confidence=Decimal("1"),
                        severity_scope=Decimal("0"),
                        user_interaction=Decimal("0.85"),
                    ),
                    sorts=FindingSorts.NO,
                    submission=None,
                    threat="Los servicios críticos sobre la red interna como "
                    "acceso a bases de datos, recursos compartidos con "
                    "información sensible y/o web services, no cuentan con un "
                    "doble factor de autenticación lo cual hace más fácil "
                    "para un atacante con un usuario comprometido acceder a "
                    "estos.",
                    unreliable_indicators=FindingUnreliableIndicators(
                        unreliable_closed_vulnerabilities=0,
                        unreliable_newest_vulnerability_report_date=datetime.fromisoformat(  # noqa: E501 pylint: disable=line-too-long
                            "2019-09-13T14:58:38+00:00"
                        ),
                        unreliable_oldest_open_vulnerability_report_date=datetime.fromisoformat(  # noqa: E501 pylint: disable=line-too-long
                            "2020-09-12T13:45:48+00:00"
                        ),
                        unreliable_oldest_vulnerability_report_date=datetime.fromisoformat(  # noqa: E501 pylint: disable=line-too-long
                            "2020-09-12T13:45:48+00:00"
                        ),
                        unreliable_open_vulnerabilities=0,
                        unreliable_status=FindingStatus.SAFE,
                        unreliable_treatment_summary=FindingTreatmentSummary(
                            accepted=0,
                            accepted_undefined=0,
                            in_progress=0,
                            untreated=0,
                        ),
                        unreliable_verification_summary=FindingVerificationSummary(  # noqa: E501 pylint: disable=line-too-long
                            requested=0, on_hold=0, verified=0
                        ),
                        unreliable_where="",
                    ),
                    verification=None,
                ),
                Finding(
                    hacker_email="unittest@fluidattacks.com",
                    group_name="oneshottest",
                    id="475041535",
                    state=FindingState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2019-02-04T17:46:10+00:00"
                        ),
                        source=Source.ASM,
                        status=FindingStateStatus.CREATED,
                        rejection=None,
                        justification=StateRemovalJustification.NO_JUSTIFICATION,  # noqa: E501 pylint: disable=line-too-long
                    ),
                    title="081. Lack of multi-factor authentication",
                    approval=None,
                    attack_vector_description="Los servicios críticos sobre "
                    "la red interna como acceso a bases de datos, recursos "
                    "compartidos con información sensible y/o web services, "
                    "no cuentan con un doble factor de autenticación lo cual "
                    "hace más fácil para un atacante con un usuario "
                    "comprometido acceder a estos",
                    creation=FindingState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2019-02-04T17:46:10+00:00"
                        ),
                        source=Source.ASM,
                        status=FindingStateStatus.CREATED,
                        rejection=None,
                        justification=StateRemovalJustification.NO_JUSTIFICATION,  # noqa: E501 pylint: disable=line-too-long
                    ),
                    description="Los servicios críticos sobre la red interna "
                    "como acceso a bases de datos, recursos compartidos con "
                    "información sensible y/o web services, no cuentan con un "
                    "doble factor de autenticación lo cual hace más fácil "
                    "para un atacante con un usuario comprometido acceder "
                    "a estos.",
                    evidences=FindingEvidences(
                        animation=None,
                        evidence1=FindingEvidence(
                            description="Evidencia",
                            modified_date=datetime.fromisoformat(
                                "2019-02-04T17:46:10+00:00"
                            ),
                            url="oneshottest-475041535-evidence_route_1",
                        ),
                        evidence2=FindingEvidence(
                            description="AAAAAAAAA",
                            modified_date=datetime.fromisoformat(
                                "2019-02-04T17:46:10+00:00"
                            ),
                            url="oneshottest-475041535-evidence_route_2",
                        ),
                        evidence3=None,
                        evidence4=None,
                        evidence5=None,
                        exploitation=None,
                        records=None,
                    ),
                    min_time_to_remediate=18,
                    recommendation="Implementar un doble factor de "
                    "autenticación ya sea por software o hardware para "
                    "incrementar el nivel de protección de la autenticación "
                    "de los recursos críticos.",
                    requirements="REQ.0229. El sistema debe solicitar a "
                    "cualquier actor que intenta autenticarse, como mínimo un "
                    "nombre de usuario y una contraseña.",
                    severity=Finding31Severity(
                        attack_complexity=Decimal("0.44"),
                        attack_vector=Decimal("0.2"),
                        availability_impact=Decimal("0.22"),
                        availability_requirement=Decimal("0.5"),
                        confidentiality_impact=Decimal("0.22"),
                        confidentiality_requirement=Decimal("0.5"),
                        exploitability=Decimal("0.94"),
                        integrity_impact=Decimal("0.22"),
                        integrity_requirement=Decimal("1"),
                        modified_attack_complexity=Decimal("0.44"),
                        modified_attack_vector=Decimal("0.85"),
                        modified_availability_impact=Decimal("0.22"),
                        modified_confidentiality_impact=Decimal("0.22"),
                        modified_integrity_impact=Decimal("0"),
                        modified_privileges_required=Decimal("0.27"),
                        modified_user_interaction=Decimal("0.62"),
                        modified_severity_scope=Decimal("0"),
                        privileges_required=Decimal("0.62"),
                        remediation_level=Decimal("0.95"),
                        report_confidence=Decimal("1"),
                        severity_scope=Decimal("0"),
                        user_interaction=Decimal("0.85"),
                    ),
                    sorts=FindingSorts.NO,
                    submission=None,
                    threat="Los servicios críticos sobre la red interna como "
                    "acceso a bases de datos, recursos compartidos con "
                    "información sensible y/o web services, no cuentan con un "
                    "doble factor de autenticación lo cual hace más fácil "
                    "para un atacante con un usuario comprometido acceder a "
                    "estos.",
                    unreliable_indicators=FindingUnreliableIndicators(
                        unreliable_closed_vulnerabilities=0,
                        unreliable_newest_vulnerability_report_date=datetime.fromisoformat(  # noqa: E501 pylint: disable=line-too-long
                            "2019-09-13T14:58:38+00:00"
                        ),
                        unreliable_oldest_open_vulnerability_report_date=datetime.fromisoformat(  # noqa: E501 pylint: disable=line-too-long
                            "2020-09-12T13:45:48+00:00"
                        ),
                        unreliable_oldest_vulnerability_report_date=datetime.fromisoformat(  # noqa: E501 pylint: disable=line-too-long
                            "2020-09-12T13:45:48+00:00"
                        ),
                        unreliable_open_vulnerabilities=0,
                        unreliable_status=FindingStatus.SAFE,
                        unreliable_treatment_summary=FindingTreatmentSummary(
                            accepted=0,
                            accepted_undefined=0,
                            in_progress=0,
                            untreated=0,
                        ),
                        unreliable_verification_summary=FindingVerificationSummary(  # noqa: E501 pylint: disable=line-too-long
                            requested=0, on_hold=0, verified=0
                        ),
                        unreliable_where="",
                    ),
                    verification=None,
                ),
                Finding(
                    hacker_email="unittest@fluidattacks.com",
                    group_name="unittesting",
                    id="560175507",
                    state=FindingState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2019-02-07T17:46:10+00:00"
                        ),
                        source=Source.ASM,
                        status=FindingStateStatus.REJECTED,
                        rejection=DraftRejection(
                            other="",
                            reasons={DraftRejectionReason.OMISSION},
                            rejected_by="customer_manager@fluidattacks.com",
                            rejection_date=datetime.fromisoformat(
                                "2019-02-07T17:46:10+00:00"
                            ),
                            submitted_by="unittest@fluidattacks.com",
                        ),
                        justification=StateRemovalJustification.NO_JUSTIFICATION,  # noqa: E501 pylint: disable=line-too-long
                    ),
                    title="006. Authentication mechanism absence or evasion",
                    approval=None,
                    attack_vector_description="Test attack vector.",
                    creation=FindingState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2019-02-07T17:46:10+00:00"
                        ),
                        source=Source.ASM,
                        status=FindingStateStatus.CREATED,
                        rejection=None,
                        justification=StateRemovalJustification.NO_JUSTIFICATION,  # noqa: E501 pylint: disable=line-too-long
                    ),
                    description="La aplicación afectada permite la inyeccion "
                    "de XML que es ejecutado de forma remota y permite la "
                    "exfiltracion de archivos o ejecucion remota de comandos "
                    "en el servidor.",
                    evidences=FindingEvidences(
                        animation=None,
                        evidence1=None,
                        evidence2=None,
                        evidence3=None,
                        evidence4=None,
                        evidence5=None,
                        exploitation=None,
                        records=None,
                    ),
                    min_time_to_remediate=18,
                    recommendation="Filtrar la informacion recibe y envia la "
                    "aplicacion medio de listas blancas",
                    requirements="REQ.0173. El sistema debe descartar toda la "
                    "informacion potencialmente insegura que sea recibida por "
                    "entradas de datos.",
                    severity=Finding31Severity(
                        attack_complexity=Decimal("0.44"),
                        attack_vector=Decimal("0.62"),
                        availability_impact=Decimal("0.22"),
                        availability_requirement=Decimal("1"),
                        confidentiality_impact=Decimal("0.22"),
                        confidentiality_requirement=Decimal("1.5"),
                        exploitability=Decimal("0.94"),
                        integrity_impact=Decimal("0"),
                        integrity_requirement=Decimal("1"),
                        modified_attack_complexity=Decimal("0.44"),
                        modified_attack_vector=Decimal("0.62"),
                        modified_availability_impact=Decimal("0.22"),
                        modified_confidentiality_impact=Decimal("0.22"),
                        modified_integrity_impact=Decimal("0"),
                        modified_privileges_required=Decimal("0.85"),
                        modified_user_interaction=Decimal("0.62"),
                        modified_severity_scope=Decimal("0"),
                        privileges_required=Decimal("0.85"),
                        remediation_level=Decimal("0.95"),
                        report_confidence=Decimal("0.96"),
                        severity_scope=Decimal("0"),
                        user_interaction=Decimal("0.62"),
                    ),
                    sorts=FindingSorts.NO,
                    submission=None,
                    threat="Test threat",
                    unreliable_indicators=FindingUnreliableIndicators(
                        unreliable_closed_vulnerabilities=0,
                        unreliable_newest_vulnerability_report_date=datetime.fromisoformat(  # noqa: E501 pylint: disable=line-too-long
                            "2019-09-13T14:58:38+00:00"
                        ),
                        unreliable_oldest_open_vulnerability_report_date=datetime.fromisoformat(  # noqa: E501 pylint: disable=line-too-long
                            "2019-09-12T13:45:48+00:00"
                        ),
                        unreliable_oldest_vulnerability_report_date=datetime.fromisoformat(  # noqa: E501 pylint: disable=line-too-long
                            "2019-09-12T13:45:48+00:00"
                        ),
                        unreliable_open_vulnerabilities=0,
                        unreliable_status=FindingStatus.SAFE,
                        unreliable_treatment_summary=FindingTreatmentSummary(
                            accepted=0,
                            accepted_undefined=0,
                            in_progress=0,
                            untreated=0,
                        ),
                        unreliable_verification_summary=FindingVerificationSummary(  # noqa: E501 pylint: disable=line-too-long
                            requested=0, on_hold=0, verified=0
                        ),
                        unreliable_where="",
                    ),
                    verification=None,
                ),
                Finding(
                    hacker_email="unittest@fluidattacks.com",
                    group_name="unittesting",
                    id="563827909",
                    state=FindingState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2022-08-22T17:46:10+00:00"
                        ),
                        source=Source.ASM,
                        status=FindingStateStatus.CREATED,
                        rejection=None,
                        justification=StateRemovalJustification.NO_JUSTIFICATION,  # noqa: E501 pylint: disable=line-too-long
                    ),
                    title="379. Inappropriate coding practices - "
                    "Unnecessary imports",
                    approval=None,
                    attack_vector_description="Test attack vector.",
                    creation=FindingState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2022-08-22T17:46:10+00:00"
                        ),
                        source=Source.ASM,
                        status=FindingStateStatus.CREATED,
                        rejection=None,
                        justification=StateRemovalJustification.NO_JUSTIFICATION,  # noqa: E501 pylint: disable=line-too-long
                    ),
                    description="The application imports modules that are not "
                    "used. This is a bad practice because it loads modules "
                    "that will not be used, and doing so unnecessarily "
                    "increases the load.",
                    evidences=FindingEvidences(
                        animation=None,
                        evidence1=None,
                        evidence2=None,
                        evidence3=None,
                        evidence4=None,
                        evidence5=None,
                        exploitation=None,
                        records=None,
                    ),
                    min_time_to_remediate=15,
                    recommendation="Import only the modules necessary for the "
                    "correct functionality of the application.",
                    requirements="158. System source code must be implemented "
                    "in a stable, updated, tested and free of known "
                    "vulnerabilities version of the chosen programming "
                    "language.",
                    severity=Finding31Severity(
                        attack_complexity=Decimal("0.44"),
                        attack_vector=Decimal("0.85"),
                        availability_impact=Decimal("0.22"),
                        availability_requirement=Decimal("1"),
                        confidentiality_impact=Decimal("0"),
                        confidentiality_requirement=Decimal("1.5"),
                        exploitability=Decimal("0.91"),
                        integrity_impact=Decimal("0"),
                        integrity_requirement=Decimal("1"),
                        modified_attack_complexity=Decimal("0.44"),
                        modified_attack_vector=Decimal("0.62"),
                        modified_availability_impact=Decimal("0.22"),
                        modified_confidentiality_impact=Decimal("0.22"),
                        modified_integrity_impact=Decimal("0"),
                        modified_privileges_required=Decimal("0.85"),
                        modified_user_interaction=Decimal("0.62"),
                        modified_severity_scope=Decimal("0"),
                        privileges_required=Decimal("0.62"),
                        remediation_level=Decimal("0.95"),
                        report_confidence=Decimal("0.96"),
                        severity_scope=Decimal("0"),
                        user_interaction=Decimal("0.85"),
                    ),
                    sorts=FindingSorts.NO,
                    submission=None,
                    threat="Authorized attacker from the Internet with access "
                    "to the application.",
                    unreliable_indicators=FindingUnreliableIndicators(
                        unreliable_closed_vulnerabilities=0,
                        unreliable_newest_vulnerability_report_date=datetime.fromisoformat(  # noqa: E501 pylint: disable=line-too-long
                            "2019-09-13T14:58:38+00:00"
                        ),
                        unreliable_oldest_open_vulnerability_report_date=datetime.fromisoformat(  # noqa: E501 pylint: disable=line-too-long
                            "2020-09-12T13:45:48+00:00"
                        ),
                        unreliable_oldest_vulnerability_report_date=datetime.fromisoformat(  # noqa: E501 pylint: disable=line-too-long
                            "2020-09-12T13:45:48+00:00"
                        ),
                        unreliable_open_vulnerabilities=0,
                        unreliable_status=FindingStatus.SAFE,
                        unreliable_treatment_summary=FindingTreatmentSummary(
                            accepted=0,
                            accepted_undefined=0,
                            in_progress=0,
                            untreated=0,
                        ),
                        unreliable_verification_summary=FindingVerificationSummary(  # noqa: E501 pylint: disable=line-too-long
                            requested=0, on_hold=0, verified=0
                        ),
                        unreliable_where="",
                    ),
                    verification=None,
                ),
            ]
        )
    },
    "db_model.findings.remove": {
        '["unittesting", "457497316"]': None,
    },
    "group_access.domain.update_me_draft_index": {
        '["unittest@fluidattacks.com", "unittesting"]': None,
    },
    "db_model.groups.get.GroupLoader.load": {
        '["unittesting"]': Group(
            created_by="unknown",
            created_date=datetime.fromisoformat("2018-03-08T00:43:18+00:00"),
            description="Integrates unit test group",
            language=GroupLanguage.EN,
            name="unittesting",
            organization_id="ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3",
            state=GroupState(
                has_machine=True,
                has_squad=True,
                managed=GroupManaged.NOT_MANAGED,
                modified_by="unknown",
                modified_date=datetime.fromisoformat(
                    "2018-03-08T00:43:18+00:00"
                ),
                status=GroupStateStatus.ACTIVE,
                tier=GroupTier.MACHINE,
                type=GroupSubscriptionType.CONTINUOUS,
                tags={"test-updates", "test-tag", "test-groups"},
                comments=None,
                justification=None,
                payment_id=None,
                pending_deletion_date=None,
                service=GroupService.WHITE,
            ),
            agent_token=None,
            business_id="14441323",
            business_name="Testing Company and Sons",
            context="Group context test",
            disambiguation="Disambiguation test",
            files=[
                GroupFile(
                    description="Test",
                    file_name="test.zip",
                    modified_by="unittest@fluidattacks.com",
                    modified_date=datetime.fromisoformat(
                        "2019-03-01T20:21:00+00:00"
                    ),
                ),
                GroupFile(
                    description="shell",
                    file_name="shell.exe",
                    modified_by="unittest@fluidattacks.com",
                    modified_date=datetime.fromisoformat(
                        "2019-04-24T19:56:00+00:00"
                    ),
                ),
                GroupFile(
                    description="shell2",
                    file_name="shell2.exe",
                    modified_by="unittest@fluidattacks.com",
                    modified_date=datetime.fromisoformat(
                        "2019-04-24T19:56:00+00:00"
                    ),
                ),
                GroupFile(
                    description="eerweterterter",
                    file_name="asdasd.py",
                    modified_by="unittest@fluidattacks.com",
                    modified_date=datetime.fromisoformat(
                        "2019-08-06T19:28:00+00:00"
                    ),
                ),
            ],
            policies=None,
            sprint_duration=2,
            sprint_start_date=datetime.fromisoformat(
                "2022-08-06T19:28:00+00:00"
            ),
        )
    },
    "db_model.group_access.get.GroupAccessLoader.load": {
        '["integrateshacker@fluidattacks.com", "unittesting",'
        ' "hacker"]': GroupAccess(
            email="integrateshacker@fluidattacks.com",
            group_name="unittesting",
            state=GroupAccessState(modified_date=None),
            confirm_deletion=None,
            expiration_time=None,
            has_access=True,
            invitation=None,
            responsibility=None,
            role="hacker",
        ),
        '["integratesuser@gmail.com", "unittesting",'
        ' "user_manager"]': GroupAccess(
            email="integratesuser@gmail.com",
            group_name="unittesting",
            state=GroupAccessState(modified_date=None),
            confirm_deletion=None,
            expiration_time=None,
            has_access=True,
            invitation=None,
            responsibility=None,
            role="user_manager",
        ),
        '["test@test.com", "unittesting"]': GroupAccess(
            email="test@test.com",
            group_name="unittesting",
            state=GroupAccessState(modified_date=None),
            confirm_deletion=None,
            expiration_time=None,
            has_access=True,
            invitation=None,
            responsibility=None,
            role=None,
        ),
        '["test2@test.com", "oneshottest"]': GroupAccess(
            email="test2@test.com",
            group_name="unittesting",
            state=GroupAccessState(modified_date=None),
            confirm_deletion=None,
            expiration_time=None,
            has_access=True,
            invitation=None,
            responsibility=None,
            role=None,
        ),
        '["test_admin@gmail.com", "unittesting", "admin"]': GroupAccess(
            email="test_admin@gmail.com",
            group_name="unittesting",
            state=GroupAccessState(modified_date=None),
            confirm_deletion=None,
            expiration_time=None,
            has_access=None,
            invitation=None,
            responsibility=None,
            role=None,
        ),
        '["test_email@gmail.com", "unittesting", ""]': GroupAccess(
            email="test_email@gmail.com",
            group_name="unittesting",
            state=GroupAccessState(modified_date=None),
            confirm_deletion=None,
            expiration_time=None,
            has_access=None,
            invitation=None,
            responsibility=None,
            role=None,
        ),
        '["unittest@fluidattacks.com", "unittesting", "admin"]': GroupAccess(
            email="unittest@fluidattacks.com",
            group_name="unittesting",
            state=GroupAccessState(modified_date=None),
            confirm_deletion=None,
            expiration_time=None,
            has_access=True,
            invitation=None,
            responsibility=None,
            role="admin",
        ),
    },
    "db_model.group_access.remove": {
        '["unittest@fluidattacks.com", "unittesting"]': None,
    },
    "db_model.group_access.update_metadata": {
        '["integrateshacker@fluidattacks.com", "unittesting"]': None,
        '["integratesuser@gmail.com", "unittesting"]': None,
        '["test@test.com", "unittesting", "user"]': None,
        '["test2@test.com", "oneshottest", "user_manager"]': None,
    },
    "db_model.group_comments.add": {
        '[["unittesting", "1672083646257", "0", "2022-04-06 16:46:23+00:00",'
        ' "Test comment", "unittest@fluidattacks.com", "unittesting"]]': None,
    },
    "dynamodb.operations.put_item": {
        '["e248e8e0-0323-41c7-bc02-4ee61d09f9c4", '
        '["unittest@fluidattacks.com", "2022-01-24 17:46:10+00:00", "ASM", '
        '"7777", "SAFE", "192.168.1.18", null, null, null, null, null]]': None,
    },
    "dynamodb.operations.update_item": {
        '["463461507", "e248e8e0-0323-41c7-bc02-4ee61d09f9c4", '
        '["unittest@fluidattacks.com", "2022-01-24 17:46:10+00:00", "ASM", '
        '"7777", "SAFE", "192.168.1.18", null, null, null, null, null]]': None,
    },
    "dynamodb.operations_legacy.delete_item": {
        '["44aa89bddf5e0a5b1aca2551799b71ff593c95a89f4402b84697e9b29f6'
        '52110"]': True,
    },
    "dynamodb.operations_legacy.put_item": {
        '["b48ee2ddd5d3869cf9e5f9a419db6d3d01858af338cae057aec9c1618fc5b790", "1673453501", "integrates_small"]': True  # noqa: E501 pylint: disable=line-too-long
    },
    "dynamodb.operations_legacy.query": {
        '["ac25d6d18e368c34a41103a9f6dbf0a787cf2551d6ef5884c844085d26013e0a"]': [  # noqa: E501 pylint: disable=line-too-long
            dict(
                additional_info=json.dumps(
                    dict(
                        report_type="XLS",
                        treatments=["ACCEPTED", "UNTREATED"],
                        states=["VULNERABLE"],
                        verifications=["REQUESTED"],
                        closing_date="null",
                        finding_title="038",
                        age=1100,
                        min_severity="2.7",
                        max_severity="null",
                    )
                ),
                subject="unittesting@fluidattacks.com",
                action_name="report",
                pk="ac25d6d18e368c34a41103a9f6dbf0a787cf2551d6ef5884c844085d26013e0a",  # noqa: E501 pylint: disable=line-too-long
                time="1616116348",
                entity="unittesting",
                queue="small",
            )
        ],
        '["049ee0097a137f2961578929a800a5f23f93f59806b901ee3324abf6eb5a4828"]': [],  # noqa: E501 pylint: disable=line-too-long
    },
    "dynamodb.operations_legacy.scan": {
        "[]": [
            {
                "additional_info": json.dumps(
                    {
                        "report_type": "XLS",
                        "treatments": [
                            "ACCEPTED",
                            "ACCEPTED_UNDEFINED",
                            "IN_PROGRESS",
                            "UNTREATED",
                        ],
                        "states": ["SAFE"],
                        "verifications": ["VERIFIED"],
                        "closing_date": "2020-06-01T00:00:00",
                        "finding_title": "065",
                        "age": "null",
                        "min_severity": "null",
                        "max_severity": "null",
                        "last_report": "null",
                        "min_release_date": "null",
                        "max_release_date": "null",
                        "location": "",
                    }
                ),
                "subject": "unittesting@fluidattacks.com",
                "action_name": "report",
                "pk": "78ebd9f895b8efcd4e6d4cf40d3dbcf3f6fc2ac655537edc0b0465bd3a80871c",  # noqa: E501 pylint: disable=line-too-long
                "time": "1672248409",
                "entity": "unittesting",
                "queue": "integrates_medium",
            },
            {
                "additional_info": json.dumps(
                    {
                        "report_type": "XLS",
                        "treatments": [
                            "ACCEPTED",
                            "ACCEPTED_UNDEFINED",
                            "IN_PROGRESS",
                            "UNTREATED",
                        ],
                        "states": ["SAFE", "VULNERABLE"],
                        "verifications": [],
                        "closing_date": "null",
                        "finding_title": "068",
                        "age": 1300,
                        "min_severity": "2.9",
                        "max_severity": "4.3",
                        "last_report": "null",
                        "min_release_date": "null",
                        "max_release_date": "null",
                        "location": "",
                    }
                ),
                "subject": "unittesting@fluidattacks.com",
                "action_name": "report",
                "pk": "ecfa753fb705d90f4636906dcd2fb8db7ddb06cb356e14fe0fb57c23e92fafb5",  # noqa: E501 pylint: disable=line-too-long
                "time": "1672248409",
                "entity": "unittesting",
                "queue": "integrates_medium",
            },
        ],
    },
    "db_model.organizations.add": {
        '["org_testusermanager1@gmail.com", "Colombia", "esdeath"]': None,
    },
    "db_model.organizations.get.OrganizationLoader.load": {
        '["unittesting"]': Organization(
            created_by="unknown@unknown.com",
            created_date=datetime.fromisoformat("2018-02-08T00:43:18+00:00"),
            id="ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3",
            name="okada",
            policies=Policies(
                modified_date=datetime.fromisoformat(
                    "2019-11-22T20:07:57+00:00"
                ),
                modified_by="integratesmanager@gmail.com",
                inactivity_period=90,
                max_acceptance_days=60,
                max_acceptance_severity=Decimal("10.0"),
                max_number_acceptances=2,
                min_acceptance_severity=Decimal("0.0"),
                min_breaking_severity=Decimal("0"),
                vulnerability_grace_period=0,
            ),
            state=OrganizationState(
                status=OrganizationStateStatus.ACTIVE,
                modified_by="unknown",
                modified_date=datetime.fromisoformat(
                    "2018-02-08T00:43:18+00:00"
                ),
                pending_deletion_date=datetime.fromisoformat(
                    "2019-11-22T20:07:57+00:00"
                ),
            ),
            country="Colombia",
            payment_methods=[
                OrganizationPaymentMethods(
                    id="38eb8f25-7945-4173-ab6e-0af4ad8b7ef3",
                    business_name="Fluid",
                    email="test@fluidattacks.com",
                    country="Colombia",
                    state="Antioquia",
                    city="Medellín",
                    documents=OrganizationDocuments(rut=None, tax_id=None),
                ),
                OrganizationPaymentMethods(
                    id="4722b0b7-cfeb-4898-8308-185dfc2523bc",
                    business_name="Testing Company and Sons",
                    email="test@fluidattacks.com",
                    country="Colombia",
                    state="Antioquia",
                    city="Medellín",
                    documents=OrganizationDocuments(rut=None, tax_id=None),
                ),
            ],
            billing_customer=None,
            vulnerabilities_url=None,
        ),
    },
    "db_model.organizations.remove": {
        '["ORG#fe80d2d4-ccb7-46d1-8489-67c6360581de", "tatsumi"]': None
    },
    "db_model.organizations.update_policies": {
        '["org_testuser1@gmail.com", '
        '"ORG#c2ee2d15-04ab-4f39-9795-fbe30cdeee86", "bulat", '
        '[21, 20, "8.3", 3, "2.2", "3.4", 17]]': None,
    },
    "db_model.organizations.update_state": {
        '["ORG#fe80d2d4-ccb7-46d1-8489-67c6360581de", '
        '"tatsumi", "org_testuser1@gmail.com"]': None,
    },
    "db_model.organization_access.update_metadata": {
        '["ORG#f2e2777d-a168-4bea-93cd-d79142b294d2", '
        '"org_testgroupmanager2@fluidattacks.com"]': None,
    },
    "db_model.organization_finding_policies.remove_org_finding_policies": {
        '["tatsumi"]': None,
    },
    "db_model.portfolios.remove_organization_portfolios": {
        '["tatsumi"]': None,
    },
    "db_model.roots.get.RootLoader.load": {
        '["unittesting", "4039d098-ffc5-4984-8ed3-eb17bca98e19"]': GitRoot(
            cloning=GitRootCloning(
                modified_date=datetime.fromisoformat(
                    "2020-11-19T13:45:55+00:00"
                ),
                reason="root OK",
                status=GitCloningStatus.OK,
                commit="5b5c92105b5c92105b5c92105b5c92105b5c9210",
                commit_date=datetime.fromisoformat(
                    "2022-02-15T18:45:06.493253+00:00"
                ),
            ),
            created_by="jdoe@fluidattacks.com",
            created_date=datetime.fromisoformat("2020-11-19T13:45:55+00:00"),
            group_name="unittesting",
            id="4039d098-ffc5-4984-8ed3-eb17bca98e19",
            organization_name="okada",
            state=GitRootState(
                branch="master",
                environment="production",
                includes_health_check=True,
                modified_by="jdoe@fluidattacks.com",
                modified_date=datetime.fromisoformat(
                    "2020-11-19T13:45:55+00:00"
                ),
                nickname="universe",
                status=RootStatus.ACTIVE,
                url="https://gitlab.com/fluidattacks/universe",
                credential_id=None,
                environment_urls=[
                    "https://app.fluidattacks.com",
                    "https://test.com",
                ],
                git_environment_urls=[],
                gitignore=["bower_components/*", "node_modules/*"],
                other=None,
                reason=None,
                use_vpn=False,
            ),
            type=RootType.GIT,
            unreliable_indicators=RootUnreliableIndicators(
                unreliable_code_languages=[],
                unreliable_last_status_update=datetime.fromisoformat(
                    "2020-11-19T13:45:55+00:00"
                ),
            ),
        ),
    },
    "db_model.stakeholders.get.StakeholderLoader.load": {
        '["continuoushacking@gmail.com", "hacker"]': Stakeholder(
            email="continuoushacking@gmail.com",
            access_token=None,
            first_name="Jhon",
            is_concurrent_session=False,
            is_registered=True,
            last_name="Hackeroy",
            legal_remember=True,
            phone=StakeholderPhone(
                country_code="CO",
                calling_country_code="57",
                national_number="3004005006",
            ),
            role="hacker",
            session_key=None,
            session_token=None,
            state=StakeholderState(
                modified_by="continuoushacking@gmail.com",
                modified_date=None,
                notifications_preferences=NotificationsPreferences(
                    email=[
                        "ACCESS_GRANTED",
                        "AGENT_TOKEN",
                        "CHARTS_REPORT",
                        "EVENT_REPORT",
                        "FILE_UPDATE",
                        "GROUP_INFORMATION",
                        "GROUP_REPORT",
                        "NEW_COMMENT",
                        "NEW_DRAFT",
                        "PORTFOLIO_UPDATE",
                        "REMEDIATE_FINDING",
                        "REMINDER_NOTIFICATION",
                        "ROOT_UPDATE",
                        "SERVICE_UPDATE",
                        "UNSUBSCRIPTION_ALERT",
                        "UPDATED_TREATMENT",
                        "VULNERABILITY_ASSIGNED",
                        "VULNERABILITY_REPORT",
                    ],
                    sms=[],
                    parameters=NotificationsParameters(
                        min_severity=Decimal("7.0")
                    ),
                ),
            ),
            tours=StakeholderTours(new_group=False, new_root=False),
        ),
        '["integrateshacker@fluidattacks.com", "hacker"]': Stakeholder(
            email="integrateshacker@fluidattacks.com",
            access_token=None,
            first_name="Ismael",
            is_concurrent_session=False,
            is_registered=True,
            last_name="Rivera",
            legal_remember=False,
            phone=StakeholderPhone(
                country_code="CO",
                calling_country_code="57",
                national_number="3004005006",
            ),
            role="hacker",
            session_key=None,
            session_token=None,
            state=StakeholderState(
                modified_by="integrateshacker@fluidattacks.com",
                modified_date=None,
                notifications_preferences=NotificationsPreferences(
                    email=[],
                    sms=[],
                    parameters=NotificationsParameters(
                        min_severity=Decimal("7.0")
                    ),
                ),
            ),
            tours=StakeholderTours(new_group=False, new_root=False),
        ),
        '["integratesuser@gmail.com", "user"]': Stakeholder(
            email="integratesuser@gmail.com",
            access_token=None,
            first_name="Jane",
            is_concurrent_session=False,
            is_registered=True,
            last_name="Doe",
            legal_remember=True,
            phone=StakeholderPhone(
                country_code="CO",
                calling_country_code="57",
                national_number="30044445556",
            ),
            role="user",
            session_key=None,
            session_token=StakeholderSessionToken(
                jti="0f98c8d494be2c9eddd973e4a861483988a1d90bb26"
                "8be48dfc442d0b4cada72",
                state=StateSessionType.IS_VALID,
            ),
            state=StakeholderState(
                modified_by="integratesuser@gmail.com",
                modified_date=None,
                notifications_preferences=NotificationsPreferences(
                    email=[
                        "ACCESS_GRANTED",
                        "AGENT_TOKEN",
                        "CHARTS_REPORT",
                        "EVENT_REPORT",
                        "FILE_UPDATE",
                        "GROUP_INFORMATION",
                        "GROUP_REPORT",
                        "NEW_COMMENT",
                        "NEW_DRAFT",
                        "PORTFOLIO_UPDATE",
                        "REMEDIATE_FINDING",
                        "REMINDER_NOTIFICATION",
                        "ROOT_UPDATE",
                        "SERVICE_UPDATE",
                        "UNSUBSCRIPTION_ALERT",
                        "UPDATED_TREATMENT",
                        "VULNERABILITY_ASSIGNED",
                        "VULNERABILITY_REPORT",
                    ],
                    sms=[],
                ),
            ),
            tours=StakeholderTours(new_group=False, new_root=False),
        ),
        '["unittest@fluidattacks.com", "admin"]': Stakeholder(
            email="unittest@fluidattacks.com",
            access_token=StakeholderAccessToken(
                iat=1634677195,
                jti="c8d9d5f095958cf200f7435508fc2dba37d07447ec12dcd0"
                "70808418d640e77d",
                salt="27c7f388ccdd7cc432871c84b63e78cd716739c40055253c"
                "e7ad1666a8532db6",
            ),
            first_name="Miguel",
            is_concurrent_session=False,
            is_registered=True,
            last_name="de Orellana",
            legal_remember=True,
            phone=StakeholderPhone(
                country_code="CO",
                calling_country_code="57",
                national_number="3006007008",
            ),
            role="admin",
            session_key=None,
            session_token=None,
            state=StakeholderState(
                modified_by="integratesuser@gmail.com",
                modified_date=None,
                notifications_preferences=NotificationsPreferences(
                    email=[],
                    sms=[],
                ),
            ),
            tours=StakeholderTours(new_group=False, new_root=False),
        ),
    },
    "db_model.stakeholders.get.StakeholderWithFallbackLoader.load": {
        '["integrateshacker@fluidattacks.com"]': Stakeholder(
            email="integrateshacker@fluidattacks.com",
            access_token=None,
            first_name="Ismael",
            is_concurrent_session=False,
            is_registered=True,
            last_name="Rivera",
            legal_remember=False,
            phone=StakeholderPhone(
                country_code="CO",
                calling_country_code="57",
                national_number="3004005006",
            ),
            role="hacker",
            session_key=None,
            session_token=None,
            state=StakeholderState(
                modified_by="integrateshacker@fluidattacks.com",
                modified_date=None,
                notifications_preferences=NotificationsPreferences(
                    email=[],
                    sms=[],
                    parameters=NotificationsParameters(
                        min_severity=Decimal("7.0")
                    ),
                ),
            ),
            tours=StakeholderTours(new_group=False, new_root=False),
        ),
        '["integratesuser@gmail.com"]': Stakeholder(
            email="integratesuser@gmail.com",
            access_token=None,
            first_name="Jane",
            is_concurrent_session=False,
            is_registered=True,
            last_name="Doe",
            legal_remember=True,
            phone=StakeholderPhone(
                country_code="CO",
                calling_country_code="57",
                national_number="30044445556",
            ),
            role="user",
            session_key=None,
            session_token=StakeholderSessionToken(
                jti="0f98c8d494be2c9eddd973e4a861483988a1d90bb26"
                "8be48dfc442d0b4cada72",
                state=StateSessionType.IS_VALID,
            ),
            state=StakeholderState(
                modified_by="integratesuser@gmail.com",
                modified_date=None,
                notifications_preferences=NotificationsPreferences(
                    email=[
                        "ACCESS_GRANTED",
                        "AGENT_TOKEN",
                        "CHARTS_REPORT",
                        "EVENT_REPORT",
                        "FILE_UPDATE",
                        "GROUP_INFORMATION",
                        "GROUP_REPORT",
                        "NEW_COMMENT",
                        "NEW_DRAFT",
                        "PORTFOLIO_UPDATE",
                        "REMEDIATE_FINDING",
                        "REMINDER_NOTIFICATION",
                        "ROOT_UPDATE",
                        "SERVICE_UPDATE",
                        "UNSUBSCRIPTION_ALERT",
                        "UPDATED_TREATMENT",
                        "VULNERABILITY_ASSIGNED",
                        "VULNERABILITY_REPORT",
                    ],
                    sms=[],
                ),
            ),
            tours=StakeholderTours(new_group=False, new_root=False),
        ),
    },
    "db_model.stakeholders.update_metadata": {
        '["integrateshacker@fluidattacks.com"]': None,
        '["integratesuser@gmail.com"]': None,
        '["test_email@test.com", "user"]': None,
        '["test_email@test.com", "admin"]': None,
    },
    "db_model.vulnerabilities.get.AssignedVulnerabilitiesLoader.load": {
        '["unittest@fluidattacks.com"]': [],
    },
    "db_model.vulnerabilities.get.EventVulnerabilitiesLoader.load": {
        '["418900978"]': tuple(),
        '["538745942"]': tuple(),
    },
    "db_model.vulnerabilities.get.FindingVulnerabilitiesLoader.load": {
        '["457497316"]': [
            Vulnerability(
                created_by="unittest@fluidattacks.com",
                created_date=datetime.fromisoformat(
                    "2018-11-27T19:54:08+00:00"
                ),
                finding_id="457497316",
                group_name="unittesting",
                hacker_email="unittest@fluidattacks.com",
                id="6192c72f-2e10-4259-9207-717b2d90d8d2",
                state=VulnerabilityState(
                    modified_by="unittest@fluidattacks.com",
                    modified_date=datetime.fromisoformat(
                        "2019-09-16T14:40:37+00:00"
                    ),
                    source=Source.ASM,
                    specific="userToken",
                    status=VulnerabilityStateStatus.SAFE,
                    where="https://10.1.1.1/",
                    commit=None,
                    reasons=None,
                    other_reason=None,
                    tool=None,
                    snippet=None,
                ),
                type=VulnerabilityType.INPUTS,
                bug_tracking_system_url=None,
                custom_severity=None,
                developer=None,
                event_id=None,
                hash=None,
                root_id=None,
                skims_method=None,
                skims_technique=None,
                stream=None,
                tags=None,
                treatment=VulnerabilityTreatment(
                    modified_date=datetime.fromisoformat(
                        "2018-11-27T19:54:08+00:00"
                    ),
                    status=VulnerabilityTreatmentStatus.UNTREATED,
                    acceptance_status=None,
                    accepted_until=None,
                    justification=None,
                    assigned=None,
                    modified_by=None,
                ),
                unreliable_indicators=VulnerabilityUnreliableIndicators(
                    unreliable_closing_date=datetime.fromisoformat(
                        "2019-09-16T14:40:37+00:00"
                    ),
                    unreliable_source=Source.ASM,
                    unreliable_efficacy=Decimal("0"),
                    unreliable_last_reattack_date=None,
                    unreliable_last_reattack_requester=None,
                    unreliable_last_requested_reattack_date=None,
                    unreliable_reattack_cycles=0,
                    unreliable_treatment_changes=0,
                ),
                verification=None,
                zero_risk=None,
            ),
        ]
    },
    "db_model.vulnerabilities.get.FindingVulnerabilitiesNonDeletedLoader.load_many_chained": {  # noqa: E501 pylint: disable=line-too-long
        '["unittesting", "0.0", "10.0"]': tuple(
            [
                Vulnerability(
                    created_by="unittest@fluidattacks.com",
                    created_date=datetime.fromisoformat(
                        "2020-01-03T17:46:10+00:00"
                    ),
                    finding_id="422286126",
                    group_name="unittesting",
                    hacker_email="unittest@fluidattacks.com",
                    id="0a848781-b6a4-422e-95fa-692151e6a98z",
                    state=VulnerabilityState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2020-01-03T17:46:10+00:00"
                        ),
                        source=Source.ASM,
                        specific="12",
                        status=VulnerabilityStateStatus.VULNERABLE,
                        where="test/data/lib_path/f060/csharp.cs",
                        commit="ea871eee64cfd5ce293411efaf4d3b446d04eb4a",
                        reasons=None,
                        other_reason=None,
                        tool=VulnerabilityTool(
                            name="tool-2",
                            impact=VulnerabilityToolImpact.INDIRECT,
                        ),
                        snippet=None,
                    ),
                    type=VulnerabilityType.LINES,
                    bug_tracking_system_url=None,
                    custom_severity=None,
                    developer=None,
                    event_id=None,
                    hash=None,
                    root_id=None,
                    skims_method=None,
                    skims_technique=None,
                    stream=None,
                    tags=None,
                    treatment=VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2020-01-03T17:46:10+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.IN_PROGRESS,
                        acceptance_status=None,
                        accepted_until=None,
                        justification="test justification",
                        assigned="integratesuser2@gmail.com",
                        modified_by="integratesuser@gmail.com",
                    ),
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_closing_date=None,
                        unreliable_source=Source.ASM,
                        unreliable_efficacy=Decimal("0"),
                        unreliable_last_reattack_date=None,
                        unreliable_last_reattack_requester=None,
                        unreliable_last_requested_reattack_date=None,
                        unreliable_reattack_cycles=0,
                        unreliable_treatment_changes=1,
                    ),
                    verification=None,
                    zero_risk=None,
                ),
                Vulnerability(
                    created_by="test@unittesting.com",
                    created_date=datetime.fromisoformat(
                        "2020-09-09T21:01:26+00:00"
                    ),
                    finding_id="422286126",
                    group_name="unittesting",
                    hacker_email="test@unittesting.com",
                    id="80d6a69f-a376-46be-98cd-2fdedcffdcc0",
                    state=VulnerabilityState(
                        modified_by="test@unittesting.com",
                        modified_date=datetime.fromisoformat(
                            "2020-09-09T21:01:26+00:00"
                        ),
                        source=Source.ASM,
                        specific="phone",
                        status=VulnerabilityStateStatus.VULNERABLE,
                        where="https://example.com",
                        commit=None,
                        reasons=None,
                        other_reason=None,
                        tool=VulnerabilityTool(
                            name="tool-2",
                            impact=VulnerabilityToolImpact.INDIRECT,
                        ),
                        snippet=None,
                    ),
                    type=VulnerabilityType.INPUTS,
                    bug_tracking_system_url=None,
                    custom_severity=None,
                    developer=None,
                    event_id=None,
                    hash=None,
                    root_id=None,
                    skims_method=None,
                    skims_technique=None,
                    stream=None,
                    tags=None,
                    treatment=VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2020-11-23T17:46:10+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.IN_PROGRESS,
                        acceptance_status=None,
                        accepted_until=None,
                        justification="This is a treatment justification",
                        assigned="integratesuser@gmail.com",
                        modified_by="integratesuser2@gmail.com",
                    ),
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_closing_date=None,
                        unreliable_source=Source.ASM,
                        unreliable_efficacy=Decimal("0"),
                        unreliable_last_reattack_date=None,
                        unreliable_last_reattack_requester=None,
                        unreliable_last_requested_reattack_date=None,
                        unreliable_reattack_cycles=0,
                        unreliable_treatment_changes=1,
                    ),
                    verification=None,
                    zero_risk=VulnerabilityZeroRisk(
                        comment_id="123456",
                        modified_by="test@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2020-09-09T21:01:26+00:00"
                        ),
                        status=VulnerabilityZeroRiskStatus.CONFIRMED,
                    ),
                ),
                Vulnerability(
                    created_by="unittest@fluidattacks.com",
                    created_date=datetime.fromisoformat(
                        "2019-09-13T13:17:41+00:00"
                    ),
                    finding_id="436992569",
                    group_name="unittesting",
                    hacker_email="unittest@fluidattacks.com",
                    id="15375781-31f2-4953-ac77-f31134225747",
                    state=VulnerabilityState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2019-09-13T13:17:41+00:00"
                        ),
                        source=Source.ASM,
                        specific="333",
                        status=VulnerabilityStateStatus.VULNERABLE,
                        where="192.168.100.101",
                        commit=None,
                        reasons=None,
                        other_reason=None,
                        tool=VulnerabilityTool(
                            name="tool-2",
                            impact=VulnerabilityToolImpact.INDIRECT,
                        ),
                        snippet=None,
                    ),
                    type=VulnerabilityType.PORTS,
                    bug_tracking_system_url=None,
                    custom_severity=None,
                    developer=None,
                    event_id=None,
                    hash=None,
                    root_id=None,
                    skims_method=None,
                    skims_technique=None,
                    stream=None,
                    tags=None,
                    treatment=VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2019-09-13T13:17:41+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.UNTREATED,
                        acceptance_status=None,
                        accepted_until=None,
                        justification=None,
                        assigned=None,
                        modified_by=None,
                    ),
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_closing_date=None,
                        unreliable_source=Source.ASM,
                        unreliable_efficacy=Decimal("0"),
                        unreliable_last_reattack_date=datetime.fromisoformat(
                            "2020-02-19T15:41:04+00:00"
                        ),
                        unreliable_last_reattack_requester="integratesuser@gmail.com",  # noqa: E501 pylint: disable=line-too-long
                        unreliable_last_requested_reattack_date=datetime.fromisoformat(  # noqa: E501 pylint: disable=line-too-long
                            "2020-02-18T15:41:04+00:00"
                        ),
                        unreliable_reattack_cycles=1,
                        unreliable_treatment_changes=0,
                    ),
                    verification=VulnerabilityVerification(
                        modified_date=datetime.fromisoformat(
                            "2020-02-19T15:41:04+00:00"
                        ),
                        status=VulnerabilityVerificationStatus.VERIFIED,
                        event_id=None,
                    ),
                    zero_risk=None,
                ),
                Vulnerability(
                    created_by="unittest@fluidattacks.com",
                    created_date=datetime.fromisoformat(
                        "2019-09-12T13:45:48+00:00"
                    ),
                    finding_id="436992569",
                    group_name="unittesting",
                    hacker_email="unittest@fluidattacks.com",
                    id="1c644e88-b7a2-498b-b248-c3d367629982",
                    state=VulnerabilityState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2019-09-12T13:45:48+00:00"
                        ),
                        source=Source.ASM,
                        specific="1111",
                        status=VulnerabilityStateStatus.VULNERABLE,
                        where="192.168.1.12",
                        commit=None,
                        reasons=None,
                        other_reason=None,
                        tool=VulnerabilityTool(
                            name="tool-2",
                            impact=VulnerabilityToolImpact.INDIRECT,
                        ),
                        snippet=None,
                    ),
                    type=VulnerabilityType.PORTS,
                    bug_tracking_system_url=None,
                    custom_severity=None,
                    developer=None,
                    event_id=None,
                    hash=None,
                    root_id=None,
                    skims_method=None,
                    skims_technique=None,
                    stream=None,
                    tags=None,
                    treatment=VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2019-09-12T13:45:48+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.UNTREATED,
                        acceptance_status=None,
                        accepted_until=None,
                        justification=None,
                        assigned=None,
                        modified_by=None,
                    ),
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_closing_date=None,
                        unreliable_source=Source.ASM,
                        unreliable_efficacy=Decimal("0"),
                        unreliable_last_reattack_date=None,
                        unreliable_last_reattack_requester=None,
                        unreliable_last_requested_reattack_date=None,
                        unreliable_reattack_cycles=0,
                        unreliable_treatment_changes=0,
                    ),
                    verification=None,
                    zero_risk=None,
                ),
                Vulnerability(
                    created_by="unittest@fluidattacks.com",
                    created_date=datetime.fromisoformat(
                        "2019-09-12T13:45:48+00:00"
                    ),
                    finding_id="436992569",
                    group_name="unittesting",
                    hacker_email="unittest@fluidattacks.com",
                    id="3ec662b9-431a-475c-97e4-ac6ad4cabd90",
                    state=VulnerabilityState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2019-09-12T13:45:48+00:00"
                        ),
                        source=Source.ASM,
                        specific="3333",
                        status=VulnerabilityStateStatus.VULNERABLE,
                        where="192.168.1.4",
                        commit=None,
                        reasons=None,
                        other_reason=None,
                        tool=VulnerabilityTool(
                            name="tool-2",
                            impact=VulnerabilityToolImpact.INDIRECT,
                        ),
                        snippet=None,
                    ),
                    type=VulnerabilityType.PORTS,
                    bug_tracking_system_url=None,
                    custom_severity=None,
                    developer=None,
                    event_id="EVENT#418900971",
                    hash=None,
                    root_id="4039d098-ffc5-4984-8ed3-eb17bca98e19",
                    skims_method=None,
                    skims_technique=None,
                    stream=None,
                    tags=None,
                    treatment=VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2019-09-12T13:45:48+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.UNTREATED,
                        acceptance_status=None,
                        accepted_until=None,
                        justification=None,
                        assigned=None,
                        modified_by=None,
                    ),
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_closing_date=None,
                        unreliable_source=Source.ASM,
                        unreliable_efficacy=Decimal("0"),
                        unreliable_last_reattack_date=None,
                        unreliable_last_reattack_requester=None,
                        unreliable_last_requested_reattack_date=None,
                        unreliable_reattack_cycles=0,
                        unreliable_treatment_changes=0,
                    ),
                    verification=VulnerabilityVerification(
                        modified_date=datetime.fromisoformat(
                            "2022-02-19T15:41:04+00:00"
                        ),
                        status=VulnerabilityVerificationStatus.ON_HOLD,
                        event_id="418900971",
                    ),
                    zero_risk=None,
                ),
                Vulnerability(
                    created_by="unittest@fluidattacks.com",
                    created_date=datetime.fromisoformat(
                        "2019-09-12T13:45:48+00:00"
                    ),
                    finding_id="436992569",
                    group_name="unittesting",
                    hacker_email="unittest@fluidattacks.com",
                    id="47910cbe-932a-411b-8a46-9570a87f4663",
                    state=VulnerabilityState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2019-09-12T13:45:48+00:00"
                        ),
                        source=Source.ASM,
                        specific="6666",
                        status=VulnerabilityStateStatus.VULNERABLE,
                        where="192.168.1.17",
                        commit=None,
                        reasons=None,
                        other_reason=None,
                        tool=None,
                        snippet=None,
                    ),
                    type=VulnerabilityType.PORTS,
                    bug_tracking_system_url=None,
                    custom_severity=None,
                    developer=None,
                    event_id="EVENT#418900971",
                    hash=None,
                    root_id=None,
                    skims_method=None,
                    skims_technique=None,
                    stream=None,
                    tags=None,
                    treatment=VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2019-09-12T13:45:48+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.UNTREATED,
                        acceptance_status=None,
                        accepted_until=None,
                        justification=None,
                        assigned=None,
                        modified_by=None,
                    ),
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_closing_date=None,
                        unreliable_source=Source.ASM,
                        unreliable_efficacy=Decimal("0"),
                        unreliable_last_reattack_date=None,
                        unreliable_last_reattack_requester=None,
                        unreliable_last_requested_reattack_date=None,
                        unreliable_reattack_cycles=0,
                        unreliable_treatment_changes=0,
                    ),
                    verification=VulnerabilityVerification(
                        modified_date=datetime.fromisoformat(
                            "2022-02-19T15:41:04+00:00"
                        ),
                        status=VulnerabilityVerificationStatus.ON_HOLD,
                        event_id="418900971",
                    ),
                    zero_risk=None,
                ),
                Vulnerability(
                    created_by="unittest@fluidattacks.com",
                    created_date=datetime.fromisoformat(
                        "2019-09-12T13:45:48+00:00"
                    ),
                    finding_id="436992569",
                    group_name="unittesting",
                    hacker_email="unittest@fluidattacks.com",
                    id="4ed30d35-33a5-44ba-af44-6cb253be053b",
                    state=VulnerabilityState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2019-09-12T13:45:48+00:00"
                        ),
                        source=Source.ASM,
                        specific="4444",
                        status=VulnerabilityStateStatus.VULNERABLE,
                        where="192.168.1.15",
                        commit=None,
                        reasons=None,
                        other_reason=None,
                        tool=VulnerabilityTool(
                            name="tool-3",
                            impact=VulnerabilityToolImpact.INDIRECT,
                        ),
                        snippet=None,
                    ),
                    type=VulnerabilityType.PORTS,
                    bug_tracking_system_url=None,
                    custom_severity=None,
                    developer=None,
                    event_id=None,
                    hash=None,
                    root_id=None,
                    skims_method=None,
                    skims_technique=None,
                    stream=None,
                    tags=None,
                    treatment=VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2019-09-12T13:45:48+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.UNTREATED,
                        acceptance_status=None,
                        accepted_until=None,
                        justification=None,
                        assigned=None,
                        modified_by=None,
                    ),
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_closing_date=None,
                        unreliable_source=Source.ASM,
                        unreliable_efficacy=Decimal("0"),
                        unreliable_last_reattack_date=None,
                        unreliable_last_reattack_requester=None,
                        unreliable_last_requested_reattack_date=None,
                        unreliable_reattack_cycles=0,
                        unreliable_treatment_changes=0,
                    ),
                    verification=None,
                    zero_risk=None,
                ),
                Vulnerability(
                    created_by="unittest@fluidattacks.com",
                    created_date=datetime.fromisoformat(
                        "2019-09-12T13:45:48+00:00"
                    ),
                    finding_id="436992569",
                    group_name="unittesting",
                    hacker_email="unittest@fluidattacks.com",
                    id="5291f6fa-b296-4e89-a760-798ce56f17d0",
                    state=VulnerabilityState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2019-09-12T13:45:48+00:00"
                        ),
                        source=Source.ASM,
                        specific="5555",
                        status=VulnerabilityStateStatus.VULNERABLE,
                        where="192.168.1.6",
                        commit=None,
                        reasons=None,
                        other_reason=None,
                        tool=VulnerabilityTool(
                            name="tool-3",
                            impact=VulnerabilityToolImpact.INDIRECT,
                        ),
                        snippet=None,
                    ),
                    type=VulnerabilityType.PORTS,
                    bug_tracking_system_url=None,
                    custom_severity=None,
                    developer=None,
                    event_id=None,
                    hash=None,
                    root_id=None,
                    skims_method=None,
                    skims_technique=None,
                    stream=None,
                    tags=None,
                    treatment=VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2019-09-12T13:45:48+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.UNTREATED,
                        acceptance_status=None,
                        accepted_until=None,
                        justification=None,
                        assigned=None,
                        modified_by=None,
                    ),
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_closing_date=None,
                        unreliable_source=Source.ASM,
                        unreliable_efficacy=Decimal("0"),
                        unreliable_last_reattack_date=None,
                        unreliable_last_reattack_requester=None,
                        unreliable_last_requested_reattack_date=None,
                        unreliable_reattack_cycles=0,
                        unreliable_treatment_changes=0,
                    ),
                    verification=None,
                    zero_risk=None,
                ),
                Vulnerability(
                    created_by="unittest@fluidattacks.com",
                    created_date=datetime.fromisoformat(
                        "2019-09-12T13:45:48+00:00"
                    ),
                    finding_id="436992569",
                    group_name="unittesting",
                    hacker_email="unittest@fluidattacks.com",
                    id="57e5c1ec-5956-40e9-8e30-284033c1140d",
                    state=VulnerabilityState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2019-09-12T13:45:48+00:00"
                        ),
                        source=Source.ASM,
                        specific="9999",
                        status=VulnerabilityStateStatus.VULNERABLE,
                        where="192.168.1.10",
                        commit=None,
                        reasons=None,
                        other_reason=None,
                        tool=VulnerabilityTool(
                            name="tool-3",
                            impact=VulnerabilityToolImpact.INDIRECT,
                        ),
                        snippet=None,
                    ),
                    type=VulnerabilityType.PORTS,
                    bug_tracking_system_url=None,
                    custom_severity=None,
                    developer=None,
                    event_id=None,
                    hash=None,
                    root_id=None,
                    skims_method=None,
                    skims_technique=None,
                    stream=None,
                    tags=None,
                    treatment=VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2019-09-12T13:45:48+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.UNTREATED,
                        acceptance_status=None,
                        accepted_until=None,
                        justification=None,
                        assigned=None,
                        modified_by=None,
                    ),
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_closing_date=None,
                        unreliable_source=Source.ASM,
                        unreliable_efficacy=Decimal("0"),
                        unreliable_last_reattack_date=None,
                        unreliable_last_reattack_requester=None,
                        unreliable_last_requested_reattack_date=None,
                        unreliable_reattack_cycles=0,
                        unreliable_treatment_changes=0,
                    ),
                    verification=None,
                    zero_risk=None,
                ),
                Vulnerability(
                    created_by="unittest@fluidattacks.com",
                    created_date=datetime.fromisoformat(
                        "2019-09-13T22:00:56+00:00"
                    ),
                    finding_id="436992569",
                    group_name="unittesting",
                    hacker_email="unittest@fluidattacks.com",
                    id="587c40de-09a0-4d85-a9f9-eaa46aa895d7",
                    state=VulnerabilityState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2019-09-13T22:00:56+00:00"
                        ),
                        source=Source.ASM,
                        specific="1111",
                        status=VulnerabilityStateStatus.VULNERABLE,
                        where="192.168.100.112",
                        commit=None,
                        reasons=None,
                        other_reason=None,
                        tool=None,
                        snippet=None,
                    ),
                    type=VulnerabilityType.PORTS,
                    bug_tracking_system_url=None,
                    custom_severity=None,
                    developer=None,
                    event_id=None,
                    hash=None,
                    root_id=None,
                    skims_method=None,
                    skims_technique=None,
                    stream=None,
                    tags=None,
                    treatment=VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2019-09-13T22:00:56+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.UNTREATED,
                        acceptance_status=None,
                        accepted_until=None,
                        justification=None,
                        assigned=None,
                        modified_by=None,
                    ),
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_closing_date=None,
                        unreliable_source=Source.ASM,
                        unreliable_efficacy=Decimal("0"),
                        unreliable_last_reattack_date=None,
                        unreliable_last_reattack_requester="integratesuser@gmail.com",  # noqa: E501 pylint: disable=line-too-long
                        unreliable_last_requested_reattack_date=datetime.fromisoformat(  # noqa: E501 pylint: disable=line-too-long
                            "2020-02-19T15:41:04+00:00"
                        ),
                        unreliable_reattack_cycles=1,
                        unreliable_treatment_changes=0,
                    ),
                    verification=VulnerabilityVerification(
                        modified_date=datetime.fromisoformat(
                            "2020-02-19T15:41:04+00:00"
                        ),
                        status=VulnerabilityVerificationStatus.REQUESTED,
                        event_id=None,
                    ),
                    zero_risk=None,
                ),
                Vulnerability(
                    created_by="unittest@fluidattacks.com",
                    created_date=datetime.fromisoformat(
                        "2019-09-13T14:58:38+00:00"
                    ),
                    finding_id="436992569",
                    group_name="unittesting",
                    hacker_email="unittest@fluidattacks.com",
                    id="5afb9a49-a359-48ce-80ee-79c145919275",
                    state=VulnerabilityState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2019-09-13T14:58:38+00:00"
                        ),
                        source=Source.ASM,
                        specific="333",
                        status=VulnerabilityStateStatus.VULNERABLE,
                        where="192.168.100.105",
                        commit=None,
                        reasons=None,
                        other_reason=None,
                        tool=None,
                        snippet=None,
                    ),
                    type=VulnerabilityType.PORTS,
                    bug_tracking_system_url=None,
                    custom_severity=None,
                    developer=None,
                    event_id=None,
                    hash=None,
                    root_id=None,
                    skims_method=None,
                    skims_technique=None,
                    stream=None,
                    tags=None,
                    treatment=VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2019-09-13T14:58:38+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.UNTREATED,
                        acceptance_status=None,
                        accepted_until=None,
                        justification=None,
                        assigned=None,
                        modified_by=None,
                    ),
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_closing_date=None,
                        unreliable_source=Source.ASM,
                        unreliable_efficacy=Decimal("0"),
                        unreliable_last_reattack_date=None,
                        unreliable_last_reattack_requester=None,
                        unreliable_last_requested_reattack_date=None,
                        unreliable_reattack_cycles=0,
                        unreliable_treatment_changes=0,
                    ),
                    verification=None,
                    zero_risk=None,
                ),
                Vulnerability(
                    created_by="unittest@fluidattacks.com",
                    created_date=datetime.fromisoformat(
                        "2019-09-13T20:37:59+00:00"
                    ),
                    finding_id="436992569",
                    group_name="unittesting",
                    hacker_email="unittest@fluidattacks.com",
                    id="5ed5c3c0-9064-41f5-8ef2-5e1eeee62955",
                    state=VulnerabilityState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2019-09-13T20:37:59+00:00"
                        ),
                        source=Source.ASM,
                        specific="1111",
                        status=VulnerabilityStateStatus.VULNERABLE,
                        where="192.168.100.111",
                        commit=None,
                        reasons=None,
                        other_reason=None,
                        tool=None,
                        snippet=None,
                    ),
                    type=VulnerabilityType.PORTS,
                    bug_tracking_system_url=None,
                    custom_severity=None,
                    developer=None,
                    event_id=None,
                    hash=None,
                    root_id=None,
                    skims_method=None,
                    skims_technique=None,
                    stream=None,
                    tags=None,
                    treatment=VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2019-09-13T20:37:59+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.UNTREATED,
                        acceptance_status=None,
                        accepted_until=None,
                        justification=None,
                        assigned=None,
                        modified_by=None,
                    ),
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_closing_date=None,
                        unreliable_source=Source.ASM,
                        unreliable_efficacy=Decimal("0"),
                        unreliable_last_reattack_date=None,
                        unreliable_last_reattack_requester=None,
                        unreliable_last_requested_reattack_date=None,
                        unreliable_reattack_cycles=0,
                        unreliable_treatment_changes=0,
                    ),
                    verification=None,
                    zero_risk=None,
                ),
                Vulnerability(
                    created_by="unittest@fluidattacks.com",
                    created_date=datetime.fromisoformat(
                        "2019-09-13T16:03:21+00:00"
                    ),
                    finding_id="436992569",
                    group_name="unittesting",
                    hacker_email="unittest@fluidattacks.com",
                    id="72bb8607-c259-4781-9599-185aac02b3cc",
                    state=VulnerabilityState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2019-09-13T16:05:05+00:00"
                        ),
                        source=Source.ASM,
                        specific="4444",
                        status=VulnerabilityStateStatus.SAFE,
                        where="192.168.100.101",
                        commit=None,
                        reasons=None,
                        other_reason=None,
                        tool=None,
                        snippet=None,
                    ),
                    type=VulnerabilityType.PORTS,
                    bug_tracking_system_url=None,
                    custom_severity=None,
                    developer=None,
                    event_id=None,
                    hash=None,
                    root_id=None,
                    skims_method=None,
                    skims_technique=None,
                    stream=None,
                    tags=None,
                    treatment=VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2019-09-13T16:03:21+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.UNTREATED,
                        acceptance_status=None,
                        accepted_until=None,
                        justification=None,
                        assigned=None,
                        modified_by=None,
                    ),
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_closing_date=datetime.fromisoformat(
                            "2019-09-13T16:05:05+00:00"
                        ),
                        unreliable_source=Source.ASM,
                        unreliable_efficacy=Decimal("0"),
                        unreliable_last_reattack_date=None,
                        unreliable_last_reattack_requester=None,
                        unreliable_last_requested_reattack_date=None,
                        unreliable_reattack_cycles=0,
                        unreliable_treatment_changes=0,
                    ),
                    verification=None,
                    zero_risk=None,
                ),
                Vulnerability(
                    created_by="unittest@fluidattacks.com",
                    created_date=datetime.fromisoformat(
                        "2019-09-12T13:45:48+00:00"
                    ),
                    finding_id="436992569",
                    group_name="unittesting",
                    hacker_email="unittest@fluidattacks.com",
                    id="759aaf00-34ee-4609-aec6-7f857c470eff",
                    state=VulnerabilityState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2019-09-12T13:45:48+00:00"
                        ),
                        source=Source.ASM,
                        specific="4444",
                        status=VulnerabilityStateStatus.VULNERABLE,
                        where="192.168.1.5",
                        commit=None,
                        reasons=None,
                        other_reason=None,
                        tool=None,
                        snippet=None,
                    ),
                    type=VulnerabilityType.PORTS,
                    bug_tracking_system_url=None,
                    custom_severity=None,
                    developer=None,
                    event_id=None,
                    hash=None,
                    root_id=None,
                    skims_method=None,
                    skims_technique=None,
                    stream=None,
                    tags=None,
                    treatment=VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2019-09-12T13:45:48+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.UNTREATED,
                        acceptance_status=None,
                        accepted_until=None,
                        justification=None,
                        assigned=None,
                        modified_by=None,
                    ),
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_closing_date=None,
                        unreliable_source=Source.ASM,
                        unreliable_efficacy=Decimal("0"),
                        unreliable_last_reattack_date=None,
                        unreliable_last_reattack_requester=None,
                        unreliable_last_requested_reattack_date=None,
                        unreliable_reattack_cycles=0,
                        unreliable_treatment_changes=0,
                    ),
                    verification=None,
                    zero_risk=None,
                ),
                Vulnerability(
                    created_by="integratesmanager@gmail.com",
                    created_date=datetime.fromisoformat(
                        "2019-09-13T13:59:20+00:00"
                    ),
                    finding_id="436992569",
                    group_name="unittesting",
                    hacker_email="integratesmanager@gmail.com",
                    id="81db1fad-c329-4356-a5eb-9ad9b0d75a7e",
                    state=VulnerabilityState(
                        modified_by="aaguirre@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2019-09-13T13:59:20+00:00"
                        ),
                        source=Source.ASM,
                        specific="333",
                        status=VulnerabilityStateStatus.VULNERABLE,
                        where="192.168.100.104",
                        commit=None,
                        reasons=None,
                        other_reason=None,
                        tool=None,
                        snippet=None,
                    ),
                    type=VulnerabilityType.PORTS,
                    bug_tracking_system_url=None,
                    custom_severity=None,
                    developer=None,
                    event_id=None,
                    hash=None,
                    root_id=None,
                    skims_method=None,
                    skims_technique=None,
                    stream=None,
                    tags=None,
                    treatment=VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2019-09-13T13:59:20+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.UNTREATED,
                        acceptance_status=None,
                        accepted_until=None,
                        justification=None,
                        assigned=None,
                        modified_by=None,
                    ),
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_closing_date=None,
                        unreliable_source=Source.ASM,
                        unreliable_efficacy=Decimal("0"),
                        unreliable_last_reattack_date=None,
                        unreliable_last_reattack_requester=None,
                        unreliable_last_requested_reattack_date=None,
                        unreliable_reattack_cycles=0,
                        unreliable_treatment_changes=0,
                    ),
                    verification=None,
                    zero_risk=None,
                ),
                Vulnerability(
                    created_by="unittest@fluidattacks.com",
                    created_date=datetime.fromisoformat(
                        "2019-09-13T15:00:03+00:00"
                    ),
                    finding_id="436992569",
                    group_name="unittesting",
                    hacker_email="unittest@fluidattacks.com",
                    id="8226e222-8128-438d-a9b7-93eeb93a36b3",
                    state=VulnerabilityState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2019-09-13T15:09:02+00:00"
                        ),
                        source=Source.ASM,
                        specific="333",
                        status=VulnerabilityStateStatus.SAFE,
                        where="192.168.100.107",
                        commit=None,
                        reasons=None,
                        other_reason=None,
                        tool=None,
                        snippet=None,
                    ),
                    type=VulnerabilityType.PORTS,
                    bug_tracking_system_url=None,
                    custom_severity=None,
                    developer=None,
                    event_id=None,
                    hash=None,
                    root_id=None,
                    skims_method=None,
                    skims_technique=None,
                    stream=None,
                    tags=None,
                    treatment=VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2019-09-13T15:00:03+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.UNTREATED,
                        acceptance_status=None,
                        accepted_until=None,
                        justification=None,
                        assigned=None,
                        modified_by=None,
                    ),
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_closing_date=datetime.fromisoformat(
                            "2019-09-13T15:09:02+00:00"
                        ),
                        unreliable_source=Source.ASM,
                        unreliable_efficacy=Decimal("0"),
                        unreliable_last_reattack_date=None,
                        unreliable_last_reattack_requester=None,
                        unreliable_last_requested_reattack_date=None,
                        unreliable_reattack_cycles=0,
                        unreliable_treatment_changes=0,
                    ),
                    verification=None,
                    zero_risk=None,
                ),
                Vulnerability(
                    created_by="unittest@fluidattacks.com",
                    created_date=datetime.fromisoformat(
                        "2019-09-12T13:45:48+00:00"
                    ),
                    finding_id="436992569",
                    group_name="unittesting",
                    hacker_email="unittest@fluidattacks.com",
                    id="95068fdd-80ca-4eb2-8311-b16b63a61f05",
                    state=VulnerabilityState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2019-09-12T13:45:48+00:00"
                        ),
                        source=Source.ASM,
                        specific="8888",
                        status=VulnerabilityStateStatus.VULNERABLE,
                        where="192.168.1.9",
                        commit=None,
                        reasons=None,
                        other_reason=None,
                        tool=None,
                        snippet=None,
                    ),
                    type=VulnerabilityType.PORTS,
                    bug_tracking_system_url=None,
                    custom_severity=None,
                    developer=None,
                    event_id=None,
                    hash=None,
                    root_id=None,
                    skims_method=None,
                    skims_technique=None,
                    stream=None,
                    tags=None,
                    treatment=VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2019-09-12T13:45:48+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.UNTREATED,
                        acceptance_status=None,
                        accepted_until=None,
                        justification=None,
                        assigned=None,
                        modified_by=None,
                    ),
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_closing_date=None,
                        unreliable_source=Source.ASM,
                        unreliable_efficacy=Decimal("0"),
                        unreliable_last_reattack_date=None,
                        unreliable_last_reattack_requester=None,
                        unreliable_last_requested_reattack_date=None,
                        unreliable_reattack_cycles=0,
                        unreliable_treatment_changes=0,
                    ),
                    verification=None,
                    zero_risk=None,
                ),
                Vulnerability(
                    created_by="unittest@fluidattacks.com",
                    created_date=datetime.fromisoformat(
                        "2019-09-16T21:01:24+00:00"
                    ),
                    finding_id="436992569",
                    group_name="unittesting",
                    hacker_email="unittest@fluidattacks.com",
                    id="987a6d71-d23c-40db-ad98-bfccf60660ed",
                    state=VulnerabilityState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2019-09-16T21:01:24+00:00"
                        ),
                        source=Source.ASM,
                        specific="888",
                        status=VulnerabilityStateStatus.VULNERABLE,
                        where="192.168.100.122",
                        commit=None,
                        reasons=None,
                        other_reason=None,
                        tool=None,
                        snippet=None,
                    ),
                    type=VulnerabilityType.PORTS,
                    bug_tracking_system_url=None,
                    custom_severity=None,
                    developer=None,
                    event_id=None,
                    hash=None,
                    root_id=None,
                    skims_method=None,
                    skims_technique=None,
                    stream=None,
                    tags=None,
                    treatment=VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2019-09-16T21:01:24+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.UNTREATED,
                        acceptance_status=None,
                        accepted_until=None,
                        justification=None,
                        assigned=None,
                        modified_by=None,
                    ),
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_closing_date=None,
                        unreliable_source=Source.ASM,
                        unreliable_efficacy=Decimal("0"),
                        unreliable_last_reattack_date=None,
                        unreliable_last_reattack_requester=None,
                        unreliable_last_requested_reattack_date=None,
                        unreliable_reattack_cycles=0,
                        unreliable_treatment_changes=0,
                    ),
                    verification=None,
                    zero_risk=None,
                ),
                Vulnerability(
                    created_by="unittest@fluidattacks.com",
                    created_date=datetime.fromisoformat(
                        "2019-09-12T13:45:48+00:00"
                    ),
                    finding_id="436992569",
                    group_name="unittesting",
                    hacker_email="unittest@fluidattacks.com",
                    id="aa6a9d70-618b-4ab0-b280-d627ce311200",
                    state=VulnerabilityState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2019-09-12T13:45:48+00:00"
                        ),
                        source=Source.ASM,
                        specific="6666",
                        status=VulnerabilityStateStatus.VULNERABLE,
                        where="192.168.1.7",
                        commit=None,
                        reasons=None,
                        other_reason=None,
                        tool=None,
                        snippet=None,
                    ),
                    type=VulnerabilityType.PORTS,
                    bug_tracking_system_url=None,
                    custom_severity=None,
                    developer=None,
                    event_id=None,
                    hash=None,
                    root_id=None,
                    skims_method=None,
                    skims_technique=None,
                    stream=None,
                    tags=None,
                    treatment=VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2019-09-12T13:45:48+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.UNTREATED,
                        acceptance_status=None,
                        accepted_until=None,
                        justification=None,
                        assigned=None,
                        modified_by=None,
                    ),
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_closing_date=None,
                        unreliable_source=Source.ASM,
                        unreliable_efficacy=Decimal("0"),
                        unreliable_last_reattack_date=None,
                        unreliable_last_reattack_requester=None,
                        unreliable_last_requested_reattack_date=None,
                        unreliable_reattack_cycles=0,
                        unreliable_treatment_changes=0,
                    ),
                    verification=None,
                    zero_risk=None,
                ),
                Vulnerability(
                    created_by="unittest@fluidattacks.com",
                    created_date=datetime.fromisoformat(
                        "2019-09-12T13:45:48+00:00"
                    ),
                    finding_id="436992569",
                    group_name="unittesting",
                    hacker_email="unittest@fluidattacks.com",
                    id="ab25380d-dfe1-4cde-aefd-acca6990d6aa",
                    state=VulnerabilityState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2019-09-12T13:45:48+00:00"
                        ),
                        source=Source.ASM,
                        specific="1111",
                        status=VulnerabilityStateStatus.VULNERABLE,
                        where="192.168.1.2",
                        commit=None,
                        reasons=None,
                        other_reason=None,
                        tool=None,
                        snippet=None,
                    ),
                    type=VulnerabilityType.PORTS,
                    bug_tracking_system_url=None,
                    custom_severity=None,
                    developer=None,
                    event_id=None,
                    hash=None,
                    root_id=None,
                    skims_method=None,
                    skims_technique=None,
                    stream=None,
                    tags=None,
                    treatment=VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2019-09-12T13:45:48+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.UNTREATED,
                        acceptance_status=None,
                        accepted_until=None,
                        justification=None,
                        assigned=None,
                        modified_by=None,
                    ),
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_closing_date=None,
                        unreliable_source=Source.ASM,
                        unreliable_efficacy=Decimal("0"),
                        unreliable_last_reattack_date=None,
                        unreliable_last_reattack_requester=None,
                        unreliable_last_requested_reattack_date=None,
                        unreliable_reattack_cycles=0,
                        unreliable_treatment_changes=0,
                    ),
                    verification=None,
                    zero_risk=None,
                ),
                Vulnerability(
                    created_by="unittest@fluidattacks.com",
                    created_date=datetime.fromisoformat(
                        "2019-09-12T13:45:48+00:00"
                    ),
                    finding_id="436992569",
                    group_name="unittesting",
                    hacker_email="unittest@fluidattacks.com",
                    id="ae16f325-a492-482b-a7a1-6285e8057480",
                    state=VulnerabilityState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2019-09-12T13:45:48+00:00"
                        ),
                        source=Source.ASM,
                        specific="2222",
                        status=VulnerabilityStateStatus.VULNERABLE,
                        where="192.168.1.3",
                        commit=None,
                        reasons=None,
                        other_reason=None,
                        tool=None,
                        snippet=None,
                    ),
                    type=VulnerabilityType.PORTS,
                    bug_tracking_system_url=None,
                    custom_severity=None,
                    developer=None,
                    event_id=None,
                    hash=None,
                    root_id=None,
                    skims_method=None,
                    skims_technique=None,
                    stream=None,
                    tags=None,
                    treatment=VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2019-09-12T13:45:48+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.UNTREATED,
                        acceptance_status=None,
                        accepted_until=None,
                        justification=None,
                        assigned=None,
                        modified_by=None,
                    ),
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_closing_date=None,
                        unreliable_source=Source.ASM,
                        unreliable_efficacy=Decimal("0"),
                        unreliable_last_reattack_date=None,
                        unreliable_last_reattack_requester=None,
                        unreliable_last_requested_reattack_date=None,
                        unreliable_reattack_cycles=0,
                        unreliable_treatment_changes=0,
                    ),
                    verification=None,
                    zero_risk=None,
                ),
                Vulnerability(
                    created_by="unittest@fluidattacks.com",
                    created_date=datetime.fromisoformat(
                        "2019-09-12T13:45:48+00:00"
                    ),
                    finding_id="436992569",
                    group_name="unittesting",
                    hacker_email="unittest@fluidattacks.com",
                    id="b16ed89e-668d-42d6-add1-73535bb0e083",
                    state=VulnerabilityState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2019-09-12T13:45:48+00:00"
                        ),
                        source=Source.ASM,
                        specific="2222",
                        status=VulnerabilityStateStatus.VULNERABLE,
                        where="192.168.1.13",
                        commit=None,
                        reasons=None,
                        other_reason=None,
                        tool=None,
                        snippet=None,
                    ),
                    type=VulnerabilityType.PORTS,
                    bug_tracking_system_url=None,
                    custom_severity=None,
                    developer=None,
                    event_id=None,
                    hash=None,
                    root_id=None,
                    skims_method=None,
                    skims_technique=None,
                    stream=None,
                    tags=None,
                    treatment=VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2019-09-12T13:45:48+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.UNTREATED,
                        acceptance_status=None,
                        accepted_until=None,
                        justification=None,
                        assigned=None,
                        modified_by=None,
                    ),
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_closing_date=None,
                        unreliable_source=Source.ASM,
                        unreliable_efficacy=Decimal("0"),
                        unreliable_last_reattack_date=None,
                        unreliable_last_reattack_requester=None,
                        unreliable_last_requested_reattack_date=None,
                        unreliable_reattack_cycles=0,
                        unreliable_treatment_changes=0,
                    ),
                    verification=None,
                    zero_risk=None,
                ),
                Vulnerability(
                    created_by="unittest@fluidattacks.com",
                    created_date=datetime.fromisoformat(
                        "2019-09-12T13:45:48+00:00"
                    ),
                    finding_id="436992569",
                    group_name="unittesting",
                    hacker_email="unittest@fluidattacks.com",
                    id="bac162ff-5c2a-4a96-9b77-fd7020976160",
                    state=VulnerabilityState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2019-09-12T13:45:48+00:00"
                        ),
                        source=Source.ASM,
                        specific="7777",
                        status=VulnerabilityStateStatus.VULNERABLE,
                        where="192.168.1.8",
                        commit=None,
                        reasons=None,
                        other_reason=None,
                        tool=None,
                        snippet=None,
                    ),
                    type=VulnerabilityType.PORTS,
                    bug_tracking_system_url=None,
                    custom_severity=None,
                    developer=None,
                    event_id=None,
                    hash=None,
                    root_id=None,
                    skims_method=None,
                    skims_technique=None,
                    stream=None,
                    tags=None,
                    treatment=VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2019-09-12T13:45:48+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.UNTREATED,
                        acceptance_status=None,
                        accepted_until=None,
                        justification=None,
                        assigned=None,
                        modified_by=None,
                    ),
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_closing_date=None,
                        unreliable_source=Source.ASM,
                        unreliable_efficacy=Decimal("0"),
                        unreliable_last_reattack_date=None,
                        unreliable_last_reattack_requester=None,
                        unreliable_last_requested_reattack_date=None,
                        unreliable_reattack_cycles=0,
                        unreliable_treatment_changes=0,
                    ),
                    verification=None,
                    zero_risk=None,
                ),
                Vulnerability(
                    created_by="unittest@fluidattacks.com",
                    created_date=datetime.fromisoformat(
                        "2019-09-13T15:53:05+00:00"
                    ),
                    finding_id="436992569",
                    group_name="unittesting",
                    hacker_email="unittest@fluidattacks.com",
                    id="bf818399-b331-4fa4-b335-98548e037378",
                    state=VulnerabilityState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2019-09-13T16:28:20+00:00"
                        ),
                        source=Source.ASM,
                        specific="333",
                        status=VulnerabilityStateStatus.SAFE,
                        where="192.168.100.109",
                        commit=None,
                        reasons=None,
                        other_reason=None,
                        tool=None,
                        snippet=None,
                    ),
                    type=VulnerabilityType.PORTS,
                    bug_tracking_system_url=None,
                    custom_severity=None,
                    developer=None,
                    event_id=None,
                    hash=None,
                    root_id=None,
                    skims_method=None,
                    skims_technique=None,
                    stream=None,
                    tags=None,
                    treatment=VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2019-09-13T15:53:05+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.UNTREATED,
                        acceptance_status=None,
                        accepted_until=None,
                        justification=None,
                        assigned=None,
                        modified_by=None,
                    ),
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_closing_date=datetime.fromisoformat(
                            "2019-09-13T16:28:20+00:00"
                        ),
                        unreliable_source=Source.ASM,
                        unreliable_efficacy=Decimal("0"),
                        unreliable_last_reattack_date=None,
                        unreliable_last_reattack_requester=None,
                        unreliable_last_requested_reattack_date=None,
                        unreliable_reattack_cycles=0,
                        unreliable_treatment_changes=0,
                    ),
                    verification=None,
                    zero_risk=None,
                ),
                Vulnerability(
                    created_by="unittest@fluidattacks.com",
                    created_date=datetime.fromisoformat(
                        "2019-09-12T13:45:48+00:00"
                    ),
                    finding_id="436992569",
                    group_name="unittesting",
                    hacker_email="unittest@fluidattacks.com",
                    id="c8161719-5ac8-45ba-a3fb-ab69ea39ddcb",
                    state=VulnerabilityState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2019-09-12T13:45:48+00:00"
                        ),
                        source=Source.ASM,
                        specific="5555",
                        status=VulnerabilityStateStatus.VULNERABLE,
                        where="192.168.1.16",
                        commit=None,
                        reasons=None,
                        other_reason=None,
                        tool=None,
                        snippet=None,
                    ),
                    type=VulnerabilityType.PORTS,
                    bug_tracking_system_url=None,
                    custom_severity=None,
                    developer=None,
                    event_id=None,
                    hash=None,
                    root_id=None,
                    skims_method=None,
                    skims_technique=None,
                    stream=None,
                    tags=None,
                    treatment=VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2019-09-12T13:45:48+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.UNTREATED,
                        acceptance_status=None,
                        accepted_until=None,
                        justification=None,
                        assigned=None,
                        modified_by=None,
                    ),
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_closing_date=None,
                        unreliable_source=Source.ASM,
                        unreliable_efficacy=Decimal("0"),
                        unreliable_last_reattack_date=None,
                        unreliable_last_reattack_requester=None,
                        unreliable_last_requested_reattack_date=None,
                        unreliable_reattack_cycles=0,
                        unreliable_treatment_changes=0,
                    ),
                    verification=None,
                    zero_risk=None,
                ),
                Vulnerability(
                    created_by="unittest@fluidattacks.com",
                    created_date=datetime.fromisoformat(
                        "2019-09-12T13:45:48+00:00"
                    ),
                    finding_id="436992569",
                    group_name="unittesting",
                    hacker_email="unittest@fluidattacks.com",
                    id="d212a841-7d48-4cb6-b776-cccc2845c383",
                    state=VulnerabilityState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2019-09-12T13:45:48+00:00"
                        ),
                        source=Source.ASM,
                        specific="3333",
                        status=VulnerabilityStateStatus.VULNERABLE,
                        where="192.168.1.14",
                        commit=None,
                        reasons=None,
                        other_reason=None,
                        tool=None,
                        snippet=None,
                    ),
                    type=VulnerabilityType.PORTS,
                    bug_tracking_system_url=None,
                    custom_severity=None,
                    developer=None,
                    event_id=None,
                    hash=None,
                    root_id=None,
                    skims_method=None,
                    skims_technique=None,
                    stream=None,
                    tags=None,
                    treatment=VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2019-09-12T13:45:48+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.UNTREATED,
                        acceptance_status=None,
                        accepted_until=None,
                        justification=None,
                        assigned=None,
                        modified_by=None,
                    ),
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_closing_date=None,
                        unreliable_source=Source.ASM,
                        unreliable_efficacy=Decimal("0"),
                        unreliable_last_reattack_date=None,
                        unreliable_last_reattack_requester=None,
                        unreliable_last_requested_reattack_date=None,
                        unreliable_reattack_cycles=0,
                        unreliable_treatment_changes=0,
                    ),
                    verification=None,
                    zero_risk=None,
                ),
                Vulnerability(
                    created_by="unittest@fluidattacks.com",
                    created_date=datetime.fromisoformat(
                        "2019-09-13T20:19:17+00:00"
                    ),
                    finding_id="436992569",
                    group_name="unittesting",
                    hacker_email="unittest@fluidattacks.com",
                    id="d4d4c6a0-3d51-42cf-b93f-4c503f67d72d",
                    state=VulnerabilityState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2019-09-13T20:19:17+00:00"
                        ),
                        source=Source.ASM,
                        specific="333",
                        status=VulnerabilityStateStatus.VULNERABLE,
                        where="192.168.100.108",
                        commit=None,
                        reasons=None,
                        other_reason=None,
                        tool=None,
                        snippet=None,
                    ),
                    type=VulnerabilityType.PORTS,
                    bug_tracking_system_url=None,
                    custom_severity=None,
                    developer=None,
                    event_id=None,
                    hash=None,
                    root_id=None,
                    skims_method=None,
                    skims_technique=None,
                    stream=None,
                    tags=None,
                    treatment=VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2019-09-13T20:19:17+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.UNTREATED,
                        acceptance_status=None,
                        accepted_until=None,
                        justification=None,
                        assigned=None,
                        modified_by=None,
                    ),
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_closing_date=None,
                        unreliable_source=Source.ASM,
                        unreliable_efficacy=Decimal("0"),
                        unreliable_last_reattack_date=None,
                        unreliable_last_reattack_requester=None,
                        unreliable_last_requested_reattack_date=None,
                        unreliable_reattack_cycles=0,
                        unreliable_treatment_changes=0,
                    ),
                    verification=None,
                    zero_risk=None,
                ),
                Vulnerability(
                    created_by="unittest@fluidattacks.com",
                    created_date=datetime.fromisoformat(
                        "2019-08-30T14:30:13+00:00"
                    ),
                    finding_id="436992569",
                    group_name="unittesting",
                    hacker_email="unittest@fluidattacks.com",
                    id="f2d577b4-855b-41fc-a844-2b96f797775c",
                    state=VulnerabilityState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2019-08-30T14:30:13+00:00"
                        ),
                        source=Source.ASM,
                        specific="asserts",
                        status=VulnerabilityStateStatus.VULNERABLE,
                        where="testing",
                        commit=None,
                        reasons=None,
                        other_reason=None,
                        tool=None,
                        snippet=None,
                    ),
                    type=VulnerabilityType.INPUTS,
                    bug_tracking_system_url=None,
                    custom_severity=None,
                    developer=None,
                    event_id=None,
                    hash=None,
                    root_id=None,
                    skims_method=None,
                    skims_technique=None,
                    stream=None,
                    tags=None,
                    treatment=VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2019-08-30T14:30:13+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.UNTREATED,
                        acceptance_status=None,
                        accepted_until=None,
                        justification=None,
                        assigned=None,
                        modified_by=None,
                    ),
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_closing_date=None,
                        unreliable_source=Source.ASM,
                        unreliable_efficacy=Decimal("0"),
                        unreliable_last_reattack_date=None,
                        unreliable_last_reattack_requester=None,
                        unreliable_last_requested_reattack_date=None,
                        unreliable_reattack_cycles=0,
                        unreliable_treatment_changes=0,
                    ),
                    verification=None,
                    zero_risk=None,
                ),
                Vulnerability(
                    created_by="unittest@fluidattacks.com",
                    created_date=datetime.fromisoformat(
                        "2019-09-16T20:02:17+00:00"
                    ),
                    finding_id="436992569",
                    group_name="unittesting",
                    hacker_email="unittest@fluidattacks.com",
                    id="fc01759b-0f2f-4e4e-9e24-5c27c91d574b",
                    state=VulnerabilityState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2019-09-16T20:02:17+00:00"
                        ),
                        source=Source.ASM,
                        specific="1111",
                        status=VulnerabilityStateStatus.VULNERABLE,
                        where="192.168.100.113",
                        commit=None,
                        reasons=None,
                        other_reason=None,
                        tool=None,
                        snippet=None,
                    ),
                    type=VulnerabilityType.PORTS,
                    bug_tracking_system_url=None,
                    custom_severity=None,
                    developer=None,
                    event_id=None,
                    hash=None,
                    root_id=None,
                    skims_method=None,
                    skims_technique=None,
                    stream=None,
                    tags=None,
                    treatment=VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2019-09-16T20:02:17+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.UNTREATED,
                        acceptance_status=None,
                        accepted_until=None,
                        justification=None,
                        assigned=None,
                        modified_by=None,
                    ),
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_closing_date=None,
                        unreliable_source=Source.ASM,
                        unreliable_efficacy=Decimal("0"),
                        unreliable_last_reattack_date=None,
                        unreliable_last_reattack_requester=None,
                        unreliable_last_requested_reattack_date=None,
                        unreliable_reattack_cycles=0,
                        unreliable_treatment_changes=0,
                    ),
                    verification=None,
                    zero_risk=None,
                ),
                Vulnerability(
                    created_by="integratesmanager@gmail.com",
                    created_date=datetime.fromisoformat(
                        "2019-09-13T14:03:05+00:00"
                    ),
                    finding_id="436992569",
                    group_name="unittesting",
                    hacker_email="integratesmanager@gmail.com",
                    id="feabfd52-0b0f-405e-bf6a-e9a224af6726",
                    state=VulnerabilityState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2019-09-13T14:03:05+00:00"
                        ),
                        source=Source.ASM,
                        specific="333",
                        status=VulnerabilityStateStatus.SAFE,
                        where="192.168.100.103",
                        commit=None,
                        reasons=None,
                        other_reason=None,
                        tool=None,
                        snippet=None,
                    ),
                    type=VulnerabilityType.PORTS,
                    bug_tracking_system_url=None,
                    custom_severity=None,
                    developer=None,
                    event_id=None,
                    hash=None,
                    root_id=None,
                    skims_method=None,
                    skims_technique=None,
                    stream=None,
                    tags=None,
                    treatment=VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2019-09-13T14:03:05+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.UNTREATED,
                        acceptance_status=None,
                        accepted_until=None,
                        justification=None,
                        assigned=None,
                        modified_by=None,
                    ),
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_closing_date=datetime.fromisoformat(
                            "2019-09-13T14:03:05+00:00"
                        ),
                        unreliable_source=Source.ASM,
                        unreliable_efficacy=Decimal("0"),
                        unreliable_last_reattack_date=None,
                        unreliable_last_reattack_requester=None,
                        unreliable_last_requested_reattack_date=None,
                        unreliable_reattack_cycles=0,
                        unreliable_treatment_changes=0,
                    ),
                    verification=None,
                    zero_risk=None,
                ),
                Vulnerability(
                    created_by="unittest@fluidattacks.com",
                    created_date=datetime.fromisoformat(
                        "2018-11-27T19:54:08+00:00"
                    ),
                    finding_id="457497316",
                    group_name="unittesting",
                    hacker_email="unittest@fluidattacks.com",
                    id="6192c72f-2e10-4259-9207-717b2d90d8d2",
                    state=VulnerabilityState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2019-09-16T14:40:37+00:00"
                        ),
                        source=Source.ASM,
                        specific="userToken",
                        status=VulnerabilityStateStatus.SAFE,
                        where="https://10.1.1.1/",
                        commit=None,
                        reasons=None,
                        other_reason=None,
                        tool=None,
                        snippet=None,
                    ),
                    type=VulnerabilityType.INPUTS,
                    bug_tracking_system_url=None,
                    custom_severity=None,
                    developer=None,
                    event_id=None,
                    hash=None,
                    root_id=None,
                    skims_method=None,
                    skims_technique=None,
                    stream=None,
                    tags=None,
                    treatment=VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2018-11-27T19:54:08+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.UNTREATED,
                        acceptance_status=None,
                        accepted_until=None,
                        justification=None,
                        assigned=None,
                        modified_by=None,
                    ),
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_closing_date=datetime.fromisoformat(
                            "2019-09-16T14:40:37+00:00"
                        ),
                        unreliable_source=Source.ASM,
                        unreliable_efficacy=Decimal("0"),
                        unreliable_last_reattack_date=None,
                        unreliable_last_reattack_requester=None,
                        unreliable_last_requested_reattack_date=None,
                        unreliable_reattack_cycles=0,
                        unreliable_treatment_changes=0,
                    ),
                    verification=None,
                    zero_risk=None,
                ),
                Vulnerability(
                    created_by="unittest@fluidattacks.com",
                    created_date=datetime.fromisoformat(
                        "2019-09-13T14:58:38+00:00"
                    ),
                    finding_id="463461507",
                    group_name="unittesting",
                    hacker_email="unittest@fluidattacks.com",
                    id="09afd608-aa53-4bbc-9094-0076181fa0ea",
                    state=VulnerabilityState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2019-09-13T14:58:38+00:00"
                        ),
                        source=Source.ASM,
                        specific="3636",
                        status=VulnerabilityStateStatus.VULNERABLE,
                        where="192.168.100.105",
                        commit=None,
                        reasons=None,
                        other_reason=None,
                        tool=None,
                        snippet=None,
                    ),
                    type=VulnerabilityType.PORTS,
                    bug_tracking_system_url=None,
                    custom_severity=None,
                    developer=None,
                    event_id=None,
                    hash=None,
                    root_id=None,
                    skims_method=None,
                    skims_technique=None,
                    stream=None,
                    tags=None,
                    treatment=VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2019-09-13T14:58:38+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.UNTREATED,
                        acceptance_status=None,
                        accepted_until=None,
                        justification=None,
                        assigned=None,
                        modified_by=None,
                    ),
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_closing_date=None,
                        unreliable_source=Source.ASM,
                        unreliable_efficacy=Decimal("0"),
                        unreliable_last_reattack_date=None,
                        unreliable_last_reattack_requester=None,
                        unreliable_last_requested_reattack_date=None,
                        unreliable_reattack_cycles=0,
                        unreliable_treatment_changes=0,
                    ),
                    verification=None,
                    zero_risk=None,
                ),
                Vulnerability(
                    created_by="unittest@fluidattacks.com",
                    created_date=datetime.fromisoformat(
                        "2019-09-12T13:45:48+00:00"
                    ),
                    finding_id="463461507",
                    group_name="unittesting",
                    hacker_email="unittest@fluidattacks.com",
                    id="e248e8e0-0323-41c7-bc02-4ee61d09f9c4",
                    state=VulnerabilityState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2019-09-12T13:45:48+00:00"
                        ),
                        source=Source.ASM,
                        specific="7777",
                        status=VulnerabilityStateStatus.VULNERABLE,
                        where="192.168.1.18",
                        commit=None,
                        reasons=None,
                        other_reason=None,
                        tool=None,
                        snippet=None,
                    ),
                    type=VulnerabilityType.PORTS,
                    bug_tracking_system_url=None,
                    custom_severity=None,
                    developer=None,
                    event_id=None,
                    hash=None,
                    root_id=None,
                    skims_method=None,
                    skims_technique=None,
                    stream=None,
                    tags=None,
                    treatment=VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2019-09-13T13:45:48+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.ACCEPTED,
                        acceptance_status=None,
                        accepted_until=datetime.fromisoformat(
                            "2021-01-16T17:46:10+00:00"
                        ),
                        justification="accepted justification",
                        assigned="integratesuser@gmail.com",
                        modified_by="integratesuser@gmail.com",
                    ),
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_closing_date=None,
                        unreliable_source=Source.ASM,
                        unreliable_efficacy=Decimal("0"),
                        unreliable_last_reattack_date=None,
                        unreliable_last_reattack_requester=None,
                        unreliable_last_requested_reattack_date=None,
                        unreliable_reattack_cycles=0,
                        unreliable_treatment_changes=2,
                    ),
                    verification=None,
                    zero_risk=None,
                ),
                Vulnerability(
                    created_by="unittest@fluidattacks.com",
                    created_date=datetime.fromisoformat(
                        "2019-01-15T15:43:39+00:00"
                    ),
                    finding_id="463558592",
                    group_name="unittesting",
                    hacker_email="unittest@fluidattacks.com",
                    id="0a848781-b6a4-422e-95fa-692151e6a98e",
                    state=VulnerabilityState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2019-01-15T15:43:39+00:00"
                        ),
                        source=Source.ASM,
                        specific="12",
                        status=VulnerabilityStateStatus.VULNERABLE,
                        where="path/to/file2.ext",
                        commit=None,
                        reasons=None,
                        other_reason=None,
                        tool=None,
                        snippet=None,
                    ),
                    type=VulnerabilityType.LINES,
                    bug_tracking_system_url=None,
                    custom_severity=None,
                    developer=None,
                    event_id=None,
                    hash=None,
                    root_id=None,
                    skims_method=None,
                    skims_technique=None,
                    stream=None,
                    tags=None,
                    treatment=VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2019-01-15T15:43:39+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.ACCEPTED,
                        acceptance_status=None,
                        accepted_until=datetime.fromisoformat(
                            "2021-01-16T17:46:10+00:00"
                        ),
                        justification="This is a treatment justification test",
                        assigned="integratesuser@gmail.com",
                        modified_by="integratesuser@gmail.com",
                    ),
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_closing_date=None,
                        unreliable_source=Source.ASM,
                        unreliable_efficacy=Decimal("0"),
                        unreliable_last_reattack_date=None,
                        unreliable_last_reattack_requester=None,
                        unreliable_last_requested_reattack_date=None,
                        unreliable_reattack_cycles=0,
                        unreliable_treatment_changes=1,
                    ),
                    verification=None,
                    zero_risk=None,
                ),
                Vulnerability(
                    created_by="unittest@fluidattacks.com",
                    created_date=datetime.fromisoformat(
                        "2019-01-15T16:04:14+00:00"
                    ),
                    finding_id="463558592",
                    group_name="unittesting",
                    hacker_email="unittest@fluidattacks.com",
                    id="242f848c-148a-4028-8e36-c7d995502590",
                    state=VulnerabilityState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2019-01-15T20:59:16+00:00"
                        ),
                        source=Source.ASM,
                        specific="12456",
                        status=VulnerabilityStateStatus.SAFE,
                        where="path/to/file2.ext",
                        commit=None,
                        reasons=None,
                        other_reason=None,
                        tool=None,
                        snippet=None,
                    ),
                    type=VulnerabilityType.LINES,
                    bug_tracking_system_url=None,
                    custom_severity=None,
                    developer=None,
                    event_id=None,
                    hash=None,
                    root_id=None,
                    skims_method=None,
                    skims_technique=None,
                    stream=None,
                    tags=None,
                    treatment=VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2019-01-15T16:04:14+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.UNTREATED,
                        acceptance_status=None,
                        accepted_until=None,
                        justification=None,
                        assigned=None,
                        modified_by=None,
                    ),
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_closing_date=datetime.fromisoformat(
                            "2019-01-15T20:59:16+00:00"
                        ),
                        unreliable_source=Source.ASM,
                        unreliable_efficacy=Decimal("0"),
                        unreliable_last_reattack_date=None,
                        unreliable_last_reattack_requester=None,
                        unreliable_last_requested_reattack_date=None,
                        unreliable_reattack_cycles=0,
                        unreliable_treatment_changes=0,
                    ),
                    verification=None,
                    zero_risk=None,
                ),
                Vulnerability(
                    created_by="unittest@fluidattacks.com",
                    created_date=datetime.fromisoformat(
                        "2019-01-16T13:47:07+00:00"
                    ),
                    finding_id="463558592",
                    group_name="unittesting",
                    hacker_email="unittest@fluidattacks.com",
                    id="3bcdb384-5547-4170-a0b6-3b397a245465",
                    state=VulnerabilityState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2019-01-16T13:47:07+00:00"
                        ),
                        source=Source.ASM,
                        specific="345",
                        status=VulnerabilityStateStatus.VULNERABLE,
                        where="path/to/file3.ext",
                        commit=None,
                        reasons=None,
                        other_reason=None,
                        tool=None,
                        snippet=None,
                    ),
                    type=VulnerabilityType.LINES,
                    bug_tracking_system_url=None,
                    custom_severity=None,
                    developer=None,
                    event_id=None,
                    hash=None,
                    root_id="4039d098-ffc5-4984-8ed3-eb17bca98e19",
                    skims_method=None,
                    skims_technique=None,
                    stream=None,
                    tags=None,
                    treatment=VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2019-01-16T13:47:07+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.UNTREATED,
                        acceptance_status=None,
                        accepted_until=None,
                        justification=None,
                        assigned=None,
                        modified_by=None,
                    ),
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_closing_date=None,
                        unreliable_source=Source.ASM,
                        unreliable_efficacy=Decimal("0"),
                        unreliable_last_reattack_date=None,
                        unreliable_last_reattack_requester="integratesuser@gmail.com",  # noqa: E501 pylint: disable=line-too-long
                        unreliable_last_requested_reattack_date=datetime.fromisoformat(  # noqa: E501 pylint: disable=line-too-long
                            "2020-02-19T15:41:04+00:00"
                        ),
                        unreliable_reattack_cycles=1,
                        unreliable_treatment_changes=0,
                    ),
                    verification=VulnerabilityVerification(
                        modified_date=datetime.fromisoformat(
                            "2020-02-19T15:41:04+00:00"
                        ),
                        status=VulnerabilityVerificationStatus.REQUESTED,
                        event_id=None,
                    ),
                    zero_risk=VulnerabilityZeroRisk(
                        comment_id="123456",
                        modified_by="test@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2018-09-28T15:32:58+00:00"
                        ),
                        status=VulnerabilityZeroRiskStatus.REQUESTED,
                    ),
                ),
                Vulnerability(
                    created_by="unittest@fluidattacks.com",
                    created_date=datetime.fromisoformat(
                        "2019-01-16T13:47:07+00:00"
                    ),
                    finding_id="463558592",
                    group_name="unittesting",
                    hacker_email="unittest@fluidattacks.com",
                    id="54b94fa0-8f4f-4b10-a38a-6e848a9eb0c6",
                    state=VulnerabilityState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2019-01-16T13:47:07+00:00"
                        ),
                        source=Source.ASM,
                        specific="564",
                        status=VulnerabilityStateStatus.VULNERABLE,
                        where="path/to/file4.ext",
                        commit=None,
                        reasons=None,
                        other_reason=None,
                        tool=None,
                        snippet=None,
                    ),
                    type=VulnerabilityType.LINES,
                    bug_tracking_system_url=None,
                    custom_severity=None,
                    developer=None,
                    event_id=None,
                    hash=None,
                    root_id=None,
                    skims_method=None,
                    skims_technique=None,
                    stream=None,
                    tags=["test1", "test2"],
                    treatment=VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2020-10-13T17:46:10+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.ACCEPTED,
                        acceptance_status=None,
                        accepted_until=datetime.fromisoformat(
                            "2021-01-16T17:46:10+00:00"
                        ),
                        justification="This is a treatment justification test",
                        assigned="integratesuser@gmail.com",
                        modified_by="integratesuser@gmail.com",
                    ),
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_closing_date=None,
                        unreliable_source=Source.ASM,
                        unreliable_efficacy=Decimal("0"),
                        unreliable_last_reattack_date=None,
                        unreliable_last_reattack_requester=None,
                        unreliable_last_requested_reattack_date=None,
                        unreliable_reattack_cycles=0,
                        unreliable_treatment_changes=1,
                    ),
                    verification=None,
                    zero_risk=VulnerabilityZeroRisk(
                        comment_id="123456",
                        modified_by="test@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2018-09-28T15:32:58+00:00"
                        ),
                        status=VulnerabilityZeroRiskStatus.REQUESTED,
                    ),
                ),
                Vulnerability(
                    created_by="unittest@fluidattacks.com",
                    created_date=datetime.fromisoformat(
                        "2019-01-15T16:04:14+00:00"
                    ),
                    finding_id="463558592",
                    group_name="unittesting",
                    hacker_email="unittest@fluidattacks.com",
                    id="6f023c26-5b10-4ded-aa27-bb563c2206ab",
                    state=VulnerabilityState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2019-01-15T20:59:16+00:00"
                        ),
                        source=Source.ASM,
                        specific="123345",
                        status=VulnerabilityStateStatus.SAFE,
                        where="test/test#.config",
                        commit=None,
                        reasons=None,
                        other_reason=None,
                        tool=None,
                        snippet=None,
                    ),
                    type=VulnerabilityType.LINES,
                    bug_tracking_system_url=None,
                    custom_severity=None,
                    developer=None,
                    event_id=None,
                    hash=None,
                    root_id="4039d098-ffc5-4984-8ed3-eb17bca98e19",
                    skims_method=None,
                    skims_technique=None,
                    stream=None,
                    tags=None,
                    treatment=VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2020-10-13T17:46:10+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.ACCEPTED,
                        acceptance_status=None,
                        accepted_until=datetime.fromisoformat(
                            "2021-01-16T17:46:10+00:00"
                        ),
                        justification="This is a treatment justification test",
                        assigned="integratesuser@gmail.com",
                        modified_by="integratesuser@gmail.com",
                    ),
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_closing_date=datetime.fromisoformat(
                            "2019-01-15T20:59:16+00:00"
                        ),
                        unreliable_source=Source.ASM,
                        unreliable_efficacy=Decimal("0"),
                        unreliable_last_reattack_date=None,
                        unreliable_last_reattack_requester=None,
                        unreliable_last_requested_reattack_date=None,
                        unreliable_reattack_cycles=0,
                        unreliable_treatment_changes=1,
                    ),
                    verification=None,
                    zero_risk=VulnerabilityZeroRisk(
                        comment_id="123456",
                        modified_by="test@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2018-09-28T15:32:58+00:00"
                        ),
                        status=VulnerabilityZeroRiskStatus.REQUESTED,
                    ),
                ),
                Vulnerability(
                    created_by="unittest@fluidattacks.com",
                    created_date=datetime.fromisoformat(
                        "2019-01-15T15:43:39+00:00"
                    ),
                    finding_id="463558592",
                    group_name="unittesting",
                    hacker_email="unittest@fluidattacks.com",
                    id="74632c0c-db08-47c2-b013-c70e5b67c49f",
                    state=VulnerabilityState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2019-01-15T15:43:39+00:00"
                        ),
                        source=Source.ASM,
                        specific="123",
                        status=VulnerabilityStateStatus.VULNERABLE,
                        where="test/test#.config",
                        commit=None,
                        reasons=None,
                        other_reason=None,
                        tool=None,
                        snippet=None,
                    ),
                    type=VulnerabilityType.LINES,
                    bug_tracking_system_url=None,
                    custom_severity=None,
                    developer=None,
                    event_id=None,
                    hash=None,
                    root_id="4039d098-ffc5-4984-8ed3-eb17bca98e19",
                    skims_method=None,
                    skims_technique=None,
                    stream=None,
                    tags=None,
                    treatment=VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2020-10-13T17:46:10+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.ACCEPTED,
                        acceptance_status=None,
                        accepted_until=datetime.fromisoformat(
                            "2021-01-16T17:46:10+00:00"
                        ),
                        justification="This is a treatment justification test",
                        assigned="integratesuser2@gmail.com",
                        modified_by="integratesuser2@gmail.com",
                    ),
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_closing_date=None,
                        unreliable_source=Source.ASM,
                        unreliable_efficacy=Decimal("0"),
                        unreliable_last_reattack_date=None,
                        unreliable_last_reattack_requester="integratesuser@gmail.com",  # noqa: E501 pylint: disable=line-too-long
                        unreliable_last_requested_reattack_date=datetime.fromisoformat(  # noqa: E501 pylint: disable=line-too-long
                            "2020-02-19T15:41:04+00:00"
                        ),
                        unreliable_reattack_cycles=1,
                        unreliable_treatment_changes=1,
                    ),
                    verification=VulnerabilityVerification(
                        modified_date=datetime.fromisoformat(
                            "2020-02-19T15:41:04+00:00"
                        ),
                        status=VulnerabilityVerificationStatus.REQUESTED,
                        event_id=None,
                    ),
                    zero_risk=VulnerabilityZeroRisk(
                        comment_id="123456",
                        modified_by="test@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2018-09-28T15:32:58+00:00"
                        ),
                        status=VulnerabilityZeroRiskStatus.REQUESTED,
                    ),
                ),
                Vulnerability(
                    created_by="unittest@fluidattacks.com",
                    created_date=datetime.fromisoformat(
                        "2019-04-08T00:45:15+00:00"
                    ),
                    finding_id="988493279",
                    group_name="unittesting",
                    hacker_email="unittest@fluidattacks.com",
                    id="47ce0fb0-4108-49b0-93cc-160dce8168a6",
                    state=VulnerabilityState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2019-04-08T00:45:15+00:00"
                        ),
                        source=Source.ASM,
                        specific="8888",
                        status=VulnerabilityStateStatus.VULNERABLE,
                        where="192.168.1.19",
                        commit=None,
                        reasons=None,
                        other_reason=None,
                        tool=VulnerabilityTool(
                            name="tool-1",
                            impact=VulnerabilityToolImpact.INDIRECT,
                        ),
                        snippet=None,
                    ),
                    type=VulnerabilityType.PORTS,
                    bug_tracking_system_url=None,
                    custom_severity=None,
                    developer=None,
                    event_id=None,
                    hash=None,
                    root_id="4039d098-ffc5-4984-8ed3-eb17bca98e19",
                    skims_method=None,
                    skims_technique=None,
                    stream=None,
                    tags=None,
                    treatment=VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2020-10-08T00:59:06+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.ACCEPTED_UNDEFINED,
                        acceptance_status=VulnerabilityAcceptanceStatus.APPROVED,  # noqa: E501 pylint: disable=line-too-long
                        accepted_until=None,
                        justification="Observations about permanently "
                        "accepted",
                        assigned="integratesuser@gmail.com",
                        modified_by="integratesuser@gmail.com",
                    ),
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_closing_date=None,
                        unreliable_source=Source.ASM,
                        unreliable_efficacy=Decimal("0"),
                        unreliable_last_reattack_date=None,
                        unreliable_last_reattack_requester=None,
                        unreliable_last_requested_reattack_date=None,
                        unreliable_reattack_cycles=0,
                        unreliable_treatment_changes=2,
                    ),
                    verification=None,
                    zero_risk=None,
                ),
                Vulnerability(
                    created_by="unittest@fluidattacks.com",
                    created_date=datetime.fromisoformat(
                        "2019-04-08T00:45:15+00:00"
                    ),
                    finding_id="988493279",
                    group_name="unittesting",
                    hacker_email="unittest@fluidattacks.com",
                    id="69b84d52-1b18-41fa-84b5-bcb8134cb1ec",
                    state=VulnerabilityState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2019-08-07T13:45:48+00:00"
                        ),
                        source=Source.ASM,
                        specific="9999",
                        status=VulnerabilityStateStatus.SAFE,
                        where="192.168.1.20",
                        commit=None,
                        reasons=None,
                        other_reason=None,
                        tool=VulnerabilityTool(
                            name="tool-1",
                            impact=VulnerabilityToolImpact.INDIRECT,
                        ),
                        snippet=None,
                    ),
                    type=VulnerabilityType.PORTS,
                    bug_tracking_system_url=None,
                    custom_severity=None,
                    developer=None,
                    event_id=None,
                    hash=None,
                    root_id=None,
                    skims_method=None,
                    skims_technique=None,
                    stream=None,
                    tags=None,
                    treatment=VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2020-11-08T00:59:06+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.ACCEPTED,
                        acceptance_status=None,
                        accepted_until=datetime.fromisoformat(
                            "2021-04-08T00:59:06+00:00"
                        ),
                        justification="test justification temporarily "
                        "accepted",
                        assigned="integratesuser2@gmail.com",
                        modified_by="integratesuser@gmail.com",
                    ),
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_closing_date=datetime.fromisoformat(
                            "2019-08-07T13:45:48+00:00"
                        ),
                        unreliable_source=Source.ASM,
                        unreliable_efficacy=Decimal("0"),
                        unreliable_last_reattack_date=None,
                        unreliable_last_reattack_requester=None,
                        unreliable_last_requested_reattack_date=None,
                        unreliable_reattack_cycles=0,
                        unreliable_treatment_changes=1,
                    ),
                    verification=None,
                    zero_risk=None,
                ),
            ]
        ),
        '["unittesting", "0.1", "3.9"]': tuple(
            [
                Vulnerability(
                    created_by="unittest@fluidattacks.com",
                    created_date=datetime.fromisoformat(
                        "2020-01-03T17:46:10+00:00"
                    ),
                    finding_id="422286126",
                    group_name="unittesting",
                    hacker_email="unittest@fluidattacks.com",
                    id="0a848781-b6a4-422e-95fa-692151e6a98z",
                    state=VulnerabilityState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2020-01-03T17:46:10+00:00"
                        ),
                        source=Source.ASM,
                        specific="12",
                        status=VulnerabilityStateStatus.VULNERABLE,
                        where="test/data/lib_path/f060/csharp.cs",
                        commit="ea871eee64cfd5ce293411efaf4d3b446d04eb4a",
                        reasons=None,
                        other_reason=None,
                        tool=VulnerabilityTool(
                            name="tool-2",
                            impact=VulnerabilityToolImpact.INDIRECT,
                        ),
                        snippet=None,
                    ),
                    type=VulnerabilityType.LINES,
                    bug_tracking_system_url=None,
                    custom_severity=None,
                    developer=None,
                    event_id=None,
                    hash=None,
                    root_id=None,
                    skims_method=None,
                    skims_technique=None,
                    stream=None,
                    tags=None,
                    treatment=VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2020-01-03T17:46:10+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.IN_PROGRESS,
                        acceptance_status=None,
                        accepted_until=None,
                        justification="test justification",
                        assigned="integratesuser2@gmail.com",
                        modified_by="integratesuser@gmail.com",
                    ),
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_closing_date=None,
                        unreliable_source=Source.ASM,
                        unreliable_efficacy=Decimal("0"),
                        unreliable_last_reattack_date=None,
                        unreliable_last_reattack_requester=None,
                        unreliable_last_requested_reattack_date=None,
                        unreliable_reattack_cycles=0,
                        unreliable_treatment_changes=1,
                    ),
                    verification=None,
                    zero_risk=None,
                ),
                Vulnerability(
                    created_by="test@unittesting.com",
                    created_date=datetime.fromisoformat(
                        "2020-09-09T21:01:26+00:00"
                    ),
                    finding_id="422286126",
                    group_name="unittesting",
                    hacker_email="test@unittesting.com",
                    id="80d6a69f-a376-46be-98cd-2fdedcffdcc0",
                    state=VulnerabilityState(
                        modified_by="test@unittesting.com",
                        modified_date=datetime.fromisoformat(
                            "2020-09-09T21:01:26+00:00"
                        ),
                        source=Source.ASM,
                        specific="phone",
                        status=VulnerabilityStateStatus.VULNERABLE,
                        where="https://example.com",
                        commit=None,
                        reasons=None,
                        other_reason=None,
                        tool=VulnerabilityTool(
                            name="tool-2",
                            impact=VulnerabilityToolImpact.INDIRECT,
                        ),
                        snippet=None,
                    ),
                    type=VulnerabilityType.INPUTS,
                    bug_tracking_system_url=None,
                    custom_severity=None,
                    developer=None,
                    event_id=None,
                    hash=None,
                    root_id=None,
                    skims_method=None,
                    skims_technique=None,
                    stream=None,
                    tags=None,
                    treatment=VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2020-11-23T17:46:10+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.IN_PROGRESS,
                        acceptance_status=None,
                        accepted_until=None,
                        justification="This is a treatment justification",
                        assigned="integratesuser@gmail.com",
                        modified_by="integratesuser2@gmail.com",
                    ),
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_closing_date=None,
                        unreliable_source=Source.ASM,
                        unreliable_efficacy=Decimal("0"),
                        unreliable_last_reattack_date=None,
                        unreliable_last_reattack_requester=None,
                        unreliable_last_requested_reattack_date=None,
                        unreliable_reattack_cycles=0,
                        unreliable_treatment_changes=1,
                    ),
                    verification=None,
                    zero_risk=VulnerabilityZeroRisk(
                        comment_id="123456",
                        modified_by="test@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2020-09-09T21:01:26+00:00"
                        ),
                        status=VulnerabilityZeroRiskStatus.CONFIRMED,
                    ),
                ),
                Vulnerability(
                    created_by="unittest@fluidattacks.com",
                    created_date=datetime.fromisoformat(
                        "2019-09-13T13:17:41+00:00"
                    ),
                    finding_id="436992569",
                    group_name="unittesting",
                    hacker_email="unittest@fluidattacks.com",
                    id="15375781-31f2-4953-ac77-f31134225747",
                    state=VulnerabilityState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2019-09-13T13:17:41+00:00"
                        ),
                        source=Source.ASM,
                        specific="333",
                        status=VulnerabilityStateStatus.VULNERABLE,
                        where="192.168.100.101",
                        commit=None,
                        reasons=None,
                        other_reason=None,
                        tool=VulnerabilityTool(
                            name="tool-2",
                            impact=VulnerabilityToolImpact.INDIRECT,
                        ),
                        snippet=None,
                    ),
                    type=VulnerabilityType.PORTS,
                    bug_tracking_system_url=None,
                    custom_severity=None,
                    developer=None,
                    event_id=None,
                    hash=None,
                    root_id=None,
                    skims_method=None,
                    skims_technique=None,
                    stream=None,
                    tags=None,
                    treatment=VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2019-09-13T13:17:41+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.UNTREATED,
                        acceptance_status=None,
                        accepted_until=None,
                        justification=None,
                        assigned=None,
                        modified_by=None,
                    ),
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_closing_date=None,
                        unreliable_source=Source.ASM,
                        unreliable_efficacy=Decimal("0"),
                        unreliable_last_reattack_date=datetime.fromisoformat(
                            "2020-02-19T15:41:04+00:00"
                        ),
                        unreliable_last_reattack_requester="integratesuser@gmail.com",  # noqa: E501 pylint: disable=line-too-long
                        unreliable_last_requested_reattack_date=datetime.fromisoformat(  # noqa: E501 pylint: disable=line-too-long
                            "2020-02-18T15:41:04+00:00"
                        ),
                        unreliable_reattack_cycles=1,
                        unreliable_treatment_changes=0,
                    ),
                    verification=VulnerabilityVerification(
                        modified_date=datetime.fromisoformat(
                            "2020-02-19T15:41:04+00:00"
                        ),
                        status=VulnerabilityVerificationStatus.VERIFIED,
                        event_id=None,
                    ),
                    zero_risk=None,
                ),
                Vulnerability(
                    created_by="unittest@fluidattacks.com",
                    created_date=datetime.fromisoformat(
                        "2019-09-12T13:45:48+00:00"
                    ),
                    finding_id="436992569",
                    group_name="unittesting",
                    hacker_email="unittest@fluidattacks.com",
                    id="1c644e88-b7a2-498b-b248-c3d367629982",
                    state=VulnerabilityState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2019-09-12T13:45:48+00:00"
                        ),
                        source=Source.ASM,
                        specific="1111",
                        status=VulnerabilityStateStatus.VULNERABLE,
                        where="192.168.1.12",
                        commit=None,
                        reasons=None,
                        other_reason=None,
                        tool=VulnerabilityTool(
                            name="tool-2",
                            impact=VulnerabilityToolImpact.INDIRECT,
                        ),
                        snippet=None,
                    ),
                    type=VulnerabilityType.PORTS,
                    bug_tracking_system_url=None,
                    custom_severity=None,
                    developer=None,
                    event_id=None,
                    hash=None,
                    root_id=None,
                    skims_method=None,
                    skims_technique=None,
                    stream=None,
                    tags=None,
                    treatment=VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2019-09-12T13:45:48+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.UNTREATED,
                        acceptance_status=None,
                        accepted_until=None,
                        justification=None,
                        assigned=None,
                        modified_by=None,
                    ),
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_closing_date=None,
                        unreliable_source=Source.ASM,
                        unreliable_efficacy=Decimal("0"),
                        unreliable_last_reattack_date=None,
                        unreliable_last_reattack_requester=None,
                        unreliable_last_requested_reattack_date=None,
                        unreliable_reattack_cycles=0,
                        unreliable_treatment_changes=0,
                    ),
                    verification=None,
                    zero_risk=None,
                ),
                Vulnerability(
                    created_by="unittest@fluidattacks.com",
                    created_date=datetime.fromisoformat(
                        "2019-09-12T13:45:48+00:00"
                    ),
                    finding_id="436992569",
                    group_name="unittesting",
                    hacker_email="unittest@fluidattacks.com",
                    id="3ec662b9-431a-475c-97e4-ac6ad4cabd90",
                    state=VulnerabilityState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2019-09-12T13:45:48+00:00"
                        ),
                        source=Source.ASM,
                        specific="3333",
                        status=VulnerabilityStateStatus.VULNERABLE,
                        where="192.168.1.4",
                        commit=None,
                        reasons=None,
                        other_reason=None,
                        tool=VulnerabilityTool(
                            name="tool-2",
                            impact=VulnerabilityToolImpact.INDIRECT,
                        ),
                        snippet=None,
                    ),
                    type=VulnerabilityType.PORTS,
                    bug_tracking_system_url=None,
                    custom_severity=None,
                    developer=None,
                    event_id="EVENT#418900971",
                    hash=None,
                    root_id="4039d098-ffc5-4984-8ed3-eb17bca98e19",
                    skims_method=None,
                    skims_technique=None,
                    stream=None,
                    tags=None,
                    treatment=VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2019-09-12T13:45:48+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.UNTREATED,
                        acceptance_status=None,
                        accepted_until=None,
                        justification=None,
                        assigned=None,
                        modified_by=None,
                    ),
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_closing_date=None,
                        unreliable_source=Source.ASM,
                        unreliable_efficacy=Decimal("0"),
                        unreliable_last_reattack_date=None,
                        unreliable_last_reattack_requester=None,
                        unreliable_last_requested_reattack_date=None,
                        unreliable_reattack_cycles=0,
                        unreliable_treatment_changes=0,
                    ),
                    verification=VulnerabilityVerification(
                        modified_date=datetime.fromisoformat(
                            "2022-02-19T15:41:04+00:00"
                        ),
                        status=VulnerabilityVerificationStatus.ON_HOLD,
                        event_id="418900971",
                    ),
                    zero_risk=None,
                ),
                Vulnerability(
                    created_by="unittest@fluidattacks.com",
                    created_date=datetime.fromisoformat(
                        "2019-09-12T13:45:48+00:00"
                    ),
                    finding_id="436992569",
                    group_name="unittesting",
                    hacker_email="unittest@fluidattacks.com",
                    id="47910cbe-932a-411b-8a46-9570a87f4663",
                    state=VulnerabilityState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2019-09-12T13:45:48+00:00"
                        ),
                        source=Source.ASM,
                        specific="6666",
                        status=VulnerabilityStateStatus.VULNERABLE,
                        where="192.168.1.17",
                        commit=None,
                        reasons=None,
                        other_reason=None,
                        tool=None,
                        snippet=None,
                    ),
                    type=VulnerabilityType.PORTS,
                    bug_tracking_system_url=None,
                    custom_severity=None,
                    developer=None,
                    event_id="EVENT#418900971",
                    hash=None,
                    root_id=None,
                    skims_method=None,
                    skims_technique=None,
                    stream=None,
                    tags=None,
                    treatment=VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2019-09-12T13:45:48+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.UNTREATED,
                        acceptance_status=None,
                        accepted_until=None,
                        justification=None,
                        assigned=None,
                        modified_by=None,
                    ),
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_closing_date=None,
                        unreliable_source=Source.ASM,
                        unreliable_efficacy=Decimal("0"),
                        unreliable_last_reattack_date=None,
                        unreliable_last_reattack_requester=None,
                        unreliable_last_requested_reattack_date=None,
                        unreliable_reattack_cycles=0,
                        unreliable_treatment_changes=0,
                    ),
                    verification=VulnerabilityVerification(
                        modified_date=datetime.fromisoformat(
                            "2022-02-19T15:41:04+00:00"
                        ),
                        status=VulnerabilityVerificationStatus.ON_HOLD,
                        event_id="418900971",
                    ),
                    zero_risk=None,
                ),
                Vulnerability(
                    created_by="unittest@fluidattacks.com",
                    created_date=datetime.fromisoformat(
                        "2019-09-12T13:45:48+00:00"
                    ),
                    finding_id="436992569",
                    group_name="unittesting",
                    hacker_email="unittest@fluidattacks.com",
                    id="4ed30d35-33a5-44ba-af44-6cb253be053b",
                    state=VulnerabilityState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2019-09-12T13:45:48+00:00"
                        ),
                        source=Source.ASM,
                        specific="4444",
                        status=VulnerabilityStateStatus.VULNERABLE,
                        where="192.168.1.15",
                        commit=None,
                        reasons=None,
                        other_reason=None,
                        tool=VulnerabilityTool(
                            name="tool-3",
                            impact=VulnerabilityToolImpact.INDIRECT,
                        ),
                        snippet=None,
                    ),
                    type=VulnerabilityType.PORTS,
                    bug_tracking_system_url=None,
                    custom_severity=None,
                    developer=None,
                    event_id=None,
                    hash=None,
                    root_id=None,
                    skims_method=None,
                    skims_technique=None,
                    stream=None,
                    tags=None,
                    treatment=VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2019-09-12T13:45:48+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.UNTREATED,
                        acceptance_status=None,
                        accepted_until=None,
                        justification=None,
                        assigned=None,
                        modified_by=None,
                    ),
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_closing_date=None,
                        unreliable_source=Source.ASM,
                        unreliable_efficacy=Decimal("0"),
                        unreliable_last_reattack_date=None,
                        unreliable_last_reattack_requester=None,
                        unreliable_last_requested_reattack_date=None,
                        unreliable_reattack_cycles=0,
                        unreliable_treatment_changes=0,
                    ),
                    verification=None,
                    zero_risk=None,
                ),
                Vulnerability(
                    created_by="unittest@fluidattacks.com",
                    created_date=datetime.fromisoformat(
                        "2019-09-12T13:45:48+00:00"
                    ),
                    finding_id="436992569",
                    group_name="unittesting",
                    hacker_email="unittest@fluidattacks.com",
                    id="5291f6fa-b296-4e89-a760-798ce56f17d0",
                    state=VulnerabilityState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2019-09-12T13:45:48+00:00"
                        ),
                        source=Source.ASM,
                        specific="5555",
                        status=VulnerabilityStateStatus.VULNERABLE,
                        where="192.168.1.6",
                        commit=None,
                        reasons=None,
                        other_reason=None,
                        tool=VulnerabilityTool(
                            name="tool-3",
                            impact=VulnerabilityToolImpact.INDIRECT,
                        ),
                        snippet=None,
                    ),
                    type=VulnerabilityType.PORTS,
                    bug_tracking_system_url=None,
                    custom_severity=None,
                    developer=None,
                    event_id=None,
                    hash=None,
                    root_id=None,
                    skims_method=None,
                    skims_technique=None,
                    stream=None,
                    tags=None,
                    treatment=VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2019-09-12T13:45:48+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.UNTREATED,
                        acceptance_status=None,
                        accepted_until=None,
                        justification=None,
                        assigned=None,
                        modified_by=None,
                    ),
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_closing_date=None,
                        unreliable_source=Source.ASM,
                        unreliable_efficacy=Decimal("0"),
                        unreliable_last_reattack_date=None,
                        unreliable_last_reattack_requester=None,
                        unreliable_last_requested_reattack_date=None,
                        unreliable_reattack_cycles=0,
                        unreliable_treatment_changes=0,
                    ),
                    verification=None,
                    zero_risk=None,
                ),
                Vulnerability(
                    created_by="unittest@fluidattacks.com",
                    created_date=datetime.fromisoformat(
                        "2019-09-12T13:45:48+00:00"
                    ),
                    finding_id="436992569",
                    group_name="unittesting",
                    hacker_email="unittest@fluidattacks.com",
                    id="57e5c1ec-5956-40e9-8e30-284033c1140d",
                    state=VulnerabilityState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2019-09-12T13:45:48+00:00"
                        ),
                        source=Source.ASM,
                        specific="9999",
                        status=VulnerabilityStateStatus.VULNERABLE,
                        where="192.168.1.10",
                        commit=None,
                        reasons=None,
                        other_reason=None,
                        tool=VulnerabilityTool(
                            name="tool-3",
                            impact=VulnerabilityToolImpact.INDIRECT,
                        ),
                        snippet=None,
                    ),
                    type=VulnerabilityType.PORTS,
                    bug_tracking_system_url=None,
                    custom_severity=None,
                    developer=None,
                    event_id=None,
                    hash=None,
                    root_id=None,
                    skims_method=None,
                    skims_technique=None,
                    stream=None,
                    tags=None,
                    treatment=VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2019-09-12T13:45:48+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.UNTREATED,
                        acceptance_status=None,
                        accepted_until=None,
                        justification=None,
                        assigned=None,
                        modified_by=None,
                    ),
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_closing_date=None,
                        unreliable_source=Source.ASM,
                        unreliable_efficacy=Decimal("0"),
                        unreliable_last_reattack_date=None,
                        unreliable_last_reattack_requester=None,
                        unreliable_last_requested_reattack_date=None,
                        unreliable_reattack_cycles=0,
                        unreliable_treatment_changes=0,
                    ),
                    verification=None,
                    zero_risk=None,
                ),
                Vulnerability(
                    created_by="unittest@fluidattacks.com",
                    created_date=datetime.fromisoformat(
                        "2019-09-13T22:00:56+00:00"
                    ),
                    finding_id="436992569",
                    group_name="unittesting",
                    hacker_email="unittest@fluidattacks.com",
                    id="587c40de-09a0-4d85-a9f9-eaa46aa895d7",
                    state=VulnerabilityState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2019-09-13T22:00:56+00:00"
                        ),
                        source=Source.ASM,
                        specific="1111",
                        status=VulnerabilityStateStatus.VULNERABLE,
                        where="192.168.100.112",
                        commit=None,
                        reasons=None,
                        other_reason=None,
                        tool=None,
                        snippet=None,
                    ),
                    type=VulnerabilityType.PORTS,
                    bug_tracking_system_url=None,
                    custom_severity=None,
                    developer=None,
                    event_id=None,
                    hash=None,
                    root_id=None,
                    skims_method=None,
                    skims_technique=None,
                    stream=None,
                    tags=None,
                    treatment=VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2019-09-13T22:00:56+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.UNTREATED,
                        acceptance_status=None,
                        accepted_until=None,
                        justification=None,
                        assigned=None,
                        modified_by=None,
                    ),
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_closing_date=None,
                        unreliable_source=Source.ASM,
                        unreliable_efficacy=Decimal("0"),
                        unreliable_last_reattack_date=None,
                        unreliable_last_reattack_requester="integratesuser@gmail.com",  # noqa: E501 pylint: disable=line-too-long
                        unreliable_last_requested_reattack_date=datetime.fromisoformat(  # noqa: E501 pylint: disable=line-too-long
                            "2020-02-19T15:41:04+00:00"
                        ),
                        unreliable_reattack_cycles=1,
                        unreliable_treatment_changes=0,
                    ),
                    verification=VulnerabilityVerification(
                        modified_date=datetime.fromisoformat(
                            "2020-02-19T15:41:04+00:00"
                        ),
                        status=VulnerabilityVerificationStatus.REQUESTED,
                        event_id=None,
                    ),
                    zero_risk=None,
                ),
                Vulnerability(
                    created_by="unittest@fluidattacks.com",
                    created_date=datetime.fromisoformat(
                        "2019-09-13T14:58:38+00:00"
                    ),
                    finding_id="436992569",
                    group_name="unittesting",
                    hacker_email="unittest@fluidattacks.com",
                    id="5afb9a49-a359-48ce-80ee-79c145919275",
                    state=VulnerabilityState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2019-09-13T14:58:38+00:00"
                        ),
                        source=Source.ASM,
                        specific="333",
                        status=VulnerabilityStateStatus.VULNERABLE,
                        where="192.168.100.105",
                        commit=None,
                        reasons=None,
                        other_reason=None,
                        tool=None,
                        snippet=None,
                    ),
                    type=VulnerabilityType.PORTS,
                    bug_tracking_system_url=None,
                    custom_severity=None,
                    developer=None,
                    event_id=None,
                    hash=None,
                    root_id=None,
                    skims_method=None,
                    skims_technique=None,
                    stream=None,
                    tags=None,
                    treatment=VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2019-09-13T14:58:38+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.UNTREATED,
                        acceptance_status=None,
                        accepted_until=None,
                        justification=None,
                        assigned=None,
                        modified_by=None,
                    ),
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_closing_date=None,
                        unreliable_source=Source.ASM,
                        unreliable_efficacy=Decimal("0"),
                        unreliable_last_reattack_date=None,
                        unreliable_last_reattack_requester=None,
                        unreliable_last_requested_reattack_date=None,
                        unreliable_reattack_cycles=0,
                        unreliable_treatment_changes=0,
                    ),
                    verification=None,
                    zero_risk=None,
                ),
                Vulnerability(
                    created_by="unittest@fluidattacks.com",
                    created_date=datetime.fromisoformat(
                        "2019-09-13T20:37:59+00:00"
                    ),
                    finding_id="436992569",
                    group_name="unittesting",
                    hacker_email="unittest@fluidattacks.com",
                    id="5ed5c3c0-9064-41f5-8ef2-5e1eeee62955",
                    state=VulnerabilityState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2019-09-13T20:37:59+00:00"
                        ),
                        source=Source.ASM,
                        specific="1111",
                        status=VulnerabilityStateStatus.VULNERABLE,
                        where="192.168.100.111",
                        commit=None,
                        reasons=None,
                        other_reason=None,
                        tool=None,
                        snippet=None,
                    ),
                    type=VulnerabilityType.PORTS,
                    bug_tracking_system_url=None,
                    custom_severity=None,
                    developer=None,
                    event_id=None,
                    hash=None,
                    root_id=None,
                    skims_method=None,
                    skims_technique=None,
                    stream=None,
                    tags=None,
                    treatment=VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2019-09-13T20:37:59+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.UNTREATED,
                        acceptance_status=None,
                        accepted_until=None,
                        justification=None,
                        assigned=None,
                        modified_by=None,
                    ),
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_closing_date=None,
                        unreliable_source=Source.ASM,
                        unreliable_efficacy=Decimal("0"),
                        unreliable_last_reattack_date=None,
                        unreliable_last_reattack_requester=None,
                        unreliable_last_requested_reattack_date=None,
                        unreliable_reattack_cycles=0,
                        unreliable_treatment_changes=0,
                    ),
                    verification=None,
                    zero_risk=None,
                ),
                Vulnerability(
                    created_by="unittest@fluidattacks.com",
                    created_date=datetime.fromisoformat(
                        "2019-09-13T16:03:21+00:00"
                    ),
                    finding_id="436992569",
                    group_name="unittesting",
                    hacker_email="unittest@fluidattacks.com",
                    id="72bb8607-c259-4781-9599-185aac02b3cc",
                    state=VulnerabilityState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2019-09-13T16:05:05+00:00"
                        ),
                        source=Source.ASM,
                        specific="4444",
                        status=VulnerabilityStateStatus.SAFE,
                        where="192.168.100.101",
                        commit=None,
                        reasons=None,
                        other_reason=None,
                        tool=None,
                        snippet=None,
                    ),
                    type=VulnerabilityType.PORTS,
                    bug_tracking_system_url=None,
                    custom_severity=None,
                    developer=None,
                    event_id=None,
                    hash=None,
                    root_id=None,
                    skims_method=None,
                    skims_technique=None,
                    stream=None,
                    tags=None,
                    treatment=VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2019-09-13T16:03:21+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.UNTREATED,
                        acceptance_status=None,
                        accepted_until=None,
                        justification=None,
                        assigned=None,
                        modified_by=None,
                    ),
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_closing_date=datetime.fromisoformat(
                            "2019-09-13T16:05:05+00:00"
                        ),
                        unreliable_source=Source.ASM,
                        unreliable_efficacy=Decimal("0"),
                        unreliable_last_reattack_date=None,
                        unreliable_last_reattack_requester=None,
                        unreliable_last_requested_reattack_date=None,
                        unreliable_reattack_cycles=0,
                        unreliable_treatment_changes=0,
                    ),
                    verification=None,
                    zero_risk=None,
                ),
                Vulnerability(
                    created_by="unittest@fluidattacks.com",
                    created_date=datetime.fromisoformat(
                        "2019-09-12T13:45:48+00:00"
                    ),
                    finding_id="436992569",
                    group_name="unittesting",
                    hacker_email="unittest@fluidattacks.com",
                    id="759aaf00-34ee-4609-aec6-7f857c470eff",
                    state=VulnerabilityState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2019-09-12T13:45:48+00:00"
                        ),
                        source=Source.ASM,
                        specific="4444",
                        status=VulnerabilityStateStatus.VULNERABLE,
                        where="192.168.1.5",
                        commit=None,
                        reasons=None,
                        other_reason=None,
                        tool=None,
                        snippet=None,
                    ),
                    type=VulnerabilityType.PORTS,
                    bug_tracking_system_url=None,
                    custom_severity=None,
                    developer=None,
                    event_id=None,
                    hash=None,
                    root_id=None,
                    skims_method=None,
                    skims_technique=None,
                    stream=None,
                    tags=None,
                    treatment=VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2019-09-12T13:45:48+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.UNTREATED,
                        acceptance_status=None,
                        accepted_until=None,
                        justification=None,
                        assigned=None,
                        modified_by=None,
                    ),
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_closing_date=None,
                        unreliable_source=Source.ASM,
                        unreliable_efficacy=Decimal("0"),
                        unreliable_last_reattack_date=None,
                        unreliable_last_reattack_requester=None,
                        unreliable_last_requested_reattack_date=None,
                        unreliable_reattack_cycles=0,
                        unreliable_treatment_changes=0,
                    ),
                    verification=None,
                    zero_risk=None,
                ),
                Vulnerability(
                    created_by="integratesmanager@gmail.com",
                    created_date=datetime.fromisoformat(
                        "2019-09-13T13:59:20+00:00"
                    ),
                    finding_id="436992569",
                    group_name="unittesting",
                    hacker_email="integratesmanager@gmail.com",
                    id="81db1fad-c329-4356-a5eb-9ad9b0d75a7e",
                    state=VulnerabilityState(
                        modified_by="aaguirre@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2019-09-13T13:59:20+00:00"
                        ),
                        source=Source.ASM,
                        specific="333",
                        status=VulnerabilityStateStatus.VULNERABLE,
                        where="192.168.100.104",
                        commit=None,
                        reasons=None,
                        other_reason=None,
                        tool=None,
                        snippet=None,
                    ),
                    type=VulnerabilityType.PORTS,
                    bug_tracking_system_url=None,
                    custom_severity=None,
                    developer=None,
                    event_id=None,
                    hash=None,
                    root_id=None,
                    skims_method=None,
                    skims_technique=None,
                    stream=None,
                    tags=None,
                    treatment=VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2019-09-13T13:59:20+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.UNTREATED,
                        acceptance_status=None,
                        accepted_until=None,
                        justification=None,
                        assigned=None,
                        modified_by=None,
                    ),
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_closing_date=None,
                        unreliable_source=Source.ASM,
                        unreliable_efficacy=Decimal("0"),
                        unreliable_last_reattack_date=None,
                        unreliable_last_reattack_requester=None,
                        unreliable_last_requested_reattack_date=None,
                        unreliable_reattack_cycles=0,
                        unreliable_treatment_changes=0,
                    ),
                    verification=None,
                    zero_risk=None,
                ),
                Vulnerability(
                    created_by="unittest@fluidattacks.com",
                    created_date=datetime.fromisoformat(
                        "2019-09-13T15:00:03+00:00"
                    ),
                    finding_id="436992569",
                    group_name="unittesting",
                    hacker_email="unittest@fluidattacks.com",
                    id="8226e222-8128-438d-a9b7-93eeb93a36b3",
                    state=VulnerabilityState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2019-09-13T15:09:02+00:00"
                        ),
                        source=Source.ASM,
                        specific="333",
                        status=VulnerabilityStateStatus.SAFE,
                        where="192.168.100.107",
                        commit=None,
                        reasons=None,
                        other_reason=None,
                        tool=None,
                        snippet=None,
                    ),
                    type=VulnerabilityType.PORTS,
                    bug_tracking_system_url=None,
                    custom_severity=None,
                    developer=None,
                    event_id=None,
                    hash=None,
                    root_id=None,
                    skims_method=None,
                    skims_technique=None,
                    stream=None,
                    tags=None,
                    treatment=VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2019-09-13T15:00:03+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.UNTREATED,
                        acceptance_status=None,
                        accepted_until=None,
                        justification=None,
                        assigned=None,
                        modified_by=None,
                    ),
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_closing_date=datetime.fromisoformat(
                            "2019-09-13T15:09:02+00:00"
                        ),
                        unreliable_source=Source.ASM,
                        unreliable_efficacy=Decimal("0"),
                        unreliable_last_reattack_date=None,
                        unreliable_last_reattack_requester=None,
                        unreliable_last_requested_reattack_date=None,
                        unreliable_reattack_cycles=0,
                        unreliable_treatment_changes=0,
                    ),
                    verification=None,
                    zero_risk=None,
                ),
                Vulnerability(
                    created_by="unittest@fluidattacks.com",
                    created_date=datetime.fromisoformat(
                        "2019-09-12T13:45:48+00:00"
                    ),
                    finding_id="436992569",
                    group_name="unittesting",
                    hacker_email="unittest@fluidattacks.com",
                    id="95068fdd-80ca-4eb2-8311-b16b63a61f05",
                    state=VulnerabilityState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2019-09-12T13:45:48+00:00"
                        ),
                        source=Source.ASM,
                        specific="8888",
                        status=VulnerabilityStateStatus.VULNERABLE,
                        where="192.168.1.9",
                        commit=None,
                        reasons=None,
                        other_reason=None,
                        tool=None,
                        snippet=None,
                    ),
                    type=VulnerabilityType.PORTS,
                    bug_tracking_system_url=None,
                    custom_severity=None,
                    developer=None,
                    event_id=None,
                    hash=None,
                    root_id=None,
                    skims_method=None,
                    skims_technique=None,
                    stream=None,
                    tags=None,
                    treatment=VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2019-09-12T13:45:48+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.UNTREATED,
                        acceptance_status=None,
                        accepted_until=None,
                        justification=None,
                        assigned=None,
                        modified_by=None,
                    ),
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_closing_date=None,
                        unreliable_source=Source.ASM,
                        unreliable_efficacy=Decimal("0"),
                        unreliable_last_reattack_date=None,
                        unreliable_last_reattack_requester=None,
                        unreliable_last_requested_reattack_date=None,
                        unreliable_reattack_cycles=0,
                        unreliable_treatment_changes=0,
                    ),
                    verification=None,
                    zero_risk=None,
                ),
                Vulnerability(
                    created_by="unittest@fluidattacks.com",
                    created_date=datetime.fromisoformat(
                        "2019-09-16T21:01:24+00:00"
                    ),
                    finding_id="436992569",
                    group_name="unittesting",
                    hacker_email="unittest@fluidattacks.com",
                    id="987a6d71-d23c-40db-ad98-bfccf60660ed",
                    state=VulnerabilityState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2019-09-16T21:01:24+00:00"
                        ),
                        source=Source.ASM,
                        specific="888",
                        status=VulnerabilityStateStatus.VULNERABLE,
                        where="192.168.100.122",
                        commit=None,
                        reasons=None,
                        other_reason=None,
                        tool=None,
                        snippet=None,
                    ),
                    type=VulnerabilityType.PORTS,
                    bug_tracking_system_url=None,
                    custom_severity=None,
                    developer=None,
                    event_id=None,
                    hash=None,
                    root_id=None,
                    skims_method=None,
                    skims_technique=None,
                    stream=None,
                    tags=None,
                    treatment=VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2019-09-16T21:01:24+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.UNTREATED,
                        acceptance_status=None,
                        accepted_until=None,
                        justification=None,
                        assigned=None,
                        modified_by=None,
                    ),
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_closing_date=None,
                        unreliable_source=Source.ASM,
                        unreliable_efficacy=Decimal("0"),
                        unreliable_last_reattack_date=None,
                        unreliable_last_reattack_requester=None,
                        unreliable_last_requested_reattack_date=None,
                        unreliable_reattack_cycles=0,
                        unreliable_treatment_changes=0,
                    ),
                    verification=None,
                    zero_risk=None,
                ),
                Vulnerability(
                    created_by="unittest@fluidattacks.com",
                    created_date=datetime.fromisoformat(
                        "2019-09-12T13:45:48+00:00"
                    ),
                    finding_id="436992569",
                    group_name="unittesting",
                    hacker_email="unittest@fluidattacks.com",
                    id="aa6a9d70-618b-4ab0-b280-d627ce311200",
                    state=VulnerabilityState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2019-09-12T13:45:48+00:00"
                        ),
                        source=Source.ASM,
                        specific="6666",
                        status=VulnerabilityStateStatus.VULNERABLE,
                        where="192.168.1.7",
                        commit=None,
                        reasons=None,
                        other_reason=None,
                        tool=None,
                        snippet=None,
                    ),
                    type=VulnerabilityType.PORTS,
                    bug_tracking_system_url=None,
                    custom_severity=None,
                    developer=None,
                    event_id=None,
                    hash=None,
                    root_id=None,
                    skims_method=None,
                    skims_technique=None,
                    stream=None,
                    tags=None,
                    treatment=VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2019-09-12T13:45:48+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.UNTREATED,
                        acceptance_status=None,
                        accepted_until=None,
                        justification=None,
                        assigned=None,
                        modified_by=None,
                    ),
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_closing_date=None,
                        unreliable_source=Source.ASM,
                        unreliable_efficacy=Decimal("0"),
                        unreliable_last_reattack_date=None,
                        unreliable_last_reattack_requester=None,
                        unreliable_last_requested_reattack_date=None,
                        unreliable_reattack_cycles=0,
                        unreliable_treatment_changes=0,
                    ),
                    verification=None,
                    zero_risk=None,
                ),
                Vulnerability(
                    created_by="unittest@fluidattacks.com",
                    created_date=datetime.fromisoformat(
                        "2019-09-12T13:45:48+00:00"
                    ),
                    finding_id="436992569",
                    group_name="unittesting",
                    hacker_email="unittest@fluidattacks.com",
                    id="ab25380d-dfe1-4cde-aefd-acca6990d6aa",
                    state=VulnerabilityState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2019-09-12T13:45:48+00:00"
                        ),
                        source=Source.ASM,
                        specific="1111",
                        status=VulnerabilityStateStatus.VULNERABLE,
                        where="192.168.1.2",
                        commit=None,
                        reasons=None,
                        other_reason=None,
                        tool=None,
                        snippet=None,
                    ),
                    type=VulnerabilityType.PORTS,
                    bug_tracking_system_url=None,
                    custom_severity=None,
                    developer=None,
                    event_id=None,
                    hash=None,
                    root_id=None,
                    skims_method=None,
                    skims_technique=None,
                    stream=None,
                    tags=None,
                    treatment=VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2019-09-12T13:45:48+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.UNTREATED,
                        acceptance_status=None,
                        accepted_until=None,
                        justification=None,
                        assigned=None,
                        modified_by=None,
                    ),
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_closing_date=None,
                        unreliable_source=Source.ASM,
                        unreliable_efficacy=Decimal("0"),
                        unreliable_last_reattack_date=None,
                        unreliable_last_reattack_requester=None,
                        unreliable_last_requested_reattack_date=None,
                        unreliable_reattack_cycles=0,
                        unreliable_treatment_changes=0,
                    ),
                    verification=None,
                    zero_risk=None,
                ),
                Vulnerability(
                    created_by="unittest@fluidattacks.com",
                    created_date=datetime.fromisoformat(
                        "2019-09-12T13:45:48+00:00"
                    ),
                    finding_id="436992569",
                    group_name="unittesting",
                    hacker_email="unittest@fluidattacks.com",
                    id="ae16f325-a492-482b-a7a1-6285e8057480",
                    state=VulnerabilityState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2019-09-12T13:45:48+00:00"
                        ),
                        source=Source.ASM,
                        specific="2222",
                        status=VulnerabilityStateStatus.VULNERABLE,
                        where="192.168.1.3",
                        commit=None,
                        reasons=None,
                        other_reason=None,
                        tool=None,
                        snippet=None,
                    ),
                    type=VulnerabilityType.PORTS,
                    bug_tracking_system_url=None,
                    custom_severity=None,
                    developer=None,
                    event_id=None,
                    hash=None,
                    root_id=None,
                    skims_method=None,
                    skims_technique=None,
                    stream=None,
                    tags=None,
                    treatment=VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2019-09-12T13:45:48+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.UNTREATED,
                        acceptance_status=None,
                        accepted_until=None,
                        justification=None,
                        assigned=None,
                        modified_by=None,
                    ),
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_closing_date=None,
                        unreliable_source=Source.ASM,
                        unreliable_efficacy=Decimal("0"),
                        unreliable_last_reattack_date=None,
                        unreliable_last_reattack_requester=None,
                        unreliable_last_requested_reattack_date=None,
                        unreliable_reattack_cycles=0,
                        unreliable_treatment_changes=0,
                    ),
                    verification=None,
                    zero_risk=None,
                ),
                Vulnerability(
                    created_by="unittest@fluidattacks.com",
                    created_date=datetime.fromisoformat(
                        "2019-09-12T13:45:48+00:00"
                    ),
                    finding_id="436992569",
                    group_name="unittesting",
                    hacker_email="unittest@fluidattacks.com",
                    id="b16ed89e-668d-42d6-add1-73535bb0e083",
                    state=VulnerabilityState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2019-09-12T13:45:48+00:00"
                        ),
                        source=Source.ASM,
                        specific="2222",
                        status=VulnerabilityStateStatus.VULNERABLE,
                        where="192.168.1.13",
                        commit=None,
                        reasons=None,
                        other_reason=None,
                        tool=None,
                        snippet=None,
                    ),
                    type=VulnerabilityType.PORTS,
                    bug_tracking_system_url=None,
                    custom_severity=None,
                    developer=None,
                    event_id=None,
                    hash=None,
                    root_id=None,
                    skims_method=None,
                    skims_technique=None,
                    stream=None,
                    tags=None,
                    treatment=VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2019-09-12T13:45:48+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.UNTREATED,
                        acceptance_status=None,
                        accepted_until=None,
                        justification=None,
                        assigned=None,
                        modified_by=None,
                    ),
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_closing_date=None,
                        unreliable_source=Source.ASM,
                        unreliable_efficacy=Decimal("0"),
                        unreliable_last_reattack_date=None,
                        unreliable_last_reattack_requester=None,
                        unreliable_last_requested_reattack_date=None,
                        unreliable_reattack_cycles=0,
                        unreliable_treatment_changes=0,
                    ),
                    verification=None,
                    zero_risk=None,
                ),
                Vulnerability(
                    created_by="unittest@fluidattacks.com",
                    created_date=datetime.fromisoformat(
                        "2019-09-12T13:45:48+00:00"
                    ),
                    finding_id="436992569",
                    group_name="unittesting",
                    hacker_email="unittest@fluidattacks.com",
                    id="bac162ff-5c2a-4a96-9b77-fd7020976160",
                    state=VulnerabilityState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2019-09-12T13:45:48+00:00"
                        ),
                        source=Source.ASM,
                        specific="7777",
                        status=VulnerabilityStateStatus.VULNERABLE,
                        where="192.168.1.8",
                        commit=None,
                        reasons=None,
                        other_reason=None,
                        tool=None,
                        snippet=None,
                    ),
                    type=VulnerabilityType.PORTS,
                    bug_tracking_system_url=None,
                    custom_severity=None,
                    developer=None,
                    event_id=None,
                    hash=None,
                    root_id=None,
                    skims_method=None,
                    skims_technique=None,
                    stream=None,
                    tags=None,
                    treatment=VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2019-09-12T13:45:48+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.UNTREATED,
                        acceptance_status=None,
                        accepted_until=None,
                        justification=None,
                        assigned=None,
                        modified_by=None,
                    ),
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_closing_date=None,
                        unreliable_source=Source.ASM,
                        unreliable_efficacy=Decimal("0"),
                        unreliable_last_reattack_date=None,
                        unreliable_last_reattack_requester=None,
                        unreliable_last_requested_reattack_date=None,
                        unreliable_reattack_cycles=0,
                        unreliable_treatment_changes=0,
                    ),
                    verification=None,
                    zero_risk=None,
                ),
                Vulnerability(
                    created_by="unittest@fluidattacks.com",
                    created_date=datetime.fromisoformat(
                        "2019-09-13T15:53:05+00:00"
                    ),
                    finding_id="436992569",
                    group_name="unittesting",
                    hacker_email="unittest@fluidattacks.com",
                    id="bf818399-b331-4fa4-b335-98548e037378",
                    state=VulnerabilityState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2019-09-13T16:28:20+00:00"
                        ),
                        source=Source.ASM,
                        specific="333",
                        status=VulnerabilityStateStatus.SAFE,
                        where="192.168.100.109",
                        commit=None,
                        reasons=None,
                        other_reason=None,
                        tool=None,
                        snippet=None,
                    ),
                    type=VulnerabilityType.PORTS,
                    bug_tracking_system_url=None,
                    custom_severity=None,
                    developer=None,
                    event_id=None,
                    hash=None,
                    root_id=None,
                    skims_method=None,
                    skims_technique=None,
                    stream=None,
                    tags=None,
                    treatment=VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2019-09-13T15:53:05+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.UNTREATED,
                        acceptance_status=None,
                        accepted_until=None,
                        justification=None,
                        assigned=None,
                        modified_by=None,
                    ),
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_closing_date=datetime.fromisoformat(
                            "2019-09-13T16:28:20+00:00"
                        ),
                        unreliable_source=Source.ASM,
                        unreliable_efficacy=Decimal("0"),
                        unreliable_last_reattack_date=None,
                        unreliable_last_reattack_requester=None,
                        unreliable_last_requested_reattack_date=None,
                        unreliable_reattack_cycles=0,
                        unreliable_treatment_changes=0,
                    ),
                    verification=None,
                    zero_risk=None,
                ),
                Vulnerability(
                    created_by="unittest@fluidattacks.com",
                    created_date=datetime.fromisoformat(
                        "2019-09-12T13:45:48+00:00"
                    ),
                    finding_id="436992569",
                    group_name="unittesting",
                    hacker_email="unittest@fluidattacks.com",
                    id="c8161719-5ac8-45ba-a3fb-ab69ea39ddcb",
                    state=VulnerabilityState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2019-09-12T13:45:48+00:00"
                        ),
                        source=Source.ASM,
                        specific="5555",
                        status=VulnerabilityStateStatus.VULNERABLE,
                        where="192.168.1.16",
                        commit=None,
                        reasons=None,
                        other_reason=None,
                        tool=None,
                        snippet=None,
                    ),
                    type=VulnerabilityType.PORTS,
                    bug_tracking_system_url=None,
                    custom_severity=None,
                    developer=None,
                    event_id=None,
                    hash=None,
                    root_id=None,
                    skims_method=None,
                    skims_technique=None,
                    stream=None,
                    tags=None,
                    treatment=VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2019-09-12T13:45:48+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.UNTREATED,
                        acceptance_status=None,
                        accepted_until=None,
                        justification=None,
                        assigned=None,
                        modified_by=None,
                    ),
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_closing_date=None,
                        unreliable_source=Source.ASM,
                        unreliable_efficacy=Decimal("0"),
                        unreliable_last_reattack_date=None,
                        unreliable_last_reattack_requester=None,
                        unreliable_last_requested_reattack_date=None,
                        unreliable_reattack_cycles=0,
                        unreliable_treatment_changes=0,
                    ),
                    verification=None,
                    zero_risk=None,
                ),
                Vulnerability(
                    created_by="unittest@fluidattacks.com",
                    created_date=datetime.fromisoformat(
                        "2019-09-12T13:45:48+00:00"
                    ),
                    finding_id="436992569",
                    group_name="unittesting",
                    hacker_email="unittest@fluidattacks.com",
                    id="d212a841-7d48-4cb6-b776-cccc2845c383",
                    state=VulnerabilityState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2019-09-12T13:45:48+00:00"
                        ),
                        source=Source.ASM,
                        specific="3333",
                        status=VulnerabilityStateStatus.VULNERABLE,
                        where="192.168.1.14",
                        commit=None,
                        reasons=None,
                        other_reason=None,
                        tool=None,
                        snippet=None,
                    ),
                    type=VulnerabilityType.PORTS,
                    bug_tracking_system_url=None,
                    custom_severity=None,
                    developer=None,
                    event_id=None,
                    hash=None,
                    root_id=None,
                    skims_method=None,
                    skims_technique=None,
                    stream=None,
                    tags=None,
                    treatment=VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2019-09-12T13:45:48+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.UNTREATED,
                        acceptance_status=None,
                        accepted_until=None,
                        justification=None,
                        assigned=None,
                        modified_by=None,
                    ),
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_closing_date=None,
                        unreliable_source=Source.ASM,
                        unreliable_efficacy=Decimal("0"),
                        unreliable_last_reattack_date=None,
                        unreliable_last_reattack_requester=None,
                        unreliable_last_requested_reattack_date=None,
                        unreliable_reattack_cycles=0,
                        unreliable_treatment_changes=0,
                    ),
                    verification=None,
                    zero_risk=None,
                ),
                Vulnerability(
                    created_by="unittest@fluidattacks.com",
                    created_date=datetime.fromisoformat(
                        "2019-09-13T20:19:17+00:00"
                    ),
                    finding_id="436992569",
                    group_name="unittesting",
                    hacker_email="unittest@fluidattacks.com",
                    id="d4d4c6a0-3d51-42cf-b93f-4c503f67d72d",
                    state=VulnerabilityState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2019-09-13T20:19:17+00:00"
                        ),
                        source=Source.ASM,
                        specific="333",
                        status=VulnerabilityStateStatus.VULNERABLE,
                        where="192.168.100.108",
                        commit=None,
                        reasons=None,
                        other_reason=None,
                        tool=None,
                        snippet=None,
                    ),
                    type=VulnerabilityType.PORTS,
                    bug_tracking_system_url=None,
                    custom_severity=None,
                    developer=None,
                    event_id=None,
                    hash=None,
                    root_id=None,
                    skims_method=None,
                    skims_technique=None,
                    stream=None,
                    tags=None,
                    treatment=VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2019-09-13T20:19:17+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.UNTREATED,
                        acceptance_status=None,
                        accepted_until=None,
                        justification=None,
                        assigned=None,
                        modified_by=None,
                    ),
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_closing_date=None,
                        unreliable_source=Source.ASM,
                        unreliable_efficacy=Decimal("0"),
                        unreliable_last_reattack_date=None,
                        unreliable_last_reattack_requester=None,
                        unreliable_last_requested_reattack_date=None,
                        unreliable_reattack_cycles=0,
                        unreliable_treatment_changes=0,
                    ),
                    verification=None,
                    zero_risk=None,
                ),
                Vulnerability(
                    created_by="unittest@fluidattacks.com",
                    created_date=datetime.fromisoformat(
                        "2019-08-30T14:30:13+00:00"
                    ),
                    finding_id="436992569",
                    group_name="unittesting",
                    hacker_email="unittest@fluidattacks.com",
                    id="f2d577b4-855b-41fc-a844-2b96f797775c",
                    state=VulnerabilityState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2019-08-30T14:30:13+00:00"
                        ),
                        source=Source.ASM,
                        specific="asserts",
                        status=VulnerabilityStateStatus.VULNERABLE,
                        where="testing",
                        commit=None,
                        reasons=None,
                        other_reason=None,
                        tool=None,
                        snippet=None,
                    ),
                    type=VulnerabilityType.INPUTS,
                    bug_tracking_system_url=None,
                    custom_severity=None,
                    developer=None,
                    event_id=None,
                    hash=None,
                    root_id=None,
                    skims_method=None,
                    skims_technique=None,
                    stream=None,
                    tags=None,
                    treatment=VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2019-08-30T14:30:13+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.UNTREATED,
                        acceptance_status=None,
                        accepted_until=None,
                        justification=None,
                        assigned=None,
                        modified_by=None,
                    ),
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_closing_date=None,
                        unreliable_source=Source.ASM,
                        unreliable_efficacy=Decimal("0"),
                        unreliable_last_reattack_date=None,
                        unreliable_last_reattack_requester=None,
                        unreliable_last_requested_reattack_date=None,
                        unreliable_reattack_cycles=0,
                        unreliable_treatment_changes=0,
                    ),
                    verification=None,
                    zero_risk=None,
                ),
                Vulnerability(
                    created_by="unittest@fluidattacks.com",
                    created_date=datetime.fromisoformat(
                        "2019-09-16T20:02:17+00:00"
                    ),
                    finding_id="436992569",
                    group_name="unittesting",
                    hacker_email="unittest@fluidattacks.com",
                    id="fc01759b-0f2f-4e4e-9e24-5c27c91d574b",
                    state=VulnerabilityState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2019-09-16T20:02:17+00:00"
                        ),
                        source=Source.ASM,
                        specific="1111",
                        status=VulnerabilityStateStatus.VULNERABLE,
                        where="192.168.100.113",
                        commit=None,
                        reasons=None,
                        other_reason=None,
                        tool=None,
                        snippet=None,
                    ),
                    type=VulnerabilityType.PORTS,
                    bug_tracking_system_url=None,
                    custom_severity=None,
                    developer=None,
                    event_id=None,
                    hash=None,
                    root_id=None,
                    skims_method=None,
                    skims_technique=None,
                    stream=None,
                    tags=None,
                    treatment=VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2019-09-16T20:02:17+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.UNTREATED,
                        acceptance_status=None,
                        accepted_until=None,
                        justification=None,
                        assigned=None,
                        modified_by=None,
                    ),
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_closing_date=None,
                        unreliable_source=Source.ASM,
                        unreliable_efficacy=Decimal("0"),
                        unreliable_last_reattack_date=None,
                        unreliable_last_reattack_requester=None,
                        unreliable_last_requested_reattack_date=None,
                        unreliable_reattack_cycles=0,
                        unreliable_treatment_changes=0,
                    ),
                    verification=None,
                    zero_risk=None,
                ),
                Vulnerability(
                    created_by="integratesmanager@gmail.com",
                    created_date=datetime.fromisoformat(
                        "2019-09-13T14:03:05+00:00"
                    ),
                    finding_id="436992569",
                    group_name="unittesting",
                    hacker_email="integratesmanager@gmail.com",
                    id="feabfd52-0b0f-405e-bf6a-e9a224af6726",
                    state=VulnerabilityState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2019-09-13T14:03:05+00:00"
                        ),
                        source=Source.ASM,
                        specific="333",
                        status=VulnerabilityStateStatus.SAFE,
                        where="192.168.100.103",
                        commit=None,
                        reasons=None,
                        other_reason=None,
                        tool=None,
                        snippet=None,
                    ),
                    type=VulnerabilityType.PORTS,
                    bug_tracking_system_url=None,
                    custom_severity=None,
                    developer=None,
                    event_id=None,
                    hash=None,
                    root_id=None,
                    skims_method=None,
                    skims_technique=None,
                    stream=None,
                    tags=None,
                    treatment=VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2019-09-13T14:03:05+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.UNTREATED,
                        acceptance_status=None,
                        accepted_until=None,
                        justification=None,
                        assigned=None,
                        modified_by=None,
                    ),
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_closing_date=datetime.fromisoformat(
                            "2019-09-13T14:03:05+00:00"
                        ),
                        unreliable_source=Source.ASM,
                        unreliable_efficacy=Decimal("0"),
                        unreliable_last_reattack_date=None,
                        unreliable_last_reattack_requester=None,
                        unreliable_last_requested_reattack_date=None,
                        unreliable_reattack_cycles=0,
                        unreliable_treatment_changes=0,
                    ),
                    verification=None,
                    zero_risk=None,
                ),
                Vulnerability(
                    created_by="unittest@fluidattacks.com",
                    created_date=datetime.fromisoformat(
                        "2018-11-27T19:54:08+00:00"
                    ),
                    finding_id="457497316",
                    group_name="unittesting",
                    hacker_email="unittest@fluidattacks.com",
                    id="6192c72f-2e10-4259-9207-717b2d90d8d2",
                    state=VulnerabilityState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2019-09-16T14:40:37+00:00"
                        ),
                        source=Source.ASM,
                        specific="userToken",
                        status=VulnerabilityStateStatus.SAFE,
                        where="https://10.1.1.1/",
                        commit=None,
                        reasons=None,
                        other_reason=None,
                        tool=None,
                        snippet=None,
                    ),
                    type=VulnerabilityType.INPUTS,
                    bug_tracking_system_url=None,
                    custom_severity=None,
                    developer=None,
                    event_id=None,
                    hash=None,
                    root_id=None,
                    skims_method=None,
                    skims_technique=None,
                    stream=None,
                    tags=None,
                    treatment=VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2018-11-27T19:54:08+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.UNTREATED,
                        acceptance_status=None,
                        accepted_until=None,
                        justification=None,
                        assigned=None,
                        modified_by=None,
                    ),
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_closing_date=datetime.fromisoformat(
                            "2019-09-16T14:40:37+00:00"
                        ),
                        unreliable_source=Source.ASM,
                        unreliable_efficacy=Decimal("0"),
                        unreliable_last_reattack_date=None,
                        unreliable_last_reattack_requester=None,
                        unreliable_last_requested_reattack_date=None,
                        unreliable_reattack_cycles=0,
                        unreliable_treatment_changes=0,
                    ),
                    verification=None,
                    zero_risk=None,
                ),
                Vulnerability(
                    created_by="unittest@fluidattacks.com",
                    created_date=datetime.fromisoformat(
                        "2019-09-13T14:58:38+00:00"
                    ),
                    finding_id="463461507",
                    group_name="unittesting",
                    hacker_email="unittest@fluidattacks.com",
                    id="09afd608-aa53-4bbc-9094-0076181fa0ea",
                    state=VulnerabilityState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2019-09-13T14:58:38+00:00"
                        ),
                        source=Source.ASM,
                        specific="3636",
                        status=VulnerabilityStateStatus.VULNERABLE,
                        where="192.168.100.105",
                        commit=None,
                        reasons=None,
                        other_reason=None,
                        tool=None,
                        snippet=None,
                    ),
                    type=VulnerabilityType.PORTS,
                    bug_tracking_system_url=None,
                    custom_severity=None,
                    developer=None,
                    event_id=None,
                    hash=None,
                    root_id=None,
                    skims_method=None,
                    skims_technique=None,
                    stream=None,
                    tags=None,
                    treatment=VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2019-09-13T14:58:38+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.UNTREATED,
                        acceptance_status=None,
                        accepted_until=None,
                        justification=None,
                        assigned=None,
                        modified_by=None,
                    ),
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_closing_date=None,
                        unreliable_source=Source.ASM,
                        unreliable_efficacy=Decimal("0"),
                        unreliable_last_reattack_date=None,
                        unreliable_last_reattack_requester=None,
                        unreliable_last_requested_reattack_date=None,
                        unreliable_reattack_cycles=0,
                        unreliable_treatment_changes=0,
                    ),
                    verification=None,
                    zero_risk=None,
                ),
                Vulnerability(
                    created_by="unittest@fluidattacks.com",
                    created_date=datetime.fromisoformat(
                        "2019-09-12T13:45:48+00:00"
                    ),
                    finding_id="463461507",
                    group_name="unittesting",
                    hacker_email="unittest@fluidattacks.com",
                    id="e248e8e0-0323-41c7-bc02-4ee61d09f9c4",
                    state=VulnerabilityState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2019-09-12T13:45:48+00:00"
                        ),
                        source=Source.ASM,
                        specific="7777",
                        status=VulnerabilityStateStatus.VULNERABLE,
                        where="192.168.1.18",
                        commit=None,
                        reasons=None,
                        other_reason=None,
                        tool=None,
                        snippet=None,
                    ),
                    type=VulnerabilityType.PORTS,
                    bug_tracking_system_url=None,
                    custom_severity=None,
                    developer=None,
                    event_id=None,
                    hash=None,
                    root_id=None,
                    skims_method=None,
                    skims_technique=None,
                    stream=None,
                    tags=None,
                    treatment=VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2019-09-13T13:45:48+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.ACCEPTED,
                        acceptance_status=None,
                        accepted_until=datetime.fromisoformat(
                            "2021-01-16T17:46:10+00:00"
                        ),
                        justification="accepted justification",
                        assigned="integratesuser@gmail.com",
                        modified_by="integratesuser@gmail.com",
                    ),
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_closing_date=None,
                        unreliable_source=Source.ASM,
                        unreliable_efficacy=Decimal("0"),
                        unreliable_last_reattack_date=None,
                        unreliable_last_reattack_requester=None,
                        unreliable_last_requested_reattack_date=None,
                        unreliable_reattack_cycles=0,
                        unreliable_treatment_changes=2,
                    ),
                    verification=None,
                    zero_risk=None,
                ),
            ]
        ),
        '["unittesting", "4", "6.9"]': tuple(
            [
                Vulnerability(
                    created_by="unittest@fluidattacks.com",
                    created_date=datetime.fromisoformat(
                        "2019-01-15T15:43:39+00:00"
                    ),
                    finding_id="463558592",
                    group_name="unittesting",
                    hacker_email="unittest@fluidattacks.com",
                    id="0a848781-b6a4-422e-95fa-692151e6a98e",
                    state=VulnerabilityState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2019-01-15T15:43:39+00:00"
                        ),
                        source=Source.ASM,
                        specific="12",
                        status=VulnerabilityStateStatus.VULNERABLE,
                        where="path/to/file2.ext",
                        commit=None,
                        reasons=None,
                        other_reason=None,
                        tool=None,
                        snippet=None,
                    ),
                    type=VulnerabilityType.LINES,
                    bug_tracking_system_url=None,
                    custom_severity=None,
                    developer=None,
                    event_id=None,
                    hash=None,
                    root_id=None,
                    skims_method=None,
                    skims_technique=None,
                    stream=None,
                    tags=None,
                    treatment=VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2019-01-15T15:43:39+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.ACCEPTED,
                        acceptance_status=None,
                        accepted_until=datetime.fromisoformat(
                            "2021-01-16T17:46:10+00:00"
                        ),
                        justification="This is a treatment justification test",
                        assigned="integratesuser@gmail.com",
                        modified_by="integratesuser@gmail.com",
                    ),
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_closing_date=None,
                        unreliable_source=Source.ASM,
                        unreliable_efficacy=Decimal("0"),
                        unreliable_last_reattack_date=None,
                        unreliable_last_reattack_requester=None,
                        unreliable_last_requested_reattack_date=None,
                        unreliable_reattack_cycles=0,
                        unreliable_treatment_changes=1,
                    ),
                    verification=None,
                    zero_risk=None,
                ),
                Vulnerability(
                    created_by="unittest@fluidattacks.com",
                    created_date=datetime.fromisoformat(
                        "2019-01-15T16:04:14+00:00"
                    ),
                    finding_id="463558592",
                    group_name="unittesting",
                    hacker_email="unittest@fluidattacks.com",
                    id="242f848c-148a-4028-8e36-c7d995502590",
                    state=VulnerabilityState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2019-01-15T20:59:16+00:00"
                        ),
                        source=Source.ASM,
                        specific="12456",
                        status=VulnerabilityStateStatus.SAFE,
                        where="path/to/file2.ext",
                        commit=None,
                        reasons=None,
                        other_reason=None,
                        tool=None,
                        snippet=None,
                    ),
                    type=VulnerabilityType.LINES,
                    bug_tracking_system_url=None,
                    custom_severity=None,
                    developer=None,
                    event_id=None,
                    hash=None,
                    root_id=None,
                    skims_method=None,
                    skims_technique=None,
                    stream=None,
                    tags=None,
                    treatment=VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2019-01-15T16:04:14+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.UNTREATED,
                        acceptance_status=None,
                        justification=None,
                        assigned=None,
                        modified_by=None,
                    ),
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_closing_date=datetime.fromisoformat(
                            "2019-01-15T20:59:16+00:00"
                        ),
                        unreliable_source=Source.ASM,
                        unreliable_efficacy=Decimal("0"),
                        unreliable_last_reattack_date=None,
                        unreliable_last_reattack_requester=None,
                        unreliable_last_requested_reattack_date=None,
                        unreliable_reattack_cycles=0,
                        unreliable_treatment_changes=0,
                    ),
                    verification=None,
                    zero_risk=None,
                ),
                Vulnerability(
                    created_by="unittest@fluidattacks.com",
                    created_date=datetime.fromisoformat(
                        "2019-01-16T13:47:07+00:00"
                    ),
                    finding_id="463558592",
                    group_name="unittesting",
                    hacker_email="unittest@fluidattacks.com",
                    id="3bcdb384-5547-4170-a0b6-3b397a245465",
                    state=VulnerabilityState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2019-01-16T13:47:07+00:00"
                        ),
                        source=Source.ASM,
                        specific="345",
                        status=VulnerabilityStateStatus.VULNERABLE,
                        where="path/to/file3.ext",
                        commit=None,
                        reasons=None,
                        other_reason=None,
                        tool=None,
                        snippet=None,
                    ),
                    type=VulnerabilityType.LINES,
                    bug_tracking_system_url=None,
                    custom_severity=None,
                    developer=None,
                    event_id=None,
                    hash=None,
                    root_id="4039d098-ffc5-4984-8ed3-eb17bca98e19",
                    skims_method=None,
                    skims_technique=None,
                    stream=None,
                    tags=None,
                    treatment=VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2019-01-16T13:47:07+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.UNTREATED,
                        acceptance_status=None,
                        accepted_until=None,
                        justification=None,
                        assigned=None,
                        modified_by=None,
                    ),
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_closing_date=None,
                        unreliable_source=Source.ASM,
                        unreliable_efficacy=Decimal("0"),
                        unreliable_last_reattack_date=None,
                        unreliable_last_reattack_requester="integratesuser@gmail.com",  # noqa: E501 pylint: disable=line-too-long
                        unreliable_last_requested_reattack_date=datetime.fromisoformat(  # noqa: E501 pylint: disable=line-too-long
                            "2020-02-19T15:41:04+00:00"
                        ),
                        unreliable_reattack_cycles=1,
                        unreliable_treatment_changes=0,
                    ),
                    verification=VulnerabilityVerification(
                        modified_date=datetime.fromisoformat(
                            "2020-02-19T15:41:04+00:00"
                        ),
                        status=VulnerabilityVerificationStatus.REQUESTED,
                        event_id=None,
                    ),
                    zero_risk=VulnerabilityZeroRisk(
                        comment_id="123456",
                        modified_by="test@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2018-09-28T15:32:58+00:00"
                        ),
                        status=VulnerabilityZeroRiskStatus.REQUESTED,
                    ),
                ),
                Vulnerability(
                    created_by="unittest@fluidattacks.com",
                    created_date=datetime.fromisoformat(
                        "2019-01-16T13:47:07+00:00"
                    ),
                    finding_id="463558592",
                    group_name="unittesting",
                    hacker_email="unittest@fluidattacks.com",
                    id="54b94fa0-8f4f-4b10-a38a-6e848a9eb0c6",
                    state=VulnerabilityState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2019-01-16T13:47:07+00:00"
                        ),
                        source=Source.ASM,
                        specific="564",
                        status=VulnerabilityStateStatus.VULNERABLE,
                        where="path/to/file4.ext",
                        commit=None,
                        reasons=None,
                        other_reason=None,
                        tool=None,
                        snippet=None,
                    ),
                    type=VulnerabilityType.LINES,
                    bug_tracking_system_url=None,
                    custom_severity=None,
                    developer=None,
                    event_id=None,
                    hash=None,
                    root_id=None,
                    skims_method=None,
                    skims_technique=None,
                    stream=None,
                    tags=["test1", "test2"],
                    treatment=VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2020-10-13T17:46:10+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.ACCEPTED,
                        acceptance_status=None,
                        accepted_until=datetime.fromisoformat(
                            "2021-01-16T17:46:10+00:00"
                        ),
                        justification="This is a treatment justification test",
                        assigned="integratesuser@gmail.com",
                        modified_by="integratesuser@gmail.com",
                    ),
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_closing_date=None,
                        unreliable_source=Source.ASM,
                        unreliable_efficacy=Decimal("0"),
                        unreliable_last_reattack_date=None,
                        unreliable_last_reattack_requester=None,
                        unreliable_last_requested_reattack_date=None,
                        unreliable_reattack_cycles=0,
                        unreliable_treatment_changes=1,
                    ),
                    verification=None,
                    zero_risk=VulnerabilityZeroRisk(
                        comment_id="123456",
                        modified_by="test@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2018-09-28T15:32:58+00:00"
                        ),
                        status=VulnerabilityZeroRiskStatus.REQUESTED,
                    ),
                ),
                Vulnerability(
                    created_by="unittest@fluidattacks.com",
                    created_date=datetime.fromisoformat(
                        "2019-01-15T16:04:14+00:00"
                    ),
                    finding_id="463558592",
                    group_name="unittesting",
                    hacker_email="unittest@fluidattacks.com",
                    id="6f023c26-5b10-4ded-aa27-bb563c2206ab",
                    state=VulnerabilityState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2019-01-15T20:59:16+00:00"
                        ),
                        source=Source.ASM,
                        specific="123345",
                        status=VulnerabilityStateStatus.SAFE,
                        where="test/test#.config",
                        commit=None,
                        reasons=None,
                        other_reason=None,
                        tool=None,
                        snippet=None,
                    ),
                    type=VulnerabilityType.LINES,
                    bug_tracking_system_url=None,
                    custom_severity=None,
                    developer=None,
                    event_id=None,
                    hash=None,
                    root_id="4039d098-ffc5-4984-8ed3-eb17bca98e19",
                    skims_method=None,
                    skims_technique=None,
                    stream=None,
                    tags=None,
                    treatment=VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2020-10-13T17:46:10+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.ACCEPTED,
                        acceptance_status=None,
                        accepted_until=datetime.fromisoformat(
                            "2021-01-16T17:46:10+00:00"
                        ),
                        justification="This is a treatment justification test",
                        assigned="integratesuser@gmail.com",
                        modified_by="integratesuser@gmail.com",
                    ),
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_closing_date=datetime.fromisoformat(
                            "2019-01-15T20:59:16+00:00"
                        ),
                        unreliable_source=Source.ASM,
                        unreliable_efficacy=Decimal("0"),
                        unreliable_last_reattack_date=None,
                        unreliable_last_reattack_requester=None,
                        unreliable_last_requested_reattack_date=None,
                        unreliable_reattack_cycles=0,
                        unreliable_treatment_changes=1,
                    ),
                    verification=None,
                    zero_risk=VulnerabilityZeroRisk(
                        comment_id="123456",
                        modified_by="test@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2018-09-28T15:32:58+00:00"
                        ),
                        status=VulnerabilityZeroRiskStatus.REQUESTED,
                    ),
                ),
                Vulnerability(
                    created_by="unittest@fluidattacks.com",
                    created_date=datetime.fromisoformat(
                        "2019-01-15T15:43:39+00:00"
                    ),
                    finding_id="463558592",
                    group_name="unittesting",
                    hacker_email="unittest@fluidattacks.com",
                    id="74632c0c-db08-47c2-b013-c70e5b67c49f",
                    state=VulnerabilityState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2019-01-15T15:43:39+00:00"
                        ),
                        source=Source.ASM,
                        specific="123",
                        status=VulnerabilityStateStatus.VULNERABLE,
                        where="test/test#.config",
                        commit=None,
                        reasons=None,
                        other_reason=None,
                        tool=None,
                        snippet=None,
                    ),
                    type=VulnerabilityType.LINES,
                    bug_tracking_system_url=None,
                    custom_severity=None,
                    developer=None,
                    event_id=None,
                    hash=None,
                    root_id="4039d098-ffc5-4984-8ed3-eb17bca98e19",
                    skims_method=None,
                    skims_technique=None,
                    stream=None,
                    tags=None,
                    treatment=VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2020-10-13T17:46:10+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.ACCEPTED,
                        acceptance_status=None,
                        accepted_until=datetime.fromisoformat(
                            "2021-01-16T17:46:10+00:00"
                        ),
                        justification="This is a treatment justification test",
                        assigned="integratesuser2@gmail.com",
                        modified_by="integratesuser2@gmail.com",
                    ),
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_closing_date=None,
                        unreliable_source=Source.ASM,
                        unreliable_efficacy=Decimal("0"),
                        unreliable_last_reattack_date=None,
                        unreliable_last_reattack_requester="integratesuser@gmail.com",  # noqa: E501 pylint: disable=line-too-long
                        unreliable_last_requested_reattack_date=datetime.fromisoformat(  # noqa: E501 pylint: disable=line-too-long
                            "2020-02-19T15:41:04+00:00"
                        ),
                        unreliable_reattack_cycles=1,
                        unreliable_treatment_changes=1,
                    ),
                    verification=VulnerabilityVerification(
                        modified_date=datetime.fromisoformat(
                            "2020-02-19T15:41:04+00:00"
                        ),
                        status=VulnerabilityVerificationStatus.REQUESTED,
                        event_id=None,
                    ),
                    zero_risk=VulnerabilityZeroRisk(
                        comment_id="123456",
                        modified_by="test@gmail.com",
                        modified_date=datetime.fromisoformat(
                            "2018-09-28T15:32:58+00:00"
                        ),
                        status=VulnerabilityZeroRiskStatus.REQUESTED,
                    ),
                ),
                Vulnerability(
                    created_by="unittest@fluidattacks.com",
                    created_date=datetime.fromisoformat(
                        "2019-04-08T00:45:15+00:00"
                    ),
                    finding_id="988493279",
                    group_name="unittesting",
                    hacker_email="unittest@fluidattacks.com",
                    id="47ce0fb0-4108-49b0-93cc-160dce8168a6",
                    state=VulnerabilityState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2019-04-08T00:45:15+00:00"
                        ),
                        source=Source.ASM,
                        specific="8888",
                        status=VulnerabilityStateStatus.VULNERABLE,
                        where="192.168.1.19",
                        commit=None,
                        reasons=None,
                        other_reason=None,
                        tool=VulnerabilityTool(
                            name="tool-1",
                            impact=VulnerabilityToolImpact.INDIRECT,
                        ),
                        snippet=None,
                    ),
                    type=VulnerabilityType.PORTS,
                    bug_tracking_system_url=None,
                    custom_severity=None,
                    developer=None,
                    event_id=None,
                    hash=None,
                    root_id="4039d098-ffc5-4984-8ed3-eb17bca98e19",
                    skims_method=None,
                    skims_technique=None,
                    stream=None,
                    tags=None,
                    treatment=VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2020-10-08T00:59:06+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.ACCEPTED_UNDEFINED,
                        acceptance_status=VulnerabilityAcceptanceStatus.APPROVED,  # noqa: E501 pylint: disable=line-too-long
                        accepted_until=None,
                        justification="Observations about permanently "
                        "accepted",
                        assigned="integratesuser@gmail.com",
                        modified_by="integratesuser@gmail.com",
                    ),
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_closing_date=None,
                        unreliable_source=Source.ASM,
                        unreliable_efficacy=Decimal("0"),
                        unreliable_last_reattack_date=None,
                        unreliable_last_reattack_requester=None,
                        unreliable_last_requested_reattack_date=None,
                        unreliable_reattack_cycles=0,
                        unreliable_treatment_changes=2,
                    ),
                    verification=None,
                    zero_risk=None,
                ),
                Vulnerability(
                    created_by="unittest@fluidattacks.com",
                    created_date=datetime.fromisoformat(
                        "2019-04-08T00:45:15+00:00"
                    ),
                    finding_id="988493279",
                    group_name="unittesting",
                    hacker_email="unittest@fluidattacks.com",
                    id="69b84d52-1b18-41fa-84b5-bcb8134cb1ec",
                    state=VulnerabilityState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2019-08-07T13:45:48+00:00"
                        ),
                        source=Source.ASM,
                        specific="9999",
                        status=VulnerabilityStateStatus.SAFE,
                        where="192.168.1.20",
                        commit=None,
                        reasons=None,
                        other_reason=None,
                        tool=VulnerabilityTool(
                            name="tool-1",
                            impact=VulnerabilityToolImpact.INDIRECT,
                        ),
                        snippet=None,
                    ),
                    type=VulnerabilityType.PORTS,
                    bug_tracking_system_url=None,
                    custom_severity=None,
                    developer=None,
                    event_id=None,
                    hash=None,
                    root_id=None,
                    skims_method=None,
                    skims_technique=None,
                    stream=None,
                    tags=None,
                    treatment=VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2020-11-08T00:59:06+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.ACCEPTED,
                        acceptance_status=None,
                        accepted_until=datetime.fromisoformat(
                            "2021-04-08T00:59:06+00:00"
                        ),
                        justification="test justification temporarily "
                        "accepted",
                        assigned="integratesuser2@gmail.com",
                        modified_by="integratesuser@gmail.com",
                    ),
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_closing_date=datetime.fromisoformat(
                            "2019-08-07T13:45:48+00:00"
                        ),
                        unreliable_source=Source.ASM,
                        unreliable_efficacy=Decimal("0"),
                        unreliable_last_reattack_date=None,
                        unreliable_last_reattack_requester=None,
                        unreliable_last_requested_reattack_date=None,
                        unreliable_reattack_cycles=0,
                        unreliable_treatment_changes=1,
                    ),
                    verification=None,
                    zero_risk=None,
                ),
            ]
        ),
    },
    "db_model.vulnerabilities.get.FindingVulnerabilitiesReleasedNonZeroRiskLoader.load": {  # noqa: E501 pylint: disable=line-too-long
        '["422286126"]': [
            Vulnerability(
                created_by="unittest@fluidattacks.com",
                created_date=datetime.fromisoformat(
                    "2020-01-03T17:46:10+00:00"
                ),
                finding_id="422286126",
                group_name="unittesting",
                hacker_email="unittest@fluidattacks.com",
                id="0a848781-b6a4-422e-95fa-692151e6a98z",
                state=VulnerabilityState(
                    modified_by="unittest@fluidattacks.com",
                    modified_date=datetime.fromisoformat(
                        "2020-01-03T17:46:10+00:00"
                    ),
                    source=Source.ASM,
                    specific="12",
                    status=VulnerabilityStateStatus.VULNERABLE,
                    where="test/data/lib_path/f060/csharp.cs",
                    commit="ea871eee64cfd5ce293411efaf4d3b446d04eb4a",
                    reasons=None,
                    other_reason=None,
                    tool=VulnerabilityTool(
                        name="tool-2",
                        impact=VulnerabilityToolImpact.INDIRECT,
                    ),
                    snippet=None,
                ),
                type=VulnerabilityType.LINES,
                bug_tracking_system_url=None,
                custom_severity=None,
                developer=None,
                event_id=None,
                hash=None,
                root_id=None,
                skims_method=None,
                skims_technique=None,
                stream=None,
                tags=None,
                treatment=VulnerabilityTreatment(
                    modified_date=datetime.fromisoformat(
                        "2020-01-03T17:46:10+00:00"
                    ),
                    status=VulnerabilityTreatmentStatus.IN_PROGRESS,
                    acceptance_status=None,
                    accepted_until=None,
                    justification="test justification",
                    assigned="integratesuser2@gmail.com",
                    modified_by="integratesuser@gmail.com",
                ),
                unreliable_indicators=VulnerabilityUnreliableIndicators(
                    unreliable_closing_date=None,
                    unreliable_source=Source.ASM,
                    unreliable_efficacy=Decimal("0"),
                    unreliable_last_reattack_date=None,
                    unreliable_last_reattack_requester=None,
                    unreliable_last_requested_reattack_date=None,
                    unreliable_reattack_cycles=0,
                    unreliable_treatment_changes=1,
                ),
                verification=None,
                zero_risk=None,
            ),
        ],
        '["988493279"]': [
            Vulnerability(
                created_by="unittest@fluidattacks.com",
                created_date=datetime.fromisoformat(
                    "2019-04-08T00:45:15+00:00"
                ),
                finding_id="988493279",
                group_name="unittesting",
                hacker_email="unittest@fluidattacks.com",
                id="47ce0fb0-4108-49b0-93cc-160dce8168a6",
                state=VulnerabilityState(
                    modified_by="unittest@fluidattacks.com",
                    modified_date=datetime.fromisoformat(
                        "2019-04-08T00:45:15+00:00"
                    ),
                    source=Source.ASM,
                    specific="8888",
                    status=VulnerabilityStateStatus.VULNERABLE,
                    where="192.168.1.19",
                    commit=None,
                    reasons=None,
                    other_reason=None,
                    tool=VulnerabilityTool(
                        name="tool-1",
                        impact=VulnerabilityToolImpact.INDIRECT,
                    ),
                    snippet=None,
                ),
                type=VulnerabilityType.PORTS,
                bug_tracking_system_url=None,
                custom_severity=None,
                developer=None,
                event_id=None,
                hash=None,
                root_id="4039d098-ffc5-4984-8ed3-eb17bca98e19",
                skims_method=None,
                skims_technique=None,
                stream=None,
                tags=None,
                treatment=VulnerabilityTreatment(
                    modified_date=datetime.fromisoformat(
                        "2020-10-08T00:59:06+00:00"
                    ),
                    status=VulnerabilityTreatmentStatus.ACCEPTED_UNDEFINED,
                    acceptance_status=VulnerabilityAcceptanceStatus.APPROVED,
                    accepted_until=None,
                    justification="Observations about permanently accepted",
                    assigned="integratesuser@gmail.com",
                    modified_by="integratesuser@gmail.com",
                ),
                unreliable_indicators=VulnerabilityUnreliableIndicators(
                    unreliable_closing_date=None,
                    unreliable_source=Source.ASM,
                    unreliable_efficacy=Decimal("0"),
                    unreliable_last_reattack_date=None,
                    unreliable_last_reattack_requester=None,
                    unreliable_last_requested_reattack_date=None,
                    unreliable_reattack_cycles=0,
                    unreliable_treatment_changes=2,
                ),
                verification=None,
                zero_risk=None,
            ),
            Vulnerability(
                created_by="unittest@fluidattacks.com",
                created_date=datetime.fromisoformat(
                    "2019-04-08T00:45:15+00:00"
                ),
                finding_id="988493279",
                group_name="unittesting",
                hacker_email="unittest@fluidattacks.com",
                id="69b84d52-1b18-41fa-84b5-bcb8134cb1ec",
                state=VulnerabilityState(
                    modified_by="unittest@fluidattacks.com",
                    modified_date=datetime.fromisoformat(
                        "2019-08-07T13:45:48+00:00"
                    ),
                    source=Source.ASM,
                    specific="9999",
                    status=VulnerabilityStateStatus.SAFE,
                    where="192.168.1.20",
                    commit=None,
                    reasons=None,
                    other_reason=None,
                    tool=VulnerabilityTool(
                        name="tool-1",
                        impact=VulnerabilityToolImpact.INDIRECT,
                    ),
                    snippet=None,
                ),
                type=VulnerabilityType.PORTS,
                bug_tracking_system_url=None,
                custom_severity=None,
                developer=None,
                event_id=None,
                hash=None,
                root_id=None,
                skims_method=None,
                skims_technique=None,
                stream=None,
                tags=None,
                treatment=VulnerabilityTreatment(
                    modified_date=datetime.fromisoformat(
                        "2020-11-08T00:59:06+00:00"
                    ),
                    status=VulnerabilityTreatmentStatus.ACCEPTED,
                    acceptance_status=None,
                    accepted_until=datetime.fromisoformat(
                        "2021-04-08T00:59:06+00:00"
                    ),
                    justification="test justification temporarily accepted",
                    assigned="integratesuser2@gmail.com",
                    modified_by="integratesuser@gmail.com",
                ),
                unreliable_indicators=VulnerabilityUnreliableIndicators(
                    unreliable_closing_date=datetime.fromisoformat(
                        "2019-08-07T13:45:48+00:00"
                    ),
                    unreliable_source=Source.ASM,
                    unreliable_efficacy=Decimal("0"),
                    unreliable_last_reattack_date=None,
                    unreliable_last_reattack_requester=None,
                    unreliable_last_requested_reattack_date=None,
                    unreliable_reattack_cycles=0,
                    unreliable_treatment_changes=1,
                ),
                verification=None,
                zero_risk=None,
            ),
        ],
    },
    "db_model.vulnerabilities.get.FindingVulnerabilitiesReleasedNonZeroRiskLoader.load_many_chained": {  # noqa: E501 pylint: disable=line-too-long
        '["463558592", "422286126"]': tuple(
            (
                Vulnerability(
                    created_by="unittest@fluidattacks.com",
                    created_date=datetime.fromisoformat(
                        "2019-01-15T15:43:39+00:00"
                    ),
                    finding_id="463558592",
                    group_name="unittesting",
                    hacker_email="unittest@fluidattacks.com",
                    id="0a848781-b6a4-422e-95fa-692151e6a98e",
                    state=VulnerabilityState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2019-01-15T15:43:39+00:00"
                        ),
                        source=Source.ASM,
                        specific="12",
                        status=VulnerabilityStateStatus.VULNERABLE,
                        where="path/to/file2.exe",
                        commit=None,
                        reasons=None,
                        tool=None,
                        snippet=None,
                    ),
                    type=VulnerabilityType.LINES,
                    bug_tracking_system_url=None,
                    custom_severity=None,
                    developer=None,
                    event_id=None,
                    hash=None,
                    root_id=None,
                    skims_method=None,
                    skims_technique=None,
                    stream=None,
                    tags=None,
                    treatment=VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2019-01-15T15:43:39+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.ACCEPTED,
                        acceptance_status=None,
                        accepted_until=datetime.fromisoformat(
                            "2021-01-16T17:46:10+00:00"
                        ),
                        justification="This is a treatment justification test",
                        assigned="integratesuser@gmail.comm",
                        modified_by="integratesuser@gmail.com",
                    ),
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_closing_date=None,
                        unreliable_source=Source.ASM,
                        unreliable_efficacy=Decimal("0"),
                        unreliable_last_reattack_date=None,
                        unreliable_last_reattack_requester=None,
                        unreliable_last_requested_reattack_date=None,
                        unreliable_reattack_cycles=0,
                        unreliable_treatment_changes=1,
                    ),
                    verification=None,
                    zero_risk=None,
                ),
                Vulnerability(
                    created_by="unittest@fluidattacks.com",
                    created_date=datetime.fromisoformat(
                        "2019-01-15T16:04:14+00:00"
                    ),
                    finding_id="463558592",
                    group_name="unittesting",
                    hacker_email="unittest@fluidattacks.com",
                    id="242f848c-148a-4028-8e36-c7d995502590",
                    state=VulnerabilityState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2019-01-15T20:59:16+00:00"
                        ),
                        source=Source.ASM,
                        specific="123456",
                        status=VulnerabilityStateStatus.SAFE,
                        where="path/to/file2.ext",
                        commit=None,
                        reasons=None,
                        tool=None,
                        snippet=None,
                    ),
                    type=VulnerabilityType.LINES,
                    bug_tracking_system_url=None,
                    custom_severity=None,
                    developer=None,
                    event_id=None,
                    hash=None,
                    root_id=None,
                    skims_method=None,
                    skims_technique=None,
                    stream=None,
                    tags=None,
                    treatment=VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2019-01-15T15:43:39+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.UNTREATED,
                        acceptance_status=None,
                        accepted_until=None,
                        justification=None,
                        assigned=None,
                        modified_by=None,
                    ),
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_closing_date=None,
                        unreliable_source=Source.ASM,
                        unreliable_efficacy=Decimal("0"),
                        unreliable_last_reattack_date=None,
                        unreliable_last_reattack_requester=None,
                        unreliable_last_requested_reattack_date=None,
                        unreliable_reattack_cycles=0,
                        unreliable_treatment_changes=0,
                    ),
                    verification=None,
                    zero_risk=None,
                ),
                Vulnerability(
                    created_by="unittest@fluidattacks.com",
                    created_date=datetime.fromisoformat(
                        "2020-01-03T17:46:10+00:00"
                    ),
                    finding_id="422286126",
                    group_name="unittesting",
                    hacker_email="unittest@fluidattacks.com",
                    id="0a848781-b6a4-422e-95fa-692151e6a98z",
                    state=VulnerabilityState(
                        modified_by="unittest@fluidattacks.com",
                        modified_date=datetime.fromisoformat(
                            "2020-01-03T17:46:10+00:00"
                        ),
                        source=Source.ASM,
                        specific="12",
                        status=VulnerabilityStateStatus.VULNERABLE,
                        where="test/data/lib_path/f060/csharp.cs",
                        commit=None,
                        reasons=None,
                        tool=VulnerabilityTool(
                            name="tool-2",
                            impact=VulnerabilityToolImpact.INDIRECT,
                        ),
                        snippet=None,
                    ),
                    type=VulnerabilityType.LINES,
                    bug_tracking_system_url=None,
                    custom_severity=None,
                    developer=None,
                    event_id=None,
                    hash=None,
                    root_id=None,
                    skims_method=None,
                    skims_technique=None,
                    stream=None,
                    tags=None,
                    treatment=VulnerabilityTreatment(
                        modified_date=datetime.fromisoformat(
                            "2020-01-03T17:46:10+00:00"
                        ),
                        status=VulnerabilityTreatmentStatus.IN_PROGRESS,
                        acceptance_status=None,
                        accepted_until=None,
                        justification="test justification",
                        assigned="integratesuser2@gmail.com",
                        modified_by="integratesuser@gmail.com",
                    ),
                    unreliable_indicators=VulnerabilityUnreliableIndicators(
                        unreliable_closing_date=None,
                        unreliable_source=Source.ASM,
                        unreliable_efficacy=Decimal("0"),
                        unreliable_last_reattack_date=None,
                        unreliable_last_reattack_requester=None,
                        unreliable_last_requested_reattack_date=None,
                        unreliable_reattack_cycles=0,
                        unreliable_treatment_changes=1,
                    ),
                    verification=None,
                    zero_risk=None,
                ),
            )
        )
    },
    "db_model.vulnerabilities.remove": {
        '["80d6a69f-a376-46be-98cd-2fdedcffdcc0"]': None,
    },
    "events.domain.remove_file_evidence": {
        '["418900978", "oneshottest"]': None,
        '["538745942", "unittesting"]': None,
    },
    "events.domain.replace_different_format": {
        '["418900978", "FILE_1"]': None,
        '["538745942", "FILE_1"]': None,
    },
    "events.domain.save_evidence": {
        '["418900978", "test-file-records.csv"]': None,
        '["538745942", "test-file-records.csv"]': None,
    },
    "events.domain.search_evidence": {
        '["418900978", "oneshottest"]': [
            "evidences/oneshottest/418900978/oneshottest-418900978-records.csv"
        ],
        '["538745942", "unittesting"]': [
            "evidences/unittesting/538745942/unittesting-538745942-records.csv"
        ],
    },
    "events.domain.update_evidence": {
        '["test-anim.webm"]': None,
        '["test-file-records.csv"]': None,
    },
    "events.domain.validate_evidence": {
        '["unittesting", "test-anim.webm"]': None,
        '["unittesting", "test-file-records.csv"]': None,
    },
    "event_comments.domain.add": {
        '[["538745942", "1672323259183", "0", '
        '"2022-12-29 14:14:19.182591+00:00", '
        '"comment test", "integratesmanager@gmail.com", "John Doe"]]': None,
    },
    "event_comments.domain.remove_comments": {
        '["418900978"]': None,
        '["538745942"]': None,
    },
    "finding_comments.domain.remove_comments": {
        '["457497316"]': None,
    },
    "findings.domain.core.remove_all_evidences": {
        '["457497316", "unittesting"]': None,
    },
    "findings.domain.evidence.download_evidence_file": {
        '["unittesting", "422286126",'
        ' "unittesting-422286126-evidence_file.csv"]': os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "findings/domain/tmp_mock/unittesting-422286126-evidence_file.csv",
        )
    },
    "findings.storage.search_evidence": {
        '["unittesting", "422286126",'
        ' "unittesting-422286126-evidence_route_1.png"]': [
            {
                "ResponseMetadata": {
                    "HTTPStatusCode": 200,
                    "HTTPHeaders": {},
                    "RetryAttempts": 0,
                },
                "IsTruncated": False,
                "Contents": [
                    {
                        "Key": "evidences/unittesting/422286126/"
                        "unittesting-422286126-evidence_file.csv",
                        "LastModified": "2019-01-15T15:43:39+00:00",
                        "ETag": '"a008e27edeaaf560cc01ef094edbbd65"',
                        "Size": 132,
                        "StorageClass": "STANDARD",
                    },
                    {
                        "Key": "evidences/unittesting/422286126/"
                        "unittesting-422286126-evidence_route_1.png",
                        "LastModified": "2020-01-03T17:46:10+00:00",
                        "ETag": '"98a8fa986a52960e0ae1e990afd06510"',
                        "Size": 16629,
                        "StorageClass": "STANDARD",
                    },
                ],
                "Name": "integrates.somedeveloperatfluid",
                "Prefix": "",
                "MaxKeys": 1000,
                "KeyCount": 2,
            }
        ]
    },
    "findings.storage.download_evidence": {
        '["unittesting", "422286126",'
        ' "unittesting-422286126-evidence_route_1.png"]': None,
    },
    "findings.domain.core.get_open_vulnerabilities": {
        '["463558592", "422286126"]': 1
    },
    "groups.domain.update_metadata": {
        '["unittesting", "mock_token", '
        '"ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3"]': None,
    },
    "groups.domain.update_state": {
        '["unittesting", "integratesmanager@gmail.com"]': None,
        '["unittesting", "ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3", '
        '"integratesmanager@gmail.com", "2022-04-06 16:46:23+00:00"]': None,
    },
    "group_access.domain.add_access": {
        '["org_testgroupmanager2@fluidattacks.com", '
        '"ORG#f2e2777d-a168-4bea-93cd-d79142b294d2", '
        '"customer_manager"]': None,
    },
    "group_access.domain.authz.get_group_level_role": {
        '["oneshottest"]': [
            "user_manager",
            "reattacker",
            "admin",
            "admin",
            "user",
        ],
    },
    "group_access.domain.authz.grant_group_level_role": {
        '["unittest@fluidattacks.com", "unittesting", "user"]': None,
    },
    "group_access.domain.Dataloaders.group_access": {
        '["unittesting", "unittest@fluidattacks.com"]': GroupAccess(
            email="unittest@fluidattacks.com",
            group_name="unittesting",
            state=GroupAccessState(
                modified_date=datetime.fromisoformat(
                    "2020-01-01T20:24:25+00:00"
                )
            ),
            confirm_deletion=None,
            expiration_time=None,
            has_access=True,
            invitation=None,
            responsibility="Tester",
            role=None,
        ),
    },
    "group_access.domain.Dataloaders.group_stakeholders_access": {
        '["unittesting"]': [
            GroupAccess(
                email="continuoushack2@gmail.com",
                group_name="unittesting",
                state=GroupAccessState(
                    modified_date=datetime.fromisoformat(
                        "2020-01-01T20:07:57+00:00"
                    )
                ),
                confirm_deletion=None,
                expiration_time=None,
                has_access=True,
                invitation=None,
                responsibility="Test",
                role="user_manager",
            ),
            GroupAccess(
                email="continuoushacking@gmail.com",
                group_name="unittesting",
                state=GroupAccessState(
                    modified_date=datetime.fromisoformat(
                        "2020-01-01T20:07:57+00:00"
                    )
                ),
                confirm_deletion=None,
                expiration_time=None,
                has_access=True,
                invitation=None,
                responsibility="Test",
                role="user_manager",
            ),
            GroupAccess(
                email="customer_manager@fluidattacks.com",
                group_name="unittesting",
                state=GroupAccessState(
                    modified_date=datetime.fromisoformat(
                        "2020-01-01T20:07:57+00:00"
                    )
                ),
                confirm_deletion=None,
                expiration_time=None,
                has_access=True,
                invitation=None,
                responsibility="Test Owner",
                role="customer_manager",
            ),
            GroupAccess(
                email="forces.unittesting@fluidattacks.com",
                group_name="unittesting",
                state=GroupAccessState(
                    modified_date=datetime.fromisoformat(
                        "2020-01-01T20:07:57+00:00"
                    )
                ),
                confirm_deletion=None,
                expiration_time=None,
                has_access=True,
                invitation=None,
                responsibility="Forces service user",
                role="service_forces",
            ),
            GroupAccess(
                email="integrateshacker@fluidattacks.com",
                group_name="unittesting",
                state=GroupAccessState(
                    modified_date=datetime.fromisoformat(
                        "2020-01-01T20:07:57+00:00"
                    )
                ),
                confirm_deletion=None,
                expiration_time=None,
                has_access=True,
                invitation=None,
                responsibility="Test",
                role="hacker",
            ),
            GroupAccess(
                email="integratesmanager@fluidattacks.com",
                group_name="unittesting",
                state=GroupAccessState(
                    modified_date=datetime.fromisoformat(
                        "2020-01-01T20:07:57+00:00"
                    )
                ),
                confirm_deletion=None,
                expiration_time=None,
                has_access=True,
                invitation=None,
                responsibility="Test",
                role=None,
            ),
            GroupAccess(
                email="integratesmanager@gmail.com",
                group_name="unittesting",
                state=GroupAccessState(
                    modified_date=datetime.fromisoformat(
                        "2020-01-01T20:07:57+00:00"
                    )
                ),
                confirm_deletion=None,
                expiration_time=None,
                has_access=True,
                invitation=None,
                responsibility="Test",
                role=None,
            ),
            GroupAccess(
                email="integratesreattacker@fluidattacks.com",
                group_name="unittesting",
                state=GroupAccessState(
                    modified_date=datetime.fromisoformat(
                        "2020-01-01T20:07:57+00:00"
                    )
                ),
                confirm_deletion=None,
                expiration_time=None,
                has_access=True,
                invitation=None,
                responsibility="Test reattacker",
                role="reattacker",
            ),
            GroupAccess(
                email="integratesresourcer@fluidattacks.com",
                group_name="unittesting",
                state=GroupAccessState(
                    modified_date=datetime.fromisoformat(
                        "2020-01-01T20:07:57+00:00"
                    )
                ),
                confirm_deletion=None,
                expiration_time=None,
                has_access=True,
                invitation=None,
                responsibility="Test",
                role="resourcer",
            ),
            GroupAccess(
                email="integratesreviewer@fluidattacks.com",
                group_name="unittesting",
                state=GroupAccessState(
                    modified_date=datetime.fromisoformat(
                        "2020-01-01T20:07:57+00:00"
                    )
                ),
                confirm_deletion=None,
                expiration_time=None,
                has_access=True,
                invitation=None,
                responsibility="Test",
                role="reviewer",
            ),
            GroupAccess(
                email="integratesserviceforces@fluidattacks.com",
                group_name="unittesting",
                state=GroupAccessState(
                    modified_date=datetime.fromisoformat(
                        "2020-01-01T20:07:57+00:00"
                    )
                ),
                confirm_deletion=None,
                expiration_time=None,
                has_access=True,
                invitation=None,
                responsibility="Test",
                role="service_forces",
            ),
            GroupAccess(
                email="integratesuser2@fluidattacks.com",
                group_name="unittesting",
                state=GroupAccessState(
                    modified_date=datetime.fromisoformat(
                        "2020-01-01T20:07:57+00:00"
                    )
                ),
                confirm_deletion=None,
                expiration_time=None,
                has_access=True,
                invitation=None,
                responsibility="Test",
                role="user",
            ),
            GroupAccess(
                email="integratesuser2@gmail.com",
                group_name="unittesting",
                state=GroupAccessState(
                    modified_date=datetime.fromisoformat(
                        "2020-01-01T20:07:57+00:00"
                    )
                ),
                confirm_deletion=None,
                expiration_time=None,
                has_access=True,
                invitation=None,
                responsibility="Test",
                role="user",
            ),
            GroupAccess(
                email="integratesuser@gmail.com",
                group_name="unittesting",
                state=GroupAccessState(
                    modified_date=datetime.fromisoformat(
                        "2020-01-01T20:07:57+00:00"
                    )
                ),
                confirm_deletion=None,
                expiration_time=None,
                has_access=True,
                invitation=None,
                responsibility="Test",
                role="user_manager",
            ),
            GroupAccess(
                email="unittest2@fluidattacks.com",
                group_name="unittesting",
                state=GroupAccessState(
                    modified_date=datetime.fromisoformat(
                        "2020-01-01T20:07:57+00:00"
                    )
                ),
                confirm_deletion=None,
                expiration_time=None,
                has_access=True,
                invitation=None,
                responsibility="Tester",
                role="customer_manager",
            ),
            GroupAccess(
                email="unittest@fluidattacks.com",
                group_name="unittesting",
                state=GroupAccessState(
                    modified_date=datetime.fromisoformat(
                        "2020-01-01T20:07:57+00:00"
                    )
                ),
                confirm_deletion=None,
                expiration_time=None,
                has_access=True,
                invitation=None,
                responsibility="Tester",
                role=None,
            ),
            GroupAccess(
                email="vulnmanager@gmail.com",
                group_name="unittesting",
                state=GroupAccessState(
                    modified_date=datetime.fromisoformat(
                        "2020-01-01T20:07:57+00:00"
                    )
                ),
                confirm_deletion=None,
                expiration_time=None,
                has_access=True,
                invitation=GroupInvitation(
                    is_used=True,
                    role="vulnerability_manager",
                    url_token="unknown",
                    responsibility="Test vulnerability manager",
                ),
                responsibility="Test vulnerability manager",
                role="vulnerability_manager",
            ),
        ],
    },
    "group_access.domain.get_group_stakeholders_emails": {
        '["oneshottest"]': [
            "continuoushacking@gmail.com",
            "integrateshacker@fluidattacks.com",
            "integratesmanager@fluidattacks.com",
            "integratesmanager@gmail.com",
            "integratesuser@gmail.com",
        ]
    },
    "group_access.domain.get_managers": {
        '["unittesting", 2]': [
            "continuoushack2@gmail.com",
            "continuoushacking@gmail.com",
        ],
        '["unittesting", 3]': [
            "continuoushack2@gmail.com",
            "continuoushacking@gmail.com",
            "integratesuser@gmail.com",
        ],
    },
    "group_access.domain.get_stakeholders_email_by_preferences": {
        '["unittesting"]': [
            "continuoushack2@gmail.com",
            "continuoushacking@gmail.com",
            "customer_manager@fluidattacks.com",
            "integratesuser@gmail.com",
            "unittest2@fluidattacks.com",
        ],
    },
    "group_access.domain.update": {
        '["unittest@fluidattacks.com", "unittesting"]': None,
    },
    "mailer.groups.send_mail_devsecops_agent_token": {
        '["integratesmanager@gmail.com", "unittesting", true]': None,
        '["integratesmanager@gmail.com", "unittesting", false]': None,
    },
    "newutils.files.assert_uploaded_file_mime": {
        '["test-file-records.csv", "images"]': False,
        '["test-big-image.jpg", "images"]': True,
        '["test-file-records.csv", "files"]': True,
    },
    "organizations.domain.add_stakeholder": {
        '["esdeath", "org_testusermanager1@gmail.com"]': None,
    },
    "organizations.domain.exists": {
        '["esdeath"]': False,
        '["esdeath_r"]': True,
        '["#@^esdeath"]': False,
    },
    "organizations.domain.get_group_names": {
        '["ORG#f2e2777d-a168-4bea-93cd-d79142b294d2"]': tuple(
            ["kurome", "sheele"]
        ),
        '["ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3"]': tuple(
            ["oneshottest", "unittesting"]
        ),
    },
    "organizations.domain.get_organization": {
        '["ORG#c2ee2d15-04ab-4f39-9795-fbe30cdeee86"]': Organization(
            created_by="testing@unittest.com",
            created_date=datetime.fromisoformat("2018-02-08T00:43:18+00:00"),
            id="ORG#c2ee2d15-04ab-4f39-9795-fbe30cdeee86",
            name="bulat",
            policies=Policies(
                modified_date=datetime.fromisoformat(
                    "2019-11-22T20:07:57+00:00"
                ),
                modified_by="integratesmanager@gmail.com",
                inactivity_period=90,
                max_acceptance_days=60,
                max_acceptance_severity=Decimal("3.4"),
                max_number_acceptances=2,
                min_acceptance_severity=Decimal("3.4"),
                min_breaking_severity=Decimal("0"),
                vulnerability_grace_period=0,
            ),
            state=OrganizationState(
                status=OrganizationStateStatus.ACTIVE,
                modified_by="unittests",
                modified_date=datetime.fromisoformat(
                    "2019-11-22T20:07:57+00:00"
                ),
            ),
            country="Colombia",
            payment_methods=None,
            billing_customer=None,
            vulnerabilities_url=None,
        )
    },
    "organizations.domain.get_stakeholders_emails": {
        '["ORG#fe80d2d4-ccb7-46d1-8489-67c6360581de"]': [
            "org_testuser1@gmail.com"
        ],
    },
    "organizations.domain.group_access_domain.remove_access": {
        '["ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3", '
        '"jdoe@fluidattacks.com"]': [
            None,
            None,
        ]
    },
    "organizations.domain.has_access": {
        '["ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3", '
        '"jdoe@fluidattacks.com"]': True,
        '["ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3", '
        '"made_up_user@gmail.com"]': False,
    },
    "organizations.domain.org_access_model.remove": {
        '["jdoe@fluidattacks.com", '
        '"ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3"]': None,
    },
    "organizations.domain.remove_access": {
        '["ORG#fe80d2d4-ccb7-46d1-8489-67c6360581de", '
        '"org_testuser1@gmail.com"]': None,
        '["ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3", '
        '"jdoe@fluidattacks.com"]': None,
    },
    "organizations.domain.remove_credentials": {
        '["ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3", '
        '"jdoe@fluidattacks.com", "org_testadmin@gmail.com"]': [None]
    },
    "organizations.domain.stakeholders_domain.remove": {
        '["jdoe@fluidattacks.com"]': None,
    },
    "organizations.domain.validate_acceptance_severity_range": {
        '["ORG#c2ee2d15-04ab-4f39-9795-fbe30cdeee86", '
        '[21, 20, "8.3", 3, "2.2", "3.4", 17]]': True,
    },
    "organizations.domain.Dataloaders.stakeholder_organizations_access": {
        '["jdoe@fluidattacks.com"]': [],
    },
    "organizations.domain.Dataloaders.user_credentials": {
        '["jdoe@fluidattacks.com"]': [
            Credentials(
                id="0b8bf4cb-8735-4232-8199-46cd9802ad2a",
                organization_id="ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3",
                owner="jdoe@fluidattacks.com",
                state=CredentialsState(
                    modified_by="jdoe@fluidattacks.com",
                    modified_date=datetime.fromisoformat(
                        "2021-12-22T03:45:00+00:00"
                    ),
                    name="Product New SSH Key",
                    type=CredentialType.SSH,
                    is_pat=False,
                    secret=SshSecret(key="LS0tLS_Test_Key"),
                    azure_organization=None,
                ),
            )
        ]
    },
    "s3.operations.list_files": {
        '["billing-test-file.png"]': ["billing-test-file.png"],
        '["unittesting-test-file.csv"]': ["unittesting-test-file.csv"],
    },
    "s3.operations.remove_file": {
        '["billing-test-file.png"]': None,
        '["unittesting-test-file.csv"]': None,
    },
    "s3.operations.sign_url": {
        '["okada", "4722b0b7-cfeb-4898-8308-185dfc2523bc", "test_file.pdf"]': "https://s3.amazonaws.com/"  # noqa: E501 pylint: disable=line-too-long
        "integrates/johndoeatfluid-test-unit/resources/billing/okada/"
        "testing%20company%20and%20sons/test_file.pdf?X-Amz-Algorithm=Test"
        "X-Amz-Credential=Testus-east-1%2Fs3%2Faws4_request&X-Amz-Date="
        "20230117T170631Z&X-Amz-Expires=10&X-Amz-SignedHeaders=host&"
        "X-Amz-Security-Token=TestX-Amz-Signature=Test"
    },
    "s3.operations.upload_memory_file": {
        '["billing-test-file.png"]': None,
        '["test-vulns.yaml"]': None,
        '["unittesting-test-file.csv"]': None,
    },
    "vulnerabilities.domain.mask_vulnerability": {
        '["unittest@fluidattacks.com", "457497316"]': None,
    },
}


def create_dummy_simple_session(
    username: str = "unittest",
) -> Request:
    request = Request("GET", "/")
    request = apply_context_attrs(request)  # type: ignore
    setattr(
        request,
        "session",
        dict(username=username, session_key=str(uuid.uuid4())),
    )
    setattr(request, "cookies", {})

    return request


async def create_dummy_session(
    username: str = "unittest", session_jwt: Optional[str] = None
) -> Request:
    request = create_dummy_simple_session(username)
    jti = sessions_utils.calculate_hash_token()["jti"]
    expiration_time = int(
        (datetime.utcnow() + timedelta(seconds=SESSION_COOKIE_AGE)).timestamp()
    )
    payload = {
        "user_email": username,
        "first_name": "unit",
        "last_name": "test",
        "jti": jti,
    }
    token = sessions_domain.encode_token(
        expiration_time=expiration_time,
        payload=payload,
        subject="starlette_session",
    )
    if session_jwt:
        request.headers["Authorization"] = f"Bearer {session_jwt}"
    else:
        request.cookies[JWT_COOKIE_NAME] = token
        # do not use me query to validate if an stakeholder
        # has been removed because update_metadata will create that user
        await stakeholders_model.update_metadata(
            email=username,
            metadata=StakeholderMetadataToUpdate(
                session_token=StakeholderSessionToken(
                    jti=jti, state=StateSessionType.IS_VALID
                )
            ),
        )
    return request


def create_dummy_info(request: Request) -> GraphQLResolveInfo:
    return GraphQLResolveInfo(
        field_name=None,  # type: ignore
        field_nodes=None,  # type: ignore
        return_type=None,  # type: ignore
        parent_type=None,  # type: ignore
        path=None,  # type: ignore
        schema=None,  # type: ignore
        fragments=None,  # type: ignore
        root_value=None,
        operation=None,  # type: ignore
        variable_values=None,  # type: ignore
        context=request,
        is_awaitable=None,  # type: ignore
    )


def get_module_at_test(file_path: str) -> str:
    match = search(r".*\/(.*\/.*)", file_path)
    if match:
        test_module = match.group(1)
    module_at_test = (
        test_module.replace("/", ".").replace("test_", "").replace("py", "")
    )
    return module_at_test


def get_mock_response(used_mock: str, parameters: str) -> Any:
    return mocked_responses[used_mock][parameters]


def get_mocked_path(mocked_object: str) -> str:
    return mocked_paths[mocked_object]


def set_mocks_return_values(
    mocked_objects: List[AsyncMock],
    paths_list: List[str],
    mocks_args: List[List[Any]],
    module_at_test: str = "",
) -> bool:
    all_values_set = False
    if module_at_test:
        for mocked_object, mocked_path, arguments in zip(
            mocked_objects, paths_list, mocks_args
        ):
            mocked_object.return_value = get_mock_response(
                module_at_test + mocked_path,
                json.dumps(arguments, default=str),
            )
        all_values_set = True
    else:
        for mocked_object, mocked_path, arguments in zip(
            mocked_objects, paths_list, mocks_args
        ):
            mocked_object.return_value = get_mock_response(
                get_mocked_path(mocked_path),
                json.dumps(arguments, default=str),
            )
        all_values_set = True
    return all_values_set


def set_mocks_side_effects(
    mocked_objects: List[AsyncMock],
    paths_list: List[str],
    mocks_args: List[List[Any]],
    module_at_test: str = "",
) -> bool:
    all_values_set = False
    for mocked_object, mocked_path, arguments in zip(
        mocked_objects, paths_list, mocks_args
    ):
        mocked_object.side_effect = get_mock_response(
            module_at_test + mocked_path,
            json.dumps(arguments, default=str),
        )
    all_values_set = True
    return all_values_set
