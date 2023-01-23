import authz
from back.test.unit.src.utils import (  # pylint: disable=import-error
    get_mock_response,
    get_mocked_path,
)
from custom_exceptions import (
    InvalidAcceptanceDays,
    InvalidAcceptanceSeverityRange,
    InvalidInactivityPeriod,
    InvalidNumberAcceptances,
    InvalidOrganization,
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
from organizations.domain import (
    add_group_access,
    add_organization,
    add_stakeholder,
    get_group_names,
    get_stakeholders,
    get_stakeholders_emails,
    has_access,
    has_group,
    update_policies,
    validate_acceptance_severity_range,
    validate_inactivity_period,
    validate_max_acceptance_days,
    validate_max_number_acceptances,
)
import pytest
from unittest.mock import (
    AsyncMock,
    patch,
)

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
@patch(get_mocked_path("loaders.company.load"), new_callable=AsyncMock)
@patch(get_mocked_path("exists"), new_callable=AsyncMock)
async def test_add_organization(  # pylint: disable=too-many-arguments
    mock_exist: AsyncMock,
    mock_loaders_company: AsyncMock,
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
    mock_loaders_company.return_value = get_mock_response(
        get_mocked_path("loaders.company.load"),
        json.dumps([organization_name]),
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
    assert mock_loaders_company.called is True
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
        assert str(repeated) == "Exception - Name taken"
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
        assert str(invalid) == "Exception - Invalid name"


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
    assert await has_access(loaders, org_id, existing_user)
    assert not await has_access(loaders, org_id, non_existent_user)


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
@patch(get_mocked_path("loaders.organization.load"), new_callable=AsyncMock)
async def test_validate_acceptance_severity_range(
    mock_loaders_organization: AsyncMock,
    organization_id: str,
    max_acceptance_severity_good: Decimal,
    max_acceptance_severity_bad: Decimal,
) -> None:
    mock_loaders_organization.return_value = get_mock_response(
        get_mocked_path("loaders.organization.load"),
        json.dumps([organization_id]),
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
    assert mock_loaders_organization.called is True

    with pytest.raises(InvalidAcceptanceSeverityRange):
        await validate_acceptance_severity_range(
            loaders=loaders,
            organization_id=organization_id,
            values=PoliciesToUpdate(
                max_acceptance_severity=max_acceptance_severity_bad
            ),
        )
    assert mock_loaders_organization.called is True


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
    [[10, -10]],
)
def test_validate_max_number_acceptances(
    value_good: int,
    value_bad: int,
) -> None:
    assert validate_max_number_acceptances(value=value_good)
    with pytest.raises(InvalidNumberAcceptances):
        validate_max_number_acceptances(value=value_bad)
