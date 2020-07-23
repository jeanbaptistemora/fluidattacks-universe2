import pytest

from backend.dal.project import get

from backend.dal.resources import (
    create, update, remove
)

pytestmark = pytest.mark.asyncio


@pytest.mark.changes_db
def test_create():
    assert get('unittesting_project') == {}

    create(
        [{'description':'this is a test','filename':'nonexistentfile'}],
        'unittesting_project','files')
    assert get('unittesting_project') == {
        'project_name':'unittesting_project',
        'files':[
            {'description':'this is a test', 'filename':'nonexistentfile'}
        ]
    }

    create(
        [{'description':'this is a test2', 'filename':'nonexistentfile2'}],
        'unittesting_project', 'files')
    assert get('unittesting_project') == {
        'project_name':'unittesting_project',
        'files':[
            {'description':'this is a test', 'filename':'nonexistentfile'},
            {'description':'this is a test2', 'filename':'nonexistentfile2'}
        ]
    }

    create(
        [{'branch':'unittesting', 'urlRepo':'nonexistent.repo'}],
        'unittesting_project', 'repositories')
    assert get('unittesting_project') == {
        'project_name':'unittesting_project',
        'files':[
            {'description':'this is a test', 'filename':'nonexistentfile'},
            {'description':'this is a test2', 'filename':'nonexistentfile2'}
        ],
        'repositories':[
            {'branch':'unittesting', 'urlRepo':'nonexistent.repo'}
        ]
    }


@pytest.mark.changes_db
def test_update():
    assert get('unittesting_project_2') == {}

    create(
        [{'description':'this is a test','filename':'nonexistentfile'}],
        'unittesting_project_2','files')
    assert get('unittesting_project_2') == {
        'project_name':'unittesting_project_2',
        'files':[
            {'description':'this is a test', 'filename':'nonexistentfile'}
        ]
    }

    update(
        [{'description':'this is a test2', 'filename':'nonexistentfile2'}],
        'unittesting_project_2', 'files')
    assert get('unittesting_project_2') == {
        'project_name':'unittesting_project_2',
        'files':[
            {'description':'this is a test2', 'filename':'nonexistentfile2'}
        ]
    }

    update(
        [{'branch':'unittesting', 'urlRepo':'nonexistent.repo'}],
        'unittesting_project_2', 'repositories')
    assert get('unittesting_project_2') == {
        'project_name':'unittesting_project_2',
        'files':[
            {'description':'this is a test2', 'filename':'nonexistentfile2'}
        ],
        'repositories':[
            {'branch':'unittesting', 'urlRepo':'nonexistent.repo'}
        ]
    }


@pytest.mark.changes_db
async def test_remove():
    assert get('unittesting_project_3') == {}

    create(
        [{'description':'this is a test','filename':'nonexistentfile'}],
        'unittesting_project_3','files')

    create(
        [{'description':'this is a test2', 'filename':'nonexistentfile2'}],
        'unittesting_project_3', 'files')

    create(
        [{'branch':'unittesting', 'urlRepo':'nonexistent.repo'}],
        'unittesting_project_3', 'repositories')
    assert get('unittesting_project_3') == {
        'project_name':'unittesting_project_3',
        'files':[
            {'description':'this is a test', 'filename':'nonexistentfile'},
            {'description':'this is a test2', 'filename':'nonexistentfile2'}
        ],
        'repositories':[
            {'branch':'unittesting', 'urlRepo':'nonexistent.repo'}
        ]
    }

    await remove('unittesting_project_3', 'files', '0')
    assert get('unittesting_project_3') == {
        'project_name':'unittesting_project_3',
        'files':[
            {'description':'this is a test2', 'filename':'nonexistentfile2'}
        ],
        'repositories':[
            {'branch':'unittesting', 'urlRepo':'nonexistent.repo'}
        ]
    }

    await remove('unittesting_project_3', 'files', '0')
    assert get('unittesting_project_3') == {
        'project_name':'unittesting_project_3',
        'files':[],
        'repositories':[
            {'branch':'unittesting', 'urlRepo':'nonexistent.repo'}
        ]
    }

    await remove('unittesting_project_3', 'files', '2')
    assert get('unittesting_project_3') == {
        'project_name':'unittesting_project_3',
        'files':[],
        'repositories':[
            {'branch':'unittesting', 'urlRepo':'nonexistent.repo'}
        ]
    }
