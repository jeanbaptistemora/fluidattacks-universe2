import pytest
from users.dal import (
    create,
    delete,
    get,
    update,
)

pytestmark = [
    pytest.mark.asyncio,
]


@pytest.mark.changes_db
async def test_delete() -> None:
    test_1 = "unittest3"
    assert {
        "company": "unittest",
        "date_joined": "2017-12-28 23:54:55",
        "last_login": "2019-10-29 13:40:37",
        "email": "unittest3",
        "legal_remember": True,
        "organization": "ORG#6ee4c12b-7881-4490-a851-07357fff1d64",
        "registered": False,
    } == await get(test_1)
    assert await delete(test_1)
    assert {} == await get(test_1)


@pytest.mark.changes_db
async def test_update() -> None:
    assert await get("unittest5") == {}

    await create("unittest4", {})
    assert await get("unittest4") == {"email": "unittest4"}

    await update("unittest4", {"last_name": "testing"})
    assert await get("unittest4") == {
        "last_name": "testing",
        "email": "unittest4",
    }
