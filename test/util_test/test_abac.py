import os

import casbin
from django.conf import settings
from django.test import TestCase

from backend.casbin_dynamodb_adapter import Adapter
from backend.dal.helpers import dynamodb


def get_fixture(path):
    dir_path = os.path.split(os.path.realpath(__file__))[0] + "/"
    return os.path.abspath(dir_path + path)


def get_enforcer():
    adapter = Adapter()

    dynamodb_resource = dynamodb.DYNAMODB_RESOURCE

    table = dynamodb_resource.Table(adapter.table_name)
    table.put_item(
        Item={
            'id': '1',
            'ptype': 'p',
            'v0': 'hacker@fluidattacks.com',
            'v1': '/integrates/registration',
            'v2': 'GET',
        }
    )

    table.put_item(
        Item={
            'id': '2',
            'ptype': 'p',
            'v0': 'anonymous',
            'v1': '/integrates/registration',
            'v2': 'GET',
        }
    )

    return casbin.Enforcer(get_fixture('../../integrates_authz_model.conf'), adapter)


class AbacTest(TestCase):

    def test_enforcer_basic(self):
        enfor = get_enforcer()

        self.assertTrue(enfor.enforce('hacker@fluidattacks.com',
                                      '/integrates/registration', 'GET'))
        self.assertTrue(enfor.enforce('hacker@fluidattacks.com',
                                      '/integrates/registration', 'POST'))

    def test_add_policy(self):
        enfor = get_enforcer()

        res = enfor.add_permission_for_user('newuser@fluidattacks.com',
                                            '/integrates/*', 'GET')
        self.assertTrue(res)

    def test_save_policy(self):
        enfor = get_enforcer()

        model = enfor.get_model()
        model.clear_policy()

        model.add_policy('p', 'p',
                         ['newuser2@fluidattacks.com', '/integrates/*', 'GET'])

        adapter = enfor.get_adapter()
        self.assertTrue(adapter.save_policy(model))

    def test_remove_policy(self):
        enfor = get_enforcer()
        res = enfor.add_permission_for_user('newuser3@fluidattacks.com',
                                            '/integrates/*', 'GET')
        self.assertTrue(res)

        res = enfor.delete_permission_for_user('newuser3@fluidattacks.com',
                                               '/integrates/*', 'GET')
        self.assertTrue(res)
