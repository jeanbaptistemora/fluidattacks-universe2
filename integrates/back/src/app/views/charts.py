# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# Starlette charts views
from analytics import (
    domain as analytics_domain,
)
from app import (
    utils,
)
from app.views.types import (
    UserAccessInfo,
)
from newutils import (
    token as token_utils,
)
from starlette.requests import (
    Request,
)
from starlette.responses import (
    Response,
)


async def graphic(request: Request) -> Response:
    return await analytics_domain.handle_graphic_request(request)


async def graphic_csv(request: Request) -> Response:
    return await analytics_domain.handle_graphic_csv_request(request)


async def graphics_for_entity(entity: str, request: Request) -> Response:
    request_data = await token_utils.get_jwt_content(request)
    response = await analytics_domain.handle_graphics_for_entity_request(
        entity=entity,
        request=request,
    )
    jwt_token = await utils.create_session_token(
        UserAccessInfo(
            first_name=request_data["first_name"],
            last_name=request_data["last_name"],
            user_email=request_data["user_email"],
        )
    )
    utils.set_token_in_response(response, jwt_token)
    return response


async def graphics_for_group(request: Request) -> Response:
    return await graphics_for_entity("group", request)


async def graphics_for_organization(request: Request) -> Response:
    return await graphics_for_entity("organization", request)


async def graphics_for_portfolio(request: Request) -> Response:
    return await graphics_for_entity("portfolio", request)


async def graphics_report(request: Request) -> Response:
    return await analytics_domain.handle_graphics_report_request(request)
