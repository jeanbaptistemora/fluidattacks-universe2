import sys
from decimal import Decimal
from typing import Optional

from ariadne import (
    convert_camel_case_to_snake,
    convert_kwargs_to_snake_case
)
from graphql.language.ast import SelectionSetNode

from backend import util
from backend.decorators import require_login
from backend.domain import organization as org_domain
from backend.typing import (
    Organization as OrganizationType,
    SimplePayload as SimplePayloadType
)


async def _do_update_organization_settings(
    _,
    info,
    identifier: str,
    **parameters
) -> SimplePayloadType:

    if identifier.startswith('ORG#'):
        org_id = identifier
        org_name = await _get_name(_, identifier)
    else:
        org_id = await _get_id(_, identifier)
        org_name = identifier
    success: bool = await org_domain.update_settings(
        org_id,
        org_name,
        parameters
    )
    if success:
        util.cloudwatch_log(
            info.context,
            f'Security: Updated settings for organization {org_name} with ID'
            f' {org_id}'
        )
    return SimplePayloadType(success=success)


async def _get_id(_, identifier: str) -> str:
    org_id = (
        identifier
        if identifier.startswith('ORG#')
        else await org_domain.get_id_by_name(identifier)
    )
    return org_id


async def _get_name(_, identifier: str) -> str:
    org_name = (
        identifier
        if not identifier.startswith('ORG#')
        else await org_domain.get_name_by_id(identifier)
    )
    return org_name


async def _get_max_acceptance_days(_, identifier: str) -> Optional[Decimal]:
    org_id = await _get_id(_, identifier)
    return await org_domain.get_max_acceptance_days(org_id)


async def _get_max_acceptance_severity(_, identifier: str) -> Decimal:
    org_id = await _get_id(_, identifier)
    return await org_domain.get_max_acceptance_severity(org_id)


async def _get_max_number_acceptations(
    _,
    identifier: str
)-> Optional[Decimal]:
    org_id = await _get_id(_, identifier)
    return await org_domain.get_max_number_acceptations(org_id)


async def _get_min_acceptance_severity(_, identifier: str) -> Decimal:
    org_id = await _get_id(_, identifier)
    return await org_domain.get_min_acceptance_severity(org_id)


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

        params = {'identifier': identifier}
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
@require_login
async def resolve_organization(_, info, identifier: str) -> OrganizationType:
    """Resolve Organization query """
    return await resolve(info, identifier)


@convert_kwargs_to_snake_case
@require_login
async def resolve_organization_mutation(obj, info, **parameters):
    """Resolve Organization mutation """
    field = util.camelcase_to_snakecase(info.field_name)
    resolver_func = getattr(sys.modules[__name__], f'_do_{field}')
    return await resolver_func(obj, info, **parameters)
