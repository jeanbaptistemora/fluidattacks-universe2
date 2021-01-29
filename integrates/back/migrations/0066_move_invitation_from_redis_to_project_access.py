"""
This migration move a group invitation from redis to project_access table
"""
# Standard library
from datetime import timedelta
from pprint import pprint
from typing import (
    Dict,
    cast,
)

# Third party libraries
from aioextensions import (
    collect,
    run,
)

# Local libraries
from backend import authz
from backend.dal.helpers.redis import (
    redis_cmd,
    redis_get_entity_attr,
    redis_ttl_entity_attr
)
from backend.domain import (
    project as group_domain,
)
from backend.utils import (
    datetime as datetime_utils,
)

TABLE_ACCESS_NAME = 'FI_project_access'


async def move_invitation_to_db(
    redis_invitation: Dict[str, str],
    invitation_token: str
) -> bool:
    prefix = 'invitation_token.data@token='
    token_ttl: int = await redis_ttl_entity_attr(
        entity='invitation_token',
        attr='data',
        token=invitation_token,
    )
    user_email = redis_invitation['user_email']
    group_name = redis_invitation['group']
    is_used = redis_invitation['is_used']
    responsibility = redis_invitation['responsibility']

    week_segs = 604800
    segs_since_the_invitation = week_segs - token_ttl
    invitation_date = datetime_utils.get_as_str(
        datetime_utils.get_now() - timedelta(seconds=segs_since_the_invitation)
    )
    group_role = await authz.get_group_level_role(user_email, group_name)
    redis_key = f'{prefix}{invitation_token}'
    new_invitation = {
        'date': invitation_date,
        'is_used': is_used,
        'responsibility': responsibility,
        'role': group_role,
        'url_token': invitation_token,
    }

    print('redis_key')
    print(redis_key)
    print('redis_invitation')
    pprint(redis_invitation)
    print('new_invitation')
    pprint(new_invitation)

    success = cast(bool, await group_domain.update_access(
        user_email,
        group_name,
        {
            'invitation': new_invitation,
            'invitation_date': None
        }
    ))

    if success:
        await redis_cmd('delete', redis_key)

    return success


async def main() -> None:
    prefix = 'invitation_token.data@token='
    invitation_tokens = await redis_cmd('keys', f'{prefix}*')
    print('invitation_tokens', invitation_tokens)

    invitation_tokens = [
        invitation_token.replace(prefix, '')
        for invitation_token in invitation_tokens
    ]
    redis_invitations = await collect([
        redis_get_entity_attr(
            entity='invitation_token',
            attr='data',
            token=invitation_token,
        )
        for invitation_token in invitation_tokens
    ])
    print('redis_invitations', redis_invitations)

    redis_invitations = await collect([
        move_invitation_to_db(
           redis_invitation,
           invitation_token
        )
        for redis_invitation, invitation_token
        in zip(redis_invitations, invitation_tokens)
    ])


if __name__ == '__main__':
    run(main())
