# Standard library
import json
import logging
import os
import string
import traceback
from typing import (
    NamedTuple,
    Union,
)

# Third party libraries
from ariadne import (
    convert_camel_case_to_snake,
)
import botocore.exceptions
from django.conf import settings
from django.http import (
    HttpRequest,
    HttpResponse,
)
from django.shortcuts import (
    render,
)

# Local libraries
from backend.dal import (
    analytics as analytics_dal,
)
from backend.decorators import (
    cache_idempotent,
)
from backend.domain import (
    organization as organization_domain,
)
from backend.services import (
    has_access_to_project as has_access_to_group,
)
from backend.utils import (
    aio,
    apm,
)
from backend.utils.encodings import (
    safe_encode,
)
from backend import util

# Containers
GraphicParameters = NamedTuple(
    'GraphicParameters',
    [
        ('document_name', str),
        ('document_type', str),
        ('entity', str),
        ('generator_name', str),
        ('generator_type', str),
        ('height', int),
        ('subject', str),
        ('width', int)
    ]
)
GraphicsForEntityParameters = NamedTuple(
    'GraphicsForEntityParameters',
    [
        ('entity', str),
        ('subject', str),
    ]
)
ReportParameters = NamedTuple(
    'ReportParameters',
    [
        ('entity', str),
        ('subject', str),
    ]
)

# Constants
LOGGER = logging.getLogger(__name__)
ALLOWED_CHARS_IN_PARAMS: str = string.ascii_letters + string.digits + '#-'


@apm.trace()
@cache_idempotent(ttl=3600)
async def get_document(
    *,
    document_name: str,
    document_type: str,
    entity: str,
    subject: str,
) -> object:
    document: str = await analytics_dal.get_document(
        os.path.join(
            convert_camel_case_to_snake(document_type),
            convert_camel_case_to_snake(document_name),
            f'{entity}:{safe_encode(subject.lower())}.json',
        )
    )

    return json.loads(document)


@apm.trace()
@cache_idempotent(ttl=3600)
async def get_graphics_report(
    *,
    entity: str,
    subject: str,
) -> bytes:
    document: bytes = await analytics_dal.get_snapshot(
        f'reports/{entity}:{safe_encode(subject.lower())}.png',
    )

    return document


async def handle_authz_claims(
    *,
    params: Union[
        GraphicParameters,
        GraphicsForEntityParameters,
        ReportParameters,
    ],
    request: HttpRequest,
) -> None:
    email = util.get_jwt_content(request)['user_email']

    if params.entity == 'group':
        if not await aio.ensure_io_bound(
            has_access_to_group, email, params.subject.lower(),
        ):
            raise PermissionError('Access denied')
    elif params.entity == 'organization':
        if not await organization_domain.has_user_access(
            email=email,
            organization_id=params.subject,
        ):
            raise PermissionError('Access denied')
    else:
        raise ValueError(f'Invalid entity: {params.entity}')


def handle_graphic_request_parameters(
    *,
    request: HttpRequest,
) -> GraphicParameters:
    document_name: str = request.GET['documentName']
    document_type: str = request.GET['documentType']
    generator_name: str = request.GET['generatorName']
    generator_type: str = request.GET['generatorType']
    entity: str = request.GET['entity']
    height: int = int(request.GET['height'])
    subject: str = request.GET['subject']
    width: int = int(request.GET['width'])

    for param_name, param_value in [
        ('documentName', document_name),
        ('documentType', document_type),
        ('entity', entity),
        ('generatorName', generator_name),
        ('generatorType', generator_type),
        ('subject', subject),
    ]:
        if set(param_value).issuperset(set(ALLOWED_CHARS_IN_PARAMS)):
            raise ValueError(
                f'Expected [{ALLOWED_CHARS_IN_PARAMS}] '
                f'in parameter: {param_name}',
            )

    return GraphicParameters(
        document_name=document_name,
        document_type=document_type,
        entity=entity,
        generator_name=generator_name,
        generator_type=generator_type,
        height=height,
        subject=subject,
        width=width,
    )


