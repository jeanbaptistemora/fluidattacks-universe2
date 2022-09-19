# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# pylint: disable=too-many-lines

import asyncio
from asyncio import (
    AbstractEventLoop,
)
from db_model.enrollment.types import (
    Enrollment,
    Trial,
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
    GroupState,
)
from db_model.organization_access.types import (
    OrganizationAccess,
)
from db_model.organizations.enums import (
    OrganizationStateStatus,
)
from db_model.organizations.types import (
    Organization,
    OrganizationState,
)
from db_model.stakeholders.types import (
    Stakeholder,
    StakeholderPhone,
)
from db_model.types import (
    Policies,
)
from dynamodb.resource import (
    dynamo_shutdown,
    dynamo_startup,
)
import pytest
from typing import (
    Any,
    AsyncGenerator,
    Generator,
)

# Constants
TEST_GROUPS: set[str] = {
    "accept_legal",
    "acknowledge_concurrent_session",
    "activate_root",
    "add_credentials",
    "add_draft",
    "add_event",
    "add_event_consult",
    "add_files_to_db",
    "add_finding_consult",
    "add_forces_execution_s3",
    "add_git_root_s3",
    "add_group",
    "add_group_consult",
    "add_group_tags",
    "add_organization",
    "add_push_token",
    "add_stakeholder",
    "add_toe_input",
    "add_toe_lines",
    "add_url_root",
    "approve_draft",
    "confirm_vulnerabilities_zero_risk",
    "deactivate_root",
    "delete_obsolete_groups",
    "download_event_file",
    "download_vulnerability_file_s3",
    "download_file",
    "enumerate_toe_input",
    "event",
    "events",
    "finding",
    "forces_executions",
    "handle_vulnerabilities_acceptance",
    "grant_stakeholder_access",
    "grant_stakeholder_organization_access",
    "groups_languages_distribution",
    "groups_with_forces",
    "invalidate_access_token",
    "me",
    "move_root",
    "old",
    "organization",
    "organization_id",
    "group_s3",
    "refresh_toe_inputs",
    "refresh_toe_lines",
    "reject_draft",
    "reject_event_solution",
    "reject_vulnerabilities_zero_risk",
    "remove_credentials",
    "remove_event_evidence_s3",
    "remove_evidence_s3",
    "remove_files_s3",
    "remove_finding_s3",
    "remove_group_s3",
    "remove_group_tag",
    "remove_stakeholder",
    "remove_stakeholder_access",
    "remove_stakeholder_organization_access",
    "remove_tags",
    "remove_toe_input",
    "remove_vulnerability",
    "report",
    "request_vulnerabilities_hold",
    "request_vulnerabilities_verification",
    "report_machine_s3",
    "request_event_verification",
    "request_vulnerabilities_zero_risk",
    "requeue_actions",
    "reset_expired_accepted_findings",
    "resources",
    "sign_post_url",
    "sign_in",
    "solve_event",
    "stakeholder",
    "submit_draft",
    "submit_organization_finding_policy",
    "subscribe_to_entity_report_s3",
    "sync_git_root_s3",
    "toe_inputs",
    "toe_lines",
    "unsubscribe_from_group",
    "update_access_token",
    "update_credentials",
    "update_event",
    "update_event_evidence_s3",
    "update_event_solving_reason",
    "update_evidence_s3",
    "update_evidence_description",
    "update_finding_description",
    "update_forces_access_token",
    "update_git_environments",
    "update_git_root_s3",
    "update_group_s3",
    "update_group_access_info",
    "update_group_disambiguation",
    "update_group_managed",
    "update_group_policies",
    "update_group_info",
    "update_group_stakeholder",
    "update_ip_root",
    "update_organization_policies",
    "update_organization_stakeholder",
    "update_nickname",
    "update_severity",
    "update_stakeholder_phone",
    "update_toe_input",
    "update_toe_lines_attacked_lines",
    "update_toe_lines_sorts",
    "update_toe_vulnerabilities",
    "update_tours",
    "update_url_root",
    "update_vulnerabilities_treatment",
    "update_vulnerability_commit",
    "update_vulnerability_treatment",
    "upload_file",
    "validate_git_access",
    "verify_stakeholder",
    "verify_vulnerabilities_request",
    "vulnerability",
    "batch",
    "batch_dispatch_s3",
}


