import pytest
from typing import (
    Any,
    Dict,
    Set,
)

# Constants
TEST_GROUPS: Set[str] = {
    "accept_legal",
    "acknowledge_concurrent_session",
    "activate_root",
    "add_draft",
    "add_draft_new",
    "add_event",
    "add_event_consult",
    "add_files_to_db",
    "add_finding_consult",
    "add_finding_consult_new",
    "add_forces_execution",
    "add_git_root",
    "add_group",
    "add_group_consult",
    "add_group_tags",
    "add_organization",
    "add_push_token",
    "approve_draft",
    "approve_draft_new",
    "confirm_vulnerabilities_zero_risk_new",
    "deactivate_root",
    "delete_obsolete_groups",
    "download_event_file",
    "download_vulnerability_file",
    "download_vulnerability_file_new",
    "download_file",
    "event",
    "events",
    "finding",
    "finding_new",
    "forces_executions",
    "handle_vulnerabilities_acceptance_new",
    "grant_stakeholder_access",
    "grant_stakeholder_organization_access",
    "groups_with_forces",
    "internal_names",
    "invalidate_access_token",
    "me",
    "old",
    "organization",
    "organization_id",
    "group",
    "group_new",
    "reject_draft",
    "reject_draft_new",
    "reject_vulnerabilities_zero_risk_new",
    "remove_event_evidence",
    "remove_evidence",
    "remove_evidence_new",
    "remove_files",
    "remove_finding",
    "remove_finding_new",
    "remove_group",
    "remove_group_new",
    "remove_group_tag",
    "remove_stakeholder_access",
    "remove_stakeholder_organization_access",
    "remove_tags_new",
    "remove_vulnerability",
    "remove_vulnerability_new",
    "report",
    "request_vulnerabilities_verification",
    "request_vulnerabilities_verification_new",
    "request_vulnerabilities_zero_risk",
    "request_vulnerabilities_zero_risk_new",
    "reset_expired_accepted_findings",
    "resources",
    "sign_post_url",
    "sign_post_url_requester",
    "sign_in",
    "solve_event",
    "stakeholder",
    "submit_draft",
    "submit_draft_new",
    "submit_organization_finding_policy",
    "subscribe_to_entity_report",
    "toe_inputs",
    "toe_lines",
    "unsubscribe_from_group",
    "update_access_token",
    "update_event_evidence",
    "update_evidence",
    "update_evidence_new",
    "update_evidence_description",
    "update_evidence_description_new",
    "update_finding_description",
    "update_finding_description_new",
    "update_forces_access_token",
    "update_group",
    "update_group_stakeholder",
    "update_organization_policies",
    "update_organization_stakeholder",
    "update_severity",
    "update_severity_new",
    "update_toe_lines_sorts",
    "update_vulnerabilities_treatment_new",
    "update_vulnerability_commit",
    "update_vulnerability_commit_new",
    "update_vulnerability_treatment",
    "update_vulnerability_treatment_new",
    "upload_file",
    "upload_file_new",
    "verify_vulnerabilities_request",
    "verify_vulnerabilities_request_new",
    "vulnerability",
    "vulnerability_new",
}


