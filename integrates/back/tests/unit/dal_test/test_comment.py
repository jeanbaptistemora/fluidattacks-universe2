import pytest

from backend.dal.comment import (
    delete, get_comments
)

pytestmark = [
    pytest.mark.asyncio,
]


@pytest.mark.changes_db
async def test_delete():
    finding_id = 500592001
    comment_id = 1558048727932
    comments = await get_comments('comment', finding_id)

    assert len(comments) >= 1
    assert await delete(finding_id, comment_id)
    assert len(await get_comments('comment', finding_id)) == 0
