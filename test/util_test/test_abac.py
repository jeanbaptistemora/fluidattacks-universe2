import casbin
from django.conf import settings
from django.test import TestCase


def get_enforcer():
    return casbin.Enforcer(settings.CASBIN_POLICY_MODEL_FILE)


class AbacTest(TestCase):

    def test_enforcer_basic(self):
        enfor = get_enforcer()

        class TestItem:
            pass

        sub1 = TestItem()
        sub1.username = ''

        sub2 = TestItem()
        sub2.username = 'someone'

        obj = '/integrates/registration'

        self.assertFalse(enfor.enforce(sub1, obj))
        self.assertTrue(enfor.enforce(sub2, obj))

        sub3 = TestItem()
        sub3.username = 'someone'
        sub3.role = 'customer'

        should_deny = (
            '/integrates/export_all_vulnerabilities',
            '/integrates/12312313/download_vulnerabilities'
        )

        should_allow = (
            '/integrates/registration',
            '/integrates/dashboard',
            '/integrates/xls/',
            '/integrates/pdf/',
        )

        for url in should_deny:
            self.assertFalse(enfor.enforce(sub3, url))

        for url in should_allow:
            self.assertTrue(enfor.enforce(sub3, url))
