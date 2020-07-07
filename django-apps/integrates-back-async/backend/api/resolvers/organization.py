import asyncio
import sys
from decimal import Decimal
from typing import (
    Dict,
    List,
    Optional
)

from ariadne import (
    convert_camel_case_to_snake,
    convert_kwargs_to_snake_case
)
from graphql.language.ast import SelectionSetNode

from backend import util
from backend.decorators import (
    enforce_group_level_auth_async,
    rename_kwargs,
    require_login,
    require_organization_access
)
from backend.domain import organization as org_domain
from backend.api.resolvers import user as user_loader
from backend.typing import (
    Organization as OrganizationType,
    SimplePayload as SimplePayloadType,
    User as UserType
)


@enforce_group_level_auth_async
async def _do_move_group_organization(
    _,
    info,
    group_name: str,
    organization_name: str,
    new_organization_name: str,
) -> SimplePayloadType:
    """
    Change the organization a group belongs to
    """
    user_data: Dict[str, str] = util.get_jwt_content(info.context)
    user_email: str = user_data['user_email']

    success = await org_domain.move_group(
        group_name,
        organization_name,
        new_organization_name,
        user_email
    )
    if success:
        util.cloudwatch_log(
            info.context,
            f'Security: User {user_email} moved group {group_name} to '
            f'organization {new_organization_name} from {organization_name}'
        )
    else:
        util.cloudwatch_log(
            info.context,
            f'Security: User {user_email} attempted to move group '
            f'{group_name} to organization {new_organization_name}'
        )
    return SimplePayloadType(success=success)


async def _do_update_organization_policies(
    _,
    info,
    organization_id: str,
    organization_name: str,
    **parameters
) -> SimplePayloadType:
    user_data = util.get_jwt_content(info.context)
    user_email = user_data['user_email']
    success: bool = await org_domain.update_policies(
        organization_id,
        organization_name,
        parameters
    )
    if success:
        util.cloudwatch_log(
            info.context,
            f'Security: User {user_email} updated policies for organization '
            f'{organization_name} with ID {organization_id}'
        )
    return SimplePayloadType(success=success)


@rename_kwargs({'identifier': 'organization_name'})
async def _get_id(_, organization_name: str, **__) -> str:
    return await org_domain.get_id_by_name(organization_name)


@rename_kwargs({'identifier': 'organization_id'})
async def _get_name(_, organization_id: str, **__) -> str:
    return await org_domain.get_name_by_id(organization_id)


@rename_kwargs({'identifier': 'organization_id'})
async def _get_max_acceptance_days(
    _,
    organization_id: str,
    **__
) -> Decimal:
    return await org_domain.get_max_acceptance_days(organization_id)


@rename_kwargs({'identifier': 'organization_id'})
async def _get_max_acceptance_severity(
    _,
    organization_id: str,
    **__
) -> Decimal:
    return await org_domain.get_max_acceptance_severity(organization_id)


@rename_kwargs({'identifier': 'organization_id'})
async def _get_max_number_acceptations(
    _,
    organization_id: str,
    **__
)-> Optional[Decimal]:
    return await org_domain.get_max_number_acceptations(organization_id)


@rename_kwargs({'identifier': 'organization_id'})
async def _get_min_acceptance_severity(
    _,
    organization_id: str,
    **__
) -> Decimal:
    return await org_domain.get_min_acceptance_severity(organization_id)


@rename_kwargs({'identifier': 'organization_id'})
async def _get_users(
    info,
    organization_id: str,
    requested_fields: list
) -> List[UserType]:
    """Get users."""
    organization_users = await org_domain.get_users(organization_id)

    as_field = True
    selection_set = SelectionSetNode()
    selection_set.selections = requested_fields

    return await asyncio.gather(*[
        asyncio.create_task(
            user_loader.resolve_for_organization(
                info,
                'ORGANIZATION',
                user_email,
                organization_id=organization_id,
                as_field=as_field,
                selection_set=selection_set,
            )
        )
        for user_email in organization_users
    ])


async def resolve(
        info,
        identifier: str,
        as_field: bool = False,
        selection_set: SelectionSetNode = SelectionSetNode()
) -> OrganizationType:
    """Async resolve fields."""
    result = dict()
    requested_fields = (
        util.get_requested_fields('organization', selection_set)
        if as_field
        else info.field_nodes[0].selection_set.selections
    )

    for requested_field in requested_fields:
        if util.is_skippable(info, requested_field):
            continue

        params = {
            'identifier': identifier,
            'requested_fields': requested_fields
        }
        field_params = util.get_field_parameters(requested_field)
        if field_params:
            params.update(field_params)

        requested_field = convert_camel_case_to_snake(
            requested_field.name.value
        )
        if requested_field.startswith('_'):
            continue

        resolver_func = getattr(
            sys.modules[__name__],
            f'_get_{requested_field}'
        )
        result[requested_field] = resolver_func(info, **params)
    return result


@convert_kwargs_to_snake_case
@rename_kwargs({
    'organization_id': 'identifier',
    'organization_name': 'identifier'
})
@require_login
@require_organization_access
async def resolve_organization(
    _,
    info,
    identifier: str
) -> OrganizationType:
    """Resolve Organization query """
    return await resolve(info, identifier)


@convert_kwargs_to_snake_case
@require_login
@require_organization_access
async def resolve_organization_mutation(obj, info, **parameters):
    """Resolve Organization mutation """
    field = util.camelcase_to_snakecase(info.field_name)
    resolver_func = getattr(sys.modules[__name__], f'_do_{field}')
    return await resolver_func(obj, info, **parameters)
