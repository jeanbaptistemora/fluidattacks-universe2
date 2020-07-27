import pytest

from django.test import TestCase
from backend.dal.forces import (
    create_execution
)

pytestmark = pytest.mark.asyncio


@pytest.mark.changes_db
async def test_create_execution():
    group = "unittesting"
    execution_id = "random_id"
    assert create_execution(project_name=group, execution_id=execution_id)
