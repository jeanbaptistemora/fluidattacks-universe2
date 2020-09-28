"""Raw data extractor from gitlab"""

from asyncio import (
    create_task,
    Queue,
)
from asgiref.sync import async_to_sync
from tap_gitlab import extractor
import aiohttp


class MockServer():
    """Mock api server"""
    def __init__(self, total_items):
        self.total_items = total_items
        self.n_requests = 0

    async def mock_get_request(
        self, session: aiohttp.ClientSession, endpoint: str, params: dict, **kargs):
        """Mock get request"""
        if self.n_requests < self.total_items:
            if endpoint == 'https://gitlab.com/api/v4/projects/project66/merge_requests':
                _resp = {
                    'test1': 'data', 'test2': 2312,
                    'page': params['page']
                }
                self.n_requests = self.n_requests + 1
                return _resp
        return None

def test_gitlab_data_emitter_no_missing_data():
    """Test if emitter pushs  all the data to the queue"""
    async def test():
        queue = Queue(maxsize=1024)
        total_items = 10
        server = MockServer(total_items)
        data_emitter = \
            await extractor.gitlab_data_emitter(
                get_request=server.mock_get_request,
                project='project66',
                resource='merge_requests',
                params={'scope': 'all'},
                api_token='mock_api_token'
            )
        emitter_task = create_task(data_emitter(queue))
        await emitter_task
        assert queue.qsize() == total_items

        for i in range(1, total_items):
            expected = {
                'type': 'gitlab_page_data',
                'project': 'project66',
                'resource': 'merge_requests',
                'page': i, 'per_page': 100,
                'records': {'test1': 'data', 'test2': 2312, 'page': i}
            }
            result = await queue.get()
            assert expected == result

    async_to_sync(test)()
