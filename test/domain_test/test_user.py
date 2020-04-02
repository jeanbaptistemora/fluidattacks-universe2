from datetime import datetime, timedelta
import pytest
from django.test import TestCase
from backend.domain.user import (
    get_all_users_report,
    get_group_level_role2,
    get_user_level_role2,
    grant_user_level_role2,
    grant_group_level_role2,
)

class UserTests(TestCase):

    def test_get_all_users_report(self):
        finish_date = \
            (datetime.today() - timedelta(days=1)).date().strftime('%Y-%m-%d')
        users = get_all_users_report('FLUID', finish_date)
        assert users >= 1

    def test_get_group_level_role2(self):
        assert get_group_level_role2('continuoushacking@gmail.com', 'unittesting') == 'customeradmin'
        assert get_group_level_role2('integratesanalyst@gmail.com', 'unittesting') == 'analyst'
        assert get_group_level_role2('integratesuser@gmail.com', 'unittesting') == 'customeradmin'
        assert get_group_level_role2('unittest@fluidattacks.com', 'any-group') == 'admin'
        assert not get_group_level_role2('asdfasdfasdfasdf@gmail.com', 'unittesting')

    def test_get_user_level_role2(self):
        assert get_user_level_role2('continuoushacking@gmail.com') == 'customeradmin'
        assert get_user_level_role2('integratesanalyst@gmail.com') == 'analyst'
        assert get_user_level_role2('integratesuser@gmail.com') == 'customeradmin'
        assert get_user_level_role2('unittest@fluidattacks.com') == 'admin'
        assert not get_user_level_role2('asdfasdfasdfasdf@gmail.com')

    def test_grant_user_level_role2(self):
        assert grant_user_level_role2('..TEST@gmail.com', 'customer')
        assert get_user_level_role2('..test@gmail.com') == 'customer'
        assert get_user_level_role2('..tEst@gmail.com') == 'customer'

        assert grant_user_level_role2('..TEST@gmail.com', 'admin')
        assert get_user_level_role2('..test@gmail.com') == 'admin'
        assert get_group_level_role2('..tEst@gmail.com', 'a-group') == 'admin'

    def test_grant_group_level_role2(self):
        assert grant_group_level_role2('..TEST2@gmail.com', 'group', 'customer')
        assert get_user_level_role2('..test2@gmail.com') == 'customer'
        assert get_user_level_role2('..tESt2@gmail.com') == 'customer'
        assert get_group_level_role2('..test2@gmail.com', 'group') == 'customer'
        assert not get_group_level_role2('..test2@gmail.com', 'other-group')
