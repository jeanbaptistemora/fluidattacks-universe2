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
from db_model.enums import (
    GitCloningStatus,
    Source,
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
from db_model.group_access.types import (
    GroupAccess,
    GroupAccessState,
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
    VulnerabilityStateStatus,
    VulnerabilityToolImpact,
    VulnerabilityTreatmentStatus,
    VulnerabilityType,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
    VulnerabilityState,
    VulnerabilityTool,
    VulnerabilityTreatment,
    VulnerabilityUnreliableIndicators,
)
from decimal import (
    Decimal,
)
from graphql import (
    GraphQLResolveInfo,
)
import json
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
    Optional,
)
import uuid

mocked_paths: Dict[str, str] = {
    "authz.validate_handle_comment_scope": "authz.validate_handle_comment_scope",  # noqa: E501 pylint: disable=line-too-long
    "dynamodb_ops.delete_item": "dynamodb.operations_legacy.delete_item",
    "dynamodb_ops.query": "dynamodb.operations_legacy.query",
    "event_comments_domain.add": "event_comments.domain.add",
    "events_model.add": "db_model.events.add",
    "events_model.update_state": "db_model.events.update_state",
    "events_model.update_evidence": "db_model.events.update_evidence",
    "findings_storage.download_evidence": "findings.storage.download_evidence",
    "findings_storage.search_evidence": "findings.storage.search_evidence",
    "finding_vulns_loader.load_many_chained": "db_model.vulnerabilities.get.FindingVulnerabilitiesReleasedNonZeroRiskLoader.load_many_chained",  # noqa: E501 pylint: disable=line-too-long
    "get_open_vulnerabilities": "findings.domain.core.get_open_vulnerabilities",  # noqa: E501 pylint: disable=line-too-long
    "get_user_level_role": "authz.policy.get_user_level_role",
    "grant_user_level_role": "authz.policy.grant_user_level_role",
    "group_access_model.update_metadata": "db_model.group_access.update_metadata",  # noqa: E501 pylint: disable=line-too-long
    "group_comments_model.add": "db_model.group_comments.add",
    "loaders.event.load": "db_model.events.get.EventLoader.load",
    "loaders.event_comments.load": "db_model.event_comments.get.EventCommentsLoader.load",  # noqa: E501 pylint: disable=line-too-long
    "loaders.group.load": "db_model.groups.get.GroupLoader.load",
    "loaders.group_access.load": "db_model.group_access.get.GroupAccessLoader.load",  # noqa: E501 pylint: disable=line-too-long
    "loaders.organization.load": "db_model.organizations.get.OrganizationLoader.load",  # noqa: E501 pylint: disable=line-too-long
    "loaders.root.load": "db_model.roots.get.RootLoader.load",
    "loaders.stakeholder.load": "db_model.stakeholders.get.StakeholderLoader.load",  # noqa: E501 pylint: disable=line-too-long
    "loaders.stakeholder_with_fallback.load": "db_model.stakeholders.get.StakeholderWithFallbackLoader.load",  # noqa: E501 pylint: disable=line-too-long
    "replace_different_format": "events.domain.replace_different_format",
    "save_evidence": "events.domain.save_evidence",
    "stakeholders_model.update_metadata": "db_model.stakeholders.update_metadata",  # noqa: E501 pylint: disable=line-too-long
    "s3_ops.list_files": "s3.operations.list_files",
    "s3_ops.remove_file": "s3.operations.remove_file",
    "s3_ops.upload_memory_file": "s3.operations.upload_memory_file",
    "update_evidence": "events.domain.update_evidence",
    "validate_evidence": "events.domain.validate_evidence",
}

mocked_responses: Dict[str, Dict[str, Any]] = {
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
    "db_model.events.add": {
        '["unittesting", "unittesting@fluidattacks.com", '
        '"4039d098-ffc5-4984-8ed3-eb17bca98e19"]': None,
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
    "dynamodb.operations_legacy.delete_item": {
        '["44aa89bddf5e0a5b1aca2551799b71ff593c95a89f4402b84697e9b29f6'
        '52110"]': True,
    },
    "dynamodb.operations_legacy.query": {
        '["ac25d6d18e368c34a41103a9f6dbf0a787cf2551d6ef5884c844085d26013e0a"]': [  # noqa: E501 pylint: disable=line-too-long
            dict(
                additional_info=json.dumps(
                    dict(
                        report_type="XLS",
                        treatments=["ACCEPTED", "NEW"],
                        states=["OPEN"],
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
    "events.domain.replace_different_format": {
        '["418900978", "FILE_1"]': None,
        '["538745942", "FILE_1"]': None,
    },
    "events.domain.save_evidence": {
        '["418900978", "test-file-records.csv"]': None,
        '["538745942", "test-file-records.csv"]': None,
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
    "db_model.stakeholders.update_metadata": {
        '["integrateshacker@fluidattacks.com"]': None,
        '["integratesuser@gmail.com"]': None,
        '["test_email@test.com", "user"]': None,
        '["test_email@test.com", "admin"]': None,
    },
    "s3.operations.list_files": {
        '["billing-test-file.png"]': ["billing-test-file.png"],
        '["unittesting-test-file.csv"]': ["unittesting-test-file.csv"],
    },
    "s3.operations.remove_file": {
        '["billing-test-file.png"]': None,
        '["unittesting-test-file.csv"]': None,
    },
    "s3.operations.upload_memory_file": {
        '["billing-test-file.png"]': None,
        '["unittesting-test-file.csv"]': None,
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


def get_mock_response(used_mock: str, parameters: str) -> Any:
    return mocked_responses[used_mock][parameters]


def get_mocked_path(mocked_object: str) -> str:
    return mocked_paths[mocked_object]