@pytest.fixture(autouse=True, scope="session")
def generic_data(  # pylint: disable=too-many-locals
    dynamo_resource: bool,  # pylint: disable=redefined-outer-name
) -> dict[str, Any]:
    assert dynamo_resource
    admin_email: str = "admin@gmail.com"
    admin_fluid_email: str = "admin@fluidattacks.com"
    architect_email: str = "architect@gmail.com"
    architect_fluid_email: str = "architect@fluidattacks.com"
    customer_manager_fluid_email: str = "customer_manager@fluidattacks.com"
    hacker_email: str = "hacker@gmail.com"
    hacker_fluid_email: str = "hacker@fluidattacks.com"
    reattacker_email: str = "reattacker@gmail.com"
    reattacker_fluid_email: str = "reattacker@fluidattacks.com"
    resourcer_email: str = "resourcer@gmail.com"
    resourcer_fluid_email: str = "resourcer@fluidattacks.com"
    reviewer_email: str = "reviewer@gmail.com"
    reviewer_fluid_email: str = "reviewer@fluidattacks.com"
    service_forces_email: str = "service_forces@gmail.com"
    service_forces_fluid_email: str = "service_forces@fluidattacks.com"
    user_email: str = "user@gmail.com"
    user_fluid_email: str = "user@fluidattacks.com"
    user_manager_email: str = "user_manager@gmail.com"
    user_manager_fluid_email: str = "user_manager@fluidattacks.com"
    vuln_manager_email: str = "vulnerability_manager@gmail.com"
    vuln_manager_fluid_email: str = "vulnerability_manager@fluidattacks.com"
    org_id: str = "ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db"
    return {
        "global_vars": {
            "admin_email": admin_email,
            "admin_fluid_email": admin_fluid_email,
            "architect_email": architect_email,
            "architect_fluid_email": architect_fluid_email,
            "customer_manager_fluid_email": customer_manager_fluid_email,
            "hacker_email": hacker_email,
            "hacker_fluid_email": hacker_fluid_email,
            "reattacker_email": reattacker_email,
            "reattacker_fluid_email": reattacker_fluid_email,
            "resourcer_email": resourcer_email,
            "resourcer_fluid_email": resourcer_fluid_email,
            "reviewer_email": reviewer_email,
            "reviewer_fluid_email": reviewer_fluid_email,
            "service_forces_email": service_forces_email,
            "service_forces_fluid_email": service_forces_fluid_email,
            "user_email": user_email,
            "user_fluid_email": user_fluid_email,
            "user_manager_email": user_manager_email,
            "user_manager_fluid_email": user_manager_fluid_email,
            "vulnerability_manager_email": vuln_manager_email,
            "vulnerability_manager_fluid_email": vuln_manager_fluid_email,
            "FIN.H.060": (
                "060. Insecure service configuration - Host verification"
            ),
            "R359": "R359. Avoid using generic exceptions.",
        },
        "db_data": {
            "enrollments": (
                Enrollment(
                    email="admin@gmail.com",
                    enrolled=True,
                    trial=Trial(
                        completed=True,
                        extension_date="",
                        extension_days=0,
                        start_date="",
                    ),
                ),
                Enrollment(
                    email="admin@fluidattacks.com",
                    enrolled=True,
                    trial=Trial(
                        completed=True,
                        extension_date="",
                        extension_days=0,
                        start_date="",
                    ),
                ),
            ),
            "stakeholders": [
                Stakeholder(
                    email=admin_email,
                    legal_remember=False,
                    push_tokens=[],
                    is_registered=True,
                    phone=StakeholderPhone(
                        country_code="US",
                        calling_country_code="1",
                        national_number="1111111111",
                    ),
                ),
                Stakeholder(
                    email=admin_fluid_email,
                    legal_remember=False,
                    push_tokens=[],
                    is_registered=True,
                    phone=StakeholderPhone(
                        calling_country_code="1",
                        country_code="US",
                        national_number="22222222222",
                    ),
                ),
                Stakeholder(
                    email=architect_email,
                    legal_remember=False,
                    push_tokens=[],
                    is_registered=True,
                    phone=StakeholderPhone(
                        calling_country_code="1",
                        country_code="US",
                        national_number="33333333333",
                    ),
                ),
                Stakeholder(
                    email=architect_fluid_email,
                    legal_remember=False,
                    push_tokens=[],
                    is_registered=True,
                    phone=StakeholderPhone(
                        calling_country_code="1",
                        country_code="US",
                        national_number="4444444444444",
                    ),
                ),
                Stakeholder(
                    email=user_email,
                    first_name="",
                    last_name="",
                    registration_date="",
                    last_login_date="",
                    legal_remember=False,
                    push_tokens=[],
                    is_registered=True,
                    phone=StakeholderPhone(
                        calling_country_code="1",
                        country_code="US",
                        national_number="2029182132",
                    ),
                ),
                Stakeholder(
                    email=user_fluid_email,
                    legal_remember=False,
                    push_tokens=[],
                    is_registered=True,
                    phone=StakeholderPhone(
                        calling_country_code="1",
                        country_code="US",
                        national_number="666666666666",
                    ),
                ),
                Stakeholder(
                    email=user_manager_email,
                    legal_remember=False,
                    push_tokens=[],
                    is_registered=True,
                    phone=StakeholderPhone(
                        calling_country_code="1",
                        country_code="US",
                        national_number="77777777777777",
                    ),
                ),
                Stakeholder(
                    email=user_manager_fluid_email,
                    legal_remember=False,
                    push_tokens=[],
                    is_registered=True,
                    phone=StakeholderPhone(
                        calling_country_code="1",
                        country_code="US",
                        national_number="88888888888",
                    ),
                ),
                Stakeholder(
                    email=hacker_email,
                    legal_remember=False,
                    push_tokens=[],
                    is_registered=True,
                    phone=StakeholderPhone(
                        calling_country_code="1",
                        country_code="US",
                        national_number="2029182131",
                    ),
                ),
                Stakeholder(
                    email=hacker_fluid_email,
                    legal_remember=False,
                    push_tokens=[],
                    is_registered=True,
                    phone=StakeholderPhone(
                        calling_country_code="57",
                        country_code="CO",
                        national_number="222222222222",
                    ),
                ),
                Stakeholder(
                    email=resourcer_email,
                    legal_remember=False,
                    push_tokens=[],
                    is_registered=True,
                    phone=StakeholderPhone(
                        calling_country_code="57",
                        country_code="CO",
                        national_number="33333333333",
                    ),
                ),
                Stakeholder(
                    email=reattacker_email,
                    legal_remember=False,
                    push_tokens=[],
                    is_registered=True,
                    phone=StakeholderPhone(
                        calling_country_code="57",
                        country_code="CO",
                        national_number="4444444444444",
                    ),
                ),
                Stakeholder(
                    email=reattacker_fluid_email,
                    legal_remember=False,
                    push_tokens=[],
                    is_registered=True,
                    phone=StakeholderPhone(
                        calling_country_code="57",
                        country_code="CO",
                        national_number="55555555555",
                    ),
                ),
                Stakeholder(
                    email=resourcer_fluid_email,
                    legal_remember=False,
                    push_tokens=[],
                    is_registered=True,
                    phone=StakeholderPhone(
                        calling_country_code="57",
                        country_code="CO",
                        national_number="66666666666",
                    ),
                ),
                Stakeholder(
                    email=reviewer_email,
                    legal_remember=False,
                    push_tokens=[],
                    is_registered=True,
                    phone=StakeholderPhone(
                        calling_country_code="57",
                        country_code="CO",
                        national_number="7777777777",
                    ),
                ),
                Stakeholder(
                    email=reviewer_fluid_email,
                    legal_remember=False,
                    push_tokens=[],
                    is_registered=True,
                    phone=StakeholderPhone(
                        calling_country_code="57",
                        country_code="CO",
                        national_number="8888888888",
                    ),
                ),
                Stakeholder(
                    email=service_forces_email,
                    legal_remember=False,
                    push_tokens=[],
                    is_registered=True,
                ),
                Stakeholder(
                    email=service_forces_fluid_email,
                    legal_remember=False,
                    push_tokens=[],
                    is_registered=True,
                ),
                Stakeholder(
                    email=customer_manager_fluid_email,
                    legal_remember=False,
                    push_tokens=[],
                    is_registered=True,
                    phone=StakeholderPhone(
                        calling_country_code="57",
                        country_code="CO",
                        national_number="9999999999999",
                    ),
                ),
                Stakeholder(
                    email=vuln_manager_email,
                    legal_remember=False,
                    push_tokens=[],
                    is_registered=True,
                    phone=StakeholderPhone(
                        calling_country_code="51",
                        country_code="PE",
                        national_number="1111111111111",
                    ),
                ),
                Stakeholder(
                    email=vuln_manager_fluid_email,
                    legal_remember=False,
                    push_tokens=[],
                    is_registered=True,
                    phone=StakeholderPhone(
                        calling_country_code="51",
                        country_code="PE",
                        national_number="222222222222",
                    ),
                ),
            ],
            "organizations": [
                {
                    "organization": Organization(
                        id="40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                        name="orgtest",
                        policies=Policies(
                            modified_by=admin_email,
                            max_acceptance_days=7,
                            modified_date="2019-11-22T20:07:57+00:00",
                            vulnerability_grace_period=5,
                        ),
                        state=OrganizationState(
                            modified_by=admin_email,
                            modified_date="2019-11-22T20:07:57+00:00",
                            status=OrganizationStateStatus.ACTIVE,
                        ),
                    ),
                },
            ],
            "organization_access": [
                OrganizationAccess(
                    organization_id="40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                    email=admin_email,
                ),
                OrganizationAccess(
                    organization_id="40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                    email=admin_fluid_email,
                ),
                OrganizationAccess(
                    organization_id="40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                    email=architect_email,
                ),
                OrganizationAccess(
                    organization_id="40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                    email=architect_fluid_email,
                ),
                OrganizationAccess(
                    organization_id="40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                    email=hacker_email,
                ),
                OrganizationAccess(
                    organization_id="40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                    email=hacker_fluid_email,
                ),
                OrganizationAccess(
                    organization_id="40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                    email=reattacker_email,
                ),
                OrganizationAccess(
                    organization_id="40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                    email=reattacker_fluid_email,
                ),
                OrganizationAccess(
                    organization_id="40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                    email=user_email,
                ),
                OrganizationAccess(
                    organization_id="40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                    email=user_fluid_email,
                ),
                OrganizationAccess(
                    organization_id="40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                    email=user_manager_email,
                ),
                OrganizationAccess(
                    organization_id="40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                    email=user_manager_fluid_email,
                ),
                OrganizationAccess(
                    organization_id="40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                    email=resourcer_email,
                ),
                OrganizationAccess(
                    organization_id="40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                    email=resourcer_fluid_email,
                ),
                OrganizationAccess(
                    organization_id="40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                    email=reviewer_email,
                ),
                OrganizationAccess(
                    organization_id="40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                    email=reviewer_fluid_email,
                ),
                OrganizationAccess(
                    organization_id="40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                    email=service_forces_email,
                ),
                OrganizationAccess(
                    organization_id="40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                    email=service_forces_fluid_email,
                ),
                OrganizationAccess(
                    organization_id="40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                    email=customer_manager_fluid_email,
                ),
                OrganizationAccess(
                    organization_id="40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                    email=vuln_manager_email,
                ),
                OrganizationAccess(
                    organization_id="40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                    email=vuln_manager_fluid_email,
                ),
            ],
            "groups": [
                {
                    "group": Group(
                        created_by="unknown",
                        created_date="2020-05-20T22:00:00+00:00",
                        description="-",
                        language=GroupLanguage.EN,
                        name="group1",
                        state=GroupState(
                            has_machine=False,
                            has_squad=True,
                            managed=GroupManaged["MANAGED"],
                            modified_by="unknown",
                            modified_date="2020-05-20T22:00:00+00:00",
                            service=GroupService.WHITE,
                            status=GroupStateStatus.ACTIVE,
                            tier=GroupTier.OTHER,
                            type=GroupSubscriptionType.CONTINUOUS,
                        ),
                        organization_id="40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                        sprint_start_date="2022-06-06T00:00:00",
                    ),
                },
                {
                    "group": Group(
                        created_by="unknown",
                        created_date="2020-05-20T22:00:00+00:00",
                        description="-",
                        language=GroupLanguage.EN,
                        name="unittesting",
                        state=GroupState(
                            has_machine=True,
                            has_squad=True,
                            managed=GroupManaged["MANAGED"],
                            modified_by="unknown",
                            modified_date="2020-05-20T22:00:00+00:00",
                            service=GroupService.WHITE,
                            status=GroupStateStatus.ACTIVE,
                            tier=GroupTier.OTHER,
                            type=GroupSubscriptionType.CONTINUOUS,
                        ),
                        organization_id="40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                        sprint_start_date="2022-06-06T00:00:00",
                    ),
                },
                {
                    "group": Group(
                        created_by="unknown",
                        created_date="2020-05-20T22:00:00+00:00",
                        description="-",
                        language=GroupLanguage.EN,
                        name="group2",
                        state=GroupState(
                            has_machine=False,
                            has_squad=True,
                            managed=GroupManaged["MANAGED"],
                            modified_by="unknown",
                            modified_date="2020-05-20T22:00:00+00:00",
                            service=GroupService.BLACK,
                            status=GroupStateStatus.ACTIVE,
                            tier=GroupTier.OTHER,
                            type=GroupSubscriptionType.ONESHOT,
                        ),
                        organization_id="40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                        sprint_start_date="2022-06-06T00:00:00",
                    ),
                },
                {
                    "group": Group(
                        created_by="unknown",
                        created_date="2020-05-20T22:00:00+00:00",
                        description="-",
                        language=GroupLanguage.EN,
                        name="group3",
                        state=GroupState(
                            has_machine=False,
                            has_squad=False,
                            managed=GroupManaged["MANAGED"],
                            modified_by="unknown",
                            modified_date="2020-05-20T22:00:00+00:00",
                            service=GroupService.BLACK,
                            status=GroupStateStatus.ACTIVE,
                            tier=GroupTier.OTHER,
                            type=GroupSubscriptionType.ONESHOT,
                        ),
                        organization_id="40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                        sprint_start_date="2022-06-06T00:00:00",
                    ),
                },
            ],
            "policies": [
                {
                    "level": "user",
                    "subject": admin_email,
                    "object": "self",
                    "role": "admin",
                },
                {
                    "level": "user",
                    "subject": admin_fluid_email,
                    "object": "self",
                    "role": "admin",
                },
                {
                    "level": "user",
                    "subject": architect_email,
                    "object": "self",
                    "role": "user",
                },
                {
                    "level": "user",
                    "subject": architect_fluid_email,
                    "object": "self",
                    "role": "user",
                },
                {
                    "level": "user",
                    "subject": hacker_email,
                    "object": "self",
                    "role": "hacker",
                },
                {
                    "level": "user",
                    "subject": hacker_fluid_email,
                    "object": "self",
                    "role": "hacker",
                },
                {
                    "level": "user",
                    "subject": reattacker_email,
                    "object": "self",
                    "role": "user",
                },
                {
                    "level": "user",
                    "subject": reattacker_fluid_email,
                    "object": "self",
                    "role": "user",
                },
                {
                    "level": "user",
                    "subject": user_email,
                    "object": "self",
                    "role": "user",
                },
                {
                    "level": "user",
                    "subject": user_fluid_email,
                    "object": "self",
                    "role": "user",
                },
                {
                    "level": "user",
                    "subject": user_manager_email,
                    "object": "self",
                    "role": "user",
                },
                {
                    "level": "user",
                    "subject": user_manager_fluid_email,
                    "object": "self",
                    "role": "user",
                },
                {
                    "level": "user",
                    "subject": resourcer_email,
                    "object": "self",
                    "role": "user",
                },
                {
                    "level": "user",
                    "subject": resourcer_fluid_email,
                    "object": "self",
                    "role": "user",
                },
                {
                    "level": "user",
                    "subject": reviewer_email,
                    "object": "self",
                    "role": "user",
                },
                {
                    "level": "user",
                    "subject": reviewer_fluid_email,
                    "object": "self",
                    "role": "user",
                },
                {
                    "level": "user",
                    "subject": service_forces_fluid_email,
                    "object": "self",
                    "role": "user",
                },
                {
                    "level": "user",
                    "subject": customer_manager_fluid_email,
                    "object": "self",
                    "role": "user",
                },
                {
                    "level": "user",
                    "subject": vuln_manager_email,
                    "object": "self",
                    "role": "user",
                },
                {
                    "level": "user",
                    "subject": vuln_manager_fluid_email,
                    "object": "self",
                    "role": "user",
                },
                {
                    "level": "group",
                    "subject": architect_email,
                    "object": "group1",
                    "role": "architect",
                },
                {
                    "level": "group",
                    "subject": architect_fluid_email,
                    "object": "group1",
                    "role": "architect",
                },
                {
                    "level": "group",
                    "subject": hacker_email,
                    "object": "group1",
                    "role": "hacker",
                },
                {
                    "level": "group",
                    "subject": hacker_email,
                    "object": "group3",
                    "role": "hacker",
                },
                {
                    "level": "group",
                    "subject": hacker_fluid_email,
                    "object": "group1",
                    "role": "hacker",
                },
                {
                    "level": "group",
                    "subject": reattacker_email,
                    "object": "group1",
                    "role": "reattacker",
                },
                {
                    "level": "group",
                    "subject": reviewer_email,
                    "object": "group3",
                    "role": "reviewer",
                },
                {
                    "level": "group",
                    "subject": reattacker_fluid_email,
                    "object": "group1",
                    "role": "reattacker",
                },
                {
                    "level": "group",
                    "subject": user_email,
                    "object": "group1",
                    "role": "user",
                },
                {
                    "level": "group",
                    "subject": user_fluid_email,
                    "object": "group1",
                    "role": "user",
                },
                {
                    "level": "group",
                    "subject": user_manager_email,
                    "object": "group1",
                    "role": "user_manager",
                },
                {
                    "level": "group",
                    "subject": user_manager_fluid_email,
                    "object": "group1",
                    "role": "user_manager",
                },
                {
                    "level": "group",
                    "subject": vuln_manager_email,
                    "object": "group1",
                    "role": "vulnerability_manager",
                },
                {
                    "level": "group",
                    "subject": vuln_manager_fluid_email,
                    "object": "group1",
                    "role": "vulnerability_manager",
                },
                {
                    "level": "group",
                    "subject": resourcer_email,
                    "object": "group1",
                    "role": "resourcer",
                },
                {
                    "level": "group",
                    "subject": resourcer_fluid_email,
                    "object": "group1",
                    "role": "resourcer",
                },
                {
                    "level": "group",
                    "subject": reviewer_email,
                    "object": "group1",
                    "role": "reviewer",
                },
                {
                    "level": "group",
                    "subject": reviewer_fluid_email,
                    "object": "group1",
                    "role": "reviewer",
                },
                {
                    "level": "group",
                    "subject": service_forces_email,
                    "object": "group1",
                    "role": "service_forces",
                },
                {
                    "level": "group",
                    "subject": service_forces_fluid_email,
                    "object": "group1",
                    "role": "service_forces",
                },
                {
                    "level": "group",
                    "subject": customer_manager_fluid_email,
                    "object": "group1",
                    "role": "customer_manager",
                },
                {
                    "level": "organization",
                    "subject": admin_email,
                    "object": org_id,
                    "role": "admin",
                },
                {
                    "level": "organization",
                    "subject": admin_fluid_email,
                    "object": org_id,
                    "role": "admin",
                },
                {
                    "level": "organization",
                    "subject": architect_email,
                    "object": org_id,
                    "role": "user",
                },
                {
                    "level": "organization",
                    "subject": architect_fluid_email,
                    "object": org_id,
                    "role": "user",
                },
                {
                    "level": "organization",
                    "subject": hacker_email,
                    "object": org_id,
                    "role": "user",
                },
                {
                    "level": "organization",
                    "subject": hacker_fluid_email,
                    "object": org_id,
                    "role": "user",
                },
                {
                    "level": "organization",
                    "subject": reattacker_email,
                    "object": org_id,
                    "role": "user",
                },
                {
                    "level": "organization",
                    "subject": reattacker_fluid_email,
                    "object": org_id,
                    "role": "user",
                },
                {
                    "level": "organization",
                    "subject": user_email,
                    "object": org_id,
                    "role": "user",
                },
                {
                    "level": "organization",
                    "subject": user_fluid_email,
                    "object": org_id,
                    "role": "user",
                },
                {
                    "level": "organization",
                    "subject": user_manager_email,
                    "object": org_id,
                    "role": "user_manager",
                },
                {
                    "level": "organization",
                    "subject": user_manager_fluid_email,
                    "object": org_id,
                    "role": "user_manager",
                },
                {
                    "level": "organization",
                    "subject": vuln_manager_email,
                    "object": org_id,
                    "role": "user",
                },
                {
                    "level": "organization",
                    "subject": vuln_manager_fluid_email,
                    "object": org_id,
                    "role": "user",
                },
                {
                    "level": "organization",
                    "subject": resourcer_email,
                    "object": org_id,
                    "role": "user",
                },
                {
                    "level": "organization",
                    "subject": resourcer_fluid_email,
                    "object": org_id,
                    "role": "user",
                },
                {
                    "level": "organization",
                    "subject": reviewer_email,
                    "object": org_id,
                    "role": "user",
                },
                {
                    "level": "organization",
                    "subject": reviewer_fluid_email,
                    "object": org_id,
                    "role": "user",
                },
                {
                    "level": "organization",
                    "subject": service_forces_fluid_email,
                    "object": org_id,
                    "role": "user",
                },
                {
                    "level": "organization",
                    "subject": customer_manager_fluid_email,
                    "object": org_id,
                    "role": "customer_manager",
                },
            ],
        },
    }


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(autouse=True, scope="session")
async def dynamo_resource(
    event_loop: AbstractEventLoop,  # pylint: disable=redefined-outer-name
) -> AsyncGenerator:
    assert event_loop
    await dynamo_startup()
    yield True
    await dynamo_shutdown()


def pytest_addoption(parser: Any) -> None:
    parser.addoption(
        "--resolver-test-group",
        action="store",
        metavar="RESOLVER_TEST_GROUP",
    )


def pytest_runtest_setup(item: Any) -> None:
    resolver_test_group = item.config.getoption("--resolver-test-group")

    if not resolver_test_group:
        raise ValueError("resolver-test-group not specified")
    if resolver_test_group not in TEST_GROUPS:
        raise ValueError(
            f"resolver-test-group must be one of: {TEST_GROUPS}",
        )

    runnable_groups = {
        mark.args[0] for mark in item.iter_markers(name="resolver_test_group")
    }

    if not runnable_groups or runnable_groups - TEST_GROUPS:
        raise ValueError(f"resolver-test-group must be one of: {TEST_GROUPS}")

    if runnable_groups and resolver_test_group not in runnable_groups:
        pytest.skip(f"Requires resolver test group in: {runnable_groups}")
