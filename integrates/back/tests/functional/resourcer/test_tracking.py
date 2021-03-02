import pytest

from back.tests.functional.customer.utils import get_result


@pytest.mark.asyncio
@pytest.mark.old
async def test_tracking():
    finding_id = '436992569'
    expected_output =  {
        'id': finding_id,
        'tracking': [
            {
                "cycle": 0,
                "open": 1,
                "closed": 0,
                "date": "2019-08-30",
                "accepted": 0,
                "accepted_undefined": 0,
                "justification": "",
                "manager": ""
            },
            {
                "cycle": 1,
                "open": 15,
                "closed": 0,
                "date": "2019-09-12",
                "accepted": 0,
                "accepted_undefined": 0,
                "justification": "",
                "manager": ""
            },
            {
                "cycle": 2,
                "open": 6,
                "closed": 0,
                "date": "2019-09-13",
                "accepted": 0,
                "accepted_undefined": 0,
                "justification": "",
                "manager": ""
            },
            {
                "cycle": 3,
                "open": 0,
                "closed": 4,
                "date": "2019-09-13",
                "accepted": 0,
                "accepted_undefined": 0,
                "justification": "",
                "manager": ""
            },
            {
                "cycle": 4,
                "open": 2,
                "closed": 0,
                "date": "2019-09-16",
                "accepted": 0,
                "accepted_undefined": 0,
                "justification": "",
                "manager": ""
            },
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
                "justification": "",
                "date": "2020-01-03",
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
                "closed": 0,
                "date": "2019-01-15",
                "accepted": 0,
                "accepted_undefined": 0,
                "justification": "",
                "manager": ""
            },
            {
                "cycle": 1,
                "open": 0,
                "closed": 1,
                "date": '2019-01-15',
                "accepted": 0,
                "accepted_undefined": 0,
                "justification": "",
                "manager": ""
            },
            {
                "cycle": 2,
                "open": 0,
                "closed": 0,
                "date": "2019-01-15",
                "justification": "This is a treatment justification test",
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
                "justification": "",
                "date": "2019-09-12",
            },
            {
                "cycle": 1,
                "open": 1,
                "closed": 0,
                "accepted": 0,
                "accepted_undefined": 0,
                "manager": "",
                "justification": "",
                "date": "2019-09-13",
            },
            {
                "cycle": 2,
                "open": 0,
                "closed": 0,
                "accepted": 1,
                "accepted_undefined": 0,
                "manager": "integratesuser@gmail.com",
                "justification": "accepted justification",
                "date": "2019-09-13",
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
