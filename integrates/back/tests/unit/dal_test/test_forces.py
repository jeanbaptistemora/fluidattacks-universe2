from forces.dal import (
    add_execution,
)
from newutils import (
    datetime as datetime_utils,
)
import pytest

pytestmark = pytest.mark.asyncio


@pytest.mark.changes_db
async def test_create_execution() -> None:
    group = "unittesting"
    execution_id = "random_id"
    now = datetime_utils.get_now()
    assert await add_execution(
        group_name=group,
        execution_id=execution_id,
        date=now,
    )
