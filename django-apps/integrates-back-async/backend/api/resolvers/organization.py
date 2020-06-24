import sys
from decimal import Decimal
from typing import Optional

from ariadne import (
    convert_camel_case_to_snake,
    convert_kwargs_to_snake_case
)
from graphql.language.ast import SelectionSetNode

from backend import util
from backend.decorators import (
    rename_kwargs,
    require_login
)
from backend.domain import organization as org_domain
from backend.typing import Organization as OrganizationType


async def _get_max_acceptance_days(_, identifier: str) -> Optional[Decimal]:
    return await org_domain.get_max_acceptance_days(identifier)


async def _get_max_acceptance_severity(_, identifier: str) -> Decimal:
    return await org_domain.get_max_acceptance_severity(identifier)


async def _get_max_number_acceptations(
    _,
    identifier: str
)-> Optional[Decimal]:
    return await org_domain.get_max_number_acceptations(identifier)


async def _get_min_acceptance_severity(_, identifier: str) -> Decimal:
    return await org_domain.get_min_acceptance_severity(identifier)


async def resolve(
        info,
        identifier: str,
        as_field: bool = False,
        selection_set: SelectionSetNode = SelectionSetNode()
) -> OrganizationType:
    """Async resolve fields."""
    result = dict()
    requested_fields = (
        selection_set.selections
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
@rename_kwargs({'organization_id': 'identifier'})
@require_login
async def resolve_organization(_, info, identifier: str) -> OrganizationType:
    """Resolve Organization query."""
    return await resolve(info, identifier)
