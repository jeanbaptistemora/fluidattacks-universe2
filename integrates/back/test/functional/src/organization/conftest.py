# pylint: disable=import-error
from back.test import (
    db,
)
from collections import (
    defaultdict,
)
from datetime import (
    datetime,
)
from db_model.credentials.types import (
    Credentials,
    CredentialsState,
    HttpsPatSecret,
    SshSecret,
)
from db_model.enums import (
    CredentialType,
    GitCloningStatus,
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
from db_model.integration_repositories.types import (
    OrganizationIntegrationRepository,
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
from db_model.roots.enums import (
    RootStatus,
    RootType,
)
from db_model.roots.types import (
    GitRoot,
    GitRootCloning,
    GitRootState,
    IPRoot,
    IPRootState,
    RootEnvironmentUrl,
)
from db_model.types import (
    Policies,
)
from decimal import (
    Decimal,
)
import pytest
from typing import (
    Any,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("organization")
@pytest.fixture(autouse=True, scope="session")
async def populate(generic_data: dict[str, Any]) -> bool:
    data: dict[str, Any] = {
        "groups": [
            {
                "group": Group(
                    created_by="unknown",
                    created_date=datetime.fromisoformat(
                        "2020-05-20T22:00:00+00:00"
                    ),
                    description="-",
                    language=GroupLanguage.EN,
                    name="group1",
                    state=GroupState(
                        has_machine=False,
                        has_squad=True,
                        managed=GroupManaged["MANAGED"],
                        modified_by="unknown",
                        modified_date=datetime.fromisoformat(
                            "2020-05-20T22:00:00+00:00"
                        ),
                        service=GroupService.WHITE,
                        status=GroupStateStatus.ACTIVE,
                        tier=GroupTier.OTHER,
                        type=GroupSubscriptionType.CONTINUOUS,
                    ),
                    organization_id="40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                ),
            },
            {
                "group": Group(
                    created_by="unknown",
                    created_date=datetime.fromisoformat(
                        "2020-05-20T22:00:00+00:00"
                    ),
                    description="-",
                    language=GroupLanguage.EN,
                    name="group2",
                    state=GroupState(
                        has_machine=False,
                        has_squad=True,
                        managed=GroupManaged["MANAGED"],
                        modified_by="unknown",
                        modified_date=datetime.fromisoformat(
                            "2020-05-20T22:00:00+00:00"
                        ),
                        service=GroupService.BLACK,
                        status=GroupStateStatus.ACTIVE,
                        tier=GroupTier.OTHER,
                        type=GroupSubscriptionType.ONESHOT,
                    ),
                    organization_id="8a7c8089-92df-49ec-8c8b-ee83e4ff3256",
                ),
            },
        ],
        "organizations": [
            {
                "organization": Organization(
                    created_by=generic_data["global_vars"]["user_email"],
                    created_date=datetime.fromisoformat(
                        "2019-11-22T20:07:57+00:00"
                    ),
                    country="Colombia",
                    id="40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                    name="orgtest",
                    policies=Policies(
                        inactivity_period=180,
                        modified_by=generic_data["global_vars"]["user_email"],
                        modified_date=datetime.fromisoformat(
                            "2019-11-22T20:07:57+00:00"
                        ),
                        max_acceptance_days=90,
                        max_number_acceptances=4,
                        max_acceptance_severity=Decimal("7.0"),
                        min_acceptance_severity=Decimal("3.0"),
                        min_breaking_severity=Decimal("2.0"),
                        vulnerability_grace_period=5,
                    ),
                    state=OrganizationState(
                        modified_by=generic_data["global_vars"]["user_email"],
                        modified_date=datetime.fromisoformat(
                            "2019-11-22T20:07:57+00:00"
                        ),
                        status=OrganizationStateStatus.ACTIVE,
                    ),
                ),
            },
            {
                "organization": Organization(
                    created_by=generic_data["global_vars"]["user_email"],
                    created_date=datetime.fromisoformat(
                        "2019-11-22T20:07:57+00:00"
                    ),
                    country="Colombia",
                    id="8a7c8089-92df-49ec-8c8b-ee83e4ff3256",
                    name="acme",
                    policies=Policies(
                        modified_by=generic_data["global_vars"]["user_email"],
                        modified_date=datetime.fromisoformat(
                            "2019-11-22T20:07:57+00:00"
                        ),
                    ),
                    state=OrganizationState(
                        modified_by=generic_data["global_vars"]["user_email"],
                        modified_date=datetime.fromisoformat(
                            "2019-11-22T20:07:57+00:00"
                        ),
                        status=OrganizationStateStatus.ACTIVE,
                    ),
                    vulnerabilities_url="https://test.com",
                ),
            },
        ],
        "roots": [
            {
                "root": GitRoot(
                    cloning=GitRootCloning(
                        modified_date=datetime.fromisoformat(
                            "2020-11-19T13:38:10+00:00"
                        ),
                        reason="root creation",
                        status=GitCloningStatus("UNKNOWN"),
                    ),
                    created_by=generic_data["global_vars"]["admin_email"],
                    created_date=datetime.fromisoformat(
                        "2020-11-19T13:37:10+00:00"
                    ),
                    group_name="group1",
                    id="63298a73-9dff-46cf-b42d-9b2f01a56690",
                    organization_name="orgtest",
                    state=GitRootState(
                        branch="master",
                        environment="production",
                        environment_urls=["https://test.com"],
                        git_environment_urls=[
                            RootEnvironmentUrl(
                                url="https://test.com",
                                id="78dd64d3198473115a7f5263d27bed15f9f2fc07",
                            )
                        ],
                        gitignore=["bower_components/*", "node_modules/*"],
                        includes_health_check=True,
                        modified_by=generic_data["global_vars"]["admin_email"],
                        modified_date=datetime.fromisoformat(
                            "2020-11-19T13:37:10+00:00"
                        ),
                        nickname="",
                        other=None,
                        reason=None,
                        status=RootStatus.ACTIVE,
                        url="https://gitlab.com/fluidattacks/universe",
                    ),
                    type=RootType.GIT,
                ),
                "historic_state": [],
            },
            {
                "root": IPRoot(
                    created_by=generic_data["global_vars"]["admin_email"],
                    created_date=datetime.fromisoformat(
                        "2020-11-21T13:37:10+00:00"
                    ),
                    group_name="group2",
                    id="83cadbdc-23f3-463a-9421-f50f8d0cb1e5",
                    organization_name="orgtest",
                    state=IPRootState(
                        address="192.168.1.1",
                        modified_by=generic_data["global_vars"]["admin_email"],
                        modified_date=datetime.fromisoformat(
                            "2020-11-21T13:37:10+00:00"
                        ),
                        nickname="",
                        other=None,
                        reason=None,
                        status=RootStatus.ACTIVE,
                    ),
                    type=RootType.IP,
                ),
                "historic_state": [],
            },
        ],
        "organization_access": [
            OrganizationAccess(
                organization_id="8a7c8089-92df-49ec-8c8b-ee83e4ff3256",
                email=generic_data["global_vars"]["admin_email"],
            ),
            OrganizationAccess(
                organization_id="40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                email=generic_data["global_vars"]["admin_email"],
            ),
        ],
        "policies": [
            {
                "level": "group",
                "subject": generic_data["global_vars"]["admin_email"],
                "object": "group3",
                "role": "admin",
            },
            {
                "level": "group",
                "subject": generic_data["global_vars"]["admin_email"],
                "object": "unittesting",
                "role": "admin",
            },
            {
                "level": "group",
                "subject": generic_data["global_vars"]["admin_email"],
                "object": "group1",
                "role": "admin",
            },
        ],
        "credentials": (
            Credentials(
                id="3912827d-2b35-4e08-bd35-1bb24457951d",
                organization_id="ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                owner="admin@gmail.com",
                state=CredentialsState(
                    modified_by="admin@gmail.com",
                    modified_date=datetime.fromisoformat(
                        "2022-02-10T14:58:10+00:00"
                    ),
                    name="SSH Key",
                    type=CredentialType.SSH,
                    secret=SshSecret(key="VGVzdCBTU0gK"),
                    is_pat=False,
                ),
            ),
            Credentials(
                id="1a5dacda-1d52-465c-9158-f6fd5dfe0998",
                organization_id="ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                owner="admin@gmail.com",
                state=CredentialsState(
                    azure_organization="testorg1",
                    modified_by="admin@gmail.com",
                    modified_date=datetime.fromisoformat(
                        "2022-02-10T14:58:10+00:00"
                    ),
                    name="pat token",
                    type=CredentialType.HTTPS,
                    secret=HttpsPatSecret(token="VGVzdCBTU0gK"),
                    is_pat=True,
                ),
            ),
        ),
        "organization_unreliable_integration_repository": (
            OrganizationIntegrationRepository(
                id=(
                    "4334ca3f5c8afb8b529782a6b96daa94160e5f3c030ebbc5f"
                    "369d800b2a8b584"
                ),
                organization_id="ORG#40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                branch="main",
                last_commit_date=datetime.fromisoformat(
                    "2022-11-02T09:37:57+00:00"
                ),
                url="ssh://git@test.com:v3/testprojects/_git/secondrepor",
                commit_count=4,
            ),
        ),
    }

    merge_dict: dict[str, list[Any]] = defaultdict(list)
    for dict_data in (generic_data["db_data"], data):
        for key, value in dict_data.items():
            if key == "groups":
                all_groups = merge_dict[key] + value
                merge_dict[key] = list(
                    {
                        group["group"].name: group for group in all_groups
                    }.values()
                )
            elif key == "organizations":
                all_organizations = merge_dict[key] + value
                merge_dict[key] = list(
                    {
                        organization["organization"].id: organization
                        for organization in all_organizations
                    }.values()
                )
            else:
                merge_dict[key].extend(value)

    return await db.populate(merge_dict)
