from . import (
    get_result,
)
from custom_exceptions import (
    InvalidCommentParent,
)
import pytest


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_finding_consult")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
        ["hacker@gmail.com"],
        ["reattacker@gmail.com"],
        ["user@gmail.com"],
        ["user_manager@gmail.com"],
        ["vulnerability_manager@gmail.com"],
        ["customer_manager@fluidattacks.com"],
    ],
)
async def test_add_finding_consultant(populate: bool, email: str) -> None:
    assert populate
    result: dict = await get_result(
        user=email,
        content="This is a comment test",
        finding="3c475384-834c-47b0-ac71-a41a022e401c",
        comment_type="CONSULT",
        parent_comment="0",
    )
    assert "errors" not in result
    assert "success" in result["data"]["addFindingConsult"]
    assert result["data"]["addFindingConsult"]["success"]


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_finding_consult")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
    ],
)
async def test_add_finding_consultant_reply(
    populate: bool, email: str
) -> None:
    assert populate
    result: dict = await get_result(
        user=email,
        content="This is a reply to a comment test",
        finding="3c475384-834c-47b0-ac71-a41a022e401c",
        comment_type="CONSULT",
        parent_comment="1558048727111",
    )
    assert "errors" not in result
    assert "success" in result["data"]["addFindingConsult"]
    assert result["data"]["addFindingConsult"]["success"]

    result = await get_result(
        user=email,
        content="This is a reply to a verification comment test",
        finding="3c475384-834c-47b0-ac71-a41a022e401c",
        comment_type="CONSULT",
        parent_comment="1673975237896",
    )
    assert "errors" not in result
    assert "success" in result["data"]["addFindingConsult"]
    assert result["data"]["addFindingConsult"]["success"]

    result = await get_result(
        user=email,
        content="This is invalid reply to a comment test",
        finding="3c475384-834c-47b0-ac71-a41a022e401c",
        comment_type="CONSULT",
        parent_comment="1558048727112",
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == str(InvalidCommentParent())


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_finding_consult")
@pytest.mark.parametrize(
    ["email"],
    [
        ["resourcer@gmail.com"],
    ],
)
async def test_add_finding_consultant_fail(populate: bool, email: str) -> None:
    assert populate
    result: dict = await get_result(
        user=email,
        content="This is a observation test",
        finding="3c475384-834c-47b0-ac71-a41a022e401c",
        comment_type="CONSULT",
        parent_comment="0",
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_finding_consult")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
        ["hacker@gmail.com"],
        ["reattacker@gmail.com"],
        ["user@gmail.com"],
        ["user_manager@gmail.com"],
        ["vulnerability_manager@gmail.com"],
        ["executive@gmail.com"],
    ],
)
async def test_add_finding_consult_without_squad(
    populate: bool, email: str
) -> None:
    assert populate
    result: dict = await get_result(
        user=email,
        content="This is a consulting test",
        finding="697510163",
        comment_type="CONSULT",
        parent_comment="0",
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == "Access denied"


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_finding_consult")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
        ["hacker@gmail.com"],
        ["reviewer@gmail.com"],
    ],
)
async def test_add_finding_observation_without_squad(
    populate: bool, email: str
) -> None:
    assert populate
    result: dict = await get_result(
        user=email,
        content="This is a observation test",
        finding="697510163",
        comment_type="OBSERVATION",
        parent_comment="0",
    )
    assert "errors" not in result
    assert "success" in result["data"]["addFindingConsult"]
    assert result["data"]["addFindingConsult"]["success"]


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("add_finding_consult")
@pytest.mark.parametrize(
    ["email"],
    [
        ["admin@gmail.com"],
    ],
)
async def test_add_finding_observation_reply(
    populate: bool, email: str
) -> None:
    assert populate
    result: dict = await get_result(
        user=email,
        content="This is a reply to a observation test",
        finding="3c475384-834c-47b0-ac71-a41a022e401c",
        comment_type="OBSERVATION",
        parent_comment="1558048727000",
    )
    assert "errors" not in result
    assert "success" in result["data"]["addFindingConsult"]
    assert result["data"]["addFindingConsult"]["success"]

    result = await get_result(
        user=email,
        content="This is invalid reply to a observation test",
        finding="3c475384-834c-47b0-ac71-a41a022e401c",
        comment_type="OBSERVATION",
        parent_comment="1673975237896",
    )
    assert "errors" in result
    assert result["errors"][0]["message"] == str(InvalidCommentParent())