def handle_graphics_for_entity_request_parameters(
    *,
    entity: str,
    request: HttpRequest,
) -> GraphicsForEntityParameters:
    if entity not in ['group', 'organization']:
        raise ValueError(
            'Invalid entity, only "group" and "organization" are valid',
        )

    subject: str = request.GET[entity]

    for param_name, param_value in [
        ('subject', subject),
    ]:
        if set(param_value).issuperset(set(ALLOWED_CHARS_IN_PARAMS)):
            raise ValueError(
                f'Expected [{ALLOWED_CHARS_IN_PARAMS}] '
                f'in parameter: {param_name}',
            )

    return GraphicsForEntityParameters(
        entity=entity,
        subject=subject,
    )


def handle_graphics_report_request_parameters(
    *,
    request: HttpRequest,
) -> ReportParameters:
    entity: str = request.GET['entity']

    if entity not in ['group', 'organization']:
        raise ValueError(
            'Invalid entity, only "group" and "organization" are valid',
        )

    subject: str = request.GET[entity]

    for param_name, param_value in [
        ('subject', subject),
    ]:
        if set(param_value).issuperset(set(ALLOWED_CHARS_IN_PARAMS)):
            raise ValueError(
                f'Expected [{ALLOWED_CHARS_IN_PARAMS}] '
                f'in parameter: {param_name}',
            )

    return ReportParameters(
        entity=entity,
        subject=subject,
    )


async def handle_graphic_request(request: HttpRequest) -> HttpResponse:
    try:
        params: GraphicParameters = \
            handle_graphic_request_parameters(request=request)

        await handle_authz_claims(params=params, request=request)

        document: object = await get_document(
            document_name=params.document_name,
            document_type=params.document_type,
            entity=params.entity,
            subject=params.subject,
        )
    except (
        botocore.exceptions.ClientError,
        KeyError,
        PermissionError,
        ValueError,
    ) as ex:
        LOGGER.exception(ex)
        response = render(request, 'graphic-error.html', dict(
            debug=settings.DEBUG,
            traceback=traceback.format_exc(),
        ))
    else:
        response = render(request, 'graphic.html', dict(
            args=dict(
                data=json.dumps(document),
                height=params.height,
                width=params.width,
            ),
            generator_src=(
                f'graphics/'
                f'generators/'
                f'{params.generator_type}/'
                f'{params.generator_name}.js'
            ),
        ))

    # Allow the frame to render if and only if we are on the same origin
    response['x-frame-options'] = 'SAMEORIGIN'

    return response


async def handle_graphics_for_entity_request(
    entity: str,
    request: HttpRequest,
) -> HttpResponse:
    try:
        await handle_authz_claims(
            params=handle_graphics_for_entity_request_parameters(
                entity=entity,
                request=request,
            ),
            request=request,
        )
    except (
        botocore.exceptions.ClientError,
        KeyError,
        PermissionError,
        ValueError,
    ) as ex:
        LOGGER.exception(ex)
        response = render(request, 'graphic-error.html', dict(
            debug=settings.DEBUG,
            traceback=traceback.format_exc(),
        ))
    else:
        response = render(request, 'graphics-for-entity.html', dict(
            debug=settings.DEBUG,
            entity=entity.title(),
        ))

    return response


async def handle_graphics_report_request(
    request: HttpRequest,
) -> HttpResponse:
    try:
        params: ReportParameters = handle_graphics_report_request_parameters(
            request=request,
        )

        await handle_authz_claims(
            params=params,
            request=request,
        )

        report: bytes = await get_graphics_report(
            entity=params.entity,
            subject=params.subject,
        )
    except (
        botocore.exceptions.ClientError,
        KeyError,
        PermissionError,
        ValueError,
    ) as ex:
        LOGGER.exception(ex)
        response = render(request, 'graphic-error.html', dict(
            debug=settings.DEBUG,
            traceback=traceback.format_exc(),
        ))
    else:
        response = HttpResponse(report, content_type='image/png')

    return response
