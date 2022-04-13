from comments.dal import (
    delete,
    get_comments,
)
import pytest

pytestmark = [
    pytest.mark.asyncio,
]


@pytest.mark.changes_db
async def test_delete() -> None:
    finding_id = "500592001"
    comment_id = "1558048727932"
    comments = await get_comments("comment", finding_id)

    assert len(comments) >= 1
    assert await delete(comment_id, finding_id)
    assert len(await get_comments("comment", finding_id)) == 0
