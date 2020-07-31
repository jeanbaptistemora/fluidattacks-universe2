from typing import Dict, Sequence, Any, Union
from asgiref.sync import async_to_sync
from backend import authz, mailer
from backend.domain import user as user_domain
from backend.utils import aio
from social_core.strategy import BaseStrategy
from social_core.backends.oauth import OAuthAuth
from django.contrib.auth.models import User

from __init__ import (
    FI_COMMUNITY_PROJECTS,
    FI_MAIL_CONTINUOUS,
    FI_MAIL_PROJECTS,
)


def get_upn(
        strategy: BaseStrategy,
        details: Dict[str, str],
        backend: OAuthAuth,
        *args: Sequence[Any],
        **kwargs: Dict[str, Any]) -> None:
    # When using a personal Microsoft account,
    # upn does not exist in response
    del strategy
    del details
    del args
    if (getattr(backend, 'name', None) == 'azuread-tenant-oauth2' and
            not kwargs['response'].get('upn')):
        kwargs['response']['upn'] = kwargs.get(  # type: ignore
            'response'
        )['email']


@async_to_sync
async def autoenroll_user(strategy: BaseStrategy, email: str) -> bool:
    # New users must have access to the community projects
    was_granted_access: bool = True

    # Registered users have this attribute set to True
    is_registered: bool = await user_domain.is_registered(email)

    if not is_registered:
        new_user_user_level_role: str = 'customer'
        new_user_group_level_role: str = 'customer'

        # Create the user into the community organization
        is_registered = await user_domain.create_without_project(
            email=email,
            role=new_user_user_level_role,
        )

        # Add a flag that may come handy later to ask for extra data
        strategy.session_set('is_new_user', True)

        # Add the user into the community projects
        for group in FI_COMMUNITY_PROJECTS.split(','):
            was_granted_access = all(await aio.materialize([
                user_domain.update_project_access(email, group, access=True),
                authz.grant_group_level_role(
                    email, group, new_user_group_level_role
                )
            ]))

    return is_registered and was_granted_access


# pylint: disable=keyword-arg-before-vararg
def create_user(
        strategy: BaseStrategy,
        details: Dict[str, str],
        backend: OAuthAuth,
        user: Union[User, None] = None,
        *args: Sequence[Any],
        **kwargs: Dict[str, Any]) -> None:
    del args
    del kwargs
    del backend
    first_name = details['first_name'][:29]
    last_name = details['last_name'][:29]
    email = details['email'].lower()

    # Grant new users access to Integrates and the community projects
    autoenroll_user(strategy, email)

    # Put details on session.
    strategy.session_set('first_name', first_name)
    strategy.session_set('last_name', last_name)

    today = user_domain.get_current_date()
    data_dict = {
        'first_name': first_name,
        'last_login': today,
        'last_name': last_name,
        'date_joined': today
    }
    if user:
        if async_to_sync(user_domain.get_data)(str(user), 'first_name'):
            async_to_sync(user_domain.update_last_login)(user)
        else:
            async_to_sync(user_domain.update_multiple_user_attributes)(
                str(user), data_dict
            )
    else:
        mail_to = [FI_MAIL_CONTINUOUS, FI_MAIL_PROJECTS]
        name = f'{first_name} {last_name}'
        context = {
            'name_user': name,
            'mail_user': email,
        }
        mailer.send_mail_new_user(mail_to, context)
        async_to_sync(user_domain.update_multiple_user_attributes)(
            email, data_dict
        )


def check_registered(
        strategy: BaseStrategy,
        details: Dict[str, str],
        backend: OAuthAuth,
        *args: Sequence[Any],
        **kwargs: Dict[str, Any]) -> None:
    del args
    del kwargs
    del backend
    email = details['email'].lower()
    is_registered = async_to_sync(user_domain.is_registered)(email)
    last_login = async_to_sync(user_domain.get_data)(email, 'last_login')
    role = authz.get_user_level_role(email)
    strategy.session_set('role', role)
    strategy.session_set('username', email)
    strategy.session_set('registered', is_registered)
    strategy.session_set('last_login', last_login)
    strategy.session_set('projects', {})
