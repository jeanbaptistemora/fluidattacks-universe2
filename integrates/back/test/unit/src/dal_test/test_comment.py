from comments.dal import (
    delete,
)
import pytest
from unittest import (
    mock,
)

pytestmark = [
    pytest.mark.asyncio,
]


@pytest.mark.changes_db
async def test_delete() -> None:
    def side_effect(table_name: str, delete_attrs: dict) -> bool:
        return bool(table_name and delete_attrs)

    finding_id = "500592001"
    comment_id = "1558048727932"
    with mock.patch("comments.dal.dynamodb_ops.delete_item") as mock_delete:
        mock_delete.side_effect = side_effect
        assert await delete(comment_id, finding_id)
