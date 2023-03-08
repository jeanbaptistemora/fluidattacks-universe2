from . import (
    get_result,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from datetime import (
    datetime,
)
from db_model.groups.enums import (
    GroupLanguage,
)
import pytest
from typing import (
    Any,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_group_info")
@pytest.mark.parametrize(
    ("email", "language"),
    (
        ("admin@gmail.com", "EN"),
        ("user_manager@gmail.com", "ES"),
        ("customer_manager@fluidattacks.com", "ES"),
    ),
)
async def test_update_group_info(
    populate: bool,
    email: str,
    language: str,
) -> None:
    assert populate
    group_name: str = "group1"
    description: str = f"Description test modified by {email}"
    business_id: str = "420938281"
    business_name: str = "Testing Company and Sons"
    sprint_duration: int = 2
    sprint_start_date: str = "2022-05-30T00:00:00+00:00"
    result: dict[str, Any] = await get_result(
        business_id=business_id,
        business_name=business_name,
        sprint_duration=sprint_duration,
        user=email,
        group=group_name,
        description=description,
        language=language,
        sprint_start_date=sprint_start_date,
    )
    assert "errors" not in result
    assert "success" in result["data"]["updateGroupInfo"]
    assert result["data"]["updateGroupInfo"]["success"]

    loaders: Dataloaders = get_new_context()
    group = await loaders.group.load(group_name)
    assert group
    assert group.business_id == business_id
    assert group.business_name == business_name
    assert group.description == description
    assert group.language == GroupLanguage[language]
    assert group.sprint_duration == 2
    assert group.sprint_start_date == datetime.fromisoformat(sprint_start_date)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_group_info")
@pytest.mark.parametrize(
    ["email"],
    [
        ["hacker@gmail.com"],
        ["user@gmail.com"],
        ["reattacker@gmail.com"],
        ["resourcer@gmail.com"],
        ["reviewer@gmail.com"],
        ["vulnerability_manager@gmail.com"],
    ],
)
@pytest.mark.parametrize(
    ("description", "language"),
    (
        ("Description test", "EN"),
        ("Description test", "ES"),
    ),
)
async def test_update_group_info_fail(
    populate: bool,
    description: str,
    email: str,
    language: str,
) -> None:
    assert populate
    group_name: str = "group1"
    business_id: str = "420938282"
    business_name: str = "Testing Company and Failures"
    sprint_duration: int = 1
    result: dict[str, Any] = await get_result(
        business_id=business_id,
        business_name=business_name,
        user=email,
        group=group_name,
        description=description,
        language=language,
        sprint_duration=sprint_duration,
        sprint_start_date="",
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"
