import authz
import pytest
from typing import (
    Any,
    Dict,
    List,
)

# Constants
pytestmark = [
    pytest.mark.asyncio,
]


@pytest.mark.parametrize(
    ["parameter", "expected"],
    [
        (
            authz.GROUP_LEVEL_ROLES,
            [
                "admin",
                "analyst",
                "closer",
                "customer",
                "customeradmin",
                "executive",
                "group_manager",
                "hacker",
                "reattacker",
                "resourcer",
                "reviewer",
                "service_forces",
                "system_owner",
            ],
        ),
        (
            authz.GROUP_LEVEL_ROLES_FOR_FLUIDATTACKS,
            [
                "admin",
                "analyst",
                "closer",
                "customer",
                "customeradmin",
                "executive",
                "group_manager",
                "hacker",
                "reattacker",
                "resourcer",
                "reviewer",
                "service_forces",
                "system_owner",
            ],
        ),
        (
            authz.USER_LEVEL_ROLES,
            [
                "admin",
                "analyst",
                "customer",
                "hacker",
            ],
        ),
        (
            authz.USER_LEVEL_ROLES_FOR_FLUIDATTACKS,
            [
                "admin",
                "analyst",
                "customer",
                "hacker",
            ],
        ),
        (
            authz.SERVICE_ATTRIBUTES,
            [
                "asm",
                "continuous",
                "forces",
                "service_black",
                "service_white",
                "squad",
            ],
        ),
    ],
)
def test_model_integrity_keys_1(
    parameter: Dict[str, Any], expected: List[str]
) -> None:
    assert sorted(parameter.keys()) == expected


@pytest.mark.parametrize(
    ["parameter"],
    [
        [authz.GROUP_LEVEL_ROLES],
        [authz.GROUP_LEVEL_ROLES_FOR_FLUIDATTACKS],
        [authz.USER_LEVEL_ROLES],
        [authz.USER_LEVEL_ROLES_FOR_FLUIDATTACKS],
    ],
)
def test_model_integrity_keys_2(parameter: Dict[str, Any]) -> None:
    for value in parameter.values():
        assert sorted(value.keys()) == ["actions", "tags"]


@pytest.mark.parametrize(
    ["roles_common", "roles_fluid"],
    [
        (authz.GROUP_LEVEL_ROLES, authz.GROUP_LEVEL_ROLES_FOR_FLUIDATTACKS),
        (
            authz.ORGANIZATION_LEVEL_ROLES,
            authz.ORGANIZATION_LEVEL_ROLES_FOR_FLUIDATTACKS,
        ),
        (authz.USER_LEVEL_ROLES, authz.USER_LEVEL_ROLES_FOR_FLUIDATTACKS),
    ],
)
def test_model_integrity_roles(
    roles_common: Dict[str, Any], roles_fluid: Dict[str, Any]
) -> None:
    assert sorted(roles_common.keys()) == sorted(roles_fluid.keys())


@pytest.mark.parametrize(
    ["permission_name", "permissions"],
    [
        ["GROUP_LEVEL_ROLES", authz.GROUP_LEVEL_ROLES],
        [
            "GROUP_LEVEL_ROLES_FOR_FLUIDATTACKS",
            authz.GROUP_LEVEL_ROLES_FOR_FLUIDATTACKS,
        ],
    ],
)
def test_model_integrity_migrated_finding_permissions(
    permission_name: str, permissions: Dict[str, Any]
) -> None:
    migrated_permissions = {
        "api_mutations_approve_draft_mutate": "api_mutations_"
        "approve_draft_new_mutate",
        "api_mutations_add_draft_mutate": "api_mutations_"
        "add_draft_new_mutate",
        "api_mutations_handle_vulnerabilities_acceptance_mutate": "api_"
        "mutations_handle_vulnerabilities_acceptance_new_mutate",
        "api_mutations_remove_finding_mutate": "api_mutations_"
        "remove_finding_new_mutate",
        "api_mutations_reject_draft_mutate": "api_mutations_"
        "reject_draft_new_mutate",
        "api_mutations_reject_vulnerabilities_zero_risk_mutate": "api_"
        "mutations_reject_vulnerabilities_zero_risk_new_mutate",
        "api_mutations_remove_finding_evidence_mutate": "api_mutations_"
        "remove_finding_evidence_new_mutate",
        "api_mutations_remove_group_mutate": "api_mutations_"
        "remove_group_new_mutate",
        "api_mutations_remove_vulnerability_mutate": "api_mutations_"
        "remove_vulnerability_new_mutate",
        "api_mutations_request_vulnerabilities_verification_mutate": "api_"
        "mutations_request_vulnerabilities_verification_new_mutate",
        "api_mutations_request_vulnerabilities_zero_risk_mutate": "api_"
        "mutations_request_vulnerabilities_zero_risk_new_mutate",
        "api_mutations_submit_draft_mutate": "api_mutations_"
        "submit_draft_new_mutate",
        "api_mutations_update_evidence_mutate": "api_mutations_"
        "update_evidence_new_mutate",
        "api_mutations_update_evidence_description_mutate": "api_mutations_"
        "update_evidence_description_new_mutate",
        "api_mutations_update_finding_description_mutate": "api_mutations_"
        "update_finding_description_new_mutate",
        "api_mutations_update_severity_mutate": "api_mutations_"
        "update_severity_new_mutate",
        "api_mutations_update_vulnerability_commit_mutate": "api_mutations_"
        "update_vulnerability_commit_new_mutate",
        "api_mutations_update_vulnerabilities_treatment_mutate": "api_"
        "mutations_update_vulnerabilities_treatment_new_mutate",
        "api_mutations_upload_file_mutate": "api_mutations_"
        "upload_file_new_mutate",
        "api_mutations_verify_vulnerabilities_request_mutate": "api_mutations_"
        "verify_vulnerabilities_request_new_mutate",
        "api_resolvers_finding_hacker_resolve": "api_resolvers_"
        "finding_new_hacker_new_resolve",
        "api_resolvers_finding_historic_state_resolve": "api_resolvers_"
        "finding_new_historic_state_new_resolve",
        "api_resolvers_finding_machine_jobs_resolve": "api_resolvers_"
        "finding_new_machine_jobs_new_resolve",
        "api_resolvers_finding_observations_resolve": "api_resolvers_"
        "finding_new_observations_new_resolve",
        "api_resolvers_finding_sorts_resolve": "api_resolvers_"
        "finding_new_sorts_new_resolve",
        "api_resolvers_finding_zero_risk_resolve": "api_resolvers_"
        "finding_new_zero_risk_new_resolve",
        "api_resolvers_group_drafts_resolve": "api_resolvers_"
        "group_drafts_new_resolve",
        "api_resolvers_query_finding_resolve": "api_resolvers_"
        "query_finding_new_resolve",
        "api_resolvers_query_finding__get_draft": "api_resolvers_"
        "query_finding_new__get_draft",
    }
    for role, value in permissions.items():
        for current_p, new_p in migrated_permissions.items():
            assert (current_p in value["actions"]) == (
                new_p in value["actions"]
            ), f"if {current_p} is included in the {role} "
            f"actions for {permission_name} then {new_p} must be included"
