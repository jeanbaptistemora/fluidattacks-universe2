from dataloaders import (
    get_new_context,
)
from db_model.stakeholders.types import (
    Stakeholder,
)
import pytest
from stakeholders.dal import (
    add,
    get,
    remove,
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
    await remove(test_1)
    assert {} == await get(test_1)


@pytest.mark.changes_db
async def test_update() -> None:
    assert await get("unittest5") == {}

    stakeholder = Stakeholder(
        email="unittest4@gmail.com",
        is_registered=True,
    )
    await add(stakeholder)
    loaders = get_new_context()
    load_stakeholder: Stakeholder = await loaders.stakeholder.load(
        "unittest4@gmail.com"
    )
    assert load_stakeholder.email == "unittest4@gmail.com"

    await update("unittest4", {"last_name": "testing"})
    assert await get("unittest4") == {
        "last_name": "testing",
        "email": "unittest4",
    }
