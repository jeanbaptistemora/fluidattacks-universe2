from dataloaders import (
    get_new_context,
)
import pytest
from vulnerabilities.domain import (
    get_managers_by_size,
    send_treatment_report_mail,
)

pytestmark = [
    pytest.mark.asyncio,
]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    [
        "modified_by",
        "justification",
        "vulnerability_id",
        "is_approved",
    ],
    [
        [
            "vulnmanager@gmail.com",
            "test",
            "15375781-31f2-4953-ac77-f31134225747",
            False,
        ],
        [
            "vulnmanager@gmail.com",
            "test",
            "15375781-31f2-4953-ac77-f31134225747",
            True,
        ],
    ],
)
async def test_send_treatment_report_mail(
    modified_by: str,
    justification: str,
    vulnerability_id: str,
    is_approved: bool,
) -> None:
    await send_treatment_report_mail(
        loaders=get_new_context(),
        modified_by=modified_by,
        justification=justification,
        vulnerability_id=vulnerability_id,
        is_approved=is_approved,
    )


@pytest.mark.asyncio
async def test_get_managers_by_size() -> None:
    group_name = "unittesting"
    email_managers = await get_managers_by_size(
        get_new_context(), group_name, 3
    )
    expected_len = 3
    assert expected_len == len(email_managers)
    email_managers = await get_managers_by_size(
        get_new_context(), group_name, 2
    )
    expected_len = 2
    assert expected_len == len(email_managers)
