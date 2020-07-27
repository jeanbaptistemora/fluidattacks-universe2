# Standard library
from datetime import (
    datetime,
)
from functools import (
    reduce,
)
from typing import (
    Any,
    Dict,
    List,
)

# Local libraries
from backend.dal import (
    forces as forces_dal,
)
from backend.typing import (
    ForcesExecution as ForcesExecutionType,
)


def match_fields(my_dict: Dict[str, Any]) -> ForcesExecutionType:
    """Replace fields from response according to schema."""
    replace_tuple = (
        ('mocked_exploits',
         'integrates_exploits'),
        ('vulnerability_count_mocked_exploits',
         'num_of_vulnerabilities_in_integrates_exploits'),
        ('vulnerability_count_integrates_exploits',
         'num_of_vulnerabilities_in_integrates_exploits'),
        ('vulnerability_count_exploits',
         'num_of_vulnerabilities_in_exploits'),
        ('vulnerability_count_accepted_exploits',
         'num_of_vulnerabilities_in_accepted_exploits')
    )
    new = {}
    for key, val in my_dict.items():
        if isinstance(val, dict):
            val = match_fields(val)
        new[reduce(lambda a, kv: a.replace(*kv), replace_tuple, key)] = val
    return new


async def get_executions(
    *,
    from_date: datetime,
    group_name: str,
    to_date: datetime,
) -> List[ForcesExecutionType]:
    return [
        match_fields(execution)
        async for execution in forces_dal.yield_executions(
            project_name=group_name,
            from_date=from_date,
            to_date=to_date
        )
    ]


async def add_forces_execution(*, project_name: str,
                               **execution_attributes) -> bool:
    return await forces_dal.create_execution(
        project_name=project_name, **execution_attributes)
