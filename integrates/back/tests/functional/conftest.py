import pytest
from typing import (
    Any,
    Dict,
    Set,
)

# Constants
TEST_GROUPS: Set[str] = {
    "activate_root",
    "add_event_consult",
    "add_files",
    "add_finding_consult",
    "add_git_root",
    "add_group_consult",
    "add_tags",
    "approve_draft",
    "approve_draft_new",
    "create_draft",
    "create_draft_new",
    "create_event",
    "create_organization",
    "create_group",
    "deactivate_root",
    "delete_finding",
    "delete_finding_new",
    "delete_tags",
    "delete_vulnerability",
    "download_event_file",
    "download_vuln_file",
    "download_file",
    "edit_group",
    "edit_stakeholder",
    "edit_stakeholder_organization",
    "event",
    "events",
    "finding",
    "finding_new",
    "forces_executions",
    "grant_stakeholder_access",
    "grant_stakeholder_organization_access",
    "groups_with_forces",
    "internal_names",
    "old",
    "organization",
    "organization_id",
    "group",
    "reject_draft",
    "reject_draft_new",
    "remove_event_evidence",
    "remove_evidence",
    "remove_files",
    "remove_group",
    "remove_stakeholder_access",
    "remove_stakeholder_organization_access",
    "remove_tag",
    "request_verification_vuln",
    "request_zero_risk_vuln",
    "resources",
    "sign_in",
    "solve_event",
    "stakeholder",
    "submit_draft",
    "submit_draft_new",
    "submit_organization_finding_policy",
    "toe_inputs",
    "toe_lines",
    "unsubscribe_from_group",
    "update_access_token",
    "update_event_evidence",
    "update_evidence",
    "update_evidence_new",
    "update_evidence_description",
    "update_finding_description",
    "update_finding_description_new",
    "update_forces_access_token",
    "update_organization_policies",
    "update_severity",
    "update_severity_new",
    "update_toe_lines_sorts",
    "update_treatment_vuln",
    "update_vuln_commit",
    "upload_file",
    "verify_request_vuln",
    "vulnerability",
}