@pytest.fixture(autouse=True, scope="session")
def generic_data() -> Dict[str, Any]:  # pylint: disable=too-many-locals
    admin_email: str = "admin@gmail.com"
    admin_fluid_email: str = "admin@fluidattacks.com"
    customer_email: str = "customer@gmail.com"
    customer_fluid_email: str = "customer@fluidattacks.com"
    customer_admin_email: str = "customeradmin@gmail.com"
    customer_admin_fluid_email: str = "customeradmin@fluidattacks.com"
    executive_email: str = "executive@gmail.com"
    executive_fluid_email: str = "executive@fluidattacks.com"
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
    system_owner_email: str = "system_owner@gmail.com"
    system_owner_fluid_email: str = "system_owner@fluidattacks.com"
    org_id: str = "ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db"
    return {
        "global_vars": {
            "admin_email": admin_email,
            "admin_fluid_email": admin_fluid_email,
            "customer_email": customer_email,
            "customer_fluid_email": customer_fluid_email,
            "customer_admin_email": customer_admin_email,
            "customer_admin_fluid_email": customer_admin_fluid_email,
            "executive_email": executive_email,
            "executive_fluid_email": executive_fluid_email,
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
            "system_owner_email": system_owner_email,
            "system_owner_fluid_email": system_owner_fluid_email,
            "FIN.H.060": "060. Insecure exceptions",
            "R359": "R359. Avoid using generic exceptions.",
        },
        "db_data": {
            "users": [
                {
                    "email": admin_email,
                    "first_login": "",
                    "first_name": "",
                    "last_login": "",
                    "last_name": "",
                    "legal_remember": False,
                    "phone_number": "-",
                    "push_tokens": [],
                    "is_registered": True,
                },
                {
                    "email": admin_fluid_email,
                    "first_login": "",
                    "first_name": "",
                    "last_login": "",
                    "last_name": "",
                    "legal_remember": False,
                    "phone_number": "-",
                    "push_tokens": [],
                    "is_registered": True,
                },
                {
                    "email": customer_email,
                    "first_login": "",
                    "first_name": "",
                    "last_login": "",
                    "last_name": "",
                    "legal_remember": False,
                    "phone_number": "-",
                    "push_tokens": [],
                    "is_registered": True,
                },
                {
                    "email": customer_fluid_email,
                    "first_login": "",
                    "first_name": "",
                    "last_login": "",
                    "last_name": "",
                    "legal_remember": False,
                    "phone_number": "-",
                    "push_tokens": [],
                    "is_registered": True,
                },
                {
                    "email": customer_admin_email,
                    "first_login": "",
                    "first_name": "",
                    "last_login": "",
                    "last_name": "",
                    "legal_remember": False,
                    "phone_number": "-",
                    "push_tokens": [],
                    "is_registered": True,
                },
                {
                    "email": customer_admin_fluid_email,
                    "first_login": "",
                    "first_name": "",
                    "last_login": "",
                    "last_name": "",
                    "legal_remember": False,
                    "phone_number": "-",
                    "push_tokens": [],
                    "is_registered": True,
                },
                {
                    "email": executive_email,
                    "first_login": "",
                    "first_name": "",
                    "last_login": "",
                    "last_name": "",
                    "legal_remember": False,
                    "phone_number": "-",
                    "push_tokens": [],
                    "is_registered": True,
                },
                {
                    "email": executive_fluid_email,
                    "first_login": "",
                    "first_name": "",
                    "last_login": "",
                    "last_name": "",
                    "legal_remember": False,
                    "phone_number": "-",
                    "push_tokens": [],
                    "is_registered": True,
                },
                {
                    "email": hacker_email,
                    "first_login": "",
                    "first_name": "",
                    "last_login": "",
                    "last_name": "",
                    "legal_remember": False,
                    "phone_number": "-",
                    "push_tokens": [],
                    "is_registered": True,
                },
                {
                    "email": hacker_fluid_email,
                    "first_login": "",
                    "first_name": "",
                    "last_login": "",
                    "last_name": "",
                    "legal_remember": False,
                    "phone_number": "-",
                    "push_tokens": [],
                    "is_registered": True,
                },
                {
                    "email": resourcer_email,
                    "first_login": "",
                    "first_name": "",
                    "last_login": "",
                    "last_name": "",
                    "legal_remember": False,
                    "phone_number": "-",
                    "push_tokens": [],
                    "is_registered": True,
                },
                {
                    "email": reattacker_email,
                    "first_login": "",
                    "first_name": "",
                    "last_login": "",
                    "last_name": "",
                    "legal_remember": False,
                    "phone_number": "-",
                    "push_tokens": [],
                    "is_registered": True,
                },
                {
                    "email": reattacker_fluid_email,
                    "first_login": "",
                    "first_name": "",
                    "last_login": "",
                    "last_name": "",
                    "legal_remember": False,
                    "phone_number": "-",
                    "push_tokens": [],
                    "is_registered": True,
                },
                {
                    "email": resourcer_fluid_email,
                    "first_login": "",
                    "first_name": "",
                    "last_login": "",
                    "last_name": "",
                    "legal_remember": False,
                    "phone_number": "-",
                    "push_tokens": [],
                    "is_registered": True,
                },
                {
                    "email": reviewer_email,
                    "first_login": "",
                    "first_name": "",
                    "last_login": "",
                    "last_name": "",
                    "legal_remember": False,
                    "phone_number": "-",
                    "push_tokens": [],
                    "is_registered": True,
                },
                {
                    "email": reviewer_fluid_email,
                    "first_login": "",
                    "first_name": "",
                    "last_login": "",
                    "last_name": "",
                    "legal_remember": False,
                    "phone_number": "-",
                    "push_tokens": [],
                    "is_registered": True,
                },
                {
                    "email": service_forces_email,
                    "first_login": "",
                    "first_name": "",
                    "last_login": "",
                    "last_name": "",
                    "legal_remember": False,
                    "phone_number": "-",
                    "push_tokens": [],
                    "is_registered": True,
                },
                {
                    "email": service_forces_fluid_email,
                    "first_login": "",
                    "first_name": "",
                    "last_login": "",
                    "last_name": "",
                    "legal_remember": False,
                    "phone_number": "-",
                    "push_tokens": [],
                    "is_registered": True,
                },
                {
                    "email": system_owner_email,
                    "first_login": "",
                    "first_name": "",
                    "last_login": "",
                    "last_name": "",
                    "legal_remember": False,
                    "phone_number": "-",
                    "push_tokens": [],
                    "is_registered": True,
                },
                {
                    "email": system_owner_fluid_email,
                    "first_login": "",
                    "first_name": "",
                    "last_login": "",
                    "last_name": "",
                    "legal_remember": False,
                    "phone_number": "-",
                    "push_tokens": [],
                    "is_registered": True,
                },
            ],
            "orgs": [
                {
                    "name": "orgtest",
                    "id": "40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                    "users": [
                        admin_email,
                        admin_fluid_email,
                        hacker_email,
                        hacker_fluid_email,
                        reattacker_email,
                        reattacker_fluid_email,
                        customer_email,
                        customer_fluid_email,
                        customer_admin_email,
                        customer_admin_fluid_email,
                        executive_email,
                        executive_fluid_email,
                        resourcer_email,
                        resourcer_fluid_email,
                        reviewer_email,
                        reviewer_fluid_email,
                        service_forces_email,
                        service_forces_fluid_email,
                        system_owner_email,
                        system_owner_fluid_email,
                    ],
                    "groups": [
                        "group1",
                        "group2",
                        "group3",
                    ],
                    "policy": {},
                    "max_acceptance_days": 7,
                },
            ],
            "groups": [
                {
                    "project_name": "group1",
                    "description": "-",
                    "language": "en",
                    "historic_configuration": [
                        {
                            "date": "2020-05-20 17:00:00",
                            "has_drills": True,
                            "has_forces": True,
                            "requester": "unknown",
                            "service": "WHITE",
                            "type": "continuous",
                        }
                    ],
                    "project_status": "ACTIVE",
                },
                {
                    "project_name": "group2",
                    "description": "-",
                    "language": "en",
                    "historic_configuration": [
                        {
                            "date": "2020-05-20 17:00:00",
                            "has_drills": True,
                            "has_forces": True,
                            "requester": "unknown",
                            "service": "BLACK",
                            "type": "oneshot",
                        }
                    ],
                    "project_status": "ACTIVE",
                },
                {
                    "project_name": "group3",
                    "description": "-",
                    "language": "en",
                    "historic_configuration": [
                        {
                            "date": "2020-05-20 17:00:00",
                            "has_drills": False,
                            "has_forces": True,
                            "requester": "unknown",
                            "service": "BLACK",
                            "type": "oneshot",
                        }
                    ],
                    "project_status": "ACTIVE",
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
                    "role": "reattacker",
                },
                {
                    "level": "user",
                    "subject": reattacker_fluid_email,
                    "object": "self",
                    "role": "reattacker",
                },
                {
                    "level": "user",
                    "subject": customer_email,
                    "object": "self",
                    "role": "customer",
                },
                {
                    "level": "user",
                    "subject": customer_fluid_email,
                    "object": "self",
                    "role": "customer",
                },
                {
                    "level": "user",
                    "subject": customer_admin_email,
                    "object": "self",
                    "role": "customeradmin",
                },
                {
                    "level": "user",
                    "subject": customer_admin_fluid_email,
                    "object": "self",
                    "role": "customeradmin",
                },
                {
                    "level": "user",
                    "subject": executive_email,
                    "object": "self",
                    "role": "executive",
                },
                {
                    "level": "user",
                    "subject": executive_fluid_email,
                    "object": "self",
                    "role": "executive",
                },
                {
                    "level": "user",
                    "subject": resourcer_email,
                    "object": "self",
                    "role": "resourcer",
                },
                {
                    "level": "user",
                    "subject": resourcer_fluid_email,
                    "object": "self",
                    "role": "resourcer",
                },
                {
                    "level": "user",
                    "subject": reviewer_email,
                    "object": "self",
                    "role": "reviewer",
                },
                {
                    "level": "user",
                    "subject": reviewer_fluid_email,
                    "object": "self",
                    "role": "reviewer",
                },
                {
                    "level": "user",
                    "subject": service_forces_email,
                    "object": "self",
                    "role": "service_forces",
                },
                {
                    "level": "user",
                    "subject": service_forces_fluid_email,
                    "object": "self",
                    "role": "service_forces",
                },
                {
                    "level": "user",
                    "subject": system_owner_email,
                    "object": "self",
                    "role": "system_owner",
                },
                {
                    "level": "user",
                    "subject": system_owner_fluid_email,
                    "object": "self",
                    "role": "system_owner",
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
                    "subject": customer_email,
                    "object": "group1",
                    "role": "customer",
                },
                {
                    "level": "group",
                    "subject": customer_fluid_email,
                    "object": "group1",
                    "role": "customer",
                },
                {
                    "level": "group",
                    "subject": customer_admin_email,
                    "object": "group1",
                    "role": "customeradmin",
                },
                {
                    "level": "group",
                    "subject": customer_admin_fluid_email,
                    "object": "group1",
                    "role": "customeradmin",
                },
                {
                    "level": "group",
                    "subject": executive_email,
                    "object": "group1",
                    "role": "executive",
                },
                {
                    "level": "group",
                    "subject": executive_fluid_email,
                    "object": "group1",
                    "role": "executive",
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
                    "subject": system_owner_email,
                    "object": "group1",
                    "role": "system_owner",
                },
                {
                    "level": "group",
                    "subject": system_owner_fluid_email,
                    "object": "group1",
                    "role": "system_owner",
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
                    "subject": hacker_email,
                    "object": org_id,
                    "role": "hacker",
                },
                {
                    "level": "organization",
                    "subject": hacker_fluid_email,
                    "object": org_id,
                    "role": "hacker",
                },
                {
                    "level": "organization",
                    "subject": reattacker_email,
                    "object": org_id,
                    "role": "reattacker",
                },
                {
                    "level": "organization",
                    "subject": reattacker_fluid_email,
                    "object": org_id,
                    "role": "reattacker",
                },
                {
                    "level": "organization",
                    "subject": customer_email,
                    "object": org_id,
                    "role": "customer",
                },
                {
                    "level": "organization",
                    "subject": customer_fluid_email,
                    "object": org_id,
                    "role": "customer",
                },
                {
                    "level": "organization",
                    "subject": customer_admin_email,
                    "object": org_id,
                    "role": "customeradmin",
                },
                {
                    "level": "organization",
                    "subject": customer_admin_fluid_email,
                    "object": org_id,
                    "role": "customeradmin",
                },
                {
                    "level": "organization",
                    "subject": executive_email,
                    "object": org_id,
                    "role": "executive",
                },
                {
                    "level": "organization",
                    "subject": executive_fluid_email,
                    "object": org_id,
                    "role": "executive",
                },
                {
                    "level": "organization",
                    "subject": resourcer_email,
                    "object": org_id,
                    "role": "resourcer",
                },
                {
                    "level": "organization",
                    "subject": resourcer_fluid_email,
                    "object": org_id,
                    "role": "resourcer",
                },
                {
                    "level": "organization",
                    "subject": reviewer_email,
                    "object": org_id,
                    "role": "reviewer",
                },
                {
                    "level": "organization",
                    "subject": reviewer_fluid_email,
                    "object": org_id,
                    "role": "reviewer",
                },
                {
                    "level": "organization",
                    "subject": service_forces_email,
                    "object": org_id,
                    "role": "service_forces",
                },
                {
                    "level": "organization",
                    "subject": service_forces_fluid_email,
                    "object": org_id,
                    "role": "service_forces",
                },
                {
                    "level": "organization",
                    "subject": system_owner_email,
                    "object": org_id,
                    "role": "system_owner",
                },
                {
                    "level": "organization",
                    "subject": system_owner_fluid_email,
                    "object": org_id,
                    "role": "system_owner",
                },
            ],
        },
    }


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
