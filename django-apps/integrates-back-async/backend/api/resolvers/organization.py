import asyncio
import sys
from decimal import Decimal
from functools import reduce
from typing import (
    cast,
    Dict,
    List,
    Optional,
    Union
)

from ariadne import (
    convert_camel_case_to_snake,
    convert_kwargs_to_snake_case
)
from graphql.language.ast import FieldNode, SelectionSetNode, ObjectFieldNode

from backend import (
    authz,
    util
)
from backend.api.resolvers import (
    analytics as analytics_loader,
    user as user_loader,
)
from backend.decorators import (
    enforce_organization_level_auth_async,
    get_entity_cache_async,
    rename_kwargs,
    require_login,
    require_organization_access
)
from backend.domain import (
    organization as org_domain,
    user as user_domain
)
from backend.typing import (
    EditUserPayload as EditUserPayloadType,
    GrantUserAccessPayload as GrantUserAccessPayloadType,
    Organization as OrganizationType,
    Project as ProjectType,
    SimplePayload as SimplePayloadType,
    User as UserType
)
from backend.utils import aio


@enforce_organization_level_auth_async
async def _do_edit_user_organization(
    _,
    info,
    **parameters
) -> EditUserPayloadType:
    success: bool = False

    organization_id: str = str(parameters.get('organization_id'))
    organization_name: str = await org_domain.get_name_by_id(organization_id)
    requester_data = util.get_jwt_content(info.context)
    requester_email = requester_data['user_email']

    user_email: str = str(parameters.get('user_email'))
    new_phone_number: str = str(parameters.get('phone_number'))
    new_role: str = str(parameters.get('role')).lower()

    if await aio.ensure_io_bound(
        authz.grant_organization_level_role,
        user_email,
        organization_id,
        new_role
    ):
        success = await user_loader.modify_user_information(
            info.context,
            {
                'email': user_email,
                'phone_number': new_phone_number,
                'responsibility': ''
            },
            ''
        )

    if success:
        util.invalidate_cache(user_email)
        util.invalidate_cache(organization_id.lower())
        util.cloudwatch_log(
            info.context,
            f'Security: User {requester_email} modified information from the '
            f'user {user_email} in the organization {organization_name}'
        )
    else:
        util.cloudwatch_log(
            info.context,
            f'Security: User {requester_email} attempted to modify '
            f'information from user {user_email} in organization '
            f'{organization_name}'
        )
    return EditUserPayloadType(
        success=success,
        modified_user=dict(
            email=user_email
        )
    )


@enforce_organization_level_auth_async
async def _do_grant_user_organization_access(
    _,
    info,
    **parameters
) -> GrantUserAccessPayloadType:
    success: bool = False

    organization_id = str(parameters.get('organization_id'))
    organization_name = await org_domain.get_name_by_id(organization_id)

    requester_data = util.get_jwt_content(info.context)
    requester_email = requester_data['user_email']

    user_email = str(parameters.get('user_email'))
    user_phone_number = str(parameters.get('phone_number'))
    user_role = str(parameters.get('role')).lower()

    user_added = await org_domain.add_user(
        organization_id, user_email, user_role
    )

    user_created = False
    user_exists = bool(user_domain.get_data(user_email, 'email'))
    if not user_exists:
        user_created = await aio.ensure_io_bound(
            user_domain.create_without_project,
            user_email,
            'customer',
            user_phone_number
        )
    success = user_added and any([user_created, user_exists])

    if success:
        util.invalidate_cache(user_email)
        util.invalidate_cache(organization_id.lower())
        util.cloudwatch_log(
            info.context,
            f'Security: User {user_email} was granted access to organization '
            f'{organization_name} with role {user_role} by user '
            f'{requester_email}'
        )
    else:
        util.cloudwatch_log(
            info.context,
            f'Security: User {requester_email} attempted to grant user '
            f'{user_email} {user_role} access to organization '
            f'{organization_name}'
        )

    return GrantUserAccessPayloadType(
        success=success,
        granted_user=dict(
            email=user_email
        )
    )


@enforce_organization_level_auth_async
async def _do_remove_user_organization_access(
    _,
    info,
    organization_id: str,
    user_email: str
) -> SimplePayloadType:
    user_data = util.get_jwt_content(info.context)
    requester_email = user_data['user_email']
    organization_name = await org_domain.get_name_by_id(organization_id)

    success: bool = await org_domain.remove_user(
        organization_id, user_email.lower()
    )
    if success:
        util.invalidate_cache(organization_id.lower())
        util.cloudwatch_log(
            info.context,
            f'Security: User {requester_email} removed user {user_email} '
            f'from organization {organization_name}'
        )
    else:
        util.cloudwatch_log(
            info.context,
            f'Security: User {requester_email} attempted to remove user '
            f'{user_email} from organization {organization_name}'
        )

    return SimplePayloadType(success=success)


