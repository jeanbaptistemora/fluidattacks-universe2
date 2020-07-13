import pytest
from django.test import TestCase

from backend.dal.project import (
    list_internal_managers, list_project_managers, update_access, get_users
)

def test_list_internal_managers():
    assert list_internal_managers('oneshottest') == []

    assert list_internal_managers('unittesting') == \
        ['unittest2@fluidattacks.com']

def test_update_access():
    assert 'unittest2@fluidattacks.com' in \
        get_users('unittesting', False)
    assert update_access('unittest2@fluidattacks.com', 'unittesting',
                        'has_access', True)
    assert 'unittest2@fluidattacks.com' in \
        get_users('unittesting', True)
    assert update_access('unittest2@fluidattacks.com', 'unittesting',
                        'has_access', False)
    assert 'unittest2@fluidattacks.com' in \
        get_users('unittesting', False)
