from . import (
    get_result,
)
from custom_exceptions import (
    StakeholderNotFound,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.group_comments.types import (
    GroupComment,
)
from db_model.stakeholders.types import (
    Stakeholder,
)
from group_access.domain import (
    get_stakeholders_subscribed_to_consult,
)
from mailer.groups import (
    send_mail_comment,
)
from newutils import (
    datetime as datetime_utils,
)
import pytest
import time
from typing import (
    Any,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_group_consult")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
        ["user@gmail.com"],
        ["user_manager@gmail.com"],
        ["vulnerability_manager@gmail.com"],
        ["hacker@gmail.com"],
        ["reviewer@gmail.com"],
        ["customer_manager@fluidattacks.com"],
    ],
)
async def test_add_group_consult(populate: bool, email: str) -> None:
    assert populate
    group_name: str = "group1"
    result: dict[str, Any] = await get_result(
        user=email,
        group=group_name,
    )
    assert "errors" not in result
    assert "success" in result["data"]["addGroupConsult"]
    assert result["data"]["addGroupConsult"]["success"]


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_group_consult")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
    ],
)
async def test_add_group_consult_with_suppress(
    populate: bool, email: str
) -> None:
    assert populate
    loaders: Dataloaders = get_new_context()
    group_name: str = "group1"
    comment_id = int(round(time.time() * 1000))
    result: dict[str, Any] = await get_result(
        user=email,
        group=group_name,
    )
    assert "errors" not in result
    assert "success" in result["data"]["addGroupConsult"]
    assert result["data"]["addGroupConsult"]["success"]

    user: Stakeholder = await loaders.stakeholder.load(email)
    comment_data = GroupComment(
        group_name=group_name,
        id=comment_id,  # type: ignore
        content="Test consult",
        creation_date=datetime_utils.get_utc_now(),
        full_name=str.join(" ", [user.first_name or "", user.last_name or ""]),
        parent_id="0",
        email=user.email,
    )

    with pytest.raises(StakeholderNotFound):
        await send_mail_comment(
            loaders=loaders,
            comment_data=comment_data,
            user_mail=email,
            recipients=["nonexistinguser@fluidattacks.com"],
            group_name=group_name,
        )

    await send_mail_comment(
        loaders=loaders,
        comment_data=comment_data,
        user_mail=email,
        recipients=await get_stakeholders_subscribed_to_consult(
            loaders=loaders, group_name=group_name, comment_type="group"
        ),
        group_name=group_name,
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_group_consult")
@pytest.mark.parametrize(
    ["email"],
    [
        ["reattacker@gmail.com"],
        ["resourcer@gmail.com"],
    ],
)
async def test_add_group_consult_fail(populate: bool, email: str) -> None:
    assert populate
    group_name: str = "group1"
    result: dict[str, Any] = await get_result(
        user=email,
        group=group_name,
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_group_consult")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
        ["user@gmail.com"],
        ["user_manager@gmail.com"],
        ["vulnerability_manager@gmail.com"],
        ["hacker@gmail.com"],
        ["reviewer@gmail.com"],
    ],
)
async def test_add_group_consult_without_squad(
    populate: bool, email: str
) -> None:
    assert populate
    group_name: str = "group3"
    result: dict[str, Any] = await get_result(
        user=email,
        group=group_name,
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
