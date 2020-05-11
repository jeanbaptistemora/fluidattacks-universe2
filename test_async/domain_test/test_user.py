from datetime import datetime, timedelta
import pytz
import pytest

from django.conf import settings
from django.test import TestCase
from backend.domain.user import (
    get_all_users_report,
    get_group_level_role,
    get_user_level_role,
    grant_user_level_role,
    grant_group_level_role,
    revoke_group_level_role,
    get_current_date,
)

class UserTests(TestCase):

    @pytest.mark.no_changes_db
    def test_get_all_users_report(self):
        finish_date = \
            (datetime.today() - timedelta(days=1)).date().strftime('%Y-%m-%d')
        users = get_all_users_report('FLUID', finish_date)
        assert users >= 1

    @pytest.mark.no_changes_db
    def test_get_group_level_role(self):
        assert get_group_level_role('continuoushacking@gmail.com', 'unittesting') == 'customeradmin'
        assert get_group_level_role('integratesanalyst@gmail.com', 'unittesting') == 'analyst'
        assert get_group_level_role('integratesuser@gmail.com', 'unittesting') == 'customeradmin'
        assert get_group_level_role('unittest@fluidattacks.com', 'any-group') == 'admin'
        assert not get_group_level_role('asdfasdfasdfasdf@gmail.com', 'unittesting')

    @pytest.mark.no_changes_db
    def test_get_user_level_role(self):
        assert get_user_level_role('continuoushacking@gmail.com') == 'customeradmin'
        assert get_user_level_role('integratesanalyst@gmail.com') == 'analyst'
        assert get_user_level_role('integratesuser@gmail.com') == 'customeradmin'
        assert get_user_level_role('unittest@fluidattacks.com') == 'admin'
        assert not get_user_level_role('asdfasdfasdfasdf@gmail.com')

    @pytest.mark.changes_db
    def test_grant_user_level_role(self):
        assert grant_user_level_role('..TEST@gmail.com', 'customer')
        assert get_user_level_role('..test@gmail.com') == 'customer'
        assert get_user_level_role('..tEst@gmail.com') == 'customer'

        assert grant_user_level_role('..TEST@gmail.com', 'admin')
        assert get_user_level_role('..test@gmail.com') == 'admin'
        assert get_group_level_role('..tEst@gmail.com', 'a-group') == 'admin'

    @pytest.mark.changes_db
    def test_grant_group_level_role(self):
        assert grant_group_level_role('..TEST2@gmail.com', 'group', 'customer')
        assert get_user_level_role('..test2@gmail.com') == 'customer'
        assert get_user_level_role('..tESt2@gmail.com') == 'customer'
        assert get_group_level_role('..test2@gmail.com', 'GROUP') == 'customer'
        assert not get_group_level_role('..test2@gmail.com', 'other-group')

    @pytest.mark.changes_db
    def test_revoke_group_level_role(self):
        assert grant_group_level_role('revoke_group_LEVEL_role@gmail.com', 'group', 'customer')
        assert grant_group_level_role('REVOKE_group_level_role@gmail.com', 'other-group', 'customer')

        assert get_group_level_role('revoke_group_level_ROLE@gmail.com', 'group') == 'customer'
        assert get_group_level_role('revoke_GROUP_level_role@gmail.com', 'other-group') == 'customer'
        assert not get_group_level_role('REVOKE_group_level_role@gmail.com', 'yet-other-group')

        assert revoke_group_level_role('revoke_GROUP_level_role@gmail.com', 'other-group')
        assert get_group_level_role('revoke_group_level_role@gmail.com', 'group') == 'customer'
        assert not get_group_level_role('revoke_group_level_role@gmail.com', 'other-group')
        assert not get_group_level_role('revoke_group_level_role@gmail.com', 'yet-other-group')

        assert revoke_group_level_role('revoke_GROUP_level_role@gmail.com', 'group')
        assert not get_group_level_role('revOke_group_level_role@gmail.com', 'group')
        assert not get_group_level_role('revoKe_group_level_role@gmail.com', 'other-group')
        assert not get_group_level_role('revokE_group_level_role@gmail.com', 'yet-other-group')

    @pytest.mark.no_changes_db
    def test_get_current_date(self):
        tzn = pytz.timezone(settings.TIME_ZONE)
        today = datetime.now(tz=tzn).today()
        date = today.strftime('%Y-%m-%d %H:%M')
        test_data = get_current_date()[:-3]
        assert isinstance(test_data, str)
        assert test_data == date
