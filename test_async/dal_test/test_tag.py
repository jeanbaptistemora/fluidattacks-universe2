import pytest

from django.test import TestCase
from decimal import Decimal
from backend.dal.tag import (
    update, get_attributes
)


class TagTest(TestCase):

    @pytest.mark.changes_db
    def test_update(self):
        # company, tag, data
        test_1 = ('imamura', 'test-updates', {
            'mean_remediate_critical_severity' : None,
            'mean_remediate' : None,
            'max_severity' : Decimal('3.3')
        })
        original = {
            'mean_remediate_critical_severity' : Decimal('0'),
            'mean_remediate' : Decimal('132'),
            'max_severity' : Decimal('6.0')
        }
        attributes = [attr for attr in original]
        assert original == get_attributes(test_1[0], test_1[1], attributes)
        assert update(*test_1)
        assert {'max_severity' : Decimal('3.3')} == \
            get_attributes(test_1[0], test_1[1], attributes)
