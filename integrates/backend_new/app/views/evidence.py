# Starlette evidences-related methods

# Standard library
from typing import List, Sequence

# Third party libraries
from magic import Magic

from starlette.requests import Request
from starlette.responses import JSONResponse, Response

# Local libraries
from backend import authz, util
from backend.dal.helpers.s3 import (
    download_file,
    list_files
)
from backend.services import (
    has_access_to_finding,
    has_access_to_event
)

from __init__ import (
    FI_AWS_S3_BUCKET,
)

BUCKET_S3 = FI_AWS_S3_BUCKET


async def enforce_group_level_role(
    request: Request,
    group: str,
    *allowed_roles: Sequence[str]
) -> Response:
    response = None
    email = request.session.get('username')

    if not email:
        return Response(
            '<script> '
            'var getUrl=window.location.href.split('
            '`${window.location.host}/`); '
            'localStorage.setItem("start_url",getUrl[getUrl.length - 1]); '
            'location = "/"; '
            '</script>'
        )

    requester_role = await authz.get_group_level_role(email, group)

    if requester_role not in allowed_roles:
        response = Response('Access denied')
        response.status_code = 403

    return response


async def get_evidence(request: Request) -> Response:
    group_name = request.path_params['group_name']
    finding_id = request.path_params['finding_id']
    file_id = request.path_params['file_id']
    evidence_type = request.path_params['evidence_type']

    allowed_roles = [
        'admin',
        'analyst',
        'closer',
        'customer',
        'customeradmin',
        'executive',
        'group_manager',
        'internal_manager',
        'resourcer',
        'reviewer'
    ]
    error = await enforce_group_level_role(
        request,
        group_name,
        *allowed_roles
    )
    if error is not None:
        return error

    username = request.session['username']
    if ((evidence_type in ['drafts', 'findings', 'vulns'] and
         await has_access_to_finding(username, finding_id)) or
        (evidence_type == 'events' and
         await has_access_to_event(username, finding_id))):
        if file_id is None:
            return Response(
                'Error - Unsent image ID',
                media_type='text/html'
            )
        evidences = await list_s3_evidences(
            f'{group_name.lower()}/{finding_id}/{file_id}'
        )
        if evidences:
            for evidence in evidences:
                start = evidence.find(finding_id) + len(finding_id)
                localfile = f'/tmp{evidence[start:]}'
                localtmp = util.replace_all(
                    localfile,
                    {'.png': '.tmp', '.gif': '.tmp'}
                )
                await download_file(BUCKET_S3, evidence, localtmp)
                return retrieve_image(request, localtmp)
        else:
            return JSONResponse(
                {
                    'data': [],
                    'message': 'Access denied or evidence not found',
                    'error': True
                }
            )
    else:
        util.cloudwatch_log(
            request,
            f'Security: Attempted to retrieve evidence without permission'
        )
        return JSONResponse(
            {
                'data': [],
                'message': 'Evidence type not found',
                'error': True
            }
        )


async def list_s3_evidences(prefix: str) -> List[str]:
    return list(await list_files(BUCKET_S3, prefix))


def retrieve_image(request: Request, img_file: str) -> Response:
    if util.assert_file_mime(
            img_file,
            ['image/png', 'image/jpeg', 'image/gif']):
        with open(img_file, 'rb') as file_obj:
            mime = Magic(mime=True)
            mime_type = mime.from_file(img_file)
            return Response(file_obj.read(), media_type=mime_type)
    else:
        return Response(
            'Error: Invalid evidence image format',
            media_type='text/html'
        )
