from analytics import (
    dal as analytics_dal,
)
from analytics.types import (
    GraphicParameters,
    GraphicsCsvParameters,
    GraphicsForEntityParameters,
    ReportParameters,
)
from ariadne import (
    convert_camel_case_to_snake,
)
import authz
import base64
import botocore.exceptions
import csv
from custom_exceptions import (
    DocumentNotFound,
    InvalidAuthorization,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from decorators import (
    retry_on_exceptions,
)
import json
import logging
import logging.config
from newutils import (
    analytics as analytics_utils,
    templates as templates_utils,
    validations,
)
from newutils.encodings import (
    safe_encode,
)
from organization_access import (
    domain as orgs_access,
)
import os
from sessions import (
    domain as sessions_domain,
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
ALLOWED_CHARS_IN_PARAMS: str = string.ascii_letters + string.digits + "#-_"
ENTITIES = {"group", "organization", "portfolio"}


async def get_csv_document(
    *,
    document_name: str,
    document_type: str,
    entity: str,
    subject: str,
) -> str:

    return await analytics_dal.get_document(
        os.path.join(
            convert_camel_case_to_snake(document_type),
            convert_camel_case_to_snake(document_name),
            f"{entity}:{safe_encode(subject.lower())}.csv",
        )
    )


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
            f"{entity}:{safe_encode(subject.lower())}.json",
        )
    )

    return json.loads(document)


@retry_on_exceptions(
    exceptions=(botocore.exceptions.ClientError,),
    max_attempts=3,
    sleep_seconds=float("0.5"),
)
async def get_graphics_report(
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
        GraphicsCsvParameters,
    ],
    request: Request,
) -> None:
    loaders: Dataloaders = get_new_context()
    user_info = await sessions_domain.get_jwt_content(request)
    email = user_info["user_email"]
    valid_filters = [30, 60, 90, 180]
    if any(
        params.subject.endswith(f"_{valid_filter}")
        for valid_filter in valid_filters
    ):
        subject = params.subject.rsplit("_", 1)[0]
    else:
        subject = params.subject

    if params.entity == "group":
        if not await authz.has_access_to_group(
            loaders, email, subject.lower()
        ):
            raise PermissionError("Access denied")
    elif params.entity == "organization":
        if not await orgs_access.has_access(
            loaders=loaders,
            email=email,
            organization_id=subject,
        ):
            raise PermissionError("Access denied")
    elif params.entity == "portfolio":
        if not await tags_domain.has_access(
            loaders=loaders, email=email, subject=subject
        ):
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
        LOGGER.exception(
            ex,
            extra=dict(
                extra=dict(
                    query_params=request.query_params,
                    url=request.url,
                )
            ),
        )
        response = templates_utils.graphic_error(request)
    else:
        response = templates_utils.graphic_view(
            request,
            document,
            params.height,
            params.width,
            params.generator_type,
            params.generator_name,
        )

    return response


async def handle_graphic_csv_request(request: Request) -> Response:
    try:
        params: GraphicsCsvParameters = handle_graphics_csv_request_parameters(
            request=request,
        )

        await handle_authz_claims(params=params, request=request)

        document: str = await get_csv_document(
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
        LOGGER.exception(
            ex,
            extra=dict(
                extra=dict(
                    query_params=request.query_params,
                    url=request.url,
                )
            ),
        )
        return templates_utils.graphic_error(request)
    else:
        reader = csv.reader(document.split("\n"), delimiter=",")
        for row in reader:
            validations.validate_sanitized_csv_input(
                *[
                    "" if analytics_utils.is_decimal(field) else str(field)
                    for field in row
                ]
            )
        return Response(document, media_type="text/csv")


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
        validations.validate_chart_field(param_value, param_name)

    # valid generator type and name, from known static graphics templates
    valid_generator_type: set[str] = {
        "barChart",
        "c3",
        "heatMapChart",
        "stackedBarChart",
        "textBox",
    }
    valid_generator_name: set[str] = {"generic"}
    if generator_type not in valid_generator_type:
        raise ValueError("Invalid generator type")

    if generator_name not in valid_generator_name:
        raise ValueError("Invalid generator name")

    if f"{generator_type}/{generator_name}" not in {
        f"{g_type}/generic" for g_type in valid_generator_type
    }:
        raise ValueError("Invalid generator type or generator name")

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
        response = Response(report, media_type="image/png")  # type: ignore

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


def handle_graphics_csv_request_parameters(
    *,
    request: Request,
) -> GraphicsCsvParameters:
    entity: str = request.query_params["entity"]

    if entity not in ENTITIES:
        raise ValueError(
            'Invalid entity, only "group", "organization"'
            ' and "portfolio" are valid',
        )

    subject: str = request.query_params["subject"]
    document_name: str = request.query_params["documentName"]
    document_type: str = request.query_params["documentType"]

    for param_name, param_value in [
        ("documentName", document_name),
        ("documentType", document_type),
        ("subject", subject),
    ]:
        if set(param_value).issuperset(set(ALLOWED_CHARS_IN_PARAMS)):
            raise ValueError(
                f"Expected [{ALLOWED_CHARS_IN_PARAMS}] "
                f"in parameter: {param_name}",
            )

    return GraphicsCsvParameters(
        entity=entity,
        subject=subject,
        document_name=document_name,
        document_type=document_type,
    )
