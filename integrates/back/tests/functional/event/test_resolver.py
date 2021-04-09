# Standard libraries
import pytest
from typing import (
    Any,
    Dict,
)

# Local libraries
from . import query


@pytest.mark.asyncio
@pytest.mark.resolver_test_group('event')
async def test_admin(populate: bool):
    assert populate
    event_id: str = '418900971'
    result: Dict[str, Any] = await query(
        user='admin@gmail.com',
        event=event_id
    )
    assert 'errors' not in result
    assert 'event' in result['data']
    assert result['data']['event']['accessibility'] == 'Repositorio'
    assert result['data']['event']['affectation'] == ''
    assert result['data']['event']['affectedComponents'] == 'affected_components_test'
    assert result['data']['event']['client'] == 'Fluid'
    assert result['data']['event']['closingDate'] == '-'
    assert result['data']['event']['consulting'] == [{'content': 'This is a test comment'}]
    assert result['data']['event']['context'] == 'FLUID'
    assert result['data']['event']['detail'] == 'Integrates unit test'
    assert result['data']['event']['eventDate'] == '2018-06-27 07:00:00'
    assert result['data']['event']['eventStatus'] == 'CREATED'
    assert result['data']['event']['eventType'] == 'OTHER'
    assert result['data']['event']['evidence'] == '1bhEW8rN33fq01SBmWjjEwEtK6HWkdMq6'
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
        },
    ]
    assert result['data']['event']['projectName'] == 'group1'
    assert result['data']['event']['subscription'] == 'ONESHOT'


@pytest.mark.asyncio
@pytest.mark.resolver_test_group('event')
async def test_analyst(populate: bool):
    assert populate
    event_id: str = '418900971'
    result: Dict[str, Any] = await query(
        user='analyst@gmail.com',
        event=event_id

    )
    assert 'errors' not in result
    assert 'event' in result['data']
    assert result['data']['event']['accessibility'] == 'Repositorio'
    assert result['data']['event']['affectation'] == ''
    assert result['data']['event']['affectedComponents'] == 'affected_components_test'
    assert result['data']['event']['client'] == 'Fluid'
    assert result['data']['event']['closingDate'] == '-'
    assert result['data']['event']['consulting'] == [{'content': 'This is a test comment'}]
    assert result['data']['event']['context'] == 'FLUID'
    assert result['data']['event']['detail'] == 'Integrates unit test'
    assert result['data']['event']['eventDate'] == '2018-06-27 07:00:00'
    assert result['data']['event']['eventStatus'] == 'CREATED'
    assert result['data']['event']['eventType'] == 'OTHER'
    assert result['data']['event']['evidence'] == '1bhEW8rN33fq01SBmWjjEwEtK6HWkdMq6'
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
        },
    ]
    assert result['data']['event']['projectName'] == 'group1'
    assert result['data']['event']['subscription'] == 'ONESHOT'



@pytest.mark.asyncio
@pytest.mark.resolver_test_group('event')
async def test_closer(populate: bool):
    assert populate
    event_id: str = '418900971'
    result: Dict[str, Any] = await query(
        user='closer@gmail.com',
        event=event_id

    )
    assert 'errors' not in result
    assert 'event' in result['data']
    assert result['data']['event']['accessibility'] == 'Repositorio'
    assert result['data']['event']['affectation'] == ''
    assert result['data']['event']['affectedComponents'] == 'affected_components_test'
    assert result['data']['event']['client'] == 'Fluid'
    assert result['data']['event']['closingDate'] == '-'
    assert result['data']['event']['consulting'] == [{'content': 'This is a test comment'}]
    assert result['data']['event']['context'] == 'FLUID'
    assert result['data']['event']['detail'] == 'Integrates unit test'
    assert result['data']['event']['eventDate'] == '2018-06-27 07:00:00'
    assert result['data']['event']['eventStatus'] == 'CREATED'
    assert result['data']['event']['eventType'] == 'OTHER'
    assert result['data']['event']['evidence'] == '1bhEW8rN33fq01SBmWjjEwEtK6HWkdMq6'
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
        },
    ]
    assert result['data']['event']['projectName'] == 'group1'
    assert result['data']['event']['subscription'] == 'ONESHOT'
