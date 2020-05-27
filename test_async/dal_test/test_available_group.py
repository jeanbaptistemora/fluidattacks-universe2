from django.test import TestCase
import pytest

import backend.dal.available_group as available_group_dal

@pytest.mark.changes_db
def test_remove():
    is_deleted = available_group_dal.remove('manila')
    assert is_deleted


def test_get_one():
    group_available = available_group_dal.get_one()
    assert isinstance(group_available, str)


def test_get_all():
    all_groups = available_group_dal.get_all()
    assert isinstance(all_groups, list)
    assert len(all_groups) == 5


def test_exists():
    existing_group = available_group_dal.exists('praga')
    assert existing_group
    non_existent_group = available_group_dal.exists('rio')
    assert not non_existent_group
