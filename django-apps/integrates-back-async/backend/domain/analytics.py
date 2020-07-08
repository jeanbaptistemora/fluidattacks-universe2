# Standard library
import json
import os
from typing import (
    NamedTuple,
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
import rollbar

# Local libraries
from backend.dal import (
    analytics as analytics_dal,
)
from backend.decorators import (
    cache_idempotent,
)
from backend.services import (
    has_access_to_project as has_access_to_group,
)
from backend.utils import (
    aio,
    apm,
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
GraphicsForGroupParameters = NamedTuple(
    'GraphicsForGroupParameters',
    [
        ('group', str),
    ]
)


@apm.trace()
@cache_idempotent(ttl=3600)
async def get_document(
    *,
    document_name: str,
    document_type: str,
    level: str,
    subject: str,
) -> object:
    document: str = await analytics_dal.get_document(
        os.path.join(
            convert_camel_case_to_snake(document_type),
            convert_camel_case_to_snake(document_name),
            f'{level}-{subject}.json',
        )
    )

    return json.loads(document)


async def get_document_from_graphic_request(
    *,
    params: GraphicParameters,
    request: HttpRequest,
) -> object:
    # Get the requester email from the session or from its API token
    email = request.session.get('username') \
        or util.get_jwt_content(request)['user_email']

    if params.entity == 'group':
        if not await aio.ensure_io_bound(
            has_access_to_group, email, params.subject,
        ):
            raise PermissionError('Access denied')

        document = await get_document(
            document_name=params.document_name,
            document_type=params.document_type,
            level=params.entity,
            subject=params.subject,
        )
    else:
        raise ValueError(f'Ivalid entity: {params.entity}')

    return document


async def handle_graphics_for_group_authz(
    *,
    params: GraphicsForGroupParameters,
    request: HttpRequest,
) -> None:
    email = util.get_jwt_content(request)['user_email']

    if not await aio.ensure_io_bound(
        has_access_to_group, email, params.group,
    ):
        raise PermissionError('Access denied')


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
        if not param_value.isalnum():
            raise ValueError(f'Expected [a-zA-Z] in parameter: {param_name}')

    return GraphicParameters(
        document_name=document_name,
        document_type=document_type,
        entity=entity,
        generator_name=generator_name,
        generator_type=generator_type,
        height=height,
        subject=subject.lower(),
        width=width,
    )


def handle_graphics_for_group_request_parameters(
    *,
    request: HttpRequest,
) -> GraphicsForGroupParameters:
    group: str = request.GET['group']

    for param_name, param_value in [
        ('group', group),
    ]:
        if not param_value.isalnum():
            raise ValueError(f'Expected [a-zA-Z] in parameter: {param_name}')

    return GraphicsForGroupParameters(
        group=group.lower(),
    )


async def handle_graphic_request(request: HttpRequest) -> HttpResponse:
    try:
        params: GraphicParameters = \
            handle_graphic_request_parameters(request=request)

        document: object = await get_document_from_graphic_request(
            params=params,
            request=request,
        )
    except (
        botocore.exceptions.ClientError,
        KeyError,
        PermissionError,
        ValueError,
    ) as exception:
        rollbar.report_exc_info()
        response = render(request, 'graphic-error.html', dict(
            debug=settings.DEBUG,
            exception=exception,
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


async def handle_graphics_for_group_request(
    request: HttpRequest,
) -> HttpResponse:
    try:
        params: GraphicsForGroupParameters = \
            handle_graphics_for_group_request_parameters(request=request)

        await handle_graphics_for_group_authz(
            params=params,
            request=request,
        )
    except (
        botocore.exceptions.ClientError,
        KeyError,
        PermissionError,
        ValueError,
    ) as exception:
        rollbar.report_exc_info()
        response = render(request, 'graphic-error.html', dict(
            debug=settings.DEBUG,
            exception=exception,
        ))
    else:
        response = render(request, 'graphics-for-group.html', dict(
            debug=settings.DEBUG,
        ))

    return response
