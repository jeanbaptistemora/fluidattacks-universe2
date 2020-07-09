# Standard library
from typing import (
    Dict,
    List,
    Tuple,
)

# Third party library
from django.core.cache import cache
from rediscluster.nodemanager import RedisClusterException

# Local imports
from backend.dal import (
    project as project_dal,
    user as user_dal,
)
from backend.utils import (
    apm,
)
from backend.utils.encodings import (
    safe_encode,
)
from .model import (
    USER_LEVEL_ROLES,
    GROUP_LEVEL_ROLES,
    ORGANIZATION_LEVEL_ROLES
)


def get_group_cache_key(group: str) -> str:
    return f'authorization.group.{safe_encode(group.lower())}'


def get_subject_cache_key(subject: str) -> str:
    return f'authorization.subject.{safe_encode(subject.lower())}'


def get_cached_group_service_attributes_policies(
    group: str,
) -> Tuple[Tuple[str, str], ...]:
    """Cached function to get 1 group features authorization policies."""
    cache_key: str = get_group_cache_key(group)

    try:
        # Attempt to retrieve data from the cache
        ret = cache.get(cache_key)
    except RedisClusterException:
        ret = None

    if ret is None:
        # Let's fetch the data from the database
        ret = tuple(
            (policy.group, policy.service)
            for policy in project_dal.get_service_policies(group))
        try:
            # Put the data in the cache
            cache.set(cache_key, ret, timeout=3600)
        except RedisClusterException:
            pass

    return ret


def get_cached_subject_policies(
    subject: str,
) -> Tuple[Tuple[str, str, str, str], ...]:
    """Cached function to get 1 user authorization policies."""
    cache_key: str = get_subject_cache_key(subject)

    try:
        # Attempt to retrieve data from the cache
        ret = cache.get(cache_key)
    except RedisClusterException:
        ret = None

    if ret is None:
        # Let's fetch the data from the database
        ret = tuple(
            (policy.level, policy.subject, policy.object, policy.role)
            for policy in user_dal.get_subject_policies(subject))
        try:
            # Put the data in the cache
            cache.set(cache_key, ret, timeout=300)
        except RedisClusterException:
            pass

    return ret


@apm.trace()
def get_group_level_role(email: str, group: str) -> str:
    # Admins are granted access to all groups
    group_role = user_dal.get_subject_policy(email, group).role
    if get_user_level_role(email) == 'admin' and not group_role:
        return 'admin'

    return group_role


def get_organization_level_role(email: str, organization: str) -> str:
    # Admins are granted access to all organization
    organization_role = user_dal.get_subject_policy(
        email, organization.lower()
    ).role
    if get_user_level_role(email) == 'admin' and not organization_role:
        return 'admin'

    return organization_role


def get_group_level_roles(email: str, groups: List[str]) -> Dict[str, str]:
    is_admin: bool = get_user_level_role(email) == 'admin'

    db_roles: Dict[str, str] = {
        object_: role
        for level, subject, object_, role in get_cached_subject_policies(email)
        if level == 'group'
        and subject == email
    }

    return {
        group: 'admin'
        if is_admin and group not in db_roles
        else db_roles.get(group, '')
        for group in groups
    }


def get_user_level_role(email: str) -> str:
    return user_dal.get_subject_policy(email, 'self').role


def grant_group_level_role(email: str, group: str, role: str) -> bool:
    if role not in GROUP_LEVEL_ROLES:
        raise ValueError(f'Invalid role value: {role}')

    policy = user_dal.SubjectPolicy(
        level='group',
        subject=email,
        object=group,
        role=role,
    )

    success: bool = True

    # If there is no user-level role for this user add one
    if not get_user_level_role(email):
        user_level_role: str = \
            role if role in USER_LEVEL_ROLES else 'customer'
        success = success and grant_user_level_role(email, user_level_role)

    return success \
        and user_dal.put_subject_policy(policy) \
        and revoke_cached_subject_policies(email)


def grant_organization_level_role(
    email: str,
    organization: str,
    role: str
) -> bool:
    if role not in ORGANIZATION_LEVEL_ROLES:
        raise ValueError(f'Invalid role value: {role}')

    policy = user_dal.SubjectPolicy(
        level='organization',
        subject=email,
        object=organization,
        role=role,
    )

    success: bool = True

    # If there is no user-level role for this user add one
    if not get_user_level_role(email):
        user_level_role: str = (
            role
            if role in USER_LEVEL_ROLES
            else 'customer'
        )
        success = success and grant_user_level_role(email, user_level_role)

    return success \
        and user_dal.put_subject_policy(policy) \
        and revoke_cached_subject_policies(email)


def grant_user_level_role(email: str, role: str) -> bool:
    if role not in USER_LEVEL_ROLES:
        raise ValueError(f'Invalid role value: {role}')

    policy = user_dal.SubjectPolicy(
        level='user',
        subject=email,
        object='self',
        role=role,
    )

    return user_dal.put_subject_policy(policy) \
        and revoke_cached_subject_policies(email)


def revoke_cached_group_service_attributes_policies(group: str) -> bool:
    """Revoke the cached policies for the provided group."""
    cache_key: str = get_group_cache_key(group)

    # Delete the cache key from the cache
    cache.delete_pattern(f'*{cache_key}*')

    # Refresh the cache key as the user is probably going to use it soon :)
    get_cached_group_service_attributes_policies(group)

    return True


def revoke_cached_subject_policies(subject: str) -> bool:
    """Revoke the cached policies for the provided subject."""
    cache_key: str = get_subject_cache_key(subject)

    # Delete the cache key from the cache
    cache.delete_pattern(f'*{cache_key}*')

    # Refresh the cache key as the user is probably going to use it soon :)
    get_cached_subject_policies(subject)

    return True


def revoke_group_level_role(email: str, group: str) -> bool:
    return user_dal.delete_subject_policy(email, group) \
        and revoke_cached_subject_policies(email)


def revoke_user_level_role(email: str) -> bool:
    return user_dal.delete_subject_policy(email, 'self') \
        and revoke_cached_subject_policies(email)
