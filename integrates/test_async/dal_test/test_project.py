import pytest
from django.test import TestCase

from backend.dal.project import (
    list_internal_managers, list_project_managers, update_access, get_users
)

pytestmark = [pytest.mark.asyncio,]

async def test_list_internal_managers():
    assert await list_internal_managers('oneshottest') == []
    assert await list_internal_managers('unittesting') == \
        ['unittest2@fluidattacks.com']

async def test_update_access():
    assert 'unittest2@fluidattacks.com' in \
        await get_users('unittesting', False)
    assert await update_access('unittest2@fluidattacks.com', 'unittesting',
                        'has_access', True)
    assert 'unittest2@fluidattacks.com' in \
        await get_users('unittesting', True)
    assert await update_access('unittest2@fluidattacks.com', 'unittesting',
                        'has_access', False)
    assert 'unittest2@fluidattacks.com' in \
        await get_users('unittesting', False)
