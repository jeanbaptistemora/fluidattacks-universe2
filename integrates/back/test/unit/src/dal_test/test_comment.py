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

comments_db = {
    "item_1": {
        "finding_id": "463558592",
        "parent": "0",
        "comment_type": "verification",
        "created": "2020-01-19 10:41:04",
        "modified": "2020-01-19 10:41:04",
        "fullname": "user Integrates",
        "comment_id": "1558048727999",
        "content": "This is a commenting test of a request verification.",
        "email": "integratesuser@gmail.com",
    },
    "item_2": {
        "finding_id": "500592001",
        "parent": "1558036062503",
        "comment_type": "comment",
        "created": "2019-05-16 18:18:47",
        "modified": "2019-05-16 18:18:47",
        "fullname": "unit test",
        "comment_id": "1558048727932",
        "content": "This is a commenting test.",
        "email": "unittest@fluidattacks.com",
    },
}


@pytest.mark.changes_db
async def test_delete() -> None:
    def side_effect(table_name: str, delete_attrs: dict) -> bool:
        for item in comments_db.values():
            if table_name and bool(
                delete_attrs[0]["finding_id"] == item["finding_id"]
                and delete_attrs[0]["comment_id"] == item["comment_id"]
            ):
                return True
        return False

    finding_id_1 = "500592001"
    comment_id_1 = "1558048727932"
    finding_id_2 = "500592001"
    comment_id_2 = "1558048727931"
    with mock.patch("comments.dal.dynamodb_ops.delete_item") as mock_delete:
        mock_delete.side_effect = side_effect
        assert await delete(comment_id_1, finding_id_1)
        assert not await delete(comment_id_2, finding_id_2)
