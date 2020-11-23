# Starlette charts views

# Third party libraries
from starlette.requests import Request
from starlette.responses import Response

# Local libraries
from backend import util
from backend.domain import analytics as analytics_domain

import backend_new.app.utils as utils


async def graphic(request: Request) -> Response:
    return await analytics_domain.handle_graphic_request(request)


async def graphics_for_group(request: Request) -> Response:
    return await graphics_for_entity('group', request)


async def graphics_for_organization(request: Request) -> Response:
    return await graphics_for_entity('organization', request)


async def graphics_for_portfolio(request: Request) -> Response:
    return await graphics_for_entity('portfolio', request)


async def graphics_report(request: Request) -> Response:
    return await analytics_domain.handle_graphics_report_request(request)


async def graphics_for_entity(entity: str, request: Request) -> Response:
    request_data = await util.get_jwt_content(request)

    response = await analytics_domain.handlegraphics_for_entity_request(
        entity=entity,
        request=request,
    )

    jwt_token = utils.create_session_token(
        dict(
            username=request_data['user_email'],
            first_name=request_data['first_name'],
            last_name=request_data['last_name'],
        )
    )
    utils.set_token_in_response(response, jwt_token)

    return response
