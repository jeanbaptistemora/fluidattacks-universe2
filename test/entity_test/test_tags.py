from django.test import TestCase
from graphene.test import Client
from backend.api.schema import SCHEMA
from backend.api.dataloaders.vulnerability import VulnerabilityLoader
from .test_utils import Request


class TagEntityTests(TestCase):
    def test_get_tag(self):
        query = '''
            query{
                tag(tag: "test-projects"){
                    name
                    projects {
                        closedVulnerabilities
                        name
                        openVulnerabilities
                    }
                }
            }
        '''
        testing_client = Client(SCHEMA)
        request = Request().get_request({
            'username': 'unittest',
            'company': 'unittest',
            'role': 'customer',
            'useremail': 'integratesuser@gmail.com'
        })
        request_loaders = {'vulnerability': VulnerabilityLoader()}
        request.loaders = request_loaders
        result = testing_client.execute(
            query, context_value=request
        )
        assert 'errors' not in result
        assert 'projects' in result['data']['tag']
