from custom_exceptions import (
    InvalidAcceptanceSeverity,
    InvalidAcceptanceSeverityRange,
    InvalidSeverity,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.types import (
    PoliciesToUpdate,
)
from decimal import (
    Decimal,
)
from organizations import (
    domain as orgs_domain,
)
from organizations.domain import (
    iterate_organizations_and_groups,
)
import pytest
from typing import (
    Any,
)

# Run async tests
pytestmark = [
    pytest.mark.asyncio,
]


async def test_get_id_for_group() -> None:
    group_name = "unittesting"
    expected_org_id = "ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3"
    loaders: Dataloaders = get_new_context()
    group = await loaders.group.load(group_name)
    assert group
    org_id = group.organization_id
    assert org_id == expected_org_id

    assert not await loaders.group.load("madeup-group")


async def test_get_stakeholder_organizations() -> None:
    loaders: Dataloaders = get_new_context()
    stakeholder_email = "integratesmanager@gmail.com"
    expected_orgs = [
        "ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3",
        "ORG#956e9107-fd8d-49bc-b550-5609a7a1f6ac",  # NOSONAR
        "ORG#c2ee2d15-04ab-4f39-9795-fbe30cdeee86",
        "ORG#c6cecc0e-bb92-4079-8b6d-c4e815c10bb1",  # NOSONAR
    ]
    stakeholder_orgs_access = (
        await loaders.stakeholder_organizations_access.load(stakeholder_email)
    )
    stakeholder_orgs_ids = [
        org.organization_id for org in stakeholder_orgs_access
    ]
    assert sorted(stakeholder_orgs_ids) == expected_orgs

    assert (
        await loaders.stakeholder_organizations_access.load(
            "madeupstakeholder@gmail.com"
        )
        == []  # NOSONAR
    )


async def test_update_policies() -> None:
    org_id = "ORG#c2ee2d15-04ab-4f39-9795-fbe30cdeee86"
    org_name = "bulat"

    new_values = PoliciesToUpdate(
        min_acceptance_severity=Decimal("-1.5"),
    )
    with pytest.raises(InvalidAcceptanceSeverity):
        await orgs_domain.update_policies(
            get_new_context(), org_id, org_name, "", new_values
        )

    new_values = PoliciesToUpdate(
        max_acceptance_severity=Decimal("5.0"),
        min_acceptance_severity=Decimal("7.4"),
    )
    with pytest.raises(InvalidAcceptanceSeverityRange):
        await orgs_domain.update_policies(
            get_new_context(), org_id, org_name, "", new_values
        )

    new_values = PoliciesToUpdate(
        min_breaking_severity=Decimal("10.5"),
    )
    with pytest.raises(InvalidSeverity):
        await orgs_domain.update_policies(
            get_new_context(), org_id, org_name, "", new_values
        )


async def test_validate_negative_values() -> None:

    with pytest.raises(InvalidSeverity):
        orgs_domain.validate_min_breaking_severity(-1)  # type: ignore


async def test_iterate_organizations() -> None:
    expected_organizations = {
        "ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3": "okada",
        "ORG#c2ee2d15-04ab-4f39-9795-fbe30cdeee86": "bulat",
        "ORG#f2e2777d-a168-4bea-93cd-d79142b294d2": "hajime",
        "ORG#fe80d2d4-ccb7-46d1-8489-67c6360581de": "tatsumi",
        "ORG#ffddc7a3-7f05-4fc7-b65d-7defffa883c2": "himura",
        "ORG#c6cecc0e-bb92-4079-8b6d-c4e815c10bb1": "makimachi",
        "ORG#956e9107-fd8d-49bc-b550-5609a7a1f6ac": "kamiya",
        "ORG#33c08ebd-2068-47e7-9673-e1aa03dc9448": "kiba",
        "ORG#7376c5fe-4634-4053-9718-e14ecbda1e6b": "imamura",
        "ORG#d32674a9-9838-4337-b222-68c88bf54647": "makoto",
        "ORG#ed6f051c-2572-420f-bc11-476c4e71b4ee": "ikari",
    }
    async for organization in orgs_domain.iterate_organizations():
        assert expected_organizations.pop(organization.id) == organization.name
    assert not expected_organizations


async def test_iterate_organizations_and_groups() -> None:
    loaders: Dataloaders = get_new_context()
    expected_organizations_and_groups: dict[str, Any] = {
        "ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3": {
            "okada": ["oneshottest", "continuoustesting", "unittesting"]
        },
        "ORG#c2ee2d15-04ab-4f39-9795-fbe30cdeee86": {"bulat": []},
        "ORG#f2e2777d-a168-4bea-93cd-d79142b294d2": {
            "hajime": ["kurome", "sheele"]
        },
        "ORG#fe80d2d4-ccb7-46d1-8489-67c6360581de": {"tatsumi": ["lubbock"]},
        "ORG#ffddc7a3-7f05-4fc7-b65d-7defffa883c2": {"himura": []},
        "ORG#c6cecc0e-bb92-4079-8b6d-c4e815c10bb1": {
            "makimachi": [
                "metropolis",
                "deletegroup",
                "gotham",
                "asgard",
                "setpendingdeletion",
            ]
        },
        "ORG#956e9107-fd8d-49bc-b550-5609a7a1f6ac": {
            "kamiya": ["barranquilla", "monteria"]
        },
        "ORG#33c08ebd-2068-47e7-9673-e1aa03dc9448": {"kiba": []},
        "ORG#7376c5fe-4634-4053-9718-e14ecbda1e6b": {
            "imamura": ["deleteimamura"]
        },
        "ORG#d32674a9-9838-4337-b222-68c88bf54647": {"makoto": []},
        "ORG#ed6f051c-2572-420f-bc11-476c4e71b4ee": {"ikari": []},
    }
    async for org_id, org_name, groups in iterate_organizations_and_groups(
        loaders
    ):  # noqa
        assert sorted(groups) == sorted(
            expected_organizations_and_groups.pop(org_id)[org_name]
        )
    assert not expected_organizations_and_groups


async def test_get_all_active_group() -> None:
    loaders: Dataloaders = get_new_context()
    test_data = await orgs_domain.get_all_active_group_names(loaders)
    expected_output = [
        "asgard",
        "barranquilla",
        "continuoustesting",
        "deletegroup",
        "deleteimamura",
        "gotham",
        "lubbock",
        "kurome",
        "metropolis",
        "monteria",
        "oneshottest",
        "setpendingdeletion",
        "sheele",
        "unittesting",
    ]
    assert sorted(list(test_data)) == sorted(expected_output)
