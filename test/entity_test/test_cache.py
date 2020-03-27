from django.test import TestCase
from graphene.test import Client
from .test_utils import Request

from backend.api.schema import SCHEMA


class CacheTests(TestCase):

    def test_mutate_cache(self):
        request = Request().get_request({
            'username': 'unittest',
            'company': 'unittest',
            'role': 'analyst',
            'useremail': 'unittest'
        })
        query = '''
            mutation {
                invalidateCache(pattern: "asdf") {
                    success
                }
            }
        '''
        testing_client = Client(SCHEMA)
        result = testing_client.execute(query, context=request)
        assert 'errors' not in result
        assert result['data']['invalidateCache']['success']
