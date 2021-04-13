# Standard libraries
import pytest
from typing import (
    Any,
    Dict,
)

# Local libraries
from . import query


@pytest.mark.asyncio
@pytest.mark.resolver_test_group('forces_executions')
async def test_admin(populate: bool):
    assert populate
    result: Dict[str, Any] = await query(
        user='admin@gmail.com',
        group='group-1',
    )
    executions = result['data']['forcesExecutions']['executions']
    assert result['data']['forcesExecutions']['fromDate'] == '2020-02-01 00:00:00+00:00'
    assert result['data']['forcesExecutions']['toDate'] == '2020-02-28 23:59:59+00:00'
    assert executions[0]['date'] == '2020-02-05T00:00:00-05:00'
    assert executions[0]['exitCode'] == '1'
    assert executions[0]['gitBranch'] == 'master'
    assert executions[0]['gitCommit'] == '6e7b34c1358db2ff4123c3c76e7fe3bf9f2838f6'
    assert executions[0]['gitOrigin'] == 'http://test.com'
    assert executions[0]['gitRepo'] == 'Repository'
    assert executions[0]['kind'] == 'dynamic'
    assert executions[0]['strictness'] == 'strict'


@pytest.mark.asyncio
@pytest.mark.resolver_test_group('forces_executions')
async def test_analyst(populate: bool):
    assert populate
    result: Dict[str, Any] = await query(
        user='analyst@gmail.com',
        group='group-1',
    )
    executions = result['data']['forcesExecutions']['executions']
    assert result['data']['forcesExecutions']['fromDate'] == '2020-02-01 00:00:00+00:00'
    assert result['data']['forcesExecutions']['toDate'] == '2020-02-28 23:59:59+00:00'
    assert executions[0]['date'] == '2020-02-05T00:00:00-05:00'
    assert executions[0]['exitCode'] == '1'
    assert executions[0]['gitBranch'] == 'master'
    assert executions[0]['gitCommit'] == '6e7b34c1358db2ff4123c3c76e7fe3bf9f2838f6'
    assert executions[0]['gitOrigin'] == 'http://test.com'
    assert executions[0]['gitRepo'] == 'Repository'
    assert executions[0]['kind'] == 'dynamic'
    assert executions[0]['strictness'] == 'strict'



@pytest.mark.asyncio
@pytest.mark.resolver_test_group('forces_executions')
async def test_analyst(populate: bool):
    assert populate
    result: Dict[str, Any] = await query(
        user='closer@gmail.com',
        group='group-1',
    )
    executions = result['data']['forcesExecutions']['executions']
    assert result['data']['forcesExecutions']['fromDate'] == '2020-02-01 00:00:00+00:00'
    assert result['data']['forcesExecutions']['toDate'] == '2020-02-28 23:59:59+00:00'
    assert executions[0]['date'] == '2020-02-05T00:00:00-05:00'
    assert executions[0]['exitCode'] == '1'
    assert executions[0]['gitBranch'] == 'master'
    assert executions[0]['gitCommit'] == '6e7b34c1358db2ff4123c3c76e7fe3bf9f2838f6'
    assert executions[0]['gitOrigin'] == 'http://test.com'
    assert executions[0]['gitRepo'] == 'Repository'
    assert executions[0]['kind'] == 'dynamic'
    assert executions[0]['strictness'] == 'strict'
