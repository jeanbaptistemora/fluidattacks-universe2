import pytest

from django.test import TestCase
from backend.dal.forces import (
    create_execution
)
from backend.utils import (
    datetime as datetime_utils,
)

pytestmark = pytest.mark.asyncio


@pytest.mark.changes_db
async def test_create_execution():
    group = "unittesting"
    execution_id = "random_id"
    now = datetime_utils.get_now()
    assert await create_execution (
        project_name=group,
        execution_id=execution_id,
        date=now
    )
