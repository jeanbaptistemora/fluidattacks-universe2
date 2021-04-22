# Standard library
import base64
import json
import logging
import logging.config
import os
import string
from functools import partial
from io import BytesIO
from typing import Union

# Third party libraries
import botocore.exceptions
from aioextensions import in_thread
from ariadne import convert_camel_case_to_snake
from PIL import Image
from starlette.requests import Request
from starlette.responses import Response

# Local libraries
from analytics import dal as analytics_dal
from back.app.views import templates
from back.settings import LOGGING
from backend import util
from backend.exceptions import DocumentNotFound
from backend.services import has_access_to_project as has_access_to_group
from backend.typing import (
    GraphicsForEntityParameters,
    GraphicParameters,
    ReportParameters,
)
from newutils.encodings import safe_encode
from newutils.context import CHARTS_LOGO_PATH
from redis_cluster.operations import redis_get_or_set_entity_attr
from organizations import domain as orgs_domain
from tags import domain as tags_domain


logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)
ALLOWED_CHARS_IN_PARAMS: str = string.ascii_letters + string.digits + '#-'
ENTITIES = {'group', 'organization', 'portfolio'}
TRANSPARENCY_RATIO: float = 0.40


def add_watermark(base_image: Image) -> bytes:
    watermark: Image = clarify(CHARTS_LOGO_PATH)
    watermark_width, watermark_height = watermark.size
    width = max(base_image.width, watermark_width)
    height = max(base_image.height, watermark_height)

    transparent = Image.new('RGB', (width, height), (0, 0, 0, 0))
    transparent.paste(base_image, (0, 0))
    transparent.paste(
        watermark,
        ((width - watermark_width) // 2, (height - watermark_height) // 2),
        watermark,
    )

    stream: BytesIO = BytesIO()
    transparent.save(stream, format='png')
    stream.seek(0)

    image_encoded = base64.b64encode(stream.read())

    return image_encoded


def clarify(image_path: str) -> Image:
    if not os.path.exists(image_path):
        raise FileNotFoundError(image_path)

    watermark = Image.open(image_path)
    watermark_mask = watermark.convert('L').point(
        lambda x: x * TRANSPARENCY_RATIO
    )
    watermark.putalpha(watermark_mask)

    return watermark


async def get_document(
    *,
    document_name: str,
    document_type: str,
    entity: str,
    subject: str,
) -> object:
    response: object = await redis_get_or_set_entity_attr(
        partial(
            get_document_no_cache,
            document_name=document_name,
            document_type=document_type,
            entity=entity,
            subject=subject,
        ),
        entity='analytics',
        attr='document',
        ttl=3600,
        id=f'{document_name}-{document_type}-{entity}-{subject}',
    )

    return response


async def get_document_no_cache(
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


async def get_graphics_report(
    *,
    entity: str,
    subject: str,
) -> bytes:
    response: bytes = await redis_get_or_set_entity_attr(
        partial(get_graphics_report_no_cache, entity=entity, subject=subject),
        entity='analytics',
        attr='graphics_report',
        ttl=3600,
        id=f'{entity}-{subject}',
    )

    return response


async def get_graphics_report_no_cache(
    *,
    entity: str,
    subject: str,
) -> bytes:
    document: bytes = await analytics_dal.get_snapshot(
        f'reports/{entity}:{safe_encode(subject.lower())}.png',
    )
    base_image: Image = Image.open(BytesIO(document))

    return await in_thread(add_watermark, base_image)


async def handle_authz_claims(
    *,
    params: Union[
        GraphicParameters,
        GraphicsForEntityParameters,
        ReportParameters,
    ],
    request: Request,
) -> None:
    user_info = await util.get_jwt_content(request)
    email = user_info['user_email']
    if params.subject.endswith('_30') or params.subject.endswith('_90'):
        subject = params.subject[:-3]
    else:
        subject = params.subject

    if params.entity == 'group':
        if not await has_access_to_group(
            email, subject.lower(),
        ):
            raise PermissionError('Access denied')
    elif params.entity == 'organization':
        if not await orgs_domain.has_user_access(
            email=email,
            organization_id=subject,
        ):
            raise PermissionError('Access denied')
    elif params.entity == 'portfolio':
        if not await tags_domain.has_user_access(email, subject):
            raise PermissionError('Access denied')
    else:
        raise ValueError(f'Invalid entity: {params.entity}')


async def handle_graphic_request(request: Request) -> Response:
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
        DocumentNotFound,
        KeyError,
        PermissionError,
        ValueError,
    ) as ex:
        LOGGER.exception(ex, extra=dict(extra=locals()))
        response = templates.graphic_error(request)
    else:
        response = templates.graphic_view(request, document, params)
        response.headers['x-frame-options'] = 'SAMEORIGIN'

    return response


def handle_graphic_request_parameters(
    *,
    request: Request,
) -> GraphicParameters:
    document_name: str = request.query_params['documentName']
    document_type: str = request.query_params['documentType']
    generator_name: str = request.query_params['generatorName']
    generator_type: str = request.query_params['generatorType']
    entity: str = request.query_params['entity']
    height: int = int(request.query_params['height'])
    subject: str = request.query_params['subject']
    width: int = int(request.query_params['width'])

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


async def handle_graphics_for_entity_request(
    entity: str,
    request: Request,
) -> Response:
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
        LOGGER.exception(ex, extra=dict(extra=locals()))
        response = templates.graphic_error(request)
    else:
        response = templates.graphics_for_entity_view(request, entity)

    return response


def handle_graphics_for_entity_request_parameters(
    *,
    entity: str,
    request: Request,
) -> GraphicsForEntityParameters:
    if entity not in ENTITIES:
        raise ValueError(
            'Invalid entity, only "group", "organization"'
            ' and "portfolio" are valid',
        )

    subject: str = request.query_params[entity]

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


async def handle_graphics_report_request(
    request: Request,
) -> Response:
    try:
        params: ReportParameters = handle_graphics_report_request_parameters(
            request=request,
        )

        await handle_authz_claims(
            params=params,
            request=request,
        )

        report: bytes = base64.b64decode(
            await get_graphics_report(
                entity=params.entity,
                subject=params.subject,
            )
        )
    except (
        botocore.exceptions.ClientError,
        KeyError,
        PermissionError,
        ValueError,
    ) as ex:
        LOGGER.exception(ex, extra=dict(extra=locals()))
        response = templates.graphic_error(request)
    else:
        response = Response(report, media_type='image/png')

    return response


def handle_graphics_report_request_parameters(
    *,
    request: Request,
) -> ReportParameters:
    entity: str = request.query_params['entity']

    if entity not in ENTITIES:
        raise ValueError(
            'Invalid entity, only "group", "organization"'
            ' and "portfolio" are valid',
        )

    subject: str = request.query_params[entity]

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
