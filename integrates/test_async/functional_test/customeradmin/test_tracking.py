import pytest

from test_async.functional_test.customer.utils import get_result

pytestmark = pytest.mark.asyncio


async def test_tracking():
    finding_id = '436992569'
    expected_output =  {
        'id': finding_id,
        'tracking': [
            {
                "cycle": 0,
                "open": 1,
                "closed": 0,
                "effectiveness": 0,
                "date": "2019-08-30",
                "new": 1,
                "in_progress": 0,
                "accepted": 0,
                "accepted_undefined": 0,
                "manager": ""
            },
            {
                "cycle": 1,
                "open": 16,
                "closed": 0,
                "effectiveness": 0,
                "date": "2019-09-12",
                "new": 16,
                "in_progress": 0,
                "accepted": 0,
                "accepted_undefined": 0,
                "manager": ""
            },
            {
                "cycle": 2,
                "open": 22,
                "closed": 4,
                "effectiveness": 15,
                "date": "2019-09-13",
                "new": 22,
                "in_progress": 0,
                "accepted": 0,
                "accepted_undefined": 0,
                "manager": ""
            },
            {
                "cycle": 3,
                "open": 24,
                "closed": 4,
                "effectiveness": 14,
                "date": "2019-09-16",
                "new": 24,
                "in_progress": 0,
                "accepted": 0,
                "accepted_undefined": 0,
                "manager": ""
            }
        ],
    }
    query = f'''{{
        finding(identifier: "{finding_id}"){{
            id
            tracking
        }}
    }}'''
    data = {'query': query}
    result = await get_result(data)
    assert 'errors' not in result
    assert result['data']['finding']['id'] == expected_output.get('id')
    assert result['data']['finding']['tracking'] == expected_output.get('tracking')

    finding_id = '422286126'
    expected_output =  {
        'id': finding_id,
        'tracking': [
            {
                "cycle": 0,
                "open": 1,
                "closed": 0,
                "effectiveness": 0,
                "date": "2020-01-03",
                "new": 0,
                "in_progress": 1,
                "accepted": 0,
                "accepted_undefined": 0,
                "manager": ""
            }
        ],
    }
    query = f'''{{
        finding(identifier: "{finding_id}"){{
            id
            tracking
        }}
    }}'''
    data = {'query': query}
    result = await get_result(data)
    assert 'errors' not in result
    assert result['data']['finding']['id'] == expected_output.get('id')
    assert result['data']['finding']['tracking'] == expected_output.get('tracking')

    finding_id = '463558592'
    expected_output =  {
        'id': finding_id,
        'tracking': [
            {
                "cycle": 0,
                "open": 1,
                "closed": 1,
                "effectiveness": 50,
                "date": "2019-01-15",
                "new": 0,
                "in_progress": 0,
                "accepted": 1,
                "accepted_undefined": 0,
                "manager": "integratesuser@gmail.com"
            }
        ],
    }
    query = f'''{{
        finding(identifier: "{finding_id}"){{
            id
            tracking
        }}
    }}'''
    data = {'query': query}
    result = await get_result(data)
    assert 'errors' not in result
    assert result['data']['finding']['id'] == expected_output.get('id')
    assert result['data']['finding']['tracking'] == expected_output.get('tracking')

    finding_id = '463461507'
    expected_output =  {
        'id': finding_id,
        'tracking': [
            {
                "cycle": 0,
                "open": 1,
                "closed": 0,
                "accepted": 0,
                "accepted_undefined": 0,
                "manager": "",
                "effectiveness": 0,
                "date": "2019-09-12",
                "new": 0,
                "in_progress": 1,
            },
            {
                "cycle": 1,
                "open": 2,
                "closed": 0,
                "accepted": 1,
                "accepted_undefined": 0,
                "manager": "",
                "effectiveness": 0,
                "date": "2019-09-13",
                "new": 1,
                "in_progress": 0,
            }
        ],
    }
    query = f'''{{
        finding(identifier: "{finding_id}"){{
            id
            tracking
        }}
    }}'''
    data = {'query': query}
    result = await get_result(data)
    assert 'errors' not in result
    assert result['data']['finding']['id'] == expected_output.get('id')
    assert result['data']['finding']['tracking'] == expected_output.get('tracking')
