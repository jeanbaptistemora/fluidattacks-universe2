import pytest

from test_async.functional_test.customer.utils import get_result

pytestmark = pytest.mark.asyncio


async def test_event():
    event_id = '418900971'
    group_name = 'unittesting'
    query = f'''{{
        event(identifier: "{event_id}"){{
            client
            evidence
            projectName
            eventType
            detail
            eventDate
            eventStatus
            historicState
            affectation
            accessibility
            affectedComponents
            context
            subscription
            evidenceFile
            closingDate
            consulting {{
                content
            }}
            __typename
        }}
    }}'''
    data = {'query': query}
    result = await get_result(data)
    assert 'errors' not in result
    assert 'event' in result['data']
    assert result['data']['event']['accessibility'] == ''
    assert result['data']['event']['affectation'] == ''
    assert result['data']['event']['affectedComponents'] == ''
    assert result['data']['event']['client'] == 'Fluid'
    assert result['data']['event']['closingDate'] == '-'
    assert result['data']['event']['consulting'] == []
    assert result['data']['event']['context'] == 'FLUID'
    assert result['data']['event']['detail'] == 'Integrates unit test'
    assert result['data']['event']['eventDate'] == '2018-06-27 07:00:00'
    assert result['data']['event']['eventStatus'] == 'CREATED'
    assert result['data']['event']['eventType'] == 'OTHER'
    assert result['data']['event']['evidence'] == ''
    assert result['data']['event']['evidenceFile'] == ''
    assert result['data']['event']['historicState'] == [
        {
            'analyst': 'unittest@fluidattacks.com',
            'date': '2018-06-27 07:00:00',
            'state': 'OPEN'
        },
        {
            'analyst': 'unittest@fluidattacks.com',
            'date': '2018-06-27 14:40:05',
            'state': 'CREATED'
        }
    ]
    assert result['data']['event']['projectName'] == group_name
    assert result['data']['event']['subscription'] == 'ONESHOT'
    query = f'''{{
        events(projectName: "{group_name}"){{
            id
            projectName
            detail
        }}
    }}'''
    data = {'query': query}
    result = await get_result(data)
    assert 'events' in result['data']
    events = result['data']['events']
    event = [event for event in events if event['id'] == event_id][0]
    assert event['projectName'] == group_name
    assert len(event['detail']) >= 1

    query = f'''
        mutation {{
            addEventConsult(eventId: "{event_id}",
                            parent: "0",
                            content: "Test comment") {{
                success
                commentId
            }}
        }}
    '''
    data = {'query': query}
    result = await get_result(data)
    assert 'errors' not in result
    assert 'success' in result['data']['addEventConsult']
    assert result['data']['addEventConsult']
    assert 'commentId' in result['data']['addEventConsult']

    query = f'''
        mutation {{
            downloadEventFile(
                eventId: "{event_id}",
                fileName: "1mvStFSToOL3bl47zaVZHBpRMZUUhU0Ad"
            ) {{
                success
                url
            }}
        }}
    '''
    data = {'query': query}
    result = await get_result(data)
    assert 'errors' not in result
    assert 'success' in result['data']['downloadEventFile']
    assert result['data']['downloadEventFile']
    assert 'url' in result['data']['downloadEventFile']

    query = f'''{{
        event(identifier: "{event_id}"){{
            consulting {{
                content
            }}
        }}
    }}'''
    data = {'query': query}
    result = await get_result(data)
    assert 'errors' not in result
    assert 'event' in result['data']
    assert result['data']['event']['consulting'] == [{'content': 'Test comment'}]
