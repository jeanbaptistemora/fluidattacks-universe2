# Standard libraries
import json
import pytest
from typing import (
    Any,
    Dict,
)

# Local libraries
from . import query


@pytest.mark.asyncio
@pytest.mark.resolver_test_group('resources')
async def test_admin(populate: bool):
    assert populate
    files: Dict[str, str] = [
        {
            "description": "Test",
            "file_name": "test.zip",
            "uploader": "unittest@fluidattacks.com",
            "upload_date": "2019-03-01 15:21"
        },
        {
            "description": "Test",
            "file_name": "shell.exe",
            "uploader": "unittest@fluidattacks.com",
            "upload_date": "2019-04-24 14:56"
        },
        {
            "description": "Test",
            "file_name": "shell2.exe",
            "uploader": "unittest@fluidattacks.com",
            "upload_date": "2019-04-24 14:59"
        },
        {
            "description": "Test",
            "file_name": "asdasd.py",
            "uploader": "unittest@fluidattacks.com",
            "upload_date": "2019-08-06 14:28"
        }
    ]
    result: Dict[str, Any] = await query(
        user='admin@gmail.com',
        group='group1',
    )
    assert 'errors' not in result
    assert result['data']['resources']['projectName'] == 'group1'
    assert json.loads(result['data']['resources']['files']) == files


@pytest.mark.asyncio
@pytest.mark.resolver_test_group('resources')
async def test_analyst(populate: bool):
    assert populate
    files: Dict[str, str] = [
        {
            "description": "Test",
            "file_name": "test.zip",
            "uploader": "unittest@fluidattacks.com",
            "upload_date": "2019-03-01 15:21"
        },
        {
            "description": "Test",
            "file_name": "shell.exe",
            "uploader": "unittest@fluidattacks.com",
            "upload_date": "2019-04-24 14:56"
        },
        {
            "description": "Test",
            "file_name": "shell2.exe",
            "uploader": "unittest@fluidattacks.com",
            "upload_date": "2019-04-24 14:59"
        },
        {
            "description": "Test",
            "file_name": "asdasd.py",
            "uploader": "unittest@fluidattacks.com",
            "upload_date": "2019-08-06 14:28"
        }
    ]
    result: Dict[str, Any] = await query(
        user='analyst@gmail.com',
        group='group1',
    )
    assert 'errors' not in result
    assert result['data']['resources']['projectName'] == 'group1'
    assert json.loads(result['data']['resources']['files']) == files



@pytest.mark.asyncio
@pytest.mark.resolver_test_group('resources')
async def test_closer(populate: bool):
    assert populate
    files: Dict[str, str] = [
        {
            "description": "Test",
            "file_name": "test.zip",
            "uploader": "unittest@fluidattacks.com",
            "upload_date": "2019-03-01 15:21"
        },
        {
            "description": "Test",
            "file_name": "shell.exe",
            "uploader": "unittest@fluidattacks.com",
            "upload_date": "2019-04-24 14:56"
        },
        {
            "description": "Test",
            "file_name": "shell2.exe",
            "uploader": "unittest@fluidattacks.com",
            "upload_date": "2019-04-24 14:59"
        },
        {
            "description": "Test",
            "file_name": "asdasd.py",
            "uploader": "unittest@fluidattacks.com",
            "upload_date": "2019-08-06 14:28"
        }
    ]
    result: Dict[str, Any] = await query(
        user='closer@gmail.com',
        group='group1',
    )
    assert 'errors' not in result
    assert result['data']['resources']['projectName'] == 'group1'
    assert json.loads(result['data']['resources']['files']) == files