@enforce_organization_level_auth_async
async def _do_update_organization_policies(
    _,
    info,
    **parameters
) -> SimplePayloadType:
    user_data = util.get_jwt_content(info.context)
    user_email = user_data['user_email']

    organization_id = parameters.pop('organization_id')
    organization_name = parameters.pop('organization_name')
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


@rename_kwargs({'identifier': 'organization_id'})
@enforce_organization_level_auth_async
async def _get_analytics(
        info,
        document_name: str,
        document_type: str,
        organization_id: str,
        **__
) -> Dict[str, object]:
    """Get analytics document."""
    return await analytics_loader.resolve(
        info,
        document_name=document_name,
        document_type=document_type,
        entity='organization',
        subject=organization_id)


@rename_kwargs({'identifier': 'organization_id'})
async def _get_id(_, organization_id: str, **kwargs) -> str:
    if kwargs.get('organization_name'):
        return await org_domain.get_id_by_name(kwargs['organization_name'])
    return organization_id


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
) -> Optional[Decimal]:
    return await org_domain.get_max_number_acceptations(organization_id)


@rename_kwargs({'identifier': 'organization_id'})
async def _get_min_acceptance_severity(
    _,
    organization_id: str,
    **__
) -> Decimal:
    return await org_domain.get_min_acceptance_severity(organization_id)


@rename_kwargs({'identifier': 'organization_id'})
async def _get_remediated_vulnerabilities(
        info, organization_id: str, **__) -> Dict[str, Dict[str, int]]:
    org_groups = await org_domain.get_groups(organization_id)
    group_attrs = await info.context.loaders['project'].load_many(org_groups)

    def filter_last_week(group: ProjectType, index: int):
        attrs = cast(Dict[str, List[List[Dict[str, int]]]], group['attrs'])
        remediated_over_time = attrs.get('remediated_over_time', [[{}], [{}]])

        return remediated_over_time[index][-1].get('y', 0)

    found_last_week: int = reduce(
        lambda acc, group: acc + filter_last_week(group, 0), group_attrs, 0)
    closed_last_week: int = reduce(
        lambda acc, group: acc + filter_last_week(group, 1), group_attrs, 0)

    open_vulns: int = reduce(lambda acc, group: acc + group['attrs'].get(
        'open_vulnerabilities', 0), group_attrs, 0)
    closed_vulns: int = reduce(lambda acc, group: acc + group['attrs'].get(
        'closed_vulnerabilities', 0), group_attrs, 0)

    return {
        'lastWeek': {
            'closed': closed_last_week,
            'open': found_last_week - closed_last_week,
        },
        'today': {
            'closed': closed_vulns,
            'open': open_vulns,
        },
    }


@rename_kwargs({'identifier': 'organization_id'})
async def _get_total_groups(_, organization_id: str, **__) -> int:
    org_groups = await org_domain.get_groups(organization_id)

    return len(org_groups)


@rename_kwargs({'identifier': 'organization_id'})
@get_entity_cache_async
async def _get_users(
    info,
    organization_id: str,
    requested_fields: list,
    **__
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


def _get_requested_fields(info, as_field: bool, as_list: bool):
    if as_field and as_list:
        to_extend = util.get_requested_fields(
            'organizations',
            info.field_nodes[0].selection_set
        )
    elif as_field:
        to_extend = util.get_requested_fields(
            'organization',
            info.field_nodes[0].selection_set
        )
    else:
        to_extend = info.field_nodes[0].selection_set.selections
    return to_extend


async def resolve(
        info,
        identifier: str,
        as_field: bool = False,
        as_list: bool = True,
        **kwargs) -> OrganizationType:
    """Async resolve fields."""
    result = dict()
    req_fields: List[Union[FieldNode, ObjectFieldNode]] = []

    req_fields.extend(_get_requested_fields(info, as_field, as_list))
    if kwargs.get('selection_set'):
        req_fields.extend(kwargs['selection_set'].selections)

    for requested_field in req_fields:
        if util.is_skippable(info, requested_field):
            continue

        params = {
            'identifier': identifier,
            'organization_name': kwargs.get('organization_name'),
            'requested_fields': req_fields
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
})
@require_login
@require_organization_access
async def resolve_organization(
    _,
    info,
    identifier: str = '',
    organization_name: str = None
) -> OrganizationType:
    """Resolve Organization query """
    return await resolve(info, identifier, organization_name=organization_name)


@convert_kwargs_to_snake_case
@require_login
@require_organization_access
async def resolve_organization_mutation(obj, info, **parameters):
    """Resolve Organization mutation """
    field = util.camelcase_to_snakecase(info.field_name)
    resolver_func = getattr(sys.modules[__name__], f'_do_{field}')
    return await resolver_func(obj, info, **parameters)