@pytest.fixture(autouse=True, scope="session")
def generic_data() -> Dict[str, Any]:  # pylint: disable=too-many-locals
    admin_email: str = "admin@gmail.com"
    admin_fluid_email: str = "admin@fluidattacks.com"
    analyst_email: str = "analyst@gmail.com"
    analyst_fluid_email: str = "analyst@fluidattacks.com"
    closer_email: str = "closer@gmail.com"
    closer_fluid_email: str = "closer@fluidattacks.com"
    customer_email: str = "customer@gmail.com"
    customer_fluid_email: str = "customer@fluidattacks.com"
    customer_admin_email: str = "customeradmin@gmail.com"
    customer_admin_fluid_email: str = "customeradmin@fluidattacks.com"
    executive_email: str = "executive@gmail.com"
    executive_fluid_email: str = "executive@fluidattacks.com"
    group_manager_email: str = "group_manager@gmail.com"
    group_manager_fluid_email: str = "group_manager@fluidattacks.com"
    resourcer_email: str = "resourcer@gmail.com"
    resourcer_fluid_email: str = "resourcer@fluidattacks.com"
    reviewer_email: str = "reviewer@gmail.com"
    reviewer_fluid_email: str = "reviewer@fluidattacks.com"
    service_forces_email: str = "service_forces@gmail.com"
    service_forces_fluid_email: str = "service_forces@fluidattacks.com"
    org_id: str = "ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db"
    return {
        "global_vars": {
            "admin_email": admin_email,
            "admin_fluid_email": admin_fluid_email,
            "analyst_email": analyst_email,
            "analyst_fluid_email": analyst_fluid_email,
            "closer_email": closer_email,
            "closer_fluid_email": closer_fluid_email,
            "customer_email": customer_email,
            "customer_fluid_email": customer_fluid_email,
            "customer_admin_email": customer_admin_email,
            "customer_admin_fluid_email": customer_admin_fluid_email,
            "executive_email": executive_email,
            "executive_fluid_email": executive_fluid_email,
            "group_manager_email": group_manager_email,
            "group_manager_fluid_email": group_manager_fluid_email,
            "resourcer_email": resourcer_email,
            "resourcer_fluid_email": resourcer_fluid_email,
            "reviewer_email": reviewer_email,
            "reviewer_fluid_email": reviewer_fluid_email,
            "service_forces_email": service_forces_email,
            "service_forces_fluid_email": service_forces_fluid_email,
            "FIN.H.060": "FIN.H.060. Insecure exceptions",
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
                    "email": analyst_email,
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
                    "email": analyst_fluid_email,
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
                    "email": closer_email,
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
                    "email": closer_fluid_email,
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
                    "email": group_manager_email,
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
                    "email": group_manager_fluid_email,
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
            ],
            "orgs": [
                {
                    "name": "orgtest",
                    "id": "40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                    "users": [
                        admin_email,
                        admin_fluid_email,
                        analyst_email,
                        analyst_fluid_email,
                        closer_email,
                        closer_fluid_email,
                        customer_email,
                        customer_fluid_email,
                        customer_admin_email,
                        customer_admin_fluid_email,
                        group_manager_email,
                        group_manager_fluid_email,
                        executive_email,
                        executive_fluid_email,
                        resourcer_email,
                        resourcer_fluid_email,
                        reviewer_email,
                        reviewer_fluid_email,
                        service_forces_email,
                        service_forces_fluid_email,
                    ],
                    "groups": [
                        "group1",
                        "group2",
                    ],
                    "policy": {},
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
                    "subject": analyst_email,
                    "object": "self",
                    "role": "analyst",
                },
                {
                    "level": "user",
                    "subject": analyst_fluid_email,
                    "object": "self",
                    "role": "analyst",
                },
                {
                    "level": "user",
                    "subject": closer_email,
                    "object": "self",
                    "role": "closer",
                },
                {
                    "level": "user",
                    "subject": closer_fluid_email,
                    "object": "self",
                    "role": "closer",
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
                    "subject": group_manager_email,
                    "object": "self",
                    "role": "group_manager",
                },
                {
                    "level": "user",
                    "subject": group_manager_fluid_email,
                    "object": "self",
                    "role": "group_manager",
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
                    "level": "group",
                    "subject": analyst_email,
                    "object": "group1",
                    "role": "analyst",
                },
                {
                    "level": "group",
                    "subject": analyst_fluid_email,
                    "object": "group1",
                    "role": "analyst",
                },
                {
                    "level": "group",
                    "subject": closer_email,
                    "object": "group1",
                    "role": "closer",
                },
                {
                    "level": "group",
                    "subject": closer_fluid_email,
                    "object": "group1",
                    "role": "closer",
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
                    "subject": group_manager_email,
                    "object": "group1",
                    "role": "group_manager",
                },
                {
                    "level": "group",
                    "subject": group_manager_fluid_email,
                    "object": "group1",
                    "role": "group_manager",
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
                    "subject": analyst_email,
                    "object": org_id,
                    "role": "analyst",
                },
                {
                    "level": "organization",
                    "subject": analyst_fluid_email,
                    "object": org_id,
                    "role": "analyst",
                },
                {
                    "level": "organization",
                    "subject": closer_email,
                    "object": org_id,
                    "role": "closer",
                },
                {
                    "level": "organization",
                    "subject": closer_fluid_email,
                    "object": org_id,
                    "role": "closer",
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
                    "subject": group_manager_email,
                    "object": org_id,
                    "role": "group_manager",
                },
                {
                    "level": "organization",
                    "subject": group_manager_fluid_email,
                    "object": org_id,
                    "role": "group_manager",
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
