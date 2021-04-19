# Third party libraries
import pytest

# Local libraries
from data_containers.toe_inputs import GitRootToeInput
from toe.inputs import domain as toe_inputs_domain

# Constants
pytestmark = [
    pytest.mark.asyncio,
]


async def test_get_by_group() -> None:
    group_name = 'unittesting'
    group_toe_inputs = await toe_inputs_domain.get_by_group(group_name)
    assert group_toe_inputs == (
        GitRootToeInput(
            commit='hh66uu5',
            component='test.com/api/Test',
            created_date='2000-01-01T00:00:00-05:00',
            entry_point='idTest',
            group_name='unittesting',
            seen_first_time_by='',
             tested_date='2020-01-02T00:00:00-05:00',
             verified='Yes',
             vulns='FIN.S.0001.Test'),
        GitRootToeInput(
            commit='e91320h',
            component='test.com/test/test.aspx',
            created_date='2020-03-14T00:00:00-05:00',
            entry_point='btnTest',
            group_name='unittesting',
            seen_first_time_by='test@test.com',
            tested_date='2021-02-02T00:00:00-05:00',
            verified='No',
            vulns=''
        ),
        GitRootToeInput(
            commit='d83027t',
            component='test.com/test2/test.aspx',
            created_date='2020-01-11T00:00:00-05:00',
            entry_point='-',
            group_name='unittesting',
            seen_first_time_by='test2@test.com',
            tested_date='2021-02-11T00:00:00-05:00',
            verified='No',
            vulns='FIN.S.0003.Test'
        ),
    )


@pytest.mark.changes_db
async def test_add() -> None:
    group_name = 'unittesting'
    toe_input = GitRootToeInput(
        commit='g42343f',
        component='test.com/test/new.aspx',
        created_date='2000-01-01T00:00:00-05:00',
        entry_point='btnTest',
        group_name=group_name,
        seen_first_time_by='new@test.com',
        tested_date='2021-02-12T00:00:00-05:00',
        verified='Yes',
        vulns='New vulns'
    )
    await toe_inputs_domain.add(toe_input)
    group_toe_inputs = await toe_inputs_domain.get_by_group(group_name)
    assert toe_input in group_toe_inputs


@pytest.mark.changes_db
async def test_delete() -> None:
    group_name = 'unittesting'
    group_toe_inputs = await toe_inputs_domain.get_by_group(group_name)
    assert len(group_toe_inputs) == 4
    await toe_inputs_domain.delete(
        entry_point='btnTest',
        component='test.com/test/new.aspx',
        group_name=group_name,
    )
    group_toe_inputs = await toe_inputs_domain.get_by_group(group_name)
    assert len(group_toe_inputs) == 3


@pytest.mark.changes_db
async def test_update() -> None:
    group_name = 'unittesting'
    toe_input = GitRootToeInput(
        commit='edited',
        component='test.com/test/test.aspx',
        created_date='2000-01-01T00:00:00-05:00',
        entry_point='btnTest',
        group_name=group_name,
        seen_first_time_by='edited@test.com',
        tested_date='2021-02-12T00:00:00-05:00',
        verified='Yes',
        vulns='Edited vulns'
    )
    await toe_inputs_domain.update(toe_input)
    group_toe_inputs = await toe_inputs_domain.get_by_group(group_name)
    assert toe_input in group_toe_inputs
