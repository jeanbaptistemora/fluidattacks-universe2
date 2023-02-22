import authz
from back.test.unit.src.utils import (  # pylint: disable=import-error
    get_mock_response,
    get_mocked_path,
    get_module_at_test,
    set_mocks_return_values,
    set_mocks_side_effects,
)
from custom_exceptions import (
    InvalidAcceptanceDays,
    InvalidAcceptanceSeverity,
    InvalidAcceptanceSeverityRange,
    InvalidInactivityPeriod,
    InvalidNumberAcceptances,
    InvalidOrganization,
    StakeholderNotInOrganization,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.constants import (
    MIN_INACTIVITY_PERIOD,
)
from db_model.types import (
    PoliciesToUpdate,
)
from decimal import (
    Decimal,
)
from group_access import (
    domain as group_access_domain,
)
import json
from organization_access import (
    domain as orgs_access,
)
from organizations.domain import (
    add_group_access,
    add_organization,
    add_stakeholder,
    get_group_names,
    get_stakeholders,
    get_stakeholders_emails,
    has_group,
    remove_access,
    remove_organization,
    update_policies,
    validate_acceptance_severity_range,
    validate_inactivity_period,
    validate_max_acceptance_days,
    validate_max_acceptance_severity,
    validate_max_number_acceptances,
)
import pytest
from unittest.mock import (
    AsyncMock,
    patch,
)

MODULE_AT_TEST = get_module_at_test(file_path=__file__)

# Run async tests
pytestmark = [
    pytest.mark.asyncio,
]


@pytest.mark.parametrize(
    ["organization_id", "email", "role"],
    [
        [
            "ORG#f2e2777d-a168-4bea-93cd-d79142b294d2",
            "org_testgroupmanager2@fluidattacks.com",
            "customer_manager",
        ],
    ],
)
@patch(
    get_mocked_path("group_access_domain.add_access"), new_callable=AsyncMock
)
@patch(get_mocked_path("get_group_names"), new_callable=AsyncMock)
@patch(
    get_mocked_path("authz.grant_organization_level_role"),
    new_callable=AsyncMock,
)
@patch(
    get_mocked_path("org_access_model.update_metadata"), new_callable=AsyncMock
)
async def test_add_customer_manager(  # pylint: disable=too-many-arguments
    mock_org_access_model_update_metadata: AsyncMock,
    mock_authz_grant_organization_level_role: AsyncMock,
    mock_get_group_names: AsyncMock,
    mock_group_access_domain_add_access: AsyncMock,
    organization_id: str,
    email: str,
    role: str,
) -> None:
    mock_org_access_model_update_metadata.return_value = get_mock_response(
        get_mocked_path("org_access_model.update_metadata"),
        json.dumps([organization_id, email]),
    )
    mock_authz_grant_organization_level_role.return_value = get_mock_response(
        get_mocked_path("authz.grant_organization_level_role"),
        json.dumps([email, organization_id, role]),
    )
    mock_get_group_names.return_value = get_mock_response(
        get_mocked_path("get_group_names"),
        json.dumps([organization_id]),
    )
    mock_group_access_domain_add_access.return_value = get_mock_response(
        get_mocked_path("group_access_domain.add_access"),
        json.dumps([email, organization_id, role]),
    )
    loaders: Dataloaders = get_new_context()

    await add_stakeholder(
        loaders=loaders,
        organization_id=organization_id,
        email=email,
        role=role,
    )
    assert mock_org_access_model_update_metadata.called is True
    assert mock_authz_grant_organization_level_role.called is True
    assert mock_get_group_names.called is True
    assert mock_group_access_domain_add_access.called is True


async def test_add_group_access() -> None:
    loaders: Dataloaders = get_new_context()
    group_name = "kurome"
    group_users = await group_access_domain.get_group_stakeholders_emails(
        loaders, group_name
    )
    assert len(group_users) == 0

    org_id = "ORG#f2e2777d-a168-4bea-93cd-d79142b294d2"  # NOSONAR
    org_group_names = await get_group_names(loaders, org_id)
    assert group_name in org_group_names
    await add_group_access(loaders, org_id, group_name)

    loaders = get_new_context()
    group_users = await group_access_domain.get_group_stakeholders_emails(
        loaders, group_name
    )
    assert len(group_users) == 1
    assert (
        await authz.get_organization_level_role(
            loaders, group_users[0], org_id
        )
        == "customer_manager"
    )


@pytest.mark.parametrize(
    ["organization_name", "email", "country"],
    [
        [
            "esdeath",
            "org_testusermanager1@gmail.com",
            "Colombia",
        ],
    ],
)
@patch(get_mocked_path("add_stakeholder"), new_callable=AsyncMock)
@patch(get_mocked_path("orgs_model.add"), new_callable=AsyncMock)
@patch(get_mocked_path("loaders.stakeholder.load"), new_callable=AsyncMock)
@patch(get_mocked_path("loaders.trial.load"), new_callable=AsyncMock)
@patch(get_mocked_path("exists"), new_callable=AsyncMock)
async def test_add_organization(  # pylint: disable=too-many-arguments
    mock_exist: AsyncMock,
    mock_loaders_trial: AsyncMock,
    mock_loaders_stakeholder: AsyncMock,
    mock_orgs_model_add: AsyncMock,
    mock_add_stakeholder: AsyncMock,
    organization_name: str,
    email: str,
    country: str,
) -> None:

    loaders: Dataloaders = get_new_context()
    mock_exist.return_value = get_mock_response(
        get_mocked_path("exists"),
        json.dumps([organization_name]),
    )
    mock_loaders_stakeholder.return_value = get_mock_response(
        get_mocked_path("loaders.stakeholder.load"),
        json.dumps([email]),
    )
    mock_loaders_trial.return_value = get_mock_response(
        get_mocked_path("loaders.trial.load"),
        json.dumps([email]),
    )
    mock_orgs_model_add.return_value = get_mock_response(
        get_mocked_path("orgs_model.add"),
        json.dumps([email, country, organization_name]),
    )
    mock_orgs_model_add.return_value = get_mock_response(
        get_mocked_path("orgs_model.add"),
        json.dumps([email, country, organization_name]),
    )
    mock_add_stakeholder.return_value = get_mock_response(
        get_mocked_path("add_stakeholder"),
        json.dumps([organization_name, email]),
    )
    result = await add_organization(
        loaders=loaders,
        organization_name=organization_name,
        email=email,
        country=country,
    )

    assert result
    assert result.created_by == email
    assert result.name == organization_name
    assert result.country == country

    assert mock_exist.called is True
    assert mock_loaders_stakeholder.called is True
    assert mock_loaders_trial.called is True
    assert mock_orgs_model_add.called is True
    assert mock_orgs_model_add.called is True
    assert mock_add_stakeholder.called is True

    with pytest.raises(InvalidOrganization) as repeated:
        repeated_name: str = organization_name + "_r"
        mock_exist.return_value = get_mock_response(
            get_mocked_path("exists"),
            json.dumps([repeated_name]),
        )
        await add_organization(
            loaders=loaders,
            organization_name=repeated_name,
            email=email,
            country=country,
        )
    assert str(repeated.value) == "Name taken"
    with pytest.raises(InvalidOrganization) as invalid:
        invalid_name: str = "#@^" + organization_name
        mock_exist.return_value = get_mock_response(
            get_mocked_path("exists"),
            json.dumps([invalid_name]),
        )
        await add_organization(
            loaders=loaders,
            organization_name=invalid_name,
            email=email,
            country=country,
        )
    assert str(invalid.value) == "Invalid name"


async def test_get_group_names() -> None:
    loaders: Dataloaders = get_new_context()
    org_id = "ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3"  # NOSONAR
    groups = await get_group_names(loaders, org_id)
    assert len(groups) == 3
    assert sorted(groups) == [
        "continuoustesting",
        "oneshottest",
        "unittesting",
    ]


async def test_get_stakeholders() -> None:
    loaders: Dataloaders = get_new_context()
    org_id = "ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3"
    org_stakeholders = await get_stakeholders(loaders, org_id)
    org_stakeholders_emails = sorted(
        [stakeholder.email for stakeholder in org_stakeholders]
    )

    expected_emails = [
        "continuoushack2@gmail.com",
        "continuoushacking@gmail.com",
        "customer_manager@fluidattacks.com",
        "forces.unittesting@fluidattacks.com",
        "integrateshacker@fluidattacks.com",
        "integratesmanager@fluidattacks.com",
        "integratesmanager@gmail.com",
        "integratesreattacker@fluidattacks.com",
        "integratesresourcer@fluidattacks.com",
        "integratesreviewer@fluidattacks.com",
        "integratesserviceforces@fluidattacks.com",
        "integratesuser2@fluidattacks.com",
        "integratesuser2@gmail.com",
        "integratesuser@gmail.com",
        "unittest2@fluidattacks.com",
        "vulnmanager@gmail.com",
    ]
    assert len(org_stakeholders_emails) == 17
    for email in expected_emails:
        assert email in org_stakeholders_emails

    second_stakeholders_emails = sorted(
        await get_stakeholders_emails(loaders, org_id)
    )
    assert len(second_stakeholders_emails) == 17
    for email in expected_emails:
        assert email in second_stakeholders_emails


async def test_has_group() -> None:
    loaders: Dataloaders = get_new_context()
    org_id = "ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3"
    existing_group = "unittesting"
    non_existent_group = "madeupgroup"
    assert await has_group(loaders, org_id, existing_group)
    assert not await has_group(loaders, org_id, non_existent_group)


async def test_has_user_access() -> None:
    loaders: Dataloaders = get_new_context()
    org_id = "ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3"
    existing_user = "integratesmanager@gmail.com"
    non_existent_user = "madeupuser@gmail.com"
    assert await orgs_access.has_access(loaders, org_id, existing_user)
    assert not await orgs_access.has_access(loaders, org_id, non_existent_user)


@pytest.mark.parametrize(
    ["organization_id", "email", "modified_by"],
    [
        [
            "ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3",
            "jdoe@fluidattacks.com",
            "org_testadmin@gmail.com",
        ]
    ],
)
@patch(MODULE_AT_TEST + "stakeholders_domain.remove", new_callable=AsyncMock)
@patch(
    MODULE_AT_TEST + "Dataloaders.stakeholder_organizations_access",
    new_callable=AsyncMock,
)
@patch(MODULE_AT_TEST + "org_access_model.remove", new_callable=AsyncMock)
@patch(MODULE_AT_TEST + "remove_credentials", new_callable=AsyncMock)
@patch(MODULE_AT_TEST + "Dataloaders.user_credentials", new_callable=AsyncMock)
@patch(
    MODULE_AT_TEST + "group_access_domain.remove_access",
    new_callable=AsyncMock,
)
@patch(MODULE_AT_TEST + "get_group_names", new_callable=AsyncMock)
@patch(MODULE_AT_TEST + "orgs_access.has_access", new_callable=AsyncMock)
async def test_remove_access(  # pylint: disable=too-many-arguments
    mock_orgs_access_has_access: AsyncMock,
    mock_get_group_names: AsyncMock,
    mock_group_access_domain_remove_access: AsyncMock,
    mock_dataloaders_user_credentials: AsyncMock,
    mock_remove_credentials: AsyncMock,
    mock_org_access_model_remove: AsyncMock,
    mock_dataloaders_stakeholder_organizations_access: AsyncMock,
    mock_stakeholders_domain_remove: AsyncMock,
    organization_id: str,
    email: str,
    modified_by: str,
) -> None:
    mocked_objects, mocked_paths, mocks_args = [
        [
            mock_orgs_access_has_access,
            mock_get_group_names,
            mock_dataloaders_user_credentials.load,
            mock_org_access_model_remove,
            mock_dataloaders_stakeholder_organizations_access.load,
            mock_stakeholders_domain_remove,
        ],
        [
            "orgs_access.has_access",
            "get_group_names",
            "Dataloaders.user_credentials",
            "org_access_model.remove",
            "Dataloaders.stakeholder_organizations_access",
            "stakeholders_domain.remove",
        ],
        [
            [organization_id, email],
            [organization_id],
            [email],
            [email, organization_id],
            [email],
            [email],
        ],
    ]
    assert set_mocks_return_values(
        mocks_args=mocks_args,
        mocked_objects=mocked_objects,
        module_at_test=MODULE_AT_TEST,
        paths_list=mocked_paths,
    )
    assert set_mocks_side_effects(
        mocks_args=[
            [organization_id, email],
            [organization_id, email, modified_by],
        ],
        mocked_objects=[
            mock_group_access_domain_remove_access,
            mock_remove_credentials,
        ],
        module_at_test=MODULE_AT_TEST,
        paths_list=["group_access_domain.remove_access", "remove_credentials"],
    )
    await remove_access(organization_id, email, modified_by)
    assert all(mock_object.called is True for mock_object in mocked_objects)

    with pytest.raises(StakeholderNotInOrganization):
        assert set_mocks_return_values(
            mocks_args=[[organization_id, "made_up_user@gmail.com"]],
            mocked_objects=[mock_orgs_access_has_access],
            module_at_test=MODULE_AT_TEST,
            paths_list=["orgs_access.has_access"],
        )
        await remove_access(
            organization_id, "made_up_user@gmail.com", modified_by
        )


@pytest.mark.parametrize(
    [
        "organization_id",
        "organization_name",
        "email",
    ],
    [
        [
            "ORG#fe80d2d4-ccb7-46d1-8489-67c6360581de",
            "tatsumi",
            "org_testuser1@gmail.com",
        ],
    ],
)
@patch(get_mocked_path("orgs_model.remove"), new_callable=AsyncMock)
@patch(
    get_mocked_path("portfolios_model.remove_organization_portfolios"),
    new_callable=AsyncMock,
)
@patch(
    get_mocked_path("policies_model.remove_org_finding_policies"),
    new_callable=AsyncMock,
)
@patch(
    get_mocked_path("credentials_model.remove_organization_credentials"),
    new_callable=AsyncMock,
)
@patch(get_mocked_path("orgs_model.update_state"), new_callable=AsyncMock)
@patch(get_mocked_path("remove_access"), new_callable=AsyncMock)
@patch(get_mocked_path("get_stakeholders_emails"), new_callable=AsyncMock)
async def test_remove_organization(  # pylint: disable=too-many-arguments
    mock_get_stakeholders_emails: AsyncMock,
    mock_remove_access: AsyncMock,
    mock_orgs_model_update_state: AsyncMock,
    mock_credentials_model_remove_organization_credentials: AsyncMock,
    mock_policies_model_remove_org_finding_policies: AsyncMock,
    mock_portfolios_model_remove_organization_portfolios: AsyncMock,
    mock_orgs_model_remove: AsyncMock,
    organization_id: str,
    organization_name: str,
    email: str,
) -> None:

    mocked_objects = [
        mock_get_stakeholders_emails,
        mock_remove_access,
        mock_orgs_model_update_state,
        mock_credentials_model_remove_organization_credentials,
        mock_policies_model_remove_org_finding_policies,
        mock_portfolios_model_remove_organization_portfolios,
        mock_orgs_model_remove,
    ]
    mocked_paths = [
        "get_stakeholders_emails",
        "remove_access",
        "orgs_model.update_state",
        "credentials_model.remove_organization_credentials",
        "policies_model.remove_org_finding_policies",
        "portfolios_model.remove_organization_portfolios",
        "orgs_model.remove",
    ]
    mocks_args = [
        [organization_id],
        [organization_id, email],
        [organization_id, organization_name, email],
        [organization_id],
        [organization_name],
        [organization_name],
        [organization_id, organization_name],
    ]
    assert set_mocks_return_values(
        mocked_objects=mocked_objects,
        paths_list=mocked_paths,
        mocks_args=mocks_args,
    )
    loaders: Dataloaders = get_new_context()
    await remove_organization(
        loaders=loaders,
        modified_by=email,
        organization_id=organization_id,
        organization_name=organization_name,
    )
    assert all(mock_object.called is True for mock_object in mocked_objects)


@pytest.mark.parametrize(
    ("organization_id", "organization_name", "email", "policies_to_update"),
    (
        (
            "ORG#c2ee2d15-04ab-4f39-9795-fbe30cdeee86",
            "bulat",
            "org_testuser1@gmail.com",
            PoliciesToUpdate(
                inactivity_period=MIN_INACTIVITY_PERIOD,
                max_acceptance_days=20,
                max_acceptance_severity=Decimal("8.3"),
                max_number_acceptances=3,
                min_acceptance_severity=Decimal("2.2"),
                min_breaking_severity=Decimal("3.4"),
                vulnerability_grace_period=17,
            ),
        ),
    ),
)
@patch(get_mocked_path("orgs_model.update_policies"), new_callable=AsyncMock)
@patch(
    get_mocked_path("validate_acceptance_severity_range"),
    new_callable=AsyncMock,
)
async def test_update_policies(  # pylint: disable=too-many-arguments
    mock_validate_acceptance_severity_range: AsyncMock,
    mock_orgs_model_update_policies: AsyncMock,
    organization_id: str,
    organization_name: str,
    email: str,
    policies_to_update: PoliciesToUpdate,
) -> None:
    loaders: Dataloaders = get_new_context()
    mock_validate_acceptance_severity_range.return_value = get_mock_response(
        get_mocked_path("validate_acceptance_severity_range"),
        json.dumps([organization_id, policies_to_update], default=str),
    )
    mock_orgs_model_update_policies.return_value = get_mock_response(
        get_mocked_path("orgs_model.update_policies"),
        json.dumps(
            [email, organization_id, organization_name, policies_to_update],
            default=str,
        ),
    )
    await update_policies(
        loaders, organization_id, organization_name, email, policies_to_update
    )

    assert mock_validate_acceptance_severity_range.called is True
    assert mock_orgs_model_update_policies.called is True


@pytest.mark.parametrize(
    [
        "organization_id",
        "max_acceptance_severity_good",
        "max_acceptance_severity_bad",
    ],
    [
        [
            "ORG#c2ee2d15-04ab-4f39-9795-fbe30cdeee86",
            Decimal("10.4"),
            Decimal("3.1"),
        ],
    ],
)
@patch(MODULE_AT_TEST + "get_organization", new_callable=AsyncMock)
async def test_validate_acceptance_severity_range(
    mock_get_organization: AsyncMock,
    organization_id: str,
    max_acceptance_severity_good: Decimal,
    max_acceptance_severity_bad: Decimal,
) -> None:
    assert set_mocks_return_values(
        mocks_args=[[organization_id]],
        mocked_objects=[mock_get_organization],
        module_at_test=MODULE_AT_TEST,
        paths_list=["get_organization"],
    )
    loaders: Dataloaders = get_new_context()
    result = await validate_acceptance_severity_range(
        loaders=loaders,
        organization_id=organization_id,
        values=PoliciesToUpdate(
            max_acceptance_severity=max_acceptance_severity_good
        ),
    )
    assert result
    mock_get_organization.assert_called_with(loaders, organization_id)

    with pytest.raises(InvalidAcceptanceSeverityRange):
        await validate_acceptance_severity_range(
            loaders=loaders,
            organization_id=organization_id,
            values=PoliciesToUpdate(
                max_acceptance_severity=max_acceptance_severity_bad
            ),
        )
    mock_get_organization.assert_called_with(loaders, organization_id)


@pytest.mark.parametrize(
    ["inactivity_period"],
    [[20]],
)
def test_validate_inactivity_period(
    inactivity_period: int,
) -> None:

    with pytest.raises(InvalidInactivityPeriod):
        validate_inactivity_period(inactivity_period)


@pytest.mark.parametrize(
    ["max_acceptance_days"],
    [[-10]],
)
def test_validate_max_acceptance_days(
    max_acceptance_days: int,
) -> None:

    with pytest.raises(InvalidAcceptanceDays):
        validate_max_acceptance_days(max_acceptance_days)


@pytest.mark.parametrize(
    ["value_good", "value_bad"],
    [[Decimal("10.0"), Decimal("-10.0")], [Decimal("5.3"), Decimal("10.1")]],
)
def test_validate_max_acceptance_severity(
    value_good: Decimal,
    value_bad: Decimal,
) -> None:
    assert validate_max_acceptance_severity(value=value_good)
    with pytest.raises(InvalidAcceptanceSeverity):
        validate_max_acceptance_severity(value=value_bad)


@pytest.mark.parametrize(
    ["value_good", "value_bad"],
    [[10, -10]],
)
def test_validate_max_number_acceptances(
    value_good: int,
    value_bad: int,
) -> None:
    assert validate_max_number_acceptances(value=value_good)
    with pytest.raises(InvalidNumberAcceptances):
        validate_max_number_acceptances(value=value_bad)
