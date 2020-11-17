# Standard
from typing import Any, Dict, List

# Third party
# None

# Local
from backend.dal import root as root_dal
from backend.exceptions import InvalidParameter
from backend.typing import GitRoot, IPRoot, URLRoot, Root
from backend.utils import validations


async def get_roots_by_group(group_name: str) -> List[Root]:
    roots = await root_dal.get_roots_by_group(group_name)

    return [
        GitRoot(
            branch=root['branch'],
            directory_filtering=root.get('directory_filtering'),
            environment=root.get('environment'),
            id=root['sk'],
            url=root['url']
        )
        if root['kind'] == 'Git'
        else IPRoot(
            address=root['address'],
            id=root['sk'],
            port=root['port']
        )
        if root['kind'] == 'IP'
        else URLRoot(
            address=root['address'],
            id=root['sk'],
            path=root['path'],
            port=root['port'],
            protocol=root['protocol']
        )
        for root in roots
    ]


async def add_git_root(user_email: str, **kwargs: Any) -> None:
    group_name: str = kwargs['group_name'].lower()

    def _is_valid() -> bool:
        if (
            validations.is_valid_url(kwargs['url'])
            and validations.is_valid_git_branch(kwargs['branch'])
        ):
            if kwargs.get('environment'):
                return validations.is_valid_url(kwargs['environment']['url'])
            return True
        return False

    if _is_valid():
        root_attributes: Dict[str, Any] = {
            'branch': kwargs['branch'],
            'directory_filtering': kwargs.get('directory_filtering'),
            'environment': kwargs.get('environment'),
            'created_by': user_email,
            'kind': 'Git',
            'url': kwargs['url']
        }

        await root_dal.add_root(group_name, root_attributes)
    else:
        raise InvalidParameter()
