from analytics import (
    dal as analytics_dal,
)
from ariadne import (
    convert_camel_case_to_snake,
)
import authz
import base64
import botocore.exceptions
from custom_exceptions import (
    DocumentNotFound,
    InvalidAuthorization,
)
from custom_types import (
    GraphicParameters,
    GraphicsForEntityParameters,
    ReportParameters,
)
from decorators import (
    retry_on_exceptions,
)
from functools import (
    partial,
)
import json
import logging
import logging.config
from newutils import (
    templates as templates_utils,
    token as token_utils,
)
from newutils.encodings import (
    safe_encode,
)
from organizations import (
    domain as orgs_domain,
)
import os
from redis_cluster.operations import (
    redis_get_or_set_entity_attr,
)
from settings import (
    LOGGING,
)
from starlette.requests import (
    Request,
)
from starlette.responses import (
    Response,
)
import string
from tags import (
    domain as tags_domain,
)
from typing import (
    Union,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)
ALLOWED_CHARS_IN_PARAMS: str = string.ascii_letters + string.digits + "#-"
ENTITIES = {"group", "organization", "portfolio"}


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
        entity="analytics",
        attr="document",
        ttl=3600,
        id=f"{document_name}-{document_type}-{entity}-{subject}",
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
            f"{entity}:{safe_encode(subject.lower())}.json",
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
        entity="analytics",
        attr="graphics_report",
        ttl=3600,
        id=f"{entity}-{subject}",
    )

    return response


@retry_on_exceptions(
    exceptions=(botocore.exceptions.ClientError,),
    max_attempts=3,
    sleep_seconds=float("0.5"),
)
async def get_graphics_report_no_cache(
    *,
    entity: str,
    subject: str,
) -> bytes:
    document: bytes = await analytics_dal.get_snapshot(
        f"reports/{entity}:{safe_encode(subject.lower())}.png",
    )
    return base64.b64encode(document)


async def handle_authz_claims(
    *,
    params: Union[
        GraphicParameters,
        GraphicsForEntityParameters,
        ReportParameters,
    ],
    request: Request,
) -> None:
    user_info = await token_utils.get_jwt_content(request)
    email = user_info["user_email"]
    if params.subject.endswith("_30") or params.subject.endswith("_90"):
        subject = params.subject[:-3]
    else:
        subject = params.subject

    if params.entity == "group":
        if not await authz.has_access_to_group(
            email,
            subject.lower(),
        ):
            raise PermissionError("Access denied")
    elif params.entity == "organization":
        if not await orgs_domain.has_user_access(
            email=email,
            organization_id=subject,
        ):
            raise PermissionError("Access denied")
    elif params.entity == "portfolio":
        if not await tags_domain.has_user_access(email, subject):
            raise PermissionError("Access denied")
    else:
        raise ValueError(f"Invalid entity: {params.entity}")


async def handle_graphic_request(request: Request) -> Response:
    try:
        params: GraphicParameters = handle_graphic_request_parameters(
            request=request
        )

        await handle_authz_claims(params=params, request=request)

        document: object = await get_document(
            document_name=params.document_name,
            document_type=params.document_type,
            entity=params.entity,
            subject=params.subject,
        )
    except (
        DocumentNotFound,
        InvalidAuthorization,
        KeyError,
        PermissionError,
        ValueError,
    ) as ex:
        LOGGER.exception(ex, extra=dict(extra=locals()))
        response = templates_utils.graphic_error(request)
    else:
        response = templates_utils.graphic_view(request, document, params)

    return response


def handle_graphic_request_parameters(
    *,
    request: Request,
) -> GraphicParameters:
    document_name: str = request.query_params["documentName"]
    document_type: str = request.query_params["documentType"]
    generator_name: str = request.query_params["generatorName"]
    generator_type: str = request.query_params["generatorType"]
    entity: str = request.query_params["entity"]
    height: int = int(request.query_params["height"])
    subject: str = request.query_params["subject"]
    width: int = int(request.query_params["width"])

    for param_name, param_value in [
        ("documentName", document_name),
        ("documentType", document_type),
        ("entity", entity),
        ("generatorName", generator_name),
        ("generatorType", generator_type),
        ("subject", subject),
    ]:
        if set(param_value).issuperset(set(ALLOWED_CHARS_IN_PARAMS)):
            raise ValueError(
                f"Expected [{ALLOWED_CHARS_IN_PARAMS}] "
                f"in parameter: {param_name}",
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
        response = templates_utils.graphic_error(request)
    else:
        response = templates_utils.graphics_for_entity_view(request, entity)

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
        ("subject", subject),
    ]:
        if set(param_value).issuperset(set(ALLOWED_CHARS_IN_PARAMS)):
            raise ValueError(
                f"Expected [{ALLOWED_CHARS_IN_PARAMS}] "
                f"in parameter: {param_name}",
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
        response = templates_utils.graphic_error(request)
    else:
        response = Response(report, media_type="image/png")

    return response


def handle_graphics_report_request_parameters(
    *,
    request: Request,
) -> ReportParameters:
    entity: str = request.query_params["entity"]

    if entity not in ENTITIES:
        raise ValueError(
            'Invalid entity, only "group", "organization"'
            ' and "portfolio" are valid',
        )

    subject: str = request.query_params[entity]

    for param_name, param_value in [
        ("subject", subject),
    ]:
        if set(param_value).issuperset(set(ALLOWED_CHARS_IN_PARAMS)):
            raise ValueError(
                f"Expected [{ALLOWED_CHARS_IN_PARAMS}] "
                f"in parameter: {param_name}",
            )

    return ReportParameters(
        entity=entity,
        subject=subject,
    )
