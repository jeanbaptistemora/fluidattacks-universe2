from forces.dal import (
    add_execution,
)
from newutils import (
    datetime as datetime_utils,
)
import pytest
from unittest import (
    mock,
)

pytestmark = pytest.mark.asyncio


@pytest.mark.changes_db
async def test_create_execution() -> None:
    def side_effect(table_name: str, execution_attributes: dict) -> bool:
        return bool(table_name and ("" not in execution_attributes.values()))

    group = "unittesting"
    execution_id = "random_id"
    now = datetime_utils.get_now()
    with mock.patch("forces.dal.dynamodb_ops.put_item") as mock_put:
        mock_put.side_effect = side_effect
        assert await add_execution(
            group_name=group,
            execution_id=execution_id,
            date=now,
        )
        assert not await add_execution(
            group_name="",
            execution_id=execution_id,
            date=now,
        )
