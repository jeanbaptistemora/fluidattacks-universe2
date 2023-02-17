from dataloaders import (
    get_new_context,
)
from db_model.enums import (
    Notification,
)
from mailer.utils import (
    get_available_notifications,
    get_group_emails_by_notification,
    get_group_rol,
    get_org_groups,
    get_org_rol,
    get_organization_country,
    get_organization_name,
    get_stakeholder_roles,
)
import pytest

pytestmark = [
    pytest.mark.asyncio,
]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    [
        "email",
        "expected",
    ],
    [
        [
            "customer_manager@fluidattacks.com",
            [
                Notification.FILE_UPDATE,
                Notification.GROUP_INFORMATION,
                Notification.PORTFOLIO_UPDATE,
                Notification.ROOT_UPDATE,
                Notification.SERVICE_UPDATE,
                Notification.UNSUBSCRIPTION_ALERT,
                Notification.UPDATED_TREATMENT,
            ],
        ],
    ],
)
async def test_get_available_notifications(
    email: str, expected: list[Notification]
) -> None:
    loaders = get_new_context()
    available_notifications = await get_available_notifications(loaders, email)
    assert available_notifications == expected


@pytest.mark.asyncio
@pytest.mark.parametrize(
    [
        "group_name",
        "notification",
    ],
    [
        [
            "unittesting",
            "updated_group_info",
        ],
    ],
)
async def test_get_group_emails_by_notification(
    group_name: str,
    notification: str,
) -> None:
    loaders = get_new_context()
    group_emails = await get_group_emails_by_notification(
        loaders=loaders, group_name=group_name, notification=notification
    )
    assert len(group_emails) == 5


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ["email", "group_name", "expected"],
    [
        [
            "customer_manager@fluidattacks.com",
            "unittesting",
            "customer_manager",
        ],
    ],
)
async def test_get_group_rol(
    email: str,
    group_name: str,
    expected: str,
) -> None:
    loaders = get_new_context()
    group_rol = await get_group_rol(loaders, email, group_name)
    assert group_rol == expected


@pytest.mark.asyncio
@pytest.mark.parametrize(
    [
        "org_id",
    ],
    [
        [
            "ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3",
        ],
    ],
)
async def test_get_org_groups(
    org_id: str,
) -> None:
    loaders = get_new_context()
    org_groups = await get_org_groups(loaders, org_id)
    assert len(org_groups) == 3


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ["email", "org_id", "expected"],
    [
        [
            "customer_manager@fluidattacks.com",
            "ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3",
            "customer_manager",
        ],
    ],
)
async def test_get_org_rol(
    email: str,
    org_id: str,
    expected: str,
) -> None:
    loaders = get_new_context()
    org_rol = await get_org_rol(loaders, email, org_id)
    assert org_rol == expected


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ["group_name", "expected"],
    [
        [
            "unittesting",
            "Colombia",
        ],
    ],
)
async def test_get_organization_country(
    group_name: str,
    expected: str,
) -> None:
    loaders = get_new_context()
    org_country = await get_organization_country(loaders, group_name)
    assert org_country == expected


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ["group_name", "expected"],
    [
        [
            "unittesting",
            "okada",
        ],
    ],
)
async def test_get_organization_name(
    group_name: str,
    expected: str,
) -> None:
    loaders = get_new_context()
    org_name = await get_organization_name(loaders, group_name)
    assert org_name == expected


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ["email", "expected"],
    [
        [
            "customer_manager@fluidattacks.com",
            dict(group={"customer_manager"}, org={"customer_manager"}),
        ],
    ],
)
async def test_get_stakeholder_roles(
    email: str,
    expected: dict[str, set[str]],
) -> None:
    loaders = get_new_context()
    stakeholder_roles = await get_stakeholder_roles(loaders, email)
    assert stakeholder_roles == expected
